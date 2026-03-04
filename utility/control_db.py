#!/usr/bin/env python3
"""
Enhanced SQLite Shell – interactive only, no command‑line arguments.
"""

import sqlite3
import os
import sys
from pathlib import Path

# Optional: enable command history on Unix-like systems
try:
    import readline
except ImportError:
    pass

# ----------------------------------------------------------------------
# Pretty table printer
# ----------------------------------------------------------------------
def print_table(rows, headers):
    """Print query results as a formatted table with aligned columns."""
    if not rows:
        print("No results found.")
        return

    # Calculate column widths
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, val in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(val)) if val is not None else 4)  # "NULL"

    # Build horizontal separator
    separator = "+-" + "-+-".join("-" * w for w in col_widths) + "-+"

    # Print header
    print(separator)
    header_line = "| " + " | ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " |"
    print(header_line)
    print(separator)

    # Print rows
    for row in rows:
        row_line = "| " + " | ".join(
            (str(val) if val is not None else "NULL").ljust(col_widths[i])
            for i, val in enumerate(row)
        ) + " |"
        print(row_line)
    print(separator)
    print(f"{len(rows)} row(s) returned.\n")

# ----------------------------------------------------------------------
# Database shell class
# ----------------------------------------------------------------------
class DatabaseShell:
    def __init__(self, db_path):
        self.db_path = Path(db_path).resolve()
        self.conn = None
        self.prompt = f"sql ({self.db_path.name})> "

    def connect(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(str(self.db_path))
            return True
        except sqlite3.Error as e:
            print(f"Connection error: {e}")
            return False

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

    def execute_sql(self, sql):
        """Execute a single SQL statement and handle results."""
        if not sql.strip():
            return

        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)

            if sql.strip().lower().startswith("select"):
                rows = cursor.fetchall()
                if rows:
                    headers = [desc[0] for desc in cursor.description]
                    print_table(rows, headers)
                else:
                    print("No results found.")
            else:
                self.conn.commit()
                print(f"Query OK, {cursor.rowcount} row(s) affected.")
        except sqlite3.Error as e:
            print(f"SQL error: {e}")

    # ------------------------------------------------------------------
    # Meta-commands (prefixed with dot)
    # ------------------------------------------------------------------
    def do_exit(self, args):
        """Exit the shell."""
        return False   # signal to stop loop

    def do_quit(self, args):
        """Exit the shell (alias for .exit)."""
        return False

    def do_help(self, args):
        """Show help for meta-commands or sqlite_master."""
        if args and "sqlite_master" in args.lower():
            print("""
SQLITE_MASTER HELP:
  SELECT * FROM sqlite_master;           -> shows all objects (tables, indexes, triggers, views)
  SELECT * FROM sqlite_master WHERE type='table';   -> only tables
            """)
        else:
            print("""
.::::::::::::::: HELP ::::::::::::::.
-------------------------------------
Meta-commands (start with a dot):
  .exit                               - exit the shell
  .quit                               - same as .exit
  .help [sqlite_master]               - show this help or details about sqlite_master
  .tables                             - list all tables
  .indexes [table]                    - list indexes (optionally for a table)
  .schema [table]                      - show CREATE statements for tables, indexes, triggers, views
  .dump [table]                        - dump database content as SQL (optionally for a table)
  .mode (column|csv|list)              - set output mode (only column is implemented)
  .cd <directory>                      - change current working directory
  .read <filename>                      - execute SQL commands from a file

SQL commands can span multiple lines; end them with a semicolon.
""")

    def do_tables(self, args):
        """List all tables in the database."""
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
            rows = cursor.fetchall()
            if rows:
                print("\n".join(row[0] for row in rows))
            else:
                print("No tables found.")
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def do_indexes(self, args):
        """List indexes. If a table name is given, show only indexes for that table."""
        table = args.strip() if args else None
        try:
            cursor = self.conn.cursor()
            if table:
                cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name=? ORDER BY name", (table,))
            else:
                cursor.execute("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index' ORDER BY tbl_name, name")
            rows = cursor.fetchall()
            if rows:
                for row in rows:
                    if table:
                        print(f"{row[0]}")   # index name only
                    else:
                        print(f"{row[1]}.{row[0]}")   # table.index
            else:
                print("No indexes found.")
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def do_schema(self, args):
        """Show CREATE statements for schema objects."""
        table = args.strip() if args else None
        try:
            cursor = self.conn.cursor()
            if table:
                cursor.execute("SELECT type, name, sql FROM sqlite_master WHERE sql NOT NULL AND name=? ORDER BY type, name", (table,))
            else:
                cursor.execute("SELECT type, name, sql FROM sqlite_master WHERE sql NOT NULL ORDER BY type, name")
            rows = cursor.fetchall()
            if rows:
                for typ, name, sql in rows:
                    print(f"-- {typ}: {name}")
                    print(sql + ";")
                    print()
            else:
                print(f"No schema found for '{table}'." if table else "No schema objects found.")
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def do_dump(self, args):
        """Dump the database (or a single table) as SQL."""
        table = args.strip() if args else None
        try:
            cursor = self.conn.cursor()
            if table:
                # Dump table structure
                cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,))
                row = cursor.fetchone()
                if row:
                    print(row[0] + ";")
                else:
                    print(f"Table '{table}' not found.")
                    return
                # Dump table data (simplified)
                cursor.execute(f"SELECT * FROM {table}")
                rows = cursor.fetchall()
                if rows:
                    col_names = [desc[0] for desc in cursor.description]
                    placeholders = ",".join("?" * len(col_names))
                    insert_stmt = f"INSERT INTO {table} ({','.join(col_names)}) VALUES ({placeholders});"
                    for row in rows:
                        # Very simple representation – for production you'd use proper escaping
                        values = []
                        for v in row:
                            if v is None:
                                values.append("NULL")
                            elif isinstance(v, (int, float)):
                                values.append(str(v))
                            else:
                                values.append(repr(str(v)))
                        print(insert_stmt.replace("?", ",".join(values)))  # not perfect, but works for basic data
                else:
                    print(f"-- No data in table {table}")
            else:
                # Full database dump using connection.iterdump()
                for line in self.conn.iterdump():
                    print(line)
        except sqlite3.Error as e:
            print(f"Error: {e}")

    def do_mode(self, args):
        """Set output mode (only 'column' is fully implemented)."""
        mode = args.strip().lower()
        if mode == "column":
            print("Output mode set to 'column'.")
        elif mode in ("csv", "list"):
            print(f"Mode '{mode}' not fully implemented; staying with 'column'.")
        else:
            print(f"Unknown mode '{mode}'. Available: column, csv, list.")

    def do_cd(self, args):
        """Change current working directory."""
        path = args.strip() or str(Path.home())
        try:
            os.chdir(path)
            print(f"Current directory: {os.getcwd()}")
        except Exception as e:
            print(f"Error: {e}")

    def do_read(self, args):
        """Read and execute SQL commands from a file."""
        filename = args.strip()
        if not filename:
            print("Usage: .read <filename>")
            return
        try:
            with open(filename, 'r') as f:
                sql_script = f.read()
            # Simple split on semicolons (ignores semicolons in strings)
            statements = sql_script.split(';')
            for stmt in statements:
                stmt = stmt.strip()
                if stmt:
                    self.execute_sql(stmt + ';')
        except Exception as e:
            print(f"Error reading file: {e}")

    # ------------------------------------------------------------------
    # Main loop
    # ------------------------------------------------------------------
    def run(self):
        """Start the interactive shell."""
        if not self.connect():
            return

        print(f"Connected to: {self.db_path}")
        print("Type '.help' for help, '.exit' to quit.")
        print("SQL statements must end with a semicolon (;).")

        multiline_buffer = []

        while True:
            try:
                if multiline_buffer:
                    line = input("   ...> ")
                else:
                    line = input(self.prompt)

                # Skip empty lines
                if not line:
                    continue

                # Check for meta-command (starts with dot)
                if line.startswith('.'):
                    # Flush any pending multi-line buffer
                    multiline_buffer = []
                    # Parse command and arguments
                    parts = line[1:].split(maxsplit=1)
                    cmd = parts[0].lower()
                    args = parts[1] if len(parts) > 1 else ""

                    # Dispatch to method if exists
                    method_name = f"do_{cmd}"
                    if hasattr(self, method_name):
                        ret = getattr(self, method_name)(args)
                        if ret is False:   # exit signal
                            break
                    else:
                        print(f"Unknown command: {line}. Type '.help'.")
                    continue

                # Handle SQL input (possibly multi-line)
                multiline_buffer.append(line)

                # If the combined input ends with a semicolon, execute it
                combined = "\n".join(multiline_buffer).strip()
                if combined.endswith(';'):
                    self.execute_sql(combined)
                    multiline_buffer = []
                # Otherwise continue reading lines

            except KeyboardInterrupt:
                print("\nInterrupted. Type '.exit' to quit.")
                multiline_buffer = []
            except EOFError:
                print()
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                multiline_buffer = []

        self.close()
        print("Goodbye!")

# ----------------------------------------------------------------------
# Interactive database selection (original style)
# ----------------------------------------------------------------------
def select_database():
    """Prompt the user to choose or create a database, returning its path."""
    # Ensure the 'db' directory exists
    db_dir = Path("db")
    db_dir.mkdir(exist_ok=True)

    db_files = list(db_dir.glob("*.db"))

    if db_files:
        print("Available databases:")
        for i, f in enumerate(db_files, 1):
            print(f"{i}. {f.name}")

        choice = input("\nEnter number, name, or 'new' to create: ").strip()
        if choice.lower() == 'new':
            name = input("New database name (without .db): ").strip()
            if not name:
                name = "database"
            if not name.endswith(".db"):
                name += ".db"
            return db_dir / name
        else:
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(db_files):
                    return db_files[idx]
                else:
                    print("Invalid number. Using first database.")
                    return db_files[0]
            except ValueError:
                # Treat as filename
                if not choice.endswith(".db"):
                    choice += ".db"
                return db_dir / choice
    else:
        print("No databases found in the 'db' directory.")
        name = input("Enter name for new database (without .db): ").strip()
        if not name:
            name = "database"
        if not name.endswith(".db"):
            name += ".db"
        return db_dir / name

# ----------------------------------------------------------------------
# Main entry point (no arguments)
# ----------------------------------------------------------------------
def main():
    db_path = select_database()
    shell = DatabaseShell(db_path)
    shell.run()

if __name__ == "__main__":
    main()
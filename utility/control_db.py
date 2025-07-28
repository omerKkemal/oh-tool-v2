import sqlite3
import os

def export_schema(db_name):
    """Export database schema to schema.sql file"""
    try:
        with sqlite3.connect(f"db/{db_name}") as conn:
            cur = conn.cursor()
            # Get all table creation SQL
            cur.execute("SELECT name, sql FROM sqlite_master WHERE type='table'")
            tables = cur.fetchall()
            
            with open('schema.sql', 'w') as f:
                for table in tables:
                    if table[1]:  # Skip None entries
                        f.write(f"-- Table: {table[0]}\n")
                        f.write(table[1] + ";\n\n")
            print("[+] Schema exported to schema.sql")
            print("[+] You can now upload this file to dbdiagram.io or other ERD tools")
    except Exception as e:
        print(f"[-] Error exporting schema: {e}")

def Help(cmd_help="?"):
    """Display help information"""
    if cmd_help == "?" or cmd_help.lower() == "help":
        print("""
        .:::::::::::::::help::::::::::::::.
        -----------------------------------
        Commands              Description
        --------              -----------
        exit    .............. exit the program
        .schema ............ export database schema to schema.sql
        sqlite_master ........ show tables metadata
        ? or help ............ display this help message
        """)
    elif cmd_help.lower() == "sqlite_master":
        print("""
        SQLITE_MASTER HELP:
        select * from sqlite_master; ........ shows all tables and queries
        select * from sqlite_master where type = 'table'; ... shows all tables
        """)

def main():
    """Main program execution"""
    check_point = True
    
    # Database selection/creation
    if not os.path.exists('db'):
        os.makedirs('db')
    
    check = input("[+] Do you have existing database? [y/n]: ")
    if check.lower() in ("y", "yes"):
        count = 0
        files = os.listdir('db/')
        for file in files:
            if file.endswith(".db"):
                count += 1
                print(file)
        if count != 0:
            db = input("[+] Enter the name of the database: ")
            if not db.endswith(".db"):
                db += ".db"
        else:
            ch = input("[+] No database was found. Create one? [y/n]: ")
            if ch.lower() in ("y", "yes"):
                db = input("[+] Enter your database name (.db): ")
                if not db.endswith(".db"):
                    db += ".db"
            else:
                exit()
    else:
        db = input("[+] Enter your new db name (include .db extension): ")
        if not db.endswith(".db"):
            db += ".db"

    # Main command loop
    while check_point:
        try:
            with sqlite3.connect(f"db/{db}") as conn:
                cur = conn.cursor()
                sql = input("sql> ").strip()
                
                if sql.lower() == "exit":
                    check_point = False
                    continue
                elif sql.lower() in ("?", "help"):
                    Help()
                    continue
                elif sql.lower() == ".schema":
                    export_schema(db)
                    continue
                elif "help" in sql.lower() and "sqlite_master" in sql.lower():
                    Help("sqlite_master")
                    continue

                try:
                    cur.execute(sql)
                    
                    # For SELECT statements, show results
                    if sql.strip().lower().startswith("select"):
                        data = cur.fetchall()
                        if not data:
                            print("No results found")
                        else:
                            # Get column names
                            col_names = [description[0] for description in cur.description]
                            print("\n" + " | ".join(col_names))
                            print("-" * (sum(len(col) for col in col_names) + 3 * len(col_names)))
                            for row in data:
                                print(" | ".join(str(item) if item is not None else "NULL" for item in row))
                            print(f"\n{len(data)} row(s) returned\n")
                    else:
                        # For other statements, show affected rows
                        print(f"Query executed successfully. Rows affected: {cur.rowcount}")
                        conn.commit()
                        
                except sqlite3.Error as e:
                    print(f"SQL Error: {e}")
                    
        except Exception as e:
            print(f"Connection Error: {e}")
            check_point = False

if __name__ == "__main__":
    main()
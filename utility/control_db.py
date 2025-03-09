import sqlite3
import os
chack_point = True
chack = input("[+] Do you have existing database?[y/n]: ")
if chack.lower() == "y" or chack.lower() == "yes":
    count = 0
    files = os.listdir('db/')
    for file in files:
        if ".db" in file:
            count = count + 1
            print(file)
    if count != 0:
        db = input("[+] Enter the name of the database: ")
    else:
        ch = input("[+] No database was found crear one[y/n]: ")
        if chack.lower() == "y" or chack.lower() == "yes":
            db = input("[+] Enter your database(.db): ")
        elif chack.lower() == "n" or chack.lower() == "no":
            exit()
elif chack.lower() == "n" or chack.lower() == "no":
    db = input("[+] Enter your new db name inckudind extention: ")
def Help(cmd_help = "?"):
    if cmd_help == "?" or cmd_help.lower() == "help":
        print("""
        .:::::::::::::::help::::::::::::::.
        -----------------------------------
        Commands              Discription
        --------              -----------
        exit    .............. used to exit.
        sqlite_master ........ sqlite qury for more help type help sqlite_master.
        ? or help ............ display this help message.
        """)
    elif cmd_help.lower() == "sqlite_master":
        print("""
        select * from sqlite_master; ........ this will get you all the tablest and qurey.
        select * from sqlite_master where type = 'table'; .......... this will get all the tables in the database.
        """)

while chack_point:
    with sqlite3.connect(f"db/{db}") as conn:
        cur = conn.cursor()
        sql = input("sql> ")
        if sql == "exit":
            chack_point = False
            continue
        elif sql == "?" or sql.lower() == "help":
            Help()
            continue
        elif "sqlite_master" in sql.lower():
            if "help" in sql.lower():
                sp = sql.split()
                Help(sp[1])
                continue

        try:
            cur.execute(f"{sql}")
            data = cur.fetchall()
            if not data:
                print("no match found or no output return")
            else:
                print(data)
        except Exception as e:
            print(e)


import pandas as pd
from sqlalchemy import create_engine
import sqlite3

def get_serverinfo():
    cnx = create_engine('sqlite:///functions/system_analyzer.db').connect()

    df = pd.read_sql_table(table_name="ServerInfo", con=cnx)

    # print(df["Server_Name"].to_list(), "_+_+_+_+_+_+_+_+_+_")   

    return df 

def entry_into_serverinfo_table(id, server_name, server_path):
    # Store file details in database
    conn = sqlite3.connect("functions/system_analyzer.db")

    c = conn.cursor()

    c.execute(
        "INSERT INTO ServerInfo (Server_Id, Server_Name, Server_Sytem_Path) VALUES (?, ?, ?)",
        (id, server_name, server_path))

    conn.commit()
    conn.close()

    print("Succesfully added server.")

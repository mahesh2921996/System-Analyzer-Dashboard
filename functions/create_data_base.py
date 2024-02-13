import sqlite3

conn = sqlite3.connect("system_analyzer.db")

c = conn.cursor()

# Dorping FILES table if already exists.
c.execute("DROP TABLE IF EXISTS ServerInfo")

# Creating table as per requirement
sql = '''CREATE TABLE ServerInfo(
   Server_Id int auto_increment,
   Server_Name varchar(100) NOT NULL,
   Server_Sytem_Path varchar(1000) NOT NULL
)'''

c.execute(sql)
print("ServerInfo table created successfully........")

conn.commit()
conn.close()
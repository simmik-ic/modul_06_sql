import sqlite3
from sqlite3 import Error

#funkcja tworzy połączenie z bazą danych z podanego pliku (db_file)
#zwraca obiekt połączenia lub None
def create_connection(db_file):
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)
       return None

#funkcja do wykonywania polecenia SQL
#wymaga obiektu utworzonego połączenia (conn) oraz tekstu skryptu (sql)
def execute_sql(conn, sql):
   try:
       c = conn.cursor()
       c.execute(sql)
       conn.commit()                #zapisz zmiany w bazie
   except Error as e:
       print(e)

#stringi zapytań dla utworzenia tabel
str_create_zamowienie = """
    CREATE TABLE IF NOT EXISTS zamowienie (
        id integer,
        skrj integer NOT NULL PRIMARY KEY,
        nr_poc varchar(8) NOT NULL,
        nazwa_poc varchar(100)
    );"""

str_create_rozkladjazdy = """
    CREATE TABLE IF NOT EXISTS rozkladjazdy (
        id integer PRIMARY KEY,
        skrj_rj integer NOT NULL,
        nazwa_stacji text,
        przyjazd text,
        odjazd text,
        FOREIGN KEY (skrj_rj) REFERENCES zamowienie (skrj)
    );"""

str_create_relacja = """
    CREATE
"""
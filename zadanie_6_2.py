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

#funkcja dodaje rekord do wybranej tabeli
def insert(conn, table, record):
    cur = conn.cursor()
    cur.execute(f"PRAGMA table_info({table});")
    kolumny_tuple = cur.fetchall()
    kolumny = [kolumna[1] for kolumna in kolumny_tuple]
    if kolumny[0] == "id": 
        kolumny = kolumny[1:]
    kol = ", ".join(kolumny)
    qmarks = ("?," * len(kolumny))[:-1]

    sql = f"""INSERT INTO {table}({kol}) VALUES({qmarks})"""

    cur = conn.cursor()
    cur.execute(sql, record)
    conn.commit()
    return cur.lastrowid


#funkcja zwraca wszystkie rekordy w wybranej tabeli (table)
def select_all(conn, table):
   cur = conn.cursor()
   cur.execute(f"SELECT * FROM {table}")
   rows = cur.fetchall()
   return rows

#funkcja zwraca rekordy w wybranej tabeli (table), które spełniają podane warunki (query)
#warunki podawane są jako słownik atrybutów tabeli i wartości
def select_where(conn, table, **query):
   cur = conn.cursor()
   qs = []
   values = ()
   for k, v in query.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)
   cur.execute(f"SELECT * FROM {table} WHERE {q}", values)
   rows = cur.fetchall()
   return rows

#funkcja aktualizuje wartości dla wybranego id rekordu w wybranej tabeli
def update(conn, table, id, **kwargs):
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (id, )

   sql = f''' UPDATE {table}
             SET {parameters}
             WHERE skrj = ?'''      #do dopracowania - w tej chwili update działa tylko w tabeli 'zamowienie'
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

#funkcja usuwa rekordy w wybranej tabeli, które spełniają podane parametry
def delete_where(conn, table, **kwargs):
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {table} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

#funkcja usuwa wszystkie rekordy w wybranej tabeli
def delete_all(conn, table):
   sql = f'DELETE FROM {table}'
   cur = conn.cursor()
   cur.execute(sql)
   conn.commit()
   print("Deleted")



#stringi zapytań dla utworzenia tabel
str_create_zamowienie = """
    CREATE TABLE IF NOT EXISTS zamowienie (
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
    CREATE TABLE IF NOT EXISTS relacja (
        id integer PRIMARY KEY,
        skrj_rel integer NOT NULL,
        stacja_poczatkowa text,
        stacja_koncowa text,
        FOREIGN KEY (skrj_rel) REFERENCES zamowienie (skrj)
    );"""



#--------------------------------------------------------------------------
#Część wykonywalna

#połącz się z bazą danych
db_file = "db_rrj2025_26.db"
conn = create_connection(db_file)

#utwórz tabele w bazie danych
execute_sql(conn, str_create_zamowienie)
execute_sql(conn, str_create_rozkladjazdy)
execute_sql(conn, str_create_relacja)

#usuń wszystkie rekordy w tabeli 'zamowienie'
delete_all(conn, 'zamowienie')

#nowa lista rekordów
rekordy = [
    (3482, '61108', 'Porazińska'),
    (13754, '1620', 'Asnyk'),
    (10875, '5620', 'Słowacki'),
    (9483, '1604', None),
    (10452, '6100', 'Panodramat'),
    (9484, '1650', None)
]

#dodaj rekordy do tabeli
for rekord in rekordy:
    insert(conn, 'zamowienie', rekord)

#popraw nazwę pociągu
update(conn, 'zamowienie', 10452, nazwa_poc="Panorama")

#wyświetl informacje o pociągach
rezultaty = select_where(conn, 'zamowienie', nr_poc='1620')
rezultaty = select_all(conn, 'zamowienie')
for rezultat in rezultaty:
    print(rezultat)

#zamknij połączenie
conn.close
import datetime
import os
import json
import re
import psycopg2 as dbapi2


class People:
    def __init__(self, resim, isim, mekan, yas, universite, work):
        self.resim = resim
        self.isim = isim
        self.mekan = mekan
        self.yas = yas
        self.universite = universite
        self.work = work


def init_kisiler_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS KISILER (
    ID SERIAL PRIMARY KEY,
    RESIM VHARCHAR DEAFULT,
    ISIM VARCHAR NOT NULL,
    MEKAN VARCHAR NOT NULL,
    YAS INTEGER,
    UNIVERSITE VARCHAR,
    WORK VARCHAR)"""

    cursor.execute(query)
    fill_kisiler_db(cursor)


def fill_kisiler_db():
    query = """INSERT INTO KISILER (RESIM, ISIM, MEKAN, YAS, UNIVERSITE, WORK) VALUES ('profil1.jpg', 'Tugba Ozkal','Afyonkarahisar',22, 'Student', 'ITU')"""
    cursor.execute(query)
    query = """INSERT INTO KISILER (RESIM, ISIM, MEKAN, YAS, UNIVERSITE, WORK) VALUES ('defaultprofil.png', 'Cagri Gokce', 'Ankara', 22, 'Engineer', 'ITU')"""
    cursor.execute(query)
    query = """INSERT INTO KISILER (RESIM, ISIM, MEKAN, YAS, UNIVERSITE, WORK) VALUES ('profil2.jpg', 'Furkan Evirgen', 'Istanbul', 26, 'CEO', 'BAU')"""
    cursor.execute(query)


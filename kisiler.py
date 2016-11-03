import datetime
import os
import json
import re
import psycopg2 as dbapi2


class People:
    def __init__(self, isim, resim, mekan, yas, universite, work):
        self.isim = isim
        self.resim = resim
        self.mekan = mekan
        self.yas = yas
        self.universite = universite
        self.work = work


def init_kisiler_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS KISILER (
    ID SERIAL PRIMARY KEY,
    ISIM VARCHAR(30) NOT NULL,
    RESIM VARCHAR(80),
    MEKAN VARCHAR(15) NOT NULL,
    YAS INTEGER,
    UNIVERSITE VARCHAR(15),
    WORK VARCHAR(15))"""

    cursor.execute(query)
    fill_kisiler_db(cursor)


def fill_kisiler_db(cursor):
    query = """INSERT INTO KISILER (RESIM, ISIM, MEKAN, YAS, UNIVERSITE, WORK) VALUES ('profil1.jpg' ,'Tugba Ozkal', 'Afyonkarahisar', 22, 'ITU', 'Student');
    INSERT INTO KISILER (RESIM,ISIM, MEKAN, YAS, UNIVERSITE, WORK) VALUES ('defaultprofil.png', 'Cagri Gokce', 'Ankara', 22, 'ITU', 'Engineer');
    INSERT INTO KISILER (RESIM,ISIM, MEKAN, YAS, UNIVERSITE, WORK) VALUES ('profil2.jpg', 'Furkan Evirgen', 'Istanbul', 26, 'BAU', 'CEO');"""

    cursor.execute(query)


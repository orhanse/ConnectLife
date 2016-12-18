import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Kisiler:
    def __init__(self, isim, resim, mekan, yas, universite, work, pozisyon, dil):
        self.isim = isim
        self.resim = resim
        self.mekan = mekan
        self.yas = yas
        self.universite = universite
        self.work = work
        self.pozisyon = pozisyon
        self.dil = dil


def init_kisiler_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS KISILER (
    ID SERIAL PRIMARY KEY,
    ISIM VARCHAR(30) NOT NULL,
    RESIM VARCHAR(80) NOT NULL DEFAULT 'defaultprofil.png',
    MEKAN VARCHAR(15) NOT NULL,
    YAS INTEGER,
    UNIVERSITE INTEGER REFERENCES UNIVERSITY(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    WORK INTEGER REFERENCES SIRKET(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    POZISYON INTEGER REFERENCES MESLEKLER(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    DIL INTEGER REFERENCES DIL(ID) ON DELETE CASCADE ON UPDATE CASCADE )"""

    cursor.execute(query)
    fill_kisiler_db(cursor)


def fill_kisiler_db(cursor):
    query = """INSERT INTO KISILER (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                   VALUES ('Tugba Ozkal', 'profil1.jpg' ,'Afyonkarahisar', 22, 1, 1, 1, 3);
                INSERT INTO KISILER (ISIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                    VALUES ('Cagri Gokce', 'Ankara', 22, 2, 2, 2, 1);
                INSERT INTO KISILER (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                    VALUES ('Furkan Evirgen', 'profil2.jpg','Istanbul', 26, 2, 1, 3, 1);
                INSERT INTO KISILER (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                    VALUES ('Kemal Hazım Ekenel', 'ekenel.png','Istanbul', 38, 2, 1, 4, 2);
                INSERT INTO KISILER (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                    VALUES ('Jeo Kaeser', 'kaeser.jpg','Almanya', 59, 2, 1, 5, 4);"""

    cursor.execute(query)


def add_kisiler(cursor, request, kisi1):
        query = """INSERT INTO KISILER
        (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL) VALUES (
        %s,
        %s,
        INITCAP(%s),
        %s,
        %s,
        %s,
        %s,
        %s
        )"""
        cursor.execute(query, (kisi1.isim, kisi1.resim, kisi1.mekan, kisi1.yas,
                               kisi1.universite, kisi1.work, kisi1.pozisyon, kisi1.dil))


def delete_kisiler(cursor, id):
        query="""DELETE FROM KISILER WHERE ID = %s"""
        cursor.execute(query, id)


def update_kisiler(cursor, id, kisi1):
            query="""
            UPDATE KISILER
            SET ISIM=%s,
            RESIM=%s,
            MEKAN=INITCAP(%s),
            YAS=%s,
            UNIVERSITE=%s,
            WORK=%s,
            POZISYON=%s,
            DIL=%s
            WHERE ID=%s
            """
            cursor.execute(query,(kisi1.isim, kisi1.resim, kisi1.mekan, kisi1.yas,
                                  kisi1.universite, kisi1.work, kisi1.pozisyon, kisi1.dil, id))
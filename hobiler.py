import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Hobiler:
    def __init__(self, isim, resim,  alan, koordinator, aciklama):
        self.isim = isim
        self.resim = resim
        self.alan = alan
        self.koordinator = koordinator
        self.aciklama = aciklama


def init_hobiler_db(cursor):

    query = """CREATE TABLE IF NOT EXISTS HOBILER (
    ID SERIAL PRIMARY KEY,
    ISIM varchar(100) NOT NULL,
    RESIM VARCHAR(80) NOT NULL DEFAULT 'defaulthobi.jpg',
    ALAN varchar(100) NOT NULL,
    KOORDINATOR INTEGER NOT NULL REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    ACIKLAMA varchar(1000) NOT NULL
   )"""

    cursor.execute(query)
    insert_hobiler(cursor)

def insert_hobiler(cursor):
    query = """INSERT INTO HOBILER
        (ISIM, RESIM, ALAN, KOORDINATOR, ACIKLAMA) VALUES (
        'Okculuk',
        'okculuk.jpg',
        'Spor',
        4,
        'Okculuk ok ve yay ile yapilan bir hobidir..'
        );
        INSERT INTO HOBILER
        (ISIM, RESIM, ALAN, KOORDINATOR, ACIKLAMA) VALUES (
        'Dagcilik',
        'dagcilik.jpg',
        'Spor',
        3,
        'Daglara ciktin mi tum ulke, tum dunya ayalarinin altindadir, boyle bir hobidir..'
        );
        INSERT INTO HOBILER
        (ISIM, RESIM, ALAN, KOORDINATOR, ACIKLAMA) VALUES (
        'Resim',
        'resim.jpg',
        'Sanat',
        1,
        'Belki bir picasso olamayabilirsin ama kendini bulacagin bir hobidir..'
        );
        INSERT INTO HOBILER
        (ISIM, RESIM, ALAN, KOORDINATOR, ACIKLAMA) VALUES (
        'Gitar',
        'gitar.jpg',
        'Muzik',
        2,
        'Herkes muzigi sever, en azindan dinlemeyi, siz de bir adim oteye gecin...'
        );
        ;"""

    cursor.execute(query)


def add_hobiler(cursor, request, hobi1):
        query = """INSERT INTO HOBILER
        (ISIM, RESIM, ALAN, KOORDINATOR, ACIKLAMA) VALUES (
        INITCAP(%s),
        INITCAP(%s),
        INITCAP(%s),
        %s,
        INITCAP(%s)
        )"""
        cursor.execute(query, (hobi1.isim, hobi1.resim, hobi1.alan,
                               hobi1.koordinator, hobi1.aciklama))

def delete_hobiler(cursor, id):
        query="""DELETE FROM HOBILER WHERE ID = %s"""
        cursor.execute(query, id)


def update_hobiler(cursor, id, hobi1):
            query="""
            UPDATE HOBILER
            SET ISIM=INITCAP(%s),
            RESIM=INITCAP(%s),
            ALAN=INITCAP(%s),
            KOORDINATOR=%s,
            ACIKLAMA=INITCAP(%s)
            WHERE ID=%s
            """
            cursor.execute(query, (hobi1.isim, hobi1.resim, hobi1.alan,
                               hobi1.koordinator, hobi1.aciklama, id))
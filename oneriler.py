import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Oneriler:
    def __init__(self, resim, kname, kpozisyon, baglanti ):

        self.resim= resim
        self.kname = kname
        self.kpozisyon = kpozisyon
        self.baglanti = baglanti

def init_oneriler_db(cursor):

    query = """CREATE TABLE IF NOT EXISTS ONERILER (
    ID SERIAL PRIMARY KEY,
    RESIM varchar(100) NOT NULL DEFAULT 'defaultprofil.png',
    KNAME INTEGER REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    KPOZISYON INTEGER REFERENCES MESLEKLER(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    BAGLANTI INTEGER DEFAULT 0
   )"""

    cursor.execute(query)
    insert_oneriler(cursor)

def insert_oneriler(cursor):
    query = """INSERT INTO ONERILER
        (RESIM,KNAME,KPOZISYON,BAGLANTI) VALUES (
        'profil1.jpg',1, 1,11);
        INSERT INTO ONERILER
        (KNAME,KPOZISYON,BAGLANTI) VALUES (
        2,2,7);
        INSERT INTO ONERILER
        (RESIM,KNAME,KPOZISYON,BAGLANTI) VALUES (
        'profil2.jpg',3,3,9);
        INSERT INTO ONERILER
        (RESIM,KNAME,KPOZISYON,BAGLANTI) VALUES (
        'ekenel.png',4,4,15);
        INSERT INTO ONERILER
        (RESIM,KNAME,KPOZISYON,BAGLANTI) VALUES (
        'kaeser.jpg',5,5,8);"""

    cursor.execute(query)

def add_oneriler(cursor, request, oneri1):
        query = """INSERT INTO ONERILER
        (RESIM,KNAME,KPOZISYON,BAGLANTI) VALUES (
        %s,
        %s,
        %s,
        %s
        )"""
        cursor.execute(query, (oneri1.resim, oneri1.kname, oneri1.kpozisyon,
                               oneri1.baglanti))

def delete_oneriler(cursor, id):
        query="""DELETE FROM ONERILER WHERE ID = %s"""
        cursor.execute(query, id)


def update_oneriler(cursor, id, oneri1):
            query="""
            UPDATE ONERILER
            SET RESIM=%s,
            KNAME=%s,
            KPOZISYON=%s,
            BAGLANTI=%s
            WHERE ID=%s
            """
            cursor.execute(query, (oneri1.resim, oneri1.kname, oneri1.kpozisyon,
                                   oneri1.baglanti, id))

import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Meslekler:
    def __init__(self, isim):
        self.isim = isim



def init_meslekler_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS MESLEKLER (
    ID SERIAL PRIMARY KEY,
    ISIM VARCHAR(30) NOT NULL
    )"""

    cursor.execute(query)
    fill_meslekler_db(cursor)


def fill_meslekler_db(cursor):
    query = """ INSERT INTO MESLEKLER (ISIM)
                    VALUES('Kurucu');
                INSERT INTO MESLEKLER (ISIM)
                    VALUES('Muhendis');
                INSERT INTO MESLEKLER (ISIM)
                    VALUES('Proje Yoneticisi');
                INSERT INTO MESLEKLER (ISIM)
                    VALUES('Teknisyen');
                INSERT INTO MESLEKLER (ISIM)
                    VALUES('Ogretmen');
                INSERT INTO MESLEKLER (ISIM)
                    VALUES('Avukat');
                INSERT INTO MESLEKLER (ISIM)
                    VALUES('Hakem');
                """

    cursor.execute(query)


def add_meslekler(cursor, request, meslek1):
        query = """INSERT INTO MESLEKLER (ISIM)
        VALUES( INITCAP(%s) )"""
        cursor.execute(query, (meslek1.isim))


def delete_meslekler(cursor, id):
        query="""DELETE FROM MESLEKLER WHERE ID = %s"""
        cursor.execute(query, id)


def update_meslekler(cursor, id, meslek1):
            query="""
            UPDATE MESLEKLER
            SET ISIM=%s
            WHERE ID=%s
            """
            cursor.execute(query, (meslek1.isim, id))
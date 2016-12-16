import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Mailler:
    def __init__(self, isim, mail, sifre):
        self.isim = isim
        self.mail = mail
        self.sifre = sifre



def init_mailler_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS MAILLER (
    ID SERIAL PRIMARY KEY,
    ISIM INTEGER REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE NOT NULL,
    MAIL VARCHAR(30) NOT NULL,
    SIFRE VARCHAR(30) NOT NULL
    )"""

    cursor.execute(query)
    fill_mailler_db(cursor)


def fill_mailler_db(cursor):
    query = """ INSERT INTO MAILLER (ISIM, MAIL, SIFRE)
                    VALUES(1, 'ozkalt@itu.edu.tr', 'tugba123');
                INSERT INTO MAILLER (ISIM, MAIL, SIFRE)
                    VALUES(2, 'cagri.gokce@itu.edu.tr', 'cagri123');
                INSERT INTO MAILLER (ISIM, MAIL, SIFRE)
                    VALUES(3, 'furkan@arhenius.com', 'furkan123');
                INSERT INTO MAILLER (ISIM, MAIL, SIFRE)
                    VALUES(4, 'ekenel@itu.edu.tr', 'hazim123');
                """
    cursor.execute(query)


def add_mailler(cursor, request, mail1):
        query = """INSERT INTO MAILLER (ISIM, MAIL, SIFRE)
        VALUES( %s, %s, %s )"""
        cursor.execute(query, (mail1.isim, mail1.mail, mail1.sifre))


def delete_mailler(cursor, id):
        query="""DELETE FROM MAILLER WHERE ID = %s"""
        cursor.execute(query, id)


def update_mailler(cursor, id, mail1):
            query = """
            UPDATE MAILLER
            SET ISIM = %s,
            MAIL = %s,
            SIFRE = %s
            WHERE ID=%s
            """
            cursor.execute(query, (mail1.isim, mail1.mail, mail1.sifre, id))
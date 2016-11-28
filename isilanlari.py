import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Isilanlari:
    def __init__(self,sirketname, pozisyon,lokasyon, basvuru, tarih):
        self.sirketname = sirketname
        self.pozisyon = pozisyon
        self.lokasyon = lokasyon
        self.basvuru = basvuru
        self.tarih = tarih

def init_isilanlari_db(cursor):

    query = """CREATE TABLE IF NOT EXISTS ISILANLARI (
    ID SERIAL PRIMARY KEY,
    SIRKETNAME INTEGER NOT NULL REFERENCES SIRKET(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    POZISYON varchar(100) NOT NULL,
    LOKASYON varchar(80) NOT NULL,
    BASVURU varchar(100) DEFAULT 0,
    TARIH date NOT NULL)"""

    cursor.execute(query)
    insert_isilanlari(cursor)

def insert_isilanlari(cursor):
    query = """INSERT INTO ISILANLARI
        (SIRKETNAME, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        1,
        'Elektrik Elektronik Mühendisi',
        'İzmir,Manisa',
        '10000+',
        to_date('17.10.2016', 'DD-MM-YYYY')
        );
        INSERT INTO ISILANLARI
         (SIRKETNAME, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        2,
        'Yazılım Mühendisi',
        'İstanbul(Avr.)',
        '1000-1500',
        to_date('16.10.2016', 'DD-MM-YYYY')
        );
        INSERT INTO ISILANLARI
         (SIRKETNAME, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        1,
        'PCB Tasarım Mühendisi',
        'Ankara',
        '5000+',
         to_date('15.10.2016', 'DD-MM-YYYY')
        );
        INSERT INTO ISILANLARI
       (SIRKETNAME, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        2,
        'Software Developer',
        'İstanbul(Asya)',
        '50-200',
         to_date('14.10.2016', 'DD-MM-YYYY')
        );"""
    cursor.execute(query)


def add_isilanlari(cursor, request, ilan1):
        query = """INSERT INTO ISILANLARI
        (SIRKETNAME, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        %s,
        INITCAP(%s),
        INITCAP(%s),
        %s,
        to_date(%s, 'DD-MM-YYYY')
        )"""
        cursor.execute(query, (ilan1.sirketname, ilan1.pozisyon, ilan1.lokasyon,
                               ilan1.basvuru, ilan1.tarih))

def delete_isilanlari(cursor, id):
        query="""DELETE FROM ISILANLARI WHERE ID = %s"""
        cursor.execute(query, id)


def update_isilanlari(cursor, id, ilan1):
            query="""
            UPDATE ISILANLARI
            SET SIRKETNAME=%s,
            POZISYON=INITCAP(%s),
            LOKASYON=%s,
            BASVURU=%s,
            TARIH=to_date(%s, 'DD-MM-YYYY')
            WHERE ID=%s
            """
            cursor.execute(query, (ilan1.sirketname, ilan1.pozisyon, ilan1.lokasyon,
                                   ilan1.basvuru, ilan1.tarih, id))
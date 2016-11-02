import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Isilanlari:
    def __init__(self, pozisyon, sirket, lokasyon, basvuru, tarih):
        self.sirket = sirket
        self.pozisyon = pozisyon
        self.lokasyon = lokasyon
        self.basvuru = basvuru
        self.tarih = tarih

def init_isilanlari_db(cursor):

    query = """CREATE TABLE IF NOT EXISTS ISILANLARI (
    ID SERIAL PRIMARY KEY,
    SIRKET varchar(100) NOT NULL,
    POZISYON varchar(100) NOT NULL,
    LOKASYON varchar(80) NOT NULL,
    BASVURU varchar(100),
    TARIH date NOT NULL)"""

    cursor.execute(query)
    insert_isilanlari(cursor)

def insert_isilanlari(cursor):
    query = """INSERT INTO ISILANLARI
        (SIRKET, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        'Vestel A.Ş.',
        'Elektrik Elektronik Mühendisi',
        'İzmir,Manisa',
        '10000+',
        to_date('17.10.2016', 'DD-MM-YYYY')
        );
        INSERT INTO ISILANLARI
         (SIRKET, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        'Arçelik A.Ş.',
        'Yazılım Mühendisi',
        'İstanbul(Avr.)',
        '1000-1500',
        to_date('16.10.2016', 'DD-MM-YYYY')
        );
        INSERT INTO ISILANLARI
         (SIRKET, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        'Aselsan Elektronik San. ve Tic. A.Ş.',
        'PCB Tasarım Mühendisi',
        'Ankara',
        '5000+',
         to_date('15.10.2016', 'DD-MM-YYYY')
        );
        INSERT INTO ISILANLARI
       (SIRKET, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        'Siemens',
        'Software Developer',
        'İstanbul(Asya)',
        '50-200',
         to_date('14.10.2016', 'DD-MM-YYYY')
        );"""
    cursor.execute(query)


def add_isilanlari(cursor, request, ilan1):
        query = """INSERT INTO ISILANLARI
        (SIRKET, POZISYON, LOKASYON, BASVURU, TARIH) VALUES (
        INITCAP(%s),
        INITCAP(%s),
        INITCAP(%s),
        %s,
        to_date(%s, 'DD-MM-YYYY')
        )"""
        cursor.execute(query, (ilan1.sirket, ilan1.pozisyon, ilan1.lokasyon,
                               ilan1.basvuru, ilan1.tarih))

def delete_isilanlari(cursor, id):
        query="""DELETE FROM ISILANLARI WHERE ID = %s"""
        cursor.execute(query, id)


def update_isilanlari(cursor, id, ilan1):
            query="""
            UPDATE ISILANLARI
            SET SIRKET=INITCAP(%s),
            POZISYON=INITCAP(%s),
            LOKASYON=%s,
            BASVURU=%s,
            TARIH=to_date(%s, 'DD-MM-YYYY')
            WHERE ID=%s
            """
            cursor.execute(query, (ilan1.sirket, ilan1.pozisyon, ilan1.lokasyon,
                                   ilan1.basvuru, ilan1.tarih, id))
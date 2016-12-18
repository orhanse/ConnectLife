import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Projeler:
    def __init__(self, baslik, konu, sahip, tarih, uniname, aciklama):
        self.baslik = baslik
        self.konu = konu
        self.sahip = sahip
        self.tarih = tarih
        self.uniname = uniname
        self.aciklama = aciklama


def init_projeler_db(cursor):

    query = """CREATE TABLE IF NOT EXISTS PROJELER (
    ID SERIAL PRIMARY KEY,
    BASLIK varchar(500) NOT NULL,
    KONU INTEGER NOT NULL REFERENCES MESLEKLER(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    SAHIP INTEGER NOT NULL REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    TARIH integer NOT NULL,
    UNINAME INTEGER NOT NULL REFERENCES UNIVERSITY(ID) ON DELETE CASCADE ON UPDATE CASCADE,
    ACIKLAMA varchar(1000) NOT NULL
   )"""

    cursor.execute(query)
    insert_projeler(cursor)

def insert_projeler(cursor):
    query = """INSERT INTO PROJELER
        (BASLIK, KONU, SAHIP, TARIH, UNINAME, ACIKLAMA) VALUES (
        'Haptik Koltuk Kullanici Arayuzu'
        2,
        2,
        2016,
        1,
        'Daha iyi bir kullanici deneyimi icin, ve daha mutlu bir hayat icin kullanilan haptik koltuklar cok yakinda insanligin hizmetinde...'
        );
        INSERT INTO PROJELER
        (BASLIK, KONU, SAHIP, TARIH, UNINAME, ACIKLAMA) VALUES (
        'Goruntu Isleme Projesi'
        2,
        4,
        2015,
        2,
        'Goruntu isleme dalinda sayisiz odul alan degereli bilim adamlarindan Hazim Ekenelden bir proje daha...'
        );
        INSERT INTO PROJELER
        (BASLIK, KONU, SAHIP, TARIH, UNINAME, ACIKLAMA) VALUES (
        'Gelecek Teknolojisi'
        3,
        1,
        2015,
        3,
        'Projemizle sizi gelecege bir adim daha yaklastiriyoruz...'
        );
        INSERT INTO PROJELER
        (BASLIK, KONU, SAHIP, TARIH, UNINAME, ACIKLAMA) VALUES (
        'Ucan Arabalar ve Yururyen Ucaklar'
        3,
        1,
        2021,
        4,
        'Bu Projemiz daha dusunce asamasindadir...'
        );"""

    cursor.execute(query)


def add_projeler(cursor, request, proje1):
        query = """INSERT INTO PROJELER
        (BASLIK, KONU, SAHIP, TARIH, UNINAME, ACIKLAMA) VALUES (
        INITCAP(%s),
        %s,
        %s,
        %s,
        %s,
        INITCAP(%s)
        )"""
        cursor.execute(query, (proje1.baslik, proje1.konu, proje1.sahip,
                               proje1.tarih, proje1.uniname, proje1.aciklama))

def delete_projeler(cursor, id):
        query="""DELETE FROM PROJELER WHERE ID = %s"""
        cursor.execute(query, id)


def update_projeler(cursor, id, proje1):
            query="""
            UPDATE PROJELER
            SET BASLIK = INITCAP(%s),
            KONU= %s,
            SAHIP =%s,
            TARIH=%s,
            UNINAME=%s,
            ACIKLAMA = INITCAP(%s)
            WHERE ID=%s
            """
            cursor.execute(query, (proje1.baslik, proje1.konu, proje1.sahip,
                                   proje1.tarih, proje1.uniname, proje1.aciklama, id))
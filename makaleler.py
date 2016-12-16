import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Makaleler:
    def __init__(self, konu, baslik , yazar, tarih, uniname):
        self.konu = konu
        self.baslik = baslik
        self.yazar = yazar
        self.tarih = tarih
        self.uniname = uniname


def init_makaleler_db(cursor):

    query = """CREATE TABLE IF NOT EXISTS MAKALELER (
    ID SERIAL PRIMARY KEY,
    KONU varchar(30) NOT NULL,
    BASLIK varchar(500) NOT NULL,
    YAZAR varchar(100) NOT NULL,
    TARIH integer NOT NULL,
    UNINAME INTEGER NOT NULL REFERENCES UNIVERSITY(ID) ON DELETE CASCADE ON UPDATE CASCADE
   )"""

    cursor.execute(query)
    insert_makaleler(cursor)

def insert_makaleler(cursor):
    query = """INSERT INTO MAKALELER
        (KONU,BASLIK, YAZAR, TARIH, UNINAME) VALUES (
        'Bilişim',
        'Hastane Bilişim Sistemlerinin Teknoloji Seçimi Açısından İncelenmesi',
        'Ülgen,Yekta',
        1994,
        3
        );
        INSERT INTO MAKALELER
        (KONU,BASLIK, YAZAR, TARIH, UNINAME ) VALUES (
        'Enerji',
        'Türkiyede Elektrik Üretimi için Enerji Kaynaklarının Etkinliğinin Değerlendirilmesi',
        'Özyiğit, Tamer',
        2008,
        4
        );
        INSERT INTO MAKALELER
        (KONU,BASLIK, YAZAR, TARIH, UNINAME ) VALUES (
        'Akademik Başarı',
        'Üniversite öğrencilerinin zaman yönetimleri ile akademik başarıları arasındaki ilişki',
        'Alay, Sema',
        2003,
        1
        );
        INSERT INTO MAKALELER
       (KONU,BASLIK, YAZAR, TARIH, UNINAME ) VALUES (
        'Girişimcilik',
        'Girişimcilik Eğilimi ve Pazar Odaklılığın İş Performansına Etkileri',
        'Özsomer, Ayşegül',
        2002,
        2
        );"""

    cursor.execute(query)


def add_makaleler(cursor, request, makale1):
        query = """INSERT INTO MAKALELER
        (KONU,BASLIK, YAZAR, TARIH, UNINAME ) VALUES (
        INITCAP(%s),
        INITCAP(%s),
        INITCAP(%s),
        %s,
        %s
        )"""
        cursor.execute(query, (makale1.konu,makale1.baslik, makale1.yazar,
                               makale1.tarih, makale1.uniname))

def delete_makaleler(cursor, id):
        query="""DELETE FROM MAKALELER WHERE ID = %s"""
        cursor.execute(query, id)


def update_makaleler(cursor, id, makale1):
            query="""
            UPDATE MAKALELER
            SET KONU=INITCAP(%s), 
            BASLIK=INITCAP(%s),
            YAZAR=INITCAP(%s),
            TARIH=%s,
            UNINAME=%s
            WHERE ID=%s
            """
            cursor.execute(query, (makale1.konu,makale1.baslik, makale1.yazar,
                                   makale1.tarih,makale1.uniname, id))
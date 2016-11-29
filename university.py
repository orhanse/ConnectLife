import json
import datetime
import re
import os
import psycopg2 as dbapi2

class University:
    def __init__(self, name, foundation_date, location, small_info, photo, rector_id):
        self.name = name
        self.foundation_date = foundation_date
        self.location = location
        self.small_info = small_info
        self.photo = photo
        self.rector_id = rector_id

def init_universities_db(cursor):
    query = """CREATE TABLE UNIVERSITY (
        ID SERIAL,
        NAME VARCHAR(100) NOT NULL,
        FOUNDATION_DATE VARCHAR(4) NOT NULL,
        LOCATION VARCHAR(80) NOT NULL,
        SMALL_INFO VARCHAR(500),
        PHOTO VARCHAR(80),
        RECTOR_ID INTEGER NOT NULL REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE DEFAULT 1,
        PRIMARY KEY (ID)
        )"""
    cursor.execute(query)
    insert_university(cursor)

def insert_university(cursor):
    query = """INSERT INTO UNIVERSITY
        (NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO) VALUES (
        'Istanbul Technical University',
        1773,
        'Maslak/Istanbul',
        'Çağın önde gelen üniversitelerinden olan İstanbul Teknik Üniversitesi, her yıl binlerce başarılı mühendis yetiştiriyor. Sizi de üniversitemizde görmekten mutluluk duyarız.',
        'itu.jpg'
        );
        INSERT INTO UNIVERSITY
        (NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO) VALUES (
        'Bogazici University',
        1863,
        'Bebek/Istanbul',
        'Üniversiteler; bilim, düşünce ve teknoloji üretme, yaygınlaştırma ve bunları topluma kazandırma suretiyle yerel ve evrensel gelişime katkıda bulunan en temel öğretim, araştırma ve bilgi yayma kurumlarıdır.',
        'bogazici.png'
        );
        INSERT INTO UNIVERSITY
        (NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO) VALUES (
        'Koc University',
        1993,
        'Sariyer/Istanbul',
        'Koç Üniversitesi bir Mükemmeliyet Merkezi olma misyonuyla, üstün yetenekli gençler ile değerli öğretim görevlilerini biraraya getirerek; bilime evrensel düzeyde katkıda bulunmayı amaçlamaktadır.',
        'koc.jpg'
        );
        INSERT INTO UNIVERSITY
        (NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO) VALUES (
        'Sabanci University',
        1994,
        'Tuzla/Istanbul',
        'Türkiye de bir dünya üniversitesi kurma vizyonuyla, Ağustos 1995 te, 22 ülkeden, farklı disiplinlerde çalışan 50 nin üzerinde bilim adamı, araştırmacı, öğrenci ve iş adamı İstanbul da düzenlenen arama konferansında bir araya geldi.',
        'sabanci.jpg'
        )"""
    cursor.execute(query)

def add_university(cursor, request, university1):
    query = """INSERT INTO UNIVERSITY
        (NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO, RECTOR_ID) VALUES (
        INITCAP(%s),
        %s,
        INITCAP(%s),
        INITCAP(%s),
        %s,
        %s
        )"""
    cursor.execute(query, (university1.name, university1.foundation_date, university1.location, university1.small_info, university1.photo, university1.rector_id))

def delete_university(cursor, id):
    query ="""DELETE FROM UNIVERSITY WHERE ID = %s"""
    cursor.execute(query, id)

def update_university(cursor, id, university1):
    query = """
        UPDATE UNIVERSITY
        SET NAME=INITCAP(%s),
        FOUNDATION_DATE=%s,
        LOCATION=INITCAP(%s),
        SMALL_INFO=INITCAP(%s),
        PHOTO=%s,
        RECTOR_ID =%s
        WHERE ID=%s
        """

    cursor.execute(query, (university1.name, university1.foundation_date, university1.location, university1.small_info, university1.photo, university1.rector_id, id))
import json
import datetime
import re
import os
import psycopg2 as dbapi2

from flask import Flask
from flask import render_template
from flask import redirect
from flask import request
from flask.helpers import url_for

class Sirket:
    def __init__(self, name, date, location, ceo_id, work_area, photo):
        self.name = name
        self.date = date
        self.location = location
        self.ceo_id = ceo_id
        self.work_area = work_area
        self.photo = photo

def init_sirketler_db(cursor):
    query = """DROP TABLE IF EXISTS SIRKET"""
    cursor.execute(query)
    query = """CREATE TABLE SIRKET (
        ID SERIAL PRIMARY KEY,
        NAME varchar(100) NOT NULL,
        DATE varchar NOT NULL,
        LOCATION varchar(80) NOT NULL,
        CEO_ID INTEGER NOT NULL REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE DEFAULT 1,
        WORK_AREA varchar(500),
        PHOTO varchar(80)
        )"""
    cursor.execute(query)
    insert_sirket(cursor)

def insert_sirket(cursor):
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, CEO_ID, WORK_AREA, PHOTO) VALUES (
        'SiMiT Lab',
        2010,
        'Istanbul/Türkiye',
        4,
        'Akıllı Etkileşim, Mobil İstihbarat, Multimedya Teknolojileri',
        'itulogo.png'
        )"""
    cursor.execute(query)
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, CEO_ID, WORK_AREA, PHOTO) VALUES (
        'Siemens AG',
        1847,
        'Berlin/Almanya',
        5,
        'Endüstri, Enerji, Sağlık',
        'siemens1.png'
        )"""
    cursor.execute(query)
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, CEO_ID, WORK_AREA, PHOTO) VALUES (
        'Vestel',
        1984,
        'Manisa/Türkiye',
        2,
        'Beyaz eşya, Elektrikli ev gereçleri, Otel ürünleri üretimi',
        'vestel1.png'
        )"""
    cursor.execute(query)
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, CEO_ID, WORK_AREA, PHOTO) VALUES (
        'Ülker Bisküvi Sanayi A.Ş.',
        1944,
        'Istanbul/Türkiye',
        2,
        'İçecek, Çikolata, Bisküvi, Dondurma',
        'ülker.png'
        )"""
    cursor.execute(query)
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, CEO_ID, WORK_AREA, PHOTO) VALUES (
        'Koç Holding',
        1926,
        'Istanbul/Türkiye',
        2,
        'Beyaz eşya, Otomotiv, Bankacılık, Akaryakıt',
        'koc.png'
        )"""
    cursor.execute(query)


def add_sirket(cursor, request, sirket):
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, CEO_ID, WORK_AREA, PHOTO) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s,
        %s
        )"""
    cursor.execute(query, (sirket.name, sirket.date, sirket.location, sirket.ceo_id, sirket.work_area, sirket.photo))

def delete_sirketler(cursor, id):
        query="""DELETE FROM SIRKET WHERE ID = %s"""
        cursor.execute(query, id)


def update_sirketler(cursor, id, sirket):
            query="""
            UPDATE SIRKET
            SET NAME=INITCAP(%s),
            DATE=%s,
            LOCATION=INITCAP(%s),
            CEO_ID=%s,
            WORK_AREA=%s,
            PHOTO=%s
            WHERE ID=%s
            """
            cursor.execute(query,(sirket.name, sirket.date, sirket.location, sirket.ceo_id, sirket.work_area, sirket.photo, id))


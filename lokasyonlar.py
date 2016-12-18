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

class Lokasyon:
    def __init__(self, name, baskent, gps, yerel_dil, photo):
        self.name = name
        self.baskent = baskent
        self.gps = gps
        self.yerel_dil = yerel_dil
        self.photo = photo

def init_lokasyonlar_db(cursor):
    query = """DROP TABLE IF EXISTS LOKASYON"""
    cursor.execute(query)
    query = """CREATE TABLE LOKASYON (
        ID SERIAL PRIMARY KEY,
        NAME varchar(100) NOT NULL,
        BASKENT varchar(100) NOT NULL,
        GPS varchar(100) NOT NULL,
        YEREL_DIL INTEGER NOT NULL REFERENCES DIL(ID) ON DELETE CASCADE ON UPDATE CASCADE DEFAULT 1,
        PHOTO varchar(80)
        )"""
    cursor.execute(query)
    insert_lokasyon(cursor)

def insert_lokasyon(cursor):
    query = """INSERT INTO LOKASYON
        (NAME, BASKENT, GPS, YEREL_DIL, PHOTO) VALUES (
        'Türkiye',
        'Ankara',
        '39° 55dk 14.772sn N 32° 51dk 14.796sn E',
        1,
        'türkiye.svg'
        )"""
    cursor.execute(query)
    query = """INSERT INTO LOKASYON
        (NAME, BASKENT, GPS, YEREL_DIL, PHOTO) VALUES (
        'İngiltere',
        'Londra',
        '51° 30dk 26.463sn N 0° 7dk 39.93sn W',
        2,
        'ingiltere.svg'
        )"""
    cursor.execute(query)
    query = """INSERT INTO LOKASYON
        (NAME, BASKENT, GPS, YEREL_DIL, PHOTO) VALUES (
        'Fransa',
        'Paris',
        '48° 51dk 23.81sn N 2° 21dk 7.999sn E',
        3,
        'fransa.svg'
        )"""
    cursor.execute(query)
    query = """INSERT INTO LOKASYON
        (NAME, BASKENT, GPS, YEREL_DIL, PHOTO) VALUES (
        'İtalya',
        'Roma',
        '41° 54dk 10.021sn N 12° 29dk 46.916sn E',
        4,
        'italya.svg'
        )"""
    cursor.execute(query)
    query = """INSERT INTO LOKASYON
        (NAME, BASKENT, GPS, YEREL_DIL, PHOTO) VALUES (
        'Almanya',
        'Berlin',
        '52° 31dk 12.025sn N 13° 24dk 17.834sn E',
        4,
        'almanya.svg'
        )"""
    cursor.execute(query)


def add_lokasyon(cursor, request, lokasyon):
    query = """INSERT INTO LOKASYON
        (NAME, BASKENT, GPS, YEREL_DIL, PHOTO) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s
        )"""
    cursor.execute(query, (lokasyon.name, lokasyon.baskent, lokasyon.gps, lokasyon.yerel_dil, lokasyon.photo))

def delete_lokasyonlar(cursor, id):
    query="""DELETE FROM LOKASYON WHERE ID = %s"""
    cursor.execute(query, id)


def update_lokasyonlar(cursor, id, lokasyon):
    query="""
        UPDATE LOKASYON
        SET NAME=INITCAP(%s),
        BASKENT=INITCAP(%s),
        GPS=INITCAP(%s),
        YEREL_DIL=%s,
        PHOTO=%s
        WHERE ID=%s
        """
    cursor.execute(query,(lokasyon.name, lokasyon.baskent, lokasyon.gps, lokasyon.yerel_dil, lokasyon.photo, id))


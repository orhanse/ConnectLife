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

class Dil:
    def __init__(self, name, ulkesi, photo, bilenler):
        self.name = name
        self.ulkesi = ulkesi
        self.photo = photo
        self.bilenler = bilenler

def init_diller_db(cursor):
    query = """DROP TABLE IF EXISTS DIL"""
    cursor.execute(query)
    query = """CREATE TABLE DIL (
        ID SERIAL PRIMARY KEY,
        NAME varchar(100) UNIQUE NOT NULL,
        ULKESI INTEGER NOT NULL REFERENCES LOKASYON(ID) ON DELETE CASCADE ON UPDATE CASCADE,
        PHOTO varchar(80),
        BILENLER INTEGER NOT NULL REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE DEFAULT 1
        )"""
    cursor.execute(query)
    insert_dil(cursor)

def insert_dil(cursor):
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO, BILENLER) VALUES (
        'Türkçe',
        1,
        'türkçe.jpeg',
        3
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO, BILENLER) VALUES (
        'İngilizce',
        2,
        'ingilizce.jpg',
        4
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO, BILENLER) VALUES (
        'Fransızca',
        3,
        'fransızca.jpg',
        1
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO, BILENLER) VALUES (
        'İtalyanca',
        4,
        'italyanca.jpg',
        3
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO, BILENLER) VALUES (
        'Almanca',
        5,
        'almanca.png',
        5
        )"""
    cursor.execute(query)


def add_dil(cursor, request, dil):
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO, BILENLER) VALUES (
        %s,
        %s,
        %s,
        %s
        )"""
    cursor.execute(query, (dil.name, dil.ulkesi, dil.photo, dil.bilenler))

def delete_diller(cursor, id):
        query="""DELETE FROM DIL WHERE ID = %s"""
        cursor.execute(query, id)


def update_diller(cursor, id, dil):
            query="""
            UPDATE DIL
            SET NAME=INITCAP(%s),
            ULKESI=%s,
            PHOTO=INITCAP(%s),
            BILENLER=%s
            WHERE ID=%s
            """
            cursor.execute(query,(dil.name, dil.ulkesi, dil.photo, dil.bilenler, id))


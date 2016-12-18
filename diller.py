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
    def __init__(self, name, ulkesi, photo):
        self.name = name
        self.ulkesi = ulkesi
        self.photo = photo

def init_diller_db(cursor):
    query = """DROP TABLE IF EXISTS DIL"""
    cursor.execute(query)
    query = """CREATE TABLE DIL (
        ID SERIAL PRIMARY KEY,
        NAME varchar(100) NOT NULL,
        ULKESI varchar(100) NOT NULL,
        PHOTO varchar(80)
        )"""
    cursor.execute(query)
    insert_dil(cursor)

def insert_dil(cursor):
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO) VALUES (
        'Türkçe',
        'Türkiye',
        'türkçe.jpeg'
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO) VALUES (
        'İngilizce',
        'İngiltere',
        'ingilizce.jpg'
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO) VALUES (
        'Fransızca',
        'Fransa',
        'fransızca.jpg'
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO) VALUES (
        'İtalyanca',
        'İtalya',
        'italyanca.jpg'
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO) VALUES (
        'Almanca',
        'Almanya',
        'almanca.png'
        )"""
    cursor.execute(query)


def add_dil(cursor, request, dil):
    query = """INSERT INTO DIL
        (NAME, ULKESI, PHOTO) VALUES (
        %s,
        %s,
        %s
        )"""
    cursor.execute(query, (dil.name, dil.ulkesi, dil.photo))

def delete_diller(cursor, id):
        query="""DELETE FROM DIL WHERE ID = %s"""
        cursor.execute(query, id)


def update_diller(cursor, id, dil):
            query="""
            UPDATE DIL
            SET NAME=INITCAP(%s),
            ULKESI=INITCAP(%s),
            PHOTO=INITCAP(%s)
            WHERE ID=%s
            """
            cursor.execute(query,(dil.name, dil.ulkesi, dil.photo, id))


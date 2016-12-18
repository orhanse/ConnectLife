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
    def __init__(self, name, ulkesi):
        self.name = name
        self.ulkesi = ulkesi

def init_diller_db(cursor):
    query = """DROP TABLE IF EXISTS DIL"""
    cursor.execute(query)
    query = """CREATE TABLE DIL (
        ID SERIAL PRIMARY KEY,
        NAME varchar(100) NOT NULL,
        ULKESI varchar(100) NOT NULL
        )"""
    cursor.execute(query)
    insert_dil(cursor)

def insert_dil(cursor):
    query = """INSERT INTO DIL
        (NAME, ULKESI) VALUES (
        'Türkçe',
        'Türkiye'
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI) VALUES (
        'İngilizce',
        'İngiltere'
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI) VALUES (
        'Fransızca',
        'Fransa'
        )"""
    cursor.execute(query)
    query = """INSERT INTO DIL
        (NAME, ULKESI) VALUES (
        'İtalyanca',
        'İtalya'
        )"""
    cursor.execute(query)


def add_dil(cursor, request, dil):
    query = """INSERT INTO DIL
        (NAME, ULKESI) VALUES (
        %s,
        %s
        )"""
    cursor.execute(query, (dil.name, dil.ulkesi))

def delete_diller(cursor, id):
        query="""DELETE FROM DIL WHERE ID = %s"""
        cursor.execute(query, id)


def update_diller(cursor, id, dil):
            query="""
            UPDATE DIL
            SET NAME=INITCAP(%s),
            ULKESI=INITCAP(%s)
            WHERE ID=%s
            """
            cursor.execute(query,(dil.name, dil.ulkesi, id))


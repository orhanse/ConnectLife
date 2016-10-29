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
    def __init__(self, name, date, location, work_area, photo):
        self.name = name
        self.date = date
        self.location = location
        self.work_area = work_area
        self.photo = photo

def init_sirketler_db(cursor):
    query = """DROP TABLE IF EXISTS SIRKET"""
    cursor.execute(query)
    query = """CREATE TABLE SIRKET (
        NAME varchar(100) NOT NULL,
        DATE integer NOT NULL,
        LOCATION varchar(80) NOT NULL,
        WORK_AREA varchar(500),
        PHOTO varchar(80),
        PRIMARY KEY (NAME, DATE, LOCATION)
        )"""
    cursor.execute(query)

def insert_sirket(cursor):
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, WORK_AREA, PHOTO) VALUES (
        'SiMiT Lab',
        2010,
        'Istanbul/Türkiye',
        'Akıllı Etkileşim, Mobil İstihbarat, Multimedya Teknolojileri',
        'itulogo.png'
        )"""
    cursor.execute(query)
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, WORK_AREA, PHOTO) VALUES (
        'Siemens AG',
        1847,
        'Berlin/Almanya',
        'Endüstri, Enerji, Sağlık',
        'siemens1.png'
        )"""
    cursor.execute(query)


def add_sirket(cursor, request, variables):
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, WORK_AREA, PHOTO) VALUES (
        %s,
        %d,
        %s,
        %s,
        %s
        )"""
    cursor.execute(query, variables)

def get_sirket_page(app):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    init_sirketler_db(cursor)

    insert_sirket(cursor)

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM SIRKET"
        cursor.execute(query)

        return render_template('sirketler.html', sirket = cursor, current_time=now.ctime())
    elif "add" in request.form:
        sirket = Sirket(request.form['name'],
                     request.form['date'],
                     request.form['location'],
                     request.form['work_area'])

        add_sirket(cursor, request, sirket)

        connection.commit()
        return redirect(url_for('sirketler_sayfasi'))

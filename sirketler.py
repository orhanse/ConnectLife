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
        ID SERIAL,
        NAME varchar(100) NOT NULL,
        DATE varchar NOT NULL,
        LOCATION varchar(80) NOT NULL,
        WORK_AREA varchar(500),
        PHOTO varchar(80)
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


def add_sirket(cursor, request, sirket):
    query = """INSERT INTO SIRKET
        (NAME, DATE, LOCATION, WORK_AREA, PHOTO) VALUES (
        %s,
        %s,
        %s,
        %s,
        %s
        )"""
    cursor.execute(query, (sirket.name, sirket.date, sirket.location, sirket.work_area, sirket.photo))

def delete_sirketler(cursor, id):
        query="""DELETE FROM SIRKET WHERE ID = %s"""
        cursor.execute(query, id)


def update_sirketler(cursor, id, sirket):
            query="""
            UPDATE SIRKET
            SET NAME=INITCAP(%s),
            DATE=%s,
            LOCATION=INITCAP(%s),
            WORK_AREA=%s,
            PHOTO=%s
            WHERE ID=%s
            """
            cursor.execute(query,(sirket.name, sirket.date, sirket.location, sirket.work_area, sirket.photo, id))

def get_sirket_page(app):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()


    connection.commit()
    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM SIRKET"
        cursor.execute(query)

        return render_template('sirketler.html', sirket = cursor, current_time=now.ctime())
    elif "add" in request.form:
        sirket = Sirket(request.form['name'],
                     request.form['date'],
                     request.form['location'],
                     request.form['work_area'],
                     request.form['photo'])

        add_sirket(cursor, request, sirket)

        connection.commit()
        return redirect(url_for('sirketler_sayfasi'))
    elif "search" in request.form:
        aranan = request.form['aranan'];
        query = """SELECT ID,NAME, DATE, LOCATION, WORK_AREA, PHOTO FROM SIRKET WHERE NAME LIKE %s"""
        cursor.execute(query,[aranan])
        sirketler=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('sirket_ara.html', sirketler = sirketler, current_time=now.ctime(), sorgu = aranan)


def get_sirket_page_update(app, sirket_id,connection):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query = """SELECT * FROM SIRKET WHERE (ID = %s)"""
        cursor.execute(query,sirket_id)
        now = datetime.datetime.now()
        return render_template('sirket_guncelle.html', sirket = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            sirket1 = Sirket(request.form['name'],
                            request.form['date'],
                            request.form['location'],
                            request.form['work_area'],
                            request.form['photo'])
            update_sirketler(cursor, request.form['sirket_id'], sirket1)
            connection.commit()
            return redirect(url_for('sirketler_sayfasi'))
        elif "delete" in request.form:
            delete_sirketler(cursor, sirket_id)
            connection.commit()
            return redirect(url_for('sirketler_sayfasi'))







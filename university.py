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

class University:
    def __init__(self, name, foundation_date, location, small_info, photo):
        self.name = name
        self.foundation_date = foundation_date
        self.location = location
        self.small_info = small_info
        self.photo = photo

def init_universities_db(cursor):
    query = """CREATE TABLE UNIVERSITY (
        ID SERIAL,
        NAME VARCHAR(100) NOT NULL,
        FOUNDATION_DATE INTEGER NOT NULL,
        LOCATION VARCHAR(80) NOT NULL,
        SMALL_INFO VARCHAR(500),
        PHOTO VARCHAR(80),
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

def add_university(cursor, request, university):
    query = """INSERT INTO UNIVERSITY
        (NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO) VALUES (
        INITCAP(%s),
        %d,
        INITCAP(%s),
        INITCAP(%s),
        %s
        )"""
    cursor.execute(query, (university.name, university.foundation_date, university.location, university.small_info, university.photo))

def get_university_page(app):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT ID, NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO FROM UNIVERSITY"
        cursor.execute(query)
        university = cursor.fetchall()

        return render_template('universiteler.html', university = cursor, current_time=now.ctime())
    elif "add" in request.form:
        university = University(request.form['name'],
                     request.form['foundation_date'],
                     request.form['location'],
                     request.form['small_info'],
                     request.form['photo'])

        add_university(cursor, request, university)
        connection.commit()
        return redirect(url_for('universiteler_sayfasi'))

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
    def __init__(self, name, faundation_date, location, small_info):
        self.name = name
        self.faundation_date = faundation_date
        self.location = location
        self.small_info = small_info

def init_universities_db(cursor):
    query = """DROP TABLE IF EXISTS UNIVERSITY"""
    cursor.execute(query)
    query = """CREATE TABLE UNIVERSITY (
        NAME varchar(100) NOT NULL,
        FAUNDATION_DATE integer NOT NULL,
        LOCATION varchar(80) NOT NULL,
        SMALL_INFO varchar(500),
        PRIMARY KEY (NAME, FAUNDATION_DATE, LOCATION)
        )"""
    cursor.execute(query)

def add_university(cursor, request, variables):
    query = """INSERT INTO UNIVERSITY
        (NAME, FAUNDATION_DATE, LOCATION, SMALL_INFO) VALUES (
        %s,
        %d,
        %s,
        %s
        )"""
    cursor.execute(query, variables)

def get_university_page(app):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    init_universities_db(cursor)

    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT * FROM UNIVERSITY"
        cursor.execute(query)

        return render_template('universiteler.html', university = cursor, current_time=now.ctime())
    elif "add" in request.form:
        university = University(request.form['name'],
                     request.form['faundation_date'],
                     request.form['location'],
                     request.form['small_info'])

        add_university(cursor, request, university)

        connection.commit()
        return redirect(url_for('universiteler_sayfasi'))

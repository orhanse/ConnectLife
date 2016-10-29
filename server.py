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

from university import *
from sirketler import *
from gruplar import *
from kisiler import *

app = Flask(__name__)

def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)
    return dsn


#KISILER
@app.route('/kisiler/initdb')
def initialize_database_kisiler():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS KISILER CASCADE;
    ''')
    init_kisiler_db(cursor)
    connection.commit()
    return redirect(url_for('home_page'))


@app.route('/kisiler')
def kisiler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    query = "SELECT ID, ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK FROM KISILER"
    cursor.execute(query)
    gruplar = cursor.fetchall()
    now = datetime.datetime.now()
    return render_template('kisiler.html', kisiler = kisiler, current_time=now.ctime())


#GRUPLAR SAYFASI
@app.route('/gruplar/initdb')
def initialize_database_gruplar():
    connection = dbapi2.connect(app.config['dsn'])
    cursor =connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS GRUPLAR CASCADE;
    ''')
    init_gruplar_db(cursor)
    connection.commit()
    return redirect(url_for('home_page'))


@app.route('/gruplar')
def gruplar_sayfasi():
    connection = dbapi2.connect( app.config['dsn'])
    cursor = connection.cursor()
    query = "SELECT ID,BASLIK,ZAMAN,ACIKLAMA,ICERIK,RESIM FROM GRUPLAR"
    cursor.execute(query)
    gruplar=cursor.fetchall()
    now = datetime.datetime.now()
    return render_template('gruplar.html', gruplar = gruplar, current_time=now.ctime())




@app.route('/')
def home_page():
    now = datetime.datetime.now()
    return render_template('home.html', current_time=now.ctime())

@app.route('/initdb')
def initialize_database():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    query = """DROP TABLE IF EXISTS COUNTER"""
    cursor.execute(query)
    query = """CREATE TABLE COUNTER (N INTEGER)"""
    cursor.execute(query)
    query = """INSERT INTO COUNTER(N) VALUES(0)"""
    cursor.execute(query)

    connection.commit()
    return redirect(url_for('home_page'))

@app.route('/count')
def counter_page():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()

    query = "UPDATE COUNTER SET N = N + 1"
    cursor.execute(query)
    connection.commit()

    query = "SELECT N FROM COUNTER"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    return "This page was accesed %d times." % count


@app.route('/universiteler', methods = ['GET', 'POST'])
def universiteler_sayfasi():
    now = datetime.datetime.now()
    return get_university_page(app)

@app.route('/sirketler')
def sirketler_sayfasi():
    now = datetime.datetime.now()
    return get_sirket_page(app)

@app.route('/isilanlari')
def isilanlari_sayfasi():
    now = datetime.datetime.now()
    return render_template('isilanlari.html', current_time=now.ctime())




if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')
    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True
    VCAP_SERVICES = os.getenv('VCAP_SERVICES')
    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""
    app.run(host='0.0.0.0', port=port, debug=debug)

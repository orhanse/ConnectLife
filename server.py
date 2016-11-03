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
from isilanlari import *

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


@app.route('/kisiler',methods=['GET', 'POST'])
def kisiler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()
    if request.method == 'GET':
        query = "SELECT ID, ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK FROM KISILER"
        cursor.execute(query)
        kisiler = cursor.fetchall()
        return render_template('kisiler.html', kisiler = kisiler, current_time=now.ctime())
    elif "add" in request.form:
        kisi1 = Kisiler(request.form['isim'],
                        request.form['resim'],
                        request.form['mekan'],
                        request.form['yas'],
                        request.form['universite'],
                        request.form['work'])
        add_kisiler(cursor, request, kisi1)
        connection.commit()
        return redirect(url_for('kisiler_sayfasi'))
    elif "search" in request.form:
        aranankisi = request.form['aranankisi'];
        query = """SELECT ID, ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK FROM KISILER WHERE ISIM LIKE %s"""
        cursor.execute(query,[aranankisi])
        kisiler=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('kisi_ara.html', kisiler = kisiler, current_time=now.ctime(), sorgu = aranankisi)


@app.route('/kisiler/<kisi_id>', methods=['GET', 'POST'])
def kisiler_update_page(kisi_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        query = """SELECT * FROM KISILER WHERE (ID = %s)"""
        cursor.execute(query, kisi_id)
        now = datetime.datetime.now()
        return render_template('kisi_guncelle.html', kisi = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            kisi1 = Kisiler(request.form['isim'],
                            request.form['resim'],
                            request.form['mekan'],
                            request.form['yas'],
                            request.form['universite'],
                            request.form['work'])
            update_kisiler(cursor, request.form['kisi_id'], kisi1)
            connection.commit()
            return redirect(url_for('kisiler_sayfasi'))
        elif "delete" in request.form:
            delete_kisiler(cursor, kisi_id)
            connection.commit()
            return redirect(url_for('kisiler_sayfasi'))



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


@app.route('/gruplar',methods=['GET', 'POST'])
def gruplar_sayfasi():
    connection = dbapi2.connect( app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()
    if request.method == 'GET':
        query = "SELECT ID,BASLIK,ZAMAN,ACIKLAMA,ICERIK,RESIM FROM GRUPLAR"
        cursor.execute(query)
        gruplar=cursor.fetchall()
        return render_template('gruplar.html', gruplar = gruplar, current_time=now.ctime())
    elif "add" in request.form:
        grup1 = Gruplar(request.form['baslik'],
                            request.form['zaman'],
                            request.form['aciklama'],
                            request.form['icerik'],
                            request.form['resim'])
        add_gruplar(cursor, request, grup1)
        connection.commit()
        return redirect(url_for('gruplar_sayfasi'))
    elif "search" in request.form:
        aranan = request.form['aranan'];
        query = """SELECT ID,BASLIK,ZAMAN,ACIKLAMA,ICERIK,RESIM FROM GRUPLAR WHERE BASLIK LIKE %s"""
        cursor.execute(query,[aranan])
        gruplar=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('grup_ara.html', gruplar = gruplar, current_time=now.ctime(), sorgu = aranan)


#Gruplari Guncelle (UPDATE) ve sil (DELETE)
@app.route('/gruplar/<grup_id>', methods=['GET', 'POST'])
def gruplar_update_page(grup_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        query = """SELECT * FROM GRUPLAR WHERE (ID = %s)"""
        cursor.execute(query,grup_id)
        now = datetime.datetime.now()
        return render_template('grup_guncelle.html', grup = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            grup1 = Gruplar(request.form['baslik'],
                            request.form['zaman'],
                            request.form['aciklama'],
                            request.form['icerik'],
                            request.form['resim'])
            update_gruplar(cursor, request.form['grup_id'], grup1)
            connection.commit()
            return redirect(url_for('gruplar_sayfasi'))
        elif "delete" in request.form:
            delete_gruplar(cursor, grup_id)
            connection.commit()
            return redirect(url_for('gruplar_sayfasi'))


#ISILANLARI
@app.route('/isilanlari/initdb')
def initialize_database_isilanlari():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS ISILANLARI CASCADE;
    ''')
    init_isilanlari_db(cursor)
    connection.commit()
    return redirect(url_for('home_page'))


@app.route('/isilanlari', methods=['GET', 'POST'])
def isilanlari_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()
    if request.method == 'GET':
        query = "SELECT ID, SIRKET, POZISYON, LOKASYON, BASVURU, TARIH FROM ISILANLARI"
        cursor.execute(query)
        isilanlari=cursor.fetchall()
        return render_template('isilanlari.html', isilanlari = isilanlari, current_time=now.ctime())
    elif "add" in request.form:
        ilan1 = Isilanlari(request.form['sirket'],
                            request.form['pozisyon'],
                            request.form['lokasyon'],
                            request.form['basvuru'],
                            request.form['tarih'])
        add_isilanlari(cursor, request, ilan1)
        connection.commit()
        return redirect(url_for('isilanlari_sayfasi'))
    elif "search" in request.form:
        aranan = request.form['aranan'];
        query = """SELECT ID, SIRKET, POZISYON, LOKASYON, BASVURU, TARIH FROM ISILANLARI WHERE SIRKET LIKE %s"""
        cursor.execute(query,[aranan])
        isilanlari=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('ilan_ara.html', isilanlari = isilanlari, current_time=now.ctime(), sorgu = aranan)

@app.route('/isilanlari/<ilan_id>', methods=['GET', 'POST'])
def isilanlari_update_page(ilan_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        query = """SELECT * FROM ISILANLARI WHERE (ID = %s)"""
        cursor.execute(query,ilan_id)
        now = datetime.datetime.now()
        return render_template('ilan_guncelle.html', ilan = cursor, current_time=now.ctime())
    elif request.method == 'POST':
        if "update" in request.form:
            ilan1 = Isilanlari(request.form['sirket'],
                            request.form['pozisyon'],
                            request.form['lokasyon'],
                            request.form['basvuru'],
                            request.form['tarih'])
            update_isilanlari(cursor, request.form['ilan_id'], ilan1)
            connection.commit()
            return redirect(url_for('isilanlari_sayfasi'))
        elif "delete" in request.form:
            delete_isilanlari(cursor, ilan_id)
            connection.commit()
            return redirect(url_for('isilanlari_sayfasi'))


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

    init_universities_db(cursor)
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
    return "This page was accessed %d times." % count


@app.route('/universiteler', methods = ['GET', 'POST'])
def universiteler_sayfasi():
    now = datetime.datetime.now()
    return get_university_page(app)

@app.route('/sirketler')
def sirketler_sayfasi():
    now = datetime.datetime.now()
    return get_sirket_page(app)



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

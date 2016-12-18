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
from meslekler import *
from mailler import *
from makaleler import *
from oneriler import *

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
    return redirect(url_for('kisiler_sayfasi'))


@app.route('/kisiler',methods=['GET', 'POST'])
def kisiler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()

    if request.method == 'GET':
        query2 = "SELECT ID, NAME FROM UNIVERSITY"
        cursor.execute(query2)
        university = cursor.fetchall()
        query = """SELECT K.ID, K.ISIM, K.RESIM, K.MEKAN, K.YAS, U.NAME, S.NAME
                    FROM KISILER AS K, UNIVERSITY AS U, SIRKET AS S
                    WHERE(
                        (K.WORK = S.ID) AND (K.UNIVERSITE = U.ID)
                    ) """
        cursor.execute(query)
        kisi2 = cursor.fetchall()
        cursor.execute("SELECT ID, NAME FROM SIRKET")
        sirket = cursor.fetchall()
        return render_template('kisiler.html', kisiler = kisi2, universite = university, work = sirket)


    elif "add" in request.form:
        kisi1 = Kisiler(request.form['isim'],
                        request.form['resim'],
                        request.form['mekan'],
                        request.form['yas'],
                        request.form['university_name'],
                        request.form['work_name'])
        add_kisiler(cursor, request, kisi1)
        connection.commit()
        return redirect(url_for('kisiler_sayfasi'))
    elif "search" in request.form:
        aranankisi = request.form['aranankisi'];
        query = """SELECT K.ID, K.ISIM, K.RESIM, K.MEKAN, K.YAS, U.NAME, S.NAME
                    FROM KISILER AS K, UNIVERSITY AS U, SIRKET AS S
                    WHERE(
                        (K.WORK = S.ID) AND (K.UNIVERSITE = U.ID)
                    ) AND (K.ISIM LIKE %s)"""
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
        cursor.execute("SELECT ID, NAME FROM UNIVERSITY")
        universiteler = cursor.fetchall()
        cursor.execute("SELECT ID, NAME FROM SIRKET")
        sirket = cursor.fetchall()
        query = """SELECT * FROM KISILER WHERE (ID = %s)"""
        cursor.execute(query, kisi_id)
        now = datetime.datetime.now()
        return render_template('kisi_guncelle.html', kisi = cursor, current_time=now.ctime(), universiteler= universiteler, sirketler=sirket)
    elif request.method == 'POST':
        if "update" in request.form:
            kisi1 = Kisiler(request.form['isim'],
                            request.form['resim'],
                            request.form['mekan'],
                            request.form['yas'],
                            request.form['university_name'],
                            request.form['work_name'])
            update_kisiler(cursor, request.form['kisi_id'], kisi1)
            connection.commit()
            return redirect(url_for('kisiler_sayfasi'))
        elif "delete" in request.form:
            delete_kisiler(cursor, kisi_id)
            connection.commit()
            return redirect(url_for('kisiler_sayfasi'))



#MESLEKLER
@app.route('/meslekler/initdb')
def initialize_database_meslekler():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS MESLEKLER CASCADE;
    ''')
    init_meslekler_db(cursor)
    connection.commit()
    return redirect(url_for('meslekler_sayfasi'))


@app.route('/meslekler',methods=['GET', 'POST'])
def meslekler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()

    if request.method == 'GET':
        query = """SELECT ID, ISIM, TANIM FROM MESLEKLER"""
        cursor.execute(query)
        meslek2 = cursor.fetchall()
        return render_template('meslekler.html', meslekler = meslek2)


    elif "add" in request.form:
        meslek1 = Meslekler(request.form['isim'],
                            request.form['tanim'])
        add_meslekler(cursor, request, meslek1)
        connection.commit()
        return redirect(url_for('meslekler_sayfasi'))

    elif "search" in request.form:
        arananmeslek = request.form['arananmeslek'];
        query = """SELECT ID, ISIM, TANIM FROM MESLEKLER WHERE ISIM LIKE %s"""
        cursor.execute(query,[arananmeslek])
        meslekler=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('meslek_ara.html', meslekler = meslekler, current_time=now.ctime(), sorgu = arananmeslek)


@app.route('/meslekler/<meslek_id>', methods=['GET', 'POST'])
def meslekler_update_page(meslek_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        query = """SELECT * FROM MESLEKLER WHERE (ID = %s)"""
        cursor.execute(query, meslek_id)
        now = datetime.datetime.now()
        return render_template('meslek_guncelle.html', meslek = cursor, current_time=now.ctime() )
    elif request.method == 'POST':
        if "update" in request.form:
            meslek1 = Meslekler(request.form['isim'],
                                request.form['tanim'])
            update_meslekler(cursor, request.form['meslek_id'], meslek1)
            connection.commit()
            return redirect(url_for('meslekler_sayfasi'))
        elif "delete" in request.form:
            delete_meslekler(cursor, meslek_id)
            connection.commit()
            return redirect(url_for('meslekler_sayfasi'))



#MAILLER SAYFASI
@app.route('/mailler/initdb')
def initialize_database_mailler():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS MAILLER CASCADE;
    ''')
    init_mailler_db(cursor)
    connection.commit()
    return redirect(url_for('mailler_sayfasi'))


@app.route('/mailler',methods=['GET', 'POST'])
def mailler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()

    if request.method == 'GET':
        query2 = """SELECT ID, ISIM FROM KISILER"""
        cursor.execute(query2)
        kisi = cursor.fetchall()
        query = """SELECT M.ID, K.ISIM, M.MAIL, M.SIFRE
                    FROM MAILLER AS M, KISILER AS K
                    WHERE(
                        (M.ISIM = K.ID)
                    )"""
        cursor.execute(query)
        mail2 = cursor.fetchall()
        return render_template('mailler.html', mailler = mail2, isim = kisi)



    elif "add" in request.form:
        mail1 = Mailler(request.form['kisi_adi'],
                            request.form['mail'],
                            request.form['sifre'])
        add_mailler(cursor, request, mail1)
        connection.commit()
        return redirect(url_for('mailler_sayfasi'))

    elif "search" in request.form:
        arananmail = request.form['arananmail'];
        query = """SELECT M.ID, K.ISIM, M.MAIL, M.SIFRE
                    FROM MAILLER AS M, KISILER AS K
                    WHERE(
                        (M.ISIM = K.ID)
                    ) AND (M.MAIL LIKE %s)"""
        cursor.execute(query,[arananmail])
        mailler=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('mail_ara.html', mailler = mailler, current_time=now.ctime(), sorgu = arananmail)


@app.route('/mailler/<mail_id>', methods=['GET', 'POST'])
def mailler_update_page(mail_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        cursor.execute("SELECT ID, ISIM FROM KISILER")
        kisiler = cursor.fetchall()
        query = """SELECT * FROM MAILLER WHERE (ID = %s)"""
        cursor.execute(query, mail_id)
        now = datetime.datetime.now()
        return render_template('mail_guncelle.html', mail = cursor, current_time=now.ctime(), isimler = kisiler )
    elif request.method == 'POST':
        if "update" in request.form:
            mail1 = Mailler(request.form['kisi_adi'],
                                request.form['mail'],
                                request.form['sifre'])
            update_mailler(cursor, request.form['mail_id'], mail1)
            connection.commit()
            return redirect(url_for('mailler_sayfasi'))
        elif "delete" in request.form:
            delete_mailler(cursor, mail_id)
            connection.commit()
            return redirect(url_for('mailler_sayfasi'))


#GRUPLAR SAYFASI
@app.route('/gruplar/initdb')
def initialize_database_gruplar():
    connection = dbapi2.connect(app.config['dsn'])
    cursor =connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS GRUPLAR CASCADE;
    ''')
    init_gruplar_db(cursor)
    init_tag_hastag_db(cursor)
    connection.commit()
    return redirect(url_for('home_page'))


@app.route('/gruplar',methods=['GET', 'POST'])
def gruplar_sayfasi():
    connection = dbapi2.connect( app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()
    if request.method == 'GET':
        query = "SELECT G.ID,G.BASLIK,G.ZAMAN,G.ACIKLAMA,G.ICERIK,G.RESIM,K.ISIM FROM KISILER AS K RIGHT JOIN GRUPLAR AS G ON G.KISILER_ID = K.ID"
        cursor.execute(query)
        gruplar=cursor.fetchall()
        query = "SELECT ID,ISIM FROM KISILER"
        cursor.execute(query)
        kisiler =cursor.fetchall()
        return render_template('gruplar.html', gruplar = gruplar, current_time=now.ctime(),kisiler=kisiler)
    elif "add" in request.form:
        grup1 = Gruplar(request.form['baslik'],
                            request.form['zaman'],
                            request.form['aciklama'],
                            request.form['icerik'],
                            request.form['resim'],
                            request.form['kisiler_isim'])
        add_gruplar(cursor, request, grup1)
        connection.commit()
        return redirect(url_for('gruplar_sayfasi'))
    elif "search" in request.form:
        aranan = request.form['aranan'];
        query = """SELECT ID,BASLIK,ZAMAN,ACIKLAMA,ICERIK,RESIM,KISILER_ID FROM GRUPLAR WHERE BASLIK LIKE %s"""
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
        grup = cursor.fetchall()
        now = datetime.datetime.now()
        query = "SELECT ID,ISIM FROM KISILER"
        cursor.execute(query)
        kisiler =cursor.fetchall()
        return render_template('grup_guncelle.html', grup = grup, current_time=now.ctime(),kisiler=kisiler)
    elif request.method == 'POST':
        if "update" in request.form:
            grup1 = Gruplar(request.form['baslik'],
                            request.form['zaman'],
                            request.form['aciklama'],
                            request.form['icerik'],
                            request.form['resim'],
                            request.form['kisiler_isim'])
            update_gruplar(cursor, request.form['grup_id'], grup1)
            connection.commit()
            return redirect(url_for('gruplar_sayfasi'))
        elif "delete" in request.form:
            delete_gruplar(cursor, grup_id)
            connection.commit()
            return redirect(url_for('gruplar_sayfasi'))

#ÖNERİLER
@app.route('/oneriler/initdb')
def initialize_database_oneriler():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS ONERILER CASCADE;
    ''')
    init_oneriler_db(cursor)
    connection.commit()
    return redirect(url_for('oneriler_sayfasi'))


@app.route('/oneriler', methods=['GET', 'POST'])
def oneriler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()
    if request.method == 'GET':
        query2 = "SELECT ID, ISIM FROM KISILER"
        cursor.execute(query2)
        kisiler = cursor.fetchall()
        query = """SELECT O.ID, O.RESIM, K.ISIM, I.POZISYON, O.BAGLANTI
                    FROM ONERILER AS O, ISILANLARI AS I, KISILER AS K
                    WHERE(
                        (O.KNAME = K.ID) AND (O.KPOZISYON = I.ID)
                     ) """
        cursor.execute(query)
        oneriler=cursor.fetchall()
        cursor.execute("SELECT ID, POZISYON FROM ISILANLARI")
        isilanlari=cursor.fetchall()
        return render_template('oneriler.html', oneriler = oneriler, current_time=now.ctime(), kname = kisiler, pozisyon=isilanlari)
    elif "add" in request.form:
        oneri1 = Oneriler( request.form['resim'],
                            request.form['kisiler_isim'],
                            request.form['kpozisyon'],
                            request.form['baglanti'])
        add_oneriler(cursor, request, oneri1)
        connection.commit()
        return redirect(url_for('oneriler_sayfasi'))
    elif "search" in request.form:
        aranan = request.form['aranan'];
        query = """SELECT O.ID, O.RESIM, K.ISIM, I.POZISYON, O.BAGLANTI
                    FROM ONERILER AS O, ISILANLARI AS I, KISILER AS K
                    WHERE(
                        (O.KNAME = K.ID) AND (O.KPOZISYON = I.ID)
                    )AND (K.ISIM LIKE %s)"""
        cursor.execute(query,[aranan])
        oneriler=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('oneri_ara.html', oneriler = oneriler, current_time=now.ctime(), sorgu = aranan)

@app.route('/oneriler/<oneri_id>', methods=['GET', 'POST'])
def oneriler_update_page(oneri_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        query = """SELECT * FROM ONERILER WHERE (ID = %s)"""
        cursor.execute(query,oneri_id)
        oneri=cursor.fetchall()
        now = datetime.datetime.now()
        cursor.execute("SELECT ID, ISIM FROM KISILER")
        kisiler=cursor.fetchall()
        cursor.execute("SELECT ID, POZISYON FROM ISILANLARI")
        isilanlari=cursor.fetchall()
        return render_template('oneri_guncelle.html', oneri = oneri,  current_time=now.ctime(), kisiler= kisiler,isilanlari= isilanlari)
    elif request.method == 'POST':
        if "update" in request.form:
            oneri1 = Oneriler( request.form['resim'],
                            request.form['kisiler_isim'],
                            request.form['kpozisyon'],
                            request.form['baglanti'])
            update_oneriler(cursor, request.form['oneri_id'], oneri1)
            connection.commit()
            return redirect(url_for('oneriler_sayfasi'))
        elif "delete" in request.form:
            delete_oneriler(cursor, oneri_id)
            connection.commit()
            return redirect(url_for('oneriler_sayfasi'))


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
        query = """SELECT I.ID, S.NAME, I.POZISYON, I.LOKASYON, I.BASVURU, I.TARIH
                    FROM ISILANLARI AS I, SIRKET AS S
                    WHERE(
                        (I.SIRKETNAME = S.ID)
                    ) """
        cursor.execute(query)
        isilanlari=cursor.fetchall()
        cursor.execute("SELECT ID, NAME FROM SIRKET")
        sirket=cursor.fetchall()
        return render_template('isilanlari.html', isilanlari = isilanlari, current_time=now.ctime(), sirketname = sirket)
    elif "add" in request.form:
        ilan1 = Isilanlari(request.form['sirket_name'],
                            request.form['pozisyon'],
                            request.form['lokasyon'],
                            request.form['basvuru'],
                            request.form['tarih'])
        add_isilanlari(cursor, request, ilan1)
        connection.commit()
        return redirect(url_for('isilanlari_sayfasi'))
    elif "search" in request.form:
        aranan = request.form['aranan'];

        query = """SELECT I.ID, S.NAME, I.POZISYON, I.LOKASYON, I.BASVURU, I.TARIH
                    FROM ISILANLARI AS I, SIRKET AS S
                    WHERE((
                        (I.SIRKETNAME = S.ID)
                    ) AND (S.NAME LIKE %s))"""
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
        ilan=cursor.fetchall()
        now = datetime.datetime.now()
        cursor.execute("SELECT ID, NAME FROM SIRKET")
        sirket=cursor.fetchall()
        return render_template('ilan_guncelle.html', ilan = ilan,  current_time=now.ctime(), sirketler = sirket)
    elif request.method == 'POST':
        if "update" in request.form:
            ilan1 = Isilanlari(request.form['sirket_name'],
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

#MAKALELER
@app.route('/makaleler/initdb')
def initialize_database_makaleler():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS MAKALELER CASCADE;
    ''')
    init_makaleler_db(cursor)
    connection.commit()
    return redirect(url_for('home_page'))


@app.route('/makaleler', methods=['GET', 'POST'])
def makaleler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()

    if request.method == 'GET':
        query = """SELECT M.ID, M.KONU, M.BASLIK, M.YAZAR, M.TARIH, U.NAME
                    FROM MAKALELER AS M, UNIVERSITY AS U
                    WHERE(
                        (M.UNINAME= U.ID)
                    ) """
        cursor.execute(query)
        makaleler=cursor.fetchall()
        cursor.execute("SELECT ID, NAME FROM UNIVERSITY")
        university=cursor.fetchall()
        return render_template('makaleler.html', makaleler = makaleler, current_time=now.ctime(), uniname = university)
    elif "add" in request.form:

        makale1 = Makaleler(request.form['konu'],
                            request.form['baslik'],
                            request.form['yazar'],
                            request.form['tarih'],
                            request.form['university_name'])
        add_makaleler(cursor, request, makale1)
        connection.commit()
        return redirect(url_for('makaleler_sayfasi'))
    elif "search" in request.form:
        aranan = request.form['aranan'];

        query = """SELECT M.ID, M.KONU,M.BASLIK, M.YAZAR, M.TARIH, U.NAME
                    FROM MAKALELER AS M, UNIVERSITY AS U
                    WHERE((
                        (M.UNINAME = U.ID)
                    ) AND (M.KONU LIKE %s))"""
        cursor.execute(query,[aranan])
        makaleler=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('makale_ara.html', makaleler = makaleler, current_time=now.ctime(), sorgu = aranan)

@app.route('/makaleler/<makale_id>', methods=['GET', 'POST'])
def makaleler_update_page(makale_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        query = """SELECT * FROM MAKALELER WHERE (ID = %s)"""
        cursor.execute(query,makale_id)
        makale=cursor.fetchall()
        now = datetime.datetime.now()
        cursor.execute("SELECT ID, NAME FROM UNIVERSITY")
        universiteler=cursor.fetchall()
        return render_template('makale_guncelle.html', makale = makale,  current_time=now.ctime(), universiteler = universiteler)
    elif request.method == 'POST':
        if "update" in request.form:
            makale1 = Makaleler(request.form['konu'],
                            request.form['baslik'],
                            request.form['yazar'],
                            request.form['tarih'],
                            request.form['university_name'])
            update_makaleler(cursor, request.form['makale_id'], makale1)
            connection.commit()
            return redirect(url_for('makaleler_sayfasi'))
        elif "delete" in request.form:
            delete_makaleler(cursor, makale_id)
            connection.commit()
            return redirect(url_for('makaleler_sayfasi'))


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
    return "This page was accessed %d times." % count

@app.route('/universiteler/initdb')
def initialize_database_university():
    connection = dbapi2.connect(app.config['dsn'])
    cursor =connection.cursor()
    cursor.execute('''
                    DROP TABLE IF EXISTS UNIVERSITY CASCADE;
                    ''')

    init_universities_db(cursor)
    connection.commit()
    return redirect(url_for('home_page'))

@app.route('/universiteler', methods = ['GET', 'POST'])
def universiteler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    now = datetime.datetime.now()

    if request.method == 'GET':
        query = "SELECT U.ID, U.NAME, U.FOUNDATION_DATE, U.LOCATION, U.SMALL_INFO, U.PHOTO, K.ISIM FROM KISILER AS K RIGHT JOIN UNIVERSITY AS U ON U.RECTOR_ID = K.ID"
        cursor.execute(query)
        university = cursor.fetchall()
        query = "SELECT ID, ISIM FROM KISILER"
        cursor.execute(query)
        rector = cursor.fetchall()
        return render_template('universiteler.html', university = university, current_time=now.ctime(), rector = rector)
    elif "add" in request.form:
        university1 = University(request.form['name'],
                    request.form['foundation_date'],
                    request.form['location'],
                    request.form['small_info'],
                    request.form['photo'],
                    request.form['rector_name'])
        add_university(cursor, request, university1)
        connection.commit()
        return redirect(url_for('universiteler_sayfasi'))
    elif "search" in request.form:
        searched = request.form['searched'];
        query = """SELECT ID, NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO, RECTOR_ID FROM UNIVERSITY WHERE NAME LIKE %s"""
        cursor.execute(query,[searched])
        university=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('universiteler_ara.html', university = university, current_time=now.ctime(), sorgu = searched)

@app.route('/universiteler/<university_id>', methods=['GET', 'POST'])
def university_update_page(university_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        cursor.close()
        cursor = connection.cursor()
        query = """SELECT * FROM UNIVERSITY WHERE (ID = %s)"""
        cursor.execute(query,university_id)
        university = cursor.fetchall()
        now = datetime.datetime.now()
        query2 = "SELECT ID, ISIM FROM KISILER"
        cursor.execute(query2)
        rector = cursor.fetchall()
        return render_template('universiteler_guncelle.html', university = university, current_time=now.ctime(), rector = rector)
    elif request.method == 'POST':
        if "update" in request.form:
            university1 = University(request.form['name'],
                            request.form['foundation_date'],
                            request.form['location'],
                            request.form['small_info'],
                            request.form['photo'],
                            request.form['rector_name'])
            update_university(cursor, request.form['university_id'], university1)
            connection.commit()
            return redirect(url_for('universiteler_sayfasi'))
        elif "delete" in request.form:
            delete_university(cursor, university_id)
            connection.commit()
            return redirect(url_for('universiteler_sayfasi'))

@app.route('/sirketler/initdb')
def initialize_database_sirket():
    connection = dbapi2.connect(app.config['dsn'])
    cursor =connection.cursor()
    cursor.execute('''
    DROP TABLE IF EXISTS SIRKET CASCADE;
    ''')

    init_sirketler_db(cursor)
    connection.commit()
    return redirect(url_for('home_page'))

@app.route('/sirketler', methods = ['GET', 'POST'])
def sirketler_sayfasi():
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        now = datetime.datetime.now()
        query = "SELECT S.ID,S.NAME,S.DATE,S.LOCATION,K.ISIM, S.WORK_AREA,S.PHOTO FROM KISILER AS K RIGHT JOIN SIRKET AS S ON S.CEO_ID = K.ID"
        cursor.execute(query)
        sirket=cursor.fetchall()
        query = "SELECT ID,ISIM FROM KISILER"
        cursor.execute(query)
        kisiler =cursor.fetchall()
        return render_template('sirketler.html', sirket = sirket, current_time=now.ctime(),kisiler=kisiler)
    elif "add" in request.form:
        sirket = Sirket(request.form['name'],
                     request.form['date'],
                     request.form['location'],
                     request.form['kisiler_isim'],
                     request.form['work_area'],
                     request.form['photo'])

        add_sirket(cursor, request, sirket)

        connection.commit()
        return redirect(url_for('sirketler_sayfasi'))
    elif "search" in request.form:
        aranan = request.form['aranan'];
        query = """SELECT ID,NAME, DATE, LOCATION, CEO_ID, WORK_AREA, PHOTO FROM SIRKET WHERE NAME LIKE %s"""
        cursor.execute(query,[aranan])
        sirket=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('sirket_ara.html', sirket = sirket, current_time=now.ctime(), sorgu = aranan)


@app.route('/sirketler/<sirket_id>', methods=['GET', 'POST'])
def sirketler_update_page(sirket_id):
    connection = dbapi2.connect(app.config['dsn'])
    cursor = connection.cursor()
    if request.method == 'GET':
        query = """SELECT * FROM SIRKET WHERE (ID = %s)"""
        cursor.execute(query,sirket_id)
        sirket = cursor.fetchall()
        now = datetime.datetime.now()
        query = "SELECT ID,ISIM FROM KISILER"
        cursor.execute(query)
        kisiler =cursor.fetchall()
        return render_template('sirket_guncelle.html', sirket = sirket, current_time=now.ctime(), kisiler = kisiler)
    elif request.method == 'POST':
        if "update" in request.form:
            sirket1 = Sirket(request.form['name'],
                            request.form['date'],
                            request.form['location'],
                            request.form['kisiler_isim'],
                            request.form['work_area'],
                            request.form['photo'])
            update_sirketler(cursor, request.form['sirket_id'], sirket1)
            connection.commit()
            return redirect(url_for('sirketler_sayfasi'))
        elif "delete" in request.form:
            delete_sirketler(cursor, sirket_id)
            connection.commit()
            return redirect(url_for('sirketler_sayfasi'))



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

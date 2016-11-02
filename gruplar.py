import datetime
import os
import json
import re
import psycopg2 as dbapi2

#Gruplar classi olusturuluyor ve yapi tanimlaniyor.
class Gruplar:
    def __init__(self, baslik, zaman, aciklama, icerik, resim):
        self.baslik = baslik
        self.zaman = zaman
        self.aciklama = aciklama
        self.icerik = icerik
        self.resim = resim

def init_gruplar_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS GRUPLAR (
    ID SERIAL,
    BASLIK VARCHAR(80) NOT NULL,
    ZAMAN DATE NOT NULL,
    ACIKLAMA VARCHAR(500) NOT NULL,
    ICERIK VARCHAR(500) NOT NULL,
    RESIM VARCHAR(80),
    PRIMARY KEY(ID)
    )"""
    cursor.execute(query)
    fill_gruplar_db(cursor)

def fill_gruplar_db(cursor):
    query="""INSERT INTO GRUPLAR
        (BASLIK, ZAMAN, ACIKLAMA, ICERIK, RESIM) VALUES (
        'Yazılım & Teknoloji ',
        to_date('02.03.2015', 'DD-MM-YYYY'),
        'Yazılım mühendisleri ve teknolojiyi takip edenler için oluşturulmuş bir topluluk. Sen de bize katıl!',
        'Icerik Eklenecektir',
        'software.jpg');
        INSERT INTO GRUPLAR
        (BASLIK, ZAMAN, ACIKLAMA, ICERIK, RESIM) VALUES (
        'Finans Klubü',
        to_date('13.09.2019', 'DD-MM-YYYY'),
        'Finans sektöründe çalışanlar, firma sahipleri, ve girişimciler için eşsiz bir kaynak. Bu grup ile finans konusunda yeni gelişmeleri kaçırmadan güncel piyasaları takip ederek doğru kararlar alabileceksiniz. Hemen gruba katılın ve tartışmaya başlayın!',
        'Icerik Eklenecektir',
        'finance.jpg');
        INSERT INTO GRUPLAR
        (BASLIK, ZAMAN, ACIKLAMA, ICERIK, RESIM) VALUES (
        'Digital Marketing',
        to_date('13.09.2019', 'DD-MM-YYYY'),
        'We know marketing! Discussions on current trends, close scope on money exchange and tips and tricks for new entrepreneur. Join us and enjoy great discussions!',
        'Icerik Eklenecektir',
        'marketing.jpeg');
        INSERT INTO GRUPLAR
        (BASLIK, ZAMAN, ACIKLAMA, ICERIK, RESIM) VALUES (
        'Mühendisler Topluluğu',
        to_date('13.09.2019', 'DD-MM-YYYY'),
        'Mühendisler ve mühendis adaylarını buluşturan bu toplulukta pratik bilgiler, iş ilanları, sektöre ilişkin başlıklar ve çok daha fazlasını bulacaksınız.',
        'Icerik Eklenecektir',
        'muhendis.jpg');
        """
    cursor.execute(query)


def add_gruplar(cursor, request, grup1):
        query = """INSERT INTO GRUPLAR
        (BASLIK, ZAMAN, ACIKLAMA, ICERIK, RESIM) VALUES (
        INITCAP(%s),
        to_date(%s, 'DD-MM-YYYY'),
        INITCAP(%s),
        INITCAP(%s),
        %s
        )"""
        cursor.execute(query, (grup1.baslik, grup1.zaman, grup1.aciklama,
                               grup1.icerik, grup1.resim))

def delete_gruplar(cursor, id):
        query="""DELETE FROM GRUPLAR WHERE ID = %s"""
        cursor.execute(query, id)


def update_gruplar(cursor, id, grup1):
            query="""
            UPDATE GRUPLAR
            SET BASLIK=INITCAP(%s),
            ZAMAN=to_date(%s, 'DD-MM-YYYY'),
            ACIKLAMA=INITCAP(%s),
            ICERIK=%s,
            RESIM=%s
            WHERE ID=%s
            """
            cursor.execute(query,(grup1.baslik, grup1.zaman, grup1.aciklama,
                                  grup1.icerik, grup1.resim, id))
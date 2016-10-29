import datetime
import os
import json
import re
import psycopg2 as dbapi2

#Gruplar classi olusturuluyor ve yapi tanimlaniyor.
class Championships:
    def __init__(self, baslik, aciklama, icerik, resim, zaman):
        self.baslik = baslik
        self.aciklama = aciklama
        self.icerik = icerik
        self.resim = resim
        self.zaman = zaman

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
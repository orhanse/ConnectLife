import datetime
import os
import json
import re
import psycopg2 as dbapi2


class Meslekler:
    def __init__(self, isim, tanim):
        self.isim = isim
        self.tanim = tanim



def init_meslekler_db(cursor):
    query = """CREATE TABLE IF NOT EXISTS MESLEKLER (
    ID SERIAL PRIMARY KEY,
    ISIM VARCHAR(30) NOT NULL,
    TANIM VARCHAR(500)
    )"""

    cursor.execute(query)
    fill_meslekler_db(cursor)


def fill_meslekler_db(cursor):
    query = """ INSERT INTO MESLEKLER (ISIM, TANIM)
                    VALUES('Kurucu', ' Bir kurumun, bir işin kurulmasını sağlayan, müessis.');
                INSERT INTO MESLEKLER (ISIM, TANIM)
                    VALUES('Muhendis', 'İnsanların her türlü ihtiyacını karşılamaya dayalı yol, köprü, bina gibi bayındırlık; tarım, beslenme gibi gıda; fizik, kimya, biyoloji, elektrik, elektronik gibi fen; uçak, otomobil, motor, iş makineleri gibi teknik ve sosyal alanlarda uzmanlaşmış, belli bir eğitim görmüş kimse');
                INSERT INTO MESLEKLER (ISIM, TANIM)
                    VALUES('Proje Yoneticisi', 'Proje yöneticileri, mühendisliğin herhangi bir alanında, planlama, temin etme ve projenin yerine getirilmesinde sorumluluk sahibidir.');
                INSERT INTO MESLEKLER (ISIM, TANIM)
                    VALUES('Teknisyen', 'Bir işin bilim yönünden çok, uygulama ve pratik yönü ile uğraşan kimse, teknik adam, tekniker.');
                INSERT INTO MESLEKLER (ISIM, TANIM)
                    VALUES('Ogretmen', 'Mesleği bilgi öğretmek olan kimse, hoca, muallim, muallime.');
                INSERT INTO MESLEKLER (ISIM, TANIM)
                    VALUES('Avukat', 'Hak ve yasa işlerinde isteyenlere yol göstermeyi, mahkemelerde, devlet dairelerinde başkalarının hakkını aramayı, korumayı meslek edinen ve bunun için yasanın gerektirdiği şartları taşıyan kimse.');
                INSERT INTO MESLEKLER (ISIM, TANIM)
                    VALUES('Hakem', 'Tarafların aralarındaki anlaşmazlığı çözmek için yetkili olarak seçtikleri ve üzerinde anlaştıkları kişi, yargıcı.');
                """

    cursor.execute(query)


def add_meslekler(cursor, request, meslek1):
        query = """INSERT INTO MESLEKLER (ISIM, TANIM)
        VALUES( INITCAP(%s), %s )"""
        cursor.execute(query, (meslek1.isim, meslek1.tanim))


def delete_meslekler(cursor, id):
        query="""DELETE FROM MESLEKLER WHERE ID = %s"""
        cursor.execute(query, id)


def update_meslekler(cursor, id, meslek1):
            query = """
            UPDATE MESLEKLER
            SET ISIM=INITCAP(%s),
            TANIM=INITCAP(%s)
            WHERE ID=%s
            """
            cursor.execute(query, (meslek1.isim, meslek1.tanim, id))
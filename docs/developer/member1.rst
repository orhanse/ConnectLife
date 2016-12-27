Parts Implemented by Tuğba Özkal
================================

General View
------------

Kişiler, mailler ve meslekler tablolarının içerikleri ve yeni çoklu ekleme, varolan çokluyu silme, güncelleme arama gibi veritabanı işlemleri bu kısımda açıklanmıştır.
|

1. Kişiler
----------

ID, isim, profil resmi (resim), yaşadığı yer (mekan), yaş, üniversite, çalıştığı yer (work), çalıştığı pozisyon ve konuştuğu dil özelliklerini içeren
kişiler tablosu figür 1.2.1'de gösterilmiştir.

.. figure:: tugba/kisiler.png
   :figclass: align-center

   figure 1.2.1

|
Üniversite, çalıştığı yer, dil ve meslek bilgileri diğer tablolardan dış anahtarla alınır.

**Tablo Oluşturma**


.. code-block:: python

   def init_kisiler_db(cursor):
       query = """CREATE TABLE IF NOT EXISTS KISILER (
       ID SERIAL PRIMARY KEY,
       ISIM VARCHAR(30) NOT NULL,
       RESIM VARCHAR(80) NOT NULL DEFAULT 'defaultprofil.png',
       MEKAN VARCHAR(15) NOT NULL,
       YAS INTEGER,
       UNIVERSITE INTEGER REFERENCES UNIVERSITY(ID) ON DELETE CASCADE ON UPDATE CASCADE,
       WORK INTEGER REFERENCES SIRKET(ID) ON DELETE CASCADE ON UPDATE CASCADE,
       POZISYON INTEGER REFERENCES MESLEKLER(ID) ON DELETE CASCADE ON UPDATE CASCADE,
       DIL INTEGER REFERENCES DIL(ID) ON DELETE CASCADE ON UPDATE CASCADE )"""

       cursor.execute(query)
       fill_kisiler_db(cursor)


|
Yukarıdaki kod diliminde kişiler tablosu oluşturulmuştur. Kişiler tablosu daha önce oluşturulduysa o tablo silinir ve sıfırdan yeni tablo oluşturulur.
Kodun bu partında birincil anahtar ve dış anahtarlar da belirlenmiştir. Bağlı olduğu diğer tablolardaki değişikliklerden etkilenme biçimleri de (ON DELETE CASCADE
, ON UPDATE CASCADE) yine bu kısımda belirtilmiştir. Son satırda çağrılan fonksiyon aşağıda gösterilmiştir.


** Başlangıç Eklemeleri***


Aşağıda belirtilen kod diliminde, daha önce oluşturduğumuz tabloya çoklular eklenir.


.. code-block:: python

   def fill_kisiler_db(cursor):
       query = """INSERT INTO KISILER (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                      VALUES ('Tugba Ozkal', 'profil1.jpg' ,'Afyonkarahisar', 22, 1, 1, 1, 3);
                   INSERT INTO KISILER (ISIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                       VALUES ('Cagri Gokce', 'Ankara', 22, 2, 2, 2, 1);
                   INSERT INTO KISILER (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                       VALUES ('Furkan Evirgen', 'profil2.jpg','Istanbul', 26, 2, 1, 3, 1);
                   INSERT INTO KISILER (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                       VALUES ('Kemal Hazım Ekenel', 'ekenel.png','Istanbul', 38, 2, 1, 4, 2);
                   INSERT INTO KISILER (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL)
                       VALUES ('Jeo Kaeser', 'kaeser.jpg','Almanya', 59, 2, 1, 5, 4);"""

|


**Yeni Kişi Ekleme**


Aşağıdaki kod dilimi, yeni kişi ekleme fonksiyonudur.
|


.. code-block:: python

   def add_kisiler(cursor, request, kisi1):
           query = """INSERT INTO KISILER
           (ISIM, RESIM, MEKAN, YAS, UNIVERSITE, WORK, POZISYON, DIL) VALUES (
           %s,
           %s,
           INITCAP(%s),
           %s,
           %s,
           %s,
           %s,
           %s
           )"""
           cursor.execute(query, (kisi1.isim, kisi1.resim, kisi1.mekan, kisi1.yas,
                                  kisi1.universite, kisi1.work, kisi1.pozisyon, kisi1.dil))

|
Burada, varlık niteliklerinin girildiği diğer bir fonksiyondan kişi1 çoklusu alınır ve içeriği uygun niteliklere eklenir.
|
kisi1 çoklusunu döndüren fonksiyon aşağıda verilmiştir.
|


.. code-block:: python

   @app.route('/kisiler',methods=['GET', 'POST'])
   def kisiler_sayfasi():
       connection = dbapi2.connect(app.config['dsn'])
       cursor = connection.cursor()
       now = datetime.datetime.now()

       if request.method == 'GET':
           query2 = "SELECT ID, NAME FROM UNIVERSITY"
           cursor.execute(query2)
           university = cursor.fetchall()
           query = """SELECT K.ID, K.ISIM, K.RESIM, K.MEKAN, K.YAS, U.NAME, S.NAME, M.ISIM, D.NAME
                       FROM KISILER AS K, UNIVERSITY AS U, SIRKET AS S, MESLEKLER AS M, DIL AS D
                       WHERE(
                           (K.WORK = S.ID) AND (K.UNIVERSITE = U.ID) AND (K.POZISYON = M.ID) AND (K.DIL = D.ID)
                       )"""
           cursor.execute(query)
           kisi2 = cursor.fetchall()
           cursor.execute("SELECT ID, NAME FROM SIRKET")
           sirket = cursor.fetchall()
           cursor.execute("SELECT ID, ISIM FROM MESLEKLER")
           pozisyon = cursor.fetchall()
           cursor.execute("SELECT ID, NAME FROM DIL")
           diller = cursor.fetchall()
           return render_template('kisiler.html', kisiler = kisi2, universite = university, work = sirket, pozisyon = pozisyon, diller = diller)
       elif "add" in request.form:
           kisi1 = Kisiler(request.form['isim'],
                               request.form['resim'],
                               request.form['mekan'],
                               request.form['yas'],
                               request.form['university_name'],
                               request.form['work_name'],
                               request.form['pozisyon_adi'],
                               request.form['dil_adi'])
           add_kisiler(cursor, request, kisi1)
           connection.commit()
           return redirect(url_for('kisiler_sayfasi'))

|

GET metoduyla alınan bilgiler, html kodlarında belirtilen 'add' metoduyla ilgili niteliklere gönderilir.

**Arama Fonksiyonu**
Arama fonksiyonunda kişinin ismi arama barına girilerek arama yapılabilir. Arama fonksiyonu aşağıda gösterilmiştir.


.. code-block:: python

   elif "search" in request.form:
           aranankisi = request.form['aranankisi'];
           query = """SELECT K.ID, K.ISIM, K.RESIM, K.MEKAN, K.YAS, U.NAME, S.NAME, M.ISIM, D.NAME
                       FROM KISILER AS K, UNIVERSITY AS U, SIRKET AS S, MESLEKLER AS M, DIL AS D
                       WHERE(
                           (K.WORK = S.ID) AND (K.UNIVERSITE = U.ID) AND (K.POZISYON = M.ID) AND (K.DIL = D.ID)
                       ) AND (K.ISIM LIKE %s)"""
           cursor.execute(query,[aranankisi])
           kisiler=cursor.fetchall()
           now = datetime.datetime.now()
           return render_template('kisi_ara.html', kisiler = kisiler, current_time=now.ctime(), sorgu = aranankisi)

|
**Güncelleme Fonksiyonu**

Aşağıdaki kod diliminde yeni kişi ekleme fonksiyonuna benzer olarak güncellenecek çoklu diğer fonksiyondan kisi1 etiketiyle çekilir ve
ilgili niteliklere güncellenen bilgiler eklenir.
|


.. code-block:: python

   def update_kisiler(cursor, id, kisi1):
               query="""
               UPDATE KISILER
               SET ISIM=%s,
               RESIM=%s,
               MEKAN=INITCAP(%s),
               YAS=%s,
               UNIVERSITE=%s,
               WORK=%s,
               POZISYON=%s,
               DIL=%s
               WHERE ID=%s
               """
               cursor.execute(query,(kisi1.isim, kisi1.resim, kisi1.mekan, kisi1.yas,
                                     kisi1.universite, kisi1.work, kisi1.pozisyon, kisi1.dil, id))



.. code-block:: python

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
           sirketler = cursor.fetchall()
           cursor.execute("SELECT ID, ISIM FROM MESLEKLER")
           pozisyonlar = cursor.fetchall()
           cursor.execute("SELECT ID, NAME FROM DIL")
           diller = cursor.fetchall()
           query = """SELECT * FROM KISILER WHERE (ID = %s)"""
           cursor.execute(query, kisi_id)
           now = datetime.datetime.now()
           return render_template('kisi_guncelle.html', kisi = cursor, current_time=now.ctime(), universiteler = universiteler, sirketler=sirketler, pozisyonlar = pozisyonlar, diller = diller)
       elif request.method == 'POST':
           if "update" in request.form:
               kisi1 = Kisiler(request.form['isim'],
                               request.form['resim'],
                               request.form['mekan'],
                               request.form['yas'],
                               request.form['university_name'],
                               request.form['work_name'],
                               request.form['pozisyon_adi'],
                               request.form['dil_adi'])
               update_kisiler(cursor, request.form['kisi_id'], kisi1)
               connection.commit()
               return redirect(url_for('kisiler_sayfasi'))

|
**Silme Fonksiyonu**

Silinmek istenen çoklunun birincil anahtarı olan ID'sini alarak fonksiyona gönderir ve çokluyu siler.


.. code-block:: python

   elif "delete" in request.form:
               delete_kisiler(cursor, kisi_id)
               connection.commit()
               return redirect(url_for('kisiler_sayfasi'))


.. code-block:: python

   def delete_kisiler(cursor, id):
           query="""DELETE FROM KISILER WHERE ID = %s"""
           cursor.execute(query, id)

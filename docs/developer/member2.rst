Parts Implemented by Çağrı Gökçe
================================
Gruplar, Tags(Etiketler), Has_Tag(Etiket İlişkisi) tabloları ve özellikleri bu bölümde açıklanacaktır. Ayrıca Python üzerinde bu tabloların kullanımı ile ilgili kodlar paylaşılacaktır ve veritabanı bağlantıları açıklanacaktır.


1. Gruplar
------------------
Gruplar varlığı ve site içerisindeki /gruplar/* sayfaları gruplar tablosunda gerçeklendi. Bu tablo id, zaman, aciklama, icerik, resim ve dış anahtar olan kişi_id satırlarından oluşmaktadır.

- ID satırı SERIAL türde tanımlanmıştır ve tablonun birincil anahtarıdır.
- Başlık, Acıklama ve İçerik satırları VARCHAR türünde tanımlanmıştır ve varlığın ilgili bölümlerini içerir.
- Resim satırı da VARCHAR türünde tanımlanmıştır. Bu satır html içerisinde <img src=""> etiketi içerisine yerleştirilmiştir ve uygun formatta verilen resimler kullanıcıya gösterilebilecek şekilde ayarlanmıştır.
- Zaman satırı DATE türünde tanımlanmıştır ve GG/AA/YY biçimindeki formatları desteklemektedir.
- Kişi_ID satırı INTEGER türünde tanımlandı ve kişiler tablosuna bağlantı kuran bir dış anahtar olarak tanımlandı.

.. figure:: cagri/gruplar_tablo.jpg
   :figclass: align-center ..
   
Gruplar tablosun site içerisinde aynı ilgi alanlarını paylaşan kullanıcıları buluşturup ortak paylaşımları görmelerini sağlamak amaçlandı. Her grup için oluşturan kişi bilgisini saklamak için Kişiler tablosuna dış anahtar ile bağlantı sağlandı. 

.. figure:: cagri/gruplar_ER.jpg
   :figclass: align-center
   |

**a. Tablo Oluşturma (CREATE)**

Tablo oluşturma işlemi *gruplar.py* dosyasındaki def *init_gruplar_db(cursor)* fonksiyonu içerisinde tanımlanmıştır. Bu fonksiyon *server.py* içerisinde */gruplar/initdb* route'u içinde çağırılıp bu sayfa açıldığında oluşturulmaktadır.

.. code-block:: python

  #Gruplar.py
  def init_gruplar_db(cursor):
      query = """CREATE TABLE IF NOT EXISTS GRUPLAR (
      ID SERIAL,
      BASLIK VARCHAR(80) NOT NULL,
      ZAMAN DATE NOT NULL,
      ACIKLAMA VARCHAR(500) NOT NULL,
      ICERIK VARCHAR(500) NOT NULL,
      RESIM VARCHAR(80),
      KISILER_ID INTEGER NOT NULL REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE DEFAULT 1,
      PRIMARY KEY(ID)
      )"""
      cursor.execute(query)
  
  #Server.py
  @app.route('/gruplar/initdb')
  ...
  init_gruplar_db(cursor)
|
    
Kişiler ID dış anahtarına silme operasyonu için *ON DELETE CASCADE* ve günceleme operasyonu için *ON UPDATE CASCADE* tanımları eklenmiştir. *CASCADE* yapısı sayesinde tablo üzerinde yapılan değişiklikler bağlı tabloya da uygulanacaktır ve o tablo da güncellenecektir. *RESTRICT* yapısı bu işlemlerin yapılmasını engellediğinden dolayı tercih edilmemiştir. Bir diğer tanım olan *DEFAULT 1* tanımı ile dış anahtarın verilmediği durumlarda *kişi_id=1* olan kişinin grup kurucusu olarak atanması sağlanmıştır.

**b. İlk değer atama**

İlk değer atama(initialization) işlemi *Gruplar.py* dosyasında tanımlanmıştır ve bu dosya içerisinde *fill_gruplar_db(cursor)* tanımında çağırılmaktadır. Tablo oluşturma işleminin hemen sonrasında bu işlem yapılır.

.. code-block:: python

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
|

**c. Grup Listeleme(SELECT)**

Veritabanındaki grupların listelenip kullanıcıya gösterilme işlemi */gruplar* sayfasının GET metodu ile çağrılması sonucu yapılmaktadır. Yapılan SELECT query'si sonucunda veritabanından gelen satırlar html sorgusunda yazdırılmaktadır. Ayrıca bir başka SELECT query yapısı da dış anahtar için yazıldı. 

.. code-block:: python

   #Server.py
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
|   

.. code-block:: html
   #HTML
   {%for id, baslik, zaman, aciklama, icerik, resim, kisi in gruplar%}

			<h2>{{baslik}}</h2>
			<p>{{zaman}}</p>
			<p>{{aciklama}}</p>
			<p>{{icerik}}</p>
			<p>{{kisi}}</p>
			<img style= "width:300px;heigth=300px;" src = "static/images/{{resim}}" class="img-responsive">
			<a class="btn btn-large btn-info" href= "{{ url_for('gruplar_update_page',grup_id=id)}}">Grubu Duzenle</a>
			<button type="button" action=" class="btn btn-success">Katıl!</button>
			</div>
		{%endfor%}

|

**c. Grup Ekleme(ADD)**
Kişiler tablosundan tüm kişi isimleri alınıp kullanıcıya gösterilmiştir ve kullanıcının dış anahtarı liste halinde rahatça seçebilmesi sağlanmıştır.

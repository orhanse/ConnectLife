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
      
|
    

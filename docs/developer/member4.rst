Parts Implemented by Selman Orhan
================================

Genel Bakış
------------

Bu raporda, projede yaptığım tablolar ve bu tabloların nasıl yapıldığı ve database bağlantılarının nasıl yapıldığı açıklanacaktır.

Benim proje kapsamında yaptığım tablolar şunlardır: 
  * Universiteler
  * Hobiler
  * Projeler 
  
Bu tablolarının içerikleri ve yeni eklenen ya da var olan çoklu üzerinde yapılan işlemler: 
  1. çoklu ekleme 
  2. çoklu silme
  3. çoklu güncelleme
  4. çoklu arama 
Bu veritabanı işlemleri bu kısımda açıklanmıştır. Veri tabanı ile ilgili screen shootlar ve ilgili kod parçaları da dosyaya eklenmiştir. Diğer tablolarla yapılan bağlantılar, ekleme, silme ve güncelleme işlemleri sırasında belirtilecektir. Ayrıca tablolarla ilgili **html dosyaları** ve ilgili işlemlerin *html kodları* da açıklanmıştır.

|

1. Universiteler Tablosu
------------------------

|

.. figure:: selman/universiteler.png
   :figclass:: align-center
   :scale: 100%
   :alt: university table database screenshot
   
   figure 1.1 - Universiteler tablosunun database görüntüsü
   
Universiteler tablosu, ID, name, founfation_date, location, small_info, photo ve rector_id değişkenlerini içeriyor. Burada *rector_id* bilgisi *dış anahtar* kullanılarak Kişiler tablosundan çekiliyor.

**Universiteler- Tablo Oluşturma**

.. code-block:: python

    class University:
        def __init__(self, name, foundation_date, location, small_info, photo, rector_id):
            self.name = name
            self.foundation_date = foundation_date
            self.location = location
            self.small_info = small_info
            self.photo = photo
            self.rector_id = rector_id
            
Yukarıda belirtilen şekilde **class** olarak tanımlanan Universiteler tablosu, aşağıda belirtilen şekilde şekilde oluşturulur. Başlangıç değerleri için database belirli tablo verileri eklemek için *init_universities_db* fonksiyonu kullanılıyor.

**Universiteler- Başlangıç verileri ekleme**

.. code-block:: python

  def init_universities_db(cursor):
      query = """CREATE TABLE UNIVERSITY (
          ID SERIAL,
          NAME VARCHAR(100) NOT NULL,
          FOUNDATION_DATE VARCHAR(4) NOT NULL,
          LOCATION VARCHAR(80) NOT NULL,
          SMALL_INFO VARCHAR(500),
          PHOTO VARCHAR(80),
          RECTOR_ID INTEGER NOT NULL REFERENCES KISILER(ID) ON DELETE CASCADE ON UPDATE CASCADE DEFAULT 1,
          PRIMARY KEY (ID)
          )"""
      cursor.execute(query)
      insert_university(cursor)

Yukarıdaki kod diliminde Universiteler tablosu oluşturulmuştur. Bu tablosu daha önce oluşturulduysa o tablo silinir ve sıfırdan yeni tablo oluşturulur. Yukarıda görüldüğü üzere; birincil anahtar olarak ID ve Kisiler tablosuna bağlanmak için kullanılan dış anahtar olarak da rector_id belirlenmiştir. Bağlı olduğu diğer tablolardaki değişikliklerden etkilenme biçimleri de  **(ON DELETE CASCADE, ON UPDATE CASCADE)** 
şeklinde belirtilmiştir.

**Universiteler- Çoklu Ekleme Metodu**

.. code-block:: python

  def add_university(cursor, request, university1):
      query = """INSERT INTO UNIVERSITY
              (NAME, FOUNDATION_DATE, LOCATION, SMALL_INFO, PHOTO, RECTOR_ID) VALUES (
              INITCAP(%s),
              %s,
              INITCAP(%s),
              INITCAP(%s),
              %s,
              %s
              )"""
      cursor.execute(query, (university1.name, university1.foundation_date, 
      university1.location, university1.small_info, university1.photo, university1.rector_id))

*GET* metoduyla kullanıcıdan alınan bilgiler, html sayfasındaki *'add'* metoduyla yukarıdaki fonksiyon yardımıyla databasedeki daha önceden oluşturulan Universiteler tablosuna eklenir.

**Universiteler- Çoklu Silme Metodu**

.. code-block:: python

  def delete_university(cursor, id):
    query ="""DELETE FROM UNIVERSITY WHERE ID = %s"""
    cursor.execute(query, id)
  
Databaseden silinmek istenen çoklu birincil anahtar yardımıyle (ID) databaseden seçilir ve *'delete'* metoduyla yukarıdaki fonksiyona gönderilir ve çoklu databaseden silinir.

**Universiteler- Çoklu Güncelleme Metodu**

.. code-block:: python

  def update_university(cursor, id, university1):
      query = """
          UPDATE UNIVERSITY
          SET NAME=INITCAP(%s),
          FOUNDATION_DATE=%s,
          LOCATION=INITCAP(%s),
          SMALL_INFO=INITCAP(%s),
          PHOTO=%s,
          RECTOR_ID =%s
          WHERE ID=%s
          """
      cursor.execute(query, (university1.name, university1.foundation_date, university1.location, 
      university1.small_info, university1.photo, university1.rector_id, id))
      
Güncellenmek istenen çoklu birincil anahtar yardımıyla database tablosundan seçilir. *'update'* ve *GET* metodları kullanılarak kullanıcıdan alınan yeni bilgiler *POST* metodu kullanılarak database eklenir.

**Universiteler- Çoklu Arama Metodu**

.. code-block:: python
  
  elif "search" in request.form:
        searched = request.form['searched'];
        query = """SELECT U.ID, U.NAME, U.FOUNDATION_DATE, U.LOCATION, U.SMALL_INFO, U.PHOTO, K.ISIM FROM UNIVERSITY AS U,
                   KISILER AS K WHERE((U.RECTOR_ID = K.ID) AND (U.NAME LIKE %s))"""
        cursor.execute(query,[searched])
        university=cursor.fetchall()
        now = datetime.datetime.now()
        return render_template('universiteler_ara.html', university = university, current_time=now.ctime(), 
        sorgu = searched)

Arama metodu Universite çoklusunun name değişkeni üzerinden arama yapar. Aramak istenen çoklu yukarıdaki fonksiyon yardımıyla databaseden aranır ve *POST* metodu yardımıyla ekrana aktarılır.

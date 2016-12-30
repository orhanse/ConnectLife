Geliştirici Rehberi (Developer Guide)
=====================================

.. figure:: developer_index/logo.jpeg
   :figclass: align-center

Web projemiz olan Connect Life projesinin geliştirici bölümüne hoş geldiniz! Bu bölümde web projemizin veritabanı tasarımı ve kod tasarımı ile ilgili detayları bulabilir, site geliştirmesi için kullandığımız araçlar ve yapılar hakkında fikir sahibi olabilirsiniz. Eğer bir geliştirici değilseniz bu bölüm size karışık gelebilir, kullanıcı rehberi bölümüne göz atmanız önerilir.

Veritabanı Tasarımı (Database Design)
-------------------------------------
ConnectLife projesinin veritabanı tasarımı bu bölümde anlatılacaktır. Sitemizin veritabanı tasarımını yaparken site üzerinde gerçekleşmesi gereken her bölüm için en az bir varlık olacak şekilde bir tasarım gerçekleştirdik. Site üzerinde tamamen işlevsel ve kullanıcının aktif bir biçimde kullanabileceği yapıları veritabanında bir tablo şeklinde tasarladık. Bu tablolar arasında Şirketler, Mailler, Diller, Projeler, Lokasyonlar, Kişiler, Üniversiteler, Makaleler, İş ilanları, Öneriler, Meslekler, İlgi Alanları ve Gruplar bulunuyor. Proje veritabanı içeriksel ve ilişkisel yapısını gösteren **E-R diyagramı** aşağıda verilmiştir. Tüm tablo yapı ve içerikleri de diyagramda gösterilmiştir.

.. figure:: ER.png
   :figclass: align-center

Veritabanı tasarımında projemiz için uygun olarak düşündüğümüz PostgreSQL veritabanını kullandık. PostgreSQL'in açık kaynaklı olması, hızlı olarak işlem yapabilmesi, sistem üzerinde efektif çalışması, python ve flask için desteğinin olması ve SQLAlchemy gibi ORM yapıları ile çalışabilmesi bu seçimi yapmamızda faydası olan nedenler arasında. En büyük avantajı ise projemizde bağıntı modelli(Relational) bir veritabanı seçmemiz gerekmesi ve PostgreSQL'in bu özelliği sağlaması oldu.

.. figure:: developer_index/postgre.png
   :figclass: align-center

Proje içerisinde veritabanı dış bağlantıları yeni bir satır ve hedef tablonun birincil anahtarı üzerinden gerçekleştirildi. Örneğin İş İlanları tablosundan Şirketler tablosuna yapılan bir dış bağlantı için İlanlar tablosunda *sirket_id* isimli bir dış anahtar tanımlanarak şirketler tablosunun birincil anahtarı gösterildi. Veritabanı tanımlarından sitenin veritabanı bütünlüğü bozulmaması için ON UPDATE ve ON DELETE terimleri ile güncelleme ve silme işlemleri yapıldığında otomatik düzenlemeler yapılması sağlandı. CASCADE komutu ile tablolar arası senkronizasyonlu güncellemeler yapıldı ve RESTRICT komutu ile veritabanı bütünlüğünü bozacak işlemlerin engellenmesi sağlandı.

Veritabanı tasarımında dikkat edilen bir önemli özellik de dış anahtar seçimlerinin kullanıcıya yansıtılırken anahtar yerine dış anahtarı simgeleyen ana nesne üzerinden yapılması oldu. Örneğin kişiler üzerinde yapılan bir dış anahtar bağlantısında ilgili tabloya yapılan ekleme işleminde kişi_id'nin güncellenmesi gereken inputa kişi isimleri yerleştirildi ve kullanıcılara veritabanı id değerleri yerine gerekli bilgiler gösterilmiş oldu. Ayrıca seçme, ekleme, güncelleme ve silme gibi işlemler ID değeri temelli yapılmasına rağmen kullanıcıya ID değerleri gösterilmedi.


Kod Yapısı (Code Structure)
---------------------------

Web projemizde güncel ve hızlı web araçlarından biri olan Flask'ı tercih ettik. Python dili üzerinde çalışan bu eklenti, Python dilini web konusundaki zorluklardan kurtarmış ve bu dilin gücünü web geliştirme ile buluşturmuş popüler eklentilerden bir tanesi. Bu konuda terchi edilen bir diğer bir eklenti ise Django. Ancak Flask dilinin daha esnek ve modüler olması, eklentilerin kullanımı ve etkileşimlerinin daha iyi olması ve daha iyi customization (çeşitlendirilebilirlik) sunması bu eklentiyi tercih sebeplerimizden oldu.

.. figure:: developer_index/flask.png
   :figclass: align-center

**Kurulum (Setup Instructions)**

Projemiz Python 3 üzerinde ve bahsedildiği gibi Flask modülü ile birlikte çalışmaktadır. Projeyi çalıştırabilmek için öncelikle Python 3 kurulumu yapılıp ardından PIP yükleme yöneticisi ile Flask eklentisi yüklenmelidir.

Python kurulumu Windows için https://www.python.org/downloads/ adresinden Python 3 sürümünü indirerek yapılabilir. Kurulum sırasında python indirme yöneticisi PIP de indirilecek şekilde seçilmelidir. Linux ve Mac işletim sistemleri için konsoldan yükleme yapılmalıdır. Linux için aşağıdaki komutlar ile Python 3 ve PIP kurulumu yapılabilir.


.. code-block:: python

   #Python 3 kurulumu
   sudo add-apt-repository ppa:jonathonf/python-3.6
   sudo apt-get update
   sudo apt-get install python3.6
   #PIP kurulumu
   sudo easy_install pip 
   
|

Kurulumların ardından Flask eklentisi yüklenmelidir. Tüm işletim sistemleri için konsolu açıp aşağıdaki kodu yazarak Flask ve Python için postgreSQL eklentisi olan Psycopg2 kurulmalıdır. 

.. code-block:: python
   #Eklenti kurulumları
   sudo pip3 install flask
   sudo pip3 install psycopg2
|

Ayrıca projenin github adresinden erişilebilmesi için Git eklentisi de kurulmalıdır. Windows ve Mac için web adresinden kurulum dosyalarına erişilebilir. Linux için aşağıdaki komut ile uygulama merkezinden indirme yapılabilir.


.. code-block:: python
   #Git kurulumu
   sudo apt-get install git-all
|

Kurulumların tamamı bittikten sonra projenin github sayfına gelinip güncel bir **Clone-URL** alınır ve git-clone komutu ile proje lokal sisteme çekilir.

.. figure:: developer_index/clone.jpg
   :figclass: align-center

Clone işlemi tamamlandığında konsoldan python3 ile server.py çalıştırıldığında proje localhost üzerinde 0.0.0.0:5000 adresinde açılacaktır.

.. code-block:: python
   python3 server.py
|

**Kod yapısı**

Kod düzeninde programın çalışması *server.py* ana dosyasında gerçekleşmektedir. Grup üyeleri her tablo için kendilerine ait .py dosyası oluşturuldu. Her tablo yapısını simgeleyen bu .py dosyalarında veritabanı ile ilgili fonksiyonlar bulunuyor. Server.py dosyası içerisinde bu dosyalar aşağıdaki gibi çağrılıyor.

.. code-block:: python
   from university import *
   from sirketler import *
   from gruplar import *
   from kisiler import *
   from isilanlari import *
   from meslekler import *
   from mailler import *
   from makaleler import *
   from oneriler import *
   from diller import *
   from projeler import *
   from lokasyonlar import *
   from hobiler import *
|

Server.py dosyasında ayrıca veritabanı ile ilgili işlemlerle ilgili iki fonksiyon bulunuyor. Veritabanının açılıp kullanıma hazır hale getirilmesi sağlanıyor. Ayrıca konfigürasyonların yapıldığı ve HTML bağlantısının sağlandığı bir fonksiyon da mevcut.


.. code-block:: python

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
|

Dosya içerisinde anasayfa için / adresine bir app.route çağrılıyor. Bu adreste anasayfa için hazırladığımız home.html render edilerek kullanıcıya sunuluyor.

.. code-block:: python

   @app.route('/')
   def home_page():
       now = datetime.datetime.now()
   return render_template('home.html', current_time=now.ctime())
   
|



**to include a code listing, use the following example**::

   .. code-block:: python

      class Foo:

         def __init__(self, x):
            self.x = x


.. toctree::
   :maxdepth: 5

   TugbaOzkal
   CagriGökce
   AhmetEginkaya
   SelmanOrhan
   GulsahDamla

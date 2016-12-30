Developer Guide
===============

.. figure:: logo.jpeg
   :figclass: align-center

Web projemiz olan Connect Life projesinin geliştirici bölümüne hoş geldiniz! Bu bölümde web projemizin veritabanı tasarımı ve kod tasarımı ile ilgili detayları bulabilir, site geliştirmesi için kullandığımız araçlar ve yapılar hakkında fikir sahibi olabilirsiniz. Eğer bir geliştirici değilseniz bu bölüm size karışık gelebilir, kullanıcı rehberi bölümüne göz atmanız önerilir.

Database Design
---------------
ConnectLife projesinin veritabanı tasarımı bu bölümde anlatılacaktır. Sitemizin veritabanı tasarımını yaparken site üzerinde gerçekleşmesi gereken her bölüm için en az bir varlık olacak şekilde bir tasarım gerçekleştirdik. Site üzerinde tamamen işlevsel ve kullanıcının aktif bir biçimde kullanabileceği yapıları veritabanında bir tablo şeklinde tasarladık. Bu tablolar arasında Şirketler, Mailler, Diller, Projeler, Lokasyonlar, Kişiler, Üniversiteler, Makaleler, İş ilanları, Öneriler, Meslekler, İlgi Alanları ve Gruplar bulunuyor. Proje veritabanı içeriksel ve ilişkisel yapısını gösteren **E-R diyagramı** aşağıda verilmiştir. Tüm tablo yapı ve içerikleri de diyagramda gösterilmiştir.

.. figure:: ER.png
   :figclass: align-center

Veritabanı tasarımında projemiz için uygun olarak düşündüğümüz PostgreSQL veritabanını kullandık. PostgreSQL'in açık kaynaklı olması, hızlı olarak işlem yapabilmesi, sistem üzerinde efektif çalışması, python ve flask için desteğinin olması ve SQLAlchemy gibi ORM yapıları ile çalışabilmesi bu seçimi yapmamızda faydası olan nedenler arasında. En büyük avantajı ise projemizde bağıntı modelli(Relational) bir veritabanı seçmemiz gerekmesi ve PostgreSQL'in bu özelliği sağlaması oldu.

.. figure:: postgre.png
   :figclass: align-center


Code
----

**explain the technical structure of your code**

**to include a code listing, use the following example**::

   .. code-block:: python

      class Foo:

         def __init__(self, x):
            self.x = x

.. toctree::

   Tuğba Özkal
   Çağrı Gökçe
   Ahmet Eğinkaya
   Selman Orhan
   Gülşah Damla

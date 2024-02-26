Projede kullanılan veri seti : https://www.kaggle.com/datasets/iabhishekofficial/mobile-price-classification
Mobil cihaz fiyat tahmini ile ilgili verileri içeren bir veri setidir.
Fiyat tahmini yapılan sütun price_range sütunudur. Bu sütun 0,1,2,3 değerlerini alır. Bu sütunu kategorik olarak hangi fiyat aralığında olduğunu tespit etmek için kullandım.
Öncelikle spark session oluşturarak indirdiğim veriyi spark verisine dönüştürdüm.
![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/b76c7699-1331-40da-96a6-81864a10cf8b)

 
Sonrasında verideki sayısal, kategorik sütunları tespit ettim.
 ![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/f8bf75de-c701-4050-b63a-0a8f19000877)

Kategorik ve sayısal değişkenler için analiz yaptım.
  ![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/d795e843-70de-4218-99db-52e2064c55f5)
![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/148b30af-f59c-4039-b454-0e977bd27664)

Korelasyon matrisinde sütunların ilişkisini tespit ettim.
 ![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/85ff1024-8b7c-416f-85c8-42c391bb1860)

Price_range ve ram arasında 0.92 gibi yüksek bir korelasyon tespit edilmiştir.
Aykırı değer ve null değer analizi yaptım. Aykırı değer ve null değer veri setinde mevcut değil.
Sonrasında verinin input girişleri için vector assembler kullanarak tek bir sütun haline getirdim.
Veriyi eğitim ve test dosyasına 0.7 eğitim  0.3 test verisi olarak ayırdım.
Makine öğrenmesi modeli olarak random forest, decision tree ve logistic regresyon kullandım.
Spark ml pipeline kullanarak bu modelleri ve vektörize işlemini pipeline içerisine aldım ve modelleri oluşturup doğruluğu kontrol ettim.
Modellerin doğruluğunu accuracy kullanarak değerlendirdim. Ve modelleri cross validation kullanarak test ettim. Cv değerini 5 olarak aldım. Tespit edilen en iyi modelleri eğitim setiyle eğitip test verisiyle test ettim ve accuracy değerleri:
 ![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/a48ddc1d-d47b-4481-92e6-d6d12bec352e)

En iyi skoru logistic regresyon verdiği için bu modeli kullandım ve bu modeli klasör içerisine kaydettim.
Kafka ya kaydetmek için  oluşturduğum test verisini de csv olarak dışarı aktardım. 
Kafka tarafında zookeper ve kafka sunucusunu docker üzerinden başlattım. Bunun için docker compose dosyası oluşturdum ve docker-compose up komutuyla kafkayı başlattım.
Kafka da kod ile topic oluşturdum bu topic replication factorü 1 ve partition değeri 5 olarak belirledim.
Dışarı aktardığım test.csv dosyasındaki verileri  bu topice ekledim.
Spark ile oluşturduğum topic teki verileri consume ettim.
Verileri kafkadan  streaming olarak 1 saniyede 1 veri olarak  aldım, gelen verileri oluşturduğum modele tahmin etmesi için yolladım ve sonucu kaydettim.
Tahmin edilen sonucu ve gerçek sonucu ekrana yazdırdım.
 ![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/bee42b16-66d7-4894-93e4-201b577d0903)

Ayrıca mongodb ile kafkadan verileri consume ederek kaydettim. 
 ![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/ace7d1bf-f23b-4946-8528-98abe2c32f0d)

![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/736a6710-2790-466d-9f87-167de008e89c)

 
Docker 
 ![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/b3d3cb8c-5c30-4da5-be68-5d3eb81f69de)

 
![image](https://github.com/enesbt/BIGDATA-PROJECT/assets/95939881/d74e9218-161e-4e5f-8abb-b8c235afdd5a)


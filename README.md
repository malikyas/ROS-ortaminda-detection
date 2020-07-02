# ROS-ortaminda-detection

Bu repoda ROS ortamında Gazebo simülasyonu üzerinden mybot isimli robotun kamerasından gelen görüntüler üzerinde MaskRCNN yapısıyla nasıl detection yapılacağı anlatılmakta. Kullanacağımız weightler insan resimleri barındıran PennFudanPed veri setiyle eğitilmiştir. Dolayısıyla detect edilecek objeler insanlardır.

NOT: Uygulamayı gerçeklemek için Ubuntu işletim sistemi gereklidir. MaskRCNN oldukça ağır bir algoritmadır. Eğer bilgisayarınıza güvenmiyorsanız uygulamayı denemeyin.

Benim Bilgisayarımın Bazı Özellikleri:

Ekran Kartı = GTX 1060 6GB (Mobile)

İşlemci = Intel i7-8750H 2.20GHz x 12 CPU

RAM = 16 GB

İşlem sırasında CPU çekirdek sıcaklıklarım 65-75 derece arasında seyretti. Ekran kartı sıcaklığım ise 55-65 arasındaydı. CPU thread kullanım yüzdeleri ise &28.2 ile %52.0 arasında seyretti. Ekran kartımdan ise 2.818 GB hafıza kullanılıyordu.

# ROS sürümü

Uygulama ROS Noetic ile yapıldı. ROS Noetic python3 kullanırken eski sürümler python2 kullanmakta. Anlatım boyunca gerekli olduğu yerlerde eğer eski bir ROS sürümü kullanıyorsanız ne yapmanız gerektiği anlatılacaktır. 

# 0- Kullanışlı Terminal Komutları

**0.1-** cd herhangi_bir_dizin -> herhangi_bir_dizin dizinine gider.

**0.2-** cd -> terminalde sadece cd yazmak /home dizinine götürür.

**0.3-** cd .. -> bir önceki dizine götürür.

**0.4-** !! -> Şu an açık olan terminalde son çalıştırılan komutu tekrar çalıştırır.

**0.5-** mkdir klasör_adı -> terminalin açık olduğu dizinde klasör_adı isimli bir klasör oluşturur.

**0.6-** mkdir -p klasör/alt_klasör -> terminalin açık olduğu dizinde klasör isimli bir klasör oluşturup onun içerisinde de alt_klasör isimli bir klasör oluşturur.

**0.7-** gedit isim.uzantı -> terminalin açık olduğu dizinde 'uzantı' uzantılı isim adında bir klasör oluşturur. Eğer bu isimde ve uzantıda bir dosya zaten varsa onu açar.

# 1- Workspace ve Paket Oluşturma

Kodların ROS ile haberleşebilmesi için ROS'un yapılandırma sistemi catkin ile yapılandırılmalıdır. Düzen ve kolaylık adına bir workspace oluşturmak iyi olacaktır. Zaten catkin ile yapılandırılmış bir workspace'iniz varsa bu adımı atlayabilirsiniz.

**1.1-** Terminalde /home dizininde "mkdir -p catkin_ws/src" komutu ile /home/catkin_ws/src dizinini oluşturun. (workspace'inizde catkin_ws yerine istediğiniz herhangi bir ismi verebilirsiniz.)

**1.2-** Aynı terminalde "cd catkin_ws" komutu ile catkin_ws klasörüne gidin ve "catkin_make" komutu ile ortamınızı derleyin. Derleme hatasız bitince catkin_ws klasöründe build, devel ve src klasörleri bulunacaktır.

![image](https://user-images.githubusercontent.com/46991761/86340950-4cd1ff80-bc5e-11ea-9695-78f969ed6cd7.png)


**1.3-** Yeni bir catkin workspace'i oluşturduğunuz zaman terminalde ROS komutları ile o workspace'e erişmek için her terminal açışınızda workspace'inizdeki devel klasöründe bulunan setup.bash'i source'lamanız gerekir. Bunu her zaman yapmamak için yeni bir terminalde "gedit .bashrc" komutunu çalıştırın. Karşınıza çıkan text editorde en alt satıra  "source /home/bilgisayarınızın-adı/catkin_ws/devel/setup.bash" satırını ekleyin, kaydedip text editörü kapatın. Terminale bu sefer de source .bashrc yazın.

![image](https://user-images.githubusercontent.com/46991761/86341212-a89c8880-bc5e-11ea-96bb-864fcbf37e90.png)


**1.4-** Terminal üzerinden "cd /catkin_ws/src" komutu ile  workspace'inizin src klasörüne gidin. "catkin_create_pkg ros_cv std_msgs rospy" komutu ile ros_cv isimli paketinizi oluşturun. Python kodlarında std_msgs ev rospy isimli ROS kütüphanelerini kullanacağımızın için paketi oluştururken bu kütüphaneleri argüman olarak vermeliyiz. Paketi oluşturduktan sonra tekrar catkin_ws klasörüne gidip workspace'inizi tekrar "catkin_make" ile yapılandırın. Yapılandırma sonrası paketinizin içinde CMakeLists.txt, package.xml ve src klasörü bulunmalıdır.

![image](https://user-images.githubusercontent.com/46991761/86341488-0b8e1f80-bc5f-11ea-8b63-132cb8abce50.png)



# 2- Mybot Kurulumu

Mybot üzerinde lidar sensörü ve kameraya sahip, hareket kabiliyeti olan örnek bir robot. 

![image](https://user-images.githubusercontent.com/46991761/86341593-2cef0b80-bc5f-11ea-8fce-307110e88d34.png)


**2.1-** Mybot'u "https://github.com/richardw05/mybot_ws" adresinden indirin. mybot_ws klasörünü zipten /home dizininize çıkarın. Klasörün ismini "mybot_ws" yapın. (Ya da istediğiniz herhangi bir isim.)

**2.2-** "cd mybot_ws" komutu ile mybot_ws klasörüne gidin ve "catkin_make" ile mybot workspace'ini yapılandırın. Hemen ardından yukarıdaki 1.3 sayılı adımdaki işlemler ile workspace'inizi source'layın.

**2.3-** Test amaçlı terminalinizi açıp "roslaunch mybot_gazebo mybot_world.launch" komutunu çalıştırın. 

**2.4-** Yine test amaçlı terminalinize "roslaunch mybot_description mybot_rviz.launch" komutunu çalıştırın. 

**2.5-** Launch işlemleri sorunsuz açıldıysa yükleme başarılı demektir.

**2.6-** ÖNEMLİ UYARI: Eğer aşağıdaki resimdeki gibi sorunlarla karşılaşıyorsanız ilgili launch fileları mybot_ws klasöründe aratın. İçlerinde "xacro.py" yazan yerleri "xacro", "type="state_publisher"" yazan yerleri "type="robot_state_publisher"" ile değiştirin.

![xacro_publisher_hataları](https://user-images.githubusercontent.com/46991761/86361243-376bce00-bc7c-11ea-953b-bfe72648e0a4.png)


# 3- ROS ile OpenCV Haberleşmesi

Workspace'lerimizi kurduk. Şimdi işin can alıcı kısmındayız. 

**3.1-** Öncelikle bu repoyu 1.4'de oluşturduğunuz "ros_cv" adlı paketin içine indirin. 

**3.2-** "cd catkin_ws" komutuyla catkin workspace'inize gidip "catkin_make" ile workspace'i yapılandırın.

**3.3-** İndirmiş olduğunuz repo da bizi ilgilendiren dosya ros_predict.py. Bu py dosyası mybot'un ROS ortamında yayınladığını kamera görüntülerine erişip, onlar üzerinden MaskRCNN ile detection yapan bir node. 

**3.4-** (Opsiyonel)- Eğer rastgele bir resimde detection yapmak istiyorsanız predict.py'ı kullanabilirsiniz. Eğer kendi veri setinizle detection yapmak istiyorsanız https://github.com/metobom/pytorch-detection-ve-segmentasyon bu repoya bakabilirsiniz.

**3.5-** ROS'dan gelen görüntüleri OpenCV formatına çevirmek için CvBridge olarak adlandırılan bir nevi köprüyü kullanacağız. Kodu bir düzenli ve basit olması için bir class altında yazdım. Tercihlerinize göre kodu düzenleyebilir, karşılaştığınız sorunlarla ilgili bir issue açabilirsiniz.

**3.6-** Yazının başlarında bahsettiğim gibi ROS Noetic öncesi Python2 kullanırken ROS Noetic Python3 kullanmakta. Noetic öncesi sürümlerde bilgisayarınızda Python2'nin yanı sıra ayrı olarak başka bir Python sürümü de kurmuş olabilirsiniz. Python sürümlerinin çakışmaması için kodunuzun başına bir "shebang" satırı koymanızda fayda var. Ek olarak yine genel olarak kullanılan encoding UTF-8'i belirtmekte de fayda var. (Meraklılarına: https://en.wikipedia.org/wiki/UTF-8)

**3.7-** Şimdi kodun anlatımına geçelim. Herhangi bir hata ile karşılaştığınızda veya anlatımda açık olmayan/mantıksız bir kısım gördüğünüzde bir issue açabilirsiniz.

**3.7.1-** 1 ve 2. satırlarda 3.6'da bahsettiğim shebang satırı ve encoding satırı bulunmakta. ÖNEMLİ UYARI: Eğer ROS Noetic öncesi bir sürüm kullanıyorsanız shebang satırındaki python3'ü python olarak değiştirin.

![image](https://user-images.githubusercontent.com/46991761/86342444-4a70a500-bc60-11ea-90da-7dcb89709078.png)


**3.7.2-** 4 ve 13. satırlar arasında kullanacağımız kütüphaneler bulunmakta. Eğer 1.4 sayılı adımda paket oluştururken rospy std_msgs argümanlarını vermeseydik ropsy ve std_msgs kütüphaneleri tanınmayacaktı. 

![image](https://user-images.githubusercontent.com/46991761/86343041-15b11d80-bc61-11ea-920d-11cb765b5b4a.png)

**3.7.3-** 16. satırda classımızı tanımlıyoruz. 17. satırda init fonksiyonumuzu tanımlıyoruz. 18. satıda node'umuzun adını tutan bir değişken tanımlıyoruz. 19. satırda rospy kütüphanesinde bulunan init_node metoduyla 'detector' isimli node'umuzu oluşturuyoruz. 21. satırda ROS formatından CV formatına çevirdiğimiz resimleri pytorch'a uygun olan tensor formatında yükleyebilmek için loader isimli bir obje tanımlıyoruz. 23. satırda 3.5 sayılı adımda belirttiğim CvBridge'ı tanımlıyoruz. 25. satırda ise mybot'un yayınladığını kamera topic'ine abone oluyoruz. 2.3 numaralı adımdaki launch komutunu çalıştırdığınızda farklı bir terminalde "rostopic list" komutunu kullanırsanız "/mybot/camera1/image_raw" topic'ini görebilirsiniz. 25. satıra tekrar dönersek Subscriber metodunda ilk parametre olarak abone olacağımız topic'i belirttik. 2. parametre olarak std_msgs.msg'dan import ettiğimiz Image'ı veriyoruz. 3. parametre olarak ileriki adımlarda anlatacağım ros_to_cv fonksiyonunu veriyoruz. Kısaca ne olduğundan bahsetmek gerekirse mybot'un kamerasından gelen ROS formatındaki görüntüler ros_to_cv fonksiyonuna verilecek. 27. satırda ise kameradan görüntü alındığına dair bir log giriyoruz. 

![image](https://user-images.githubusercontent.com/46991761/86345610-6aa26300-bc64-11ea-9aa3-0bcdf43273ea.png)

**3.7.4-** 30. satırda ROS formatından CV formatına çevirilmiş görüntüleri torch'un istediği formata çeviren bir fonksiyon tanımlıyoruz. 33. satırda 21. satırda tanımladığımız loader ile resmi float veri yapısında bir tensora çeviriyoruz. Floata çevirme sebebinden üstünkörü bahsetmek gerekirse, CNN modelimizin kullandığı loss fonksiyonu, optimizer ve cuda yapısı ile ilgili. 34. satırda konumuzun dışında kalıyor fakat yine üstünkörü bahsetmek gerekirse gradient tabanlı bir CNN kullandığımız için Variable fonksiyonu içinde requires_grad'a True veriyoruz. Variable fonksiyonu pytorch'un eski sürümlerinden kalma Variable veri tipiyle alakalı. Eski pytorch sürümlerinde Variable fonksiyonu variable veri tipi döndürürken artık bir tensor döndürüyor. Özetle burada önemli olan kısım requires_grad=True :D. 35. satırda da görüntüyü cuda tensorüne çeviriyoruz. Bunun yapılma amacı cuda teknolojisi ile ekran kartını kullanabilmek.

![image](https://user-images.githubusercontent.com/46991761/86346881-38920080-bc66-11ea-890f-a2593e5bf9fb.png)


**3.7.5-** 37. satırda CV formatında çevrilmiş görüntüler üzerinden detection yapacak fonksiyonumuzu tanımlıyoruz. 38. PennFudanPed veri setiyle önceden eğitilmiş "network" isimli weightlerimizi yüklüyoruz. Fonksiyona bir görüntü verildiği zaman bu weightleri kullanarak detection yapacak. Bu "https://drive.google.com/drive/folders/1gD5s89JLXen9nEypHiciG01urIVUbSEp" adresten network isimli weightleri indirebilirsiniz. İndirdiğiniz network isimli dosyayı ros_cv paketiniz içindeki bu repodan indirdiğiniz pytorch_detector isimli klasörün içine atın ve 38. satırdaki torch.load'ın içine network isimli dosyanın bulunduğu dizini girin. 39. satır yine konumuzun dışında kalıyor. Fakat yine üstünkörü anlatmak gerekirse CNN modelimizde eğitim sırasında overfitting vb. sorunları engellemek için kullanılan, fakat eğitilmiş modelle detection yaparken işimize çomak sokabilecek olan, Dropout vb. layerları deaktif ediyor. 40. satırda ise CV formatındaki görüntüyü 3.7.4 sayılı adımda tanımladığımız img_loader fonksiyonu ile yüklüyoruz. 41 ve 42. satırlarda da detection'ı yapıyor ve 43. satırda modelimizin yaptığı tahminleri (detectionları) döndürüyoruz. 

![image](https://user-images.githubusercontent.com/46991761/86349414-ba375d80-bc69-11ea-8867-a92fa9428e1e.png)

**3.7.6-** predictor fonksiyonu ile döndürdüğümüz pred bir dictionary'dir. Bu dictionary bizim kullanacağımız detection sonucu tahmin edilen boundary box kordinatları, bu boundary box'ların tahmin sonucu yüzde kaç ihtimalle tahmin edilen nesne olduğunu ve mask'ları döndürüyor. 45. satırda pred isimli dictionary'den dönen boundary box kordinatlarını ve doğruluk oranlarını kullanarak ROS formatından CV formatına çevirmiş olduğumuz görüntüler üzerinde detect edilen objeleri boundary box içine alan fonksiyonu tanımlıyoruz. 46. satıda numpy array olarak dönen boundary box kordinatlarını boxes_np değişkenine atıyoruz. 48. satırde iter_num içinde bir görüntüde kaç detection yapıldığının sayısını tutuyoruz. Bu sayıyı aynı görüntüdeki tüm detect edilen insanları boundary box içine almak için kullanacağız. 49. satırda bir görüntüdeki tüm detect edilen insanları boundary box içine almak için bir döngü oluşturup bu döngüyü iter_num kadar devam ettiriyoruz. 50 ve 51. satırdaki tl ve br değişkenleri top left ve bottom right'ı temsil etmekte. Bu değişkenler pred dictionary'sinden dönen boundary box'ların sol üst ve sağ alt kordinatlarını tutmakta. 52. satırda yine dictionary'den dönen tahmin sonuçlarını (skorları) kullanarak belirlediğimiz bir oranın üstünde olan detectionları 53. satırda cv2.rectangle metodu ile çizdiriyoruz. Son olarak 54. satırda da boundary box çizilmiş görüntüleri döndürüyoruz.

![image](https://user-images.githubusercontent.com/46991761/86351146-7a25aa00-bc6c-11ea-893f-c57cfc222346.png)

**3.7.7-** 56. satırda tanımladığımız drawMask fonksiyonu ise yine dictionary'den dönen maskları çizdiren fonksiyon. 57 ve 58. satırlarda gelen görüntülerin yükseklik ve genişliklerini h ve w değişkenlerine atıyoruz. Dönen maskları siyah beyaz olacak. Detect edilen insanlar beyaz, arkaplan siyah olacak. Bir görüntüdeki tüm detect edilen insanları çizebilmek için 59.satırda resimle aynı şekilde boş, siyah bir resim tanımlıyoruz. 60. satırda dictionary'den dönen mask sayısı kadar sayan bir döngü içinde 59. satırda tanımladığımız siyah görüntünün pikselleriyle maskları topluyoruz. Böylece elimizde detect edilen tüm insanların masklarını bulunduran binary (siyah beyaz) bir görüntü elde ediyoruz. Eğer bu toplama işlemini yapmasaydık her bir frame'de sadece detect edilen bir insanın maskını görecektik. Son olarak elde ettiğimiz görüntüyü 62. satırda döndürüyoruz.

![image](https://user-images.githubusercontent.com/46991761/86352833-1badfb00-bc6f-11ea-9ac0-b4980280ebde.png)


**3.7.8-** 64. satırda 3.7.3 sayılı adımda bahsettiğim ros_to_cv fonksiyonunu tanımlıyoruz. Bu fonksiyonda bir try, except yapısı kullanıyoruz. Bunun sebebi ROS'dan bozuk görüntü gelmesi ihtimalinde terminalde bir hata uyarısı yazdırmak. Ve işlemin devam etmesini sağlamak. 66. satırda tanımladığımız CvBridge ile ROS'dan gelen görüntüyü CV formatına 'bgr8' olarak çeviriyoruz. Çevrilen görüntüyü yukarıda uzun uzun anlattığım fonksiyonları kullanarak işliyor ve en son cv2.imshow metoduyla ekrana çıkarıyoruz. NOT: mask çizdirmek için output=self.drawBox(cv_image)'ı commentleyin. Boundary box çizdirmek için ise tam tersini yapın.

![image](https://user-images.githubusercontent.com/46991761/86353514-084f5f80-bc70-11ea-98ba-d6a83b37ce9a.png)

**3.7.8-** 80. satırda bir main fonksiyonu tanımlıyoruz. İçerisinde işlemi 'q' tuşuna basınca bitirecek bir mekanizma oluşturmak amacıyla try except yapısını kullanıyoruz. try kısmında tanımladığımız class'ı çağırıyor ve 83. satırda ROS kapatılana node'u devam ettirmek için rospy.spin() kullanıyoruz.

![image](https://user-images.githubusercontent.com/46991761/86353853-a2170c80-bc70-11ea-9881-2daeb99704a5.png)


**3.7.9-** Son olarak 89. satırda class ve fonksiyonlarla tanımladığımız tüm işlemleri çağırıyoruz.

![image](https://user-images.githubusercontent.com/46991761/86353970-db4f7c80-bc70-11ea-80d9-13e0485e1a87.png)



# 4- Tüm İşlemleri Başlatma

**4.1-** Öncelikle terminalinizde "roslaunch mybot_gazebo mybot_world.launch" komutunu çalıştırın.

**4.2-** Açılan Gazebo penceresinde Insert'e gidip kutu içerisinde gösterilmiş Gazebonun model kütüphanesinden Standing Person ve Walking Person modellerini mybot'un kamerasının önüne koyun. (Komutu ilk defa çalıştırdığınızda Gazebo internetten modelleri indireceği için açılma biraz uzun sürebilir.)

![image](https://user-images.githubusercontent.com/46991761/86355589-9547e800-bc73-11ea-958e-c8f09377ac7f.png)


**4.3-** Farklı bir terminalde "roslaunch mybot_description mybot_rviz.launch" komutunu çalıştırın. 

**4.4-** 4.2 sayılı adımın sonucunda açılan rviz penceresinde rviz ortamına robotumuzu ve kameramızı eklemeliyiz. Açılan pencerede öncelikle kutu içerisindeki Fixed Frame kısmında map'e tıklayıp odom ile değiştirin. Sonra Add'e tıklayıp açılan pencereden Camera ve RobotModel'i bulup ekleyin.


![image](https://user-images.githubusercontent.com/46991761/86355929-1901d480-bc74-11ea-9be7-882d8963500d.png)

**4.5-** Camera ve RobotModel'i ekledikten sonra soldaki menüde beliren Camera'ya tıklayıp Image Topic kısmına "/mybot/camera1/image_raw" yazın. Yazdıktan sonra sol altta robotun kamerasından Gazebo ortamındaki görüntü belirecektir.

![image](https://user-images.githubusercontent.com/46991761/86356443-eefce200-bc74-11ea-8171-03c9bdf28b65.png)

**4.6-** Son olarak yeni bir terminalde "rosrun ros_cv ros_predict.py" komutunu çalıştırın. Bir kaç saniye sonra çıktı ekrana gelecektir.

**4.7-** Örnek mask çıktısı aşağıda görülmekte.

![image](https://user-images.githubusercontent.com/46991761/86357517-9890a300-bc76-11ea-9719-aba60e1371fe.png)


# 5- Son Olarak...

Elimden geldiğince açık bir şekilde anlatmaya çalıştım. Eğer sorun yaşadığnız veya anlamadığınız, mantıksız bulduğunuz bir yer olursa bir **issue** açın.

**Mail:** unutkan2013@yandex.com
**LinkedIn:** https://www.linkedin.com/in/mertcan-kar%C4%B1k-b37429189/
















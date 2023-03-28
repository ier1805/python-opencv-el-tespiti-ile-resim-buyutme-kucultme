import cv2 as cv #cv2 kütüphanesini içe aktarma
from cvzone.HandTrackingModule import HandDetector #pip install cvzone - HandDetector- el tespit kütüphanesini içe aktarma
import mediapipe as mp #pip insstall mediapipe
import math
"""
Mediapipe kütüphanesi kullanarak ellere bulur. 
Yer işaretlerini pikseller halinde dışarıya aktarır.
Kaç parmağın dışarda veya içerde olduğunu veya iki parmak arasındaki mesafeyi bulma gibi ekstra işlevler yapar.
Ayrıca bulunan elin sınırlayıcı kutu bilgilerini gösterir.
""" 
kamera = cv.VideoCapture(0) # Kamera görüntüsü
kamera.set(3,1280) # Kamera genişlik ayarı
kamera.set(4,720)  # Kamera yükseklik ayarı  # Kamera parlaklık ayarı 

tespit = HandDetector(detectionCon=0.8,maxHands=2) # Algılanacak eşik değeri, maksimum kullanılacak el sayısı

baslangicMesafe= None
deger = 0
xmerkez, ymerkez = 600,600
derece = 0

while True:
    ret, cerceve = kamera.read() # read() bir boolean (True/False) - Eğer çerçeve bize doğru çıktı verirse görüntü devam eder. 
    elGoruntusu, cerceve = tespit.findHands(cerceve) # BGR görüntüsünde elleri bulur.
    #elGoruntusu = tespit.findHands(cerceve,draw=False) # El görüntüsündeki çizgiler istenmiyorsa draw = False
     #image read - resim okuma 
    resim = cv.imread("atauni.jpg")
    if len(elGoruntusu)==2: 
       
       #print(tespit.fingersUp(elGoruntusu[0]),tespit.fingersUp(elGoruntusu[1]))
       
        if (tespit.fingersUp(elGoruntusu[0])==[1,1,0,0,0] and tespit.fingersUp(elGoruntusu[1])==[1,1,0,0,0]):
           birinciEl = elGoruntusu[0]
           lmList1 = birinciEl['lmList']
           ikinciEl = elGoruntusu[1]
           lmList2 = ikinciEl['lmList']
           p1Koordinatı = lmList1[8][0:2]
           p2Koordinatı = lmList2[8][0:2]
           p3Koordinatı = lmList2[8][0:2]
           #print(birinciEl)
           #print(ikinciEl)
           #print(p1Koordinatı)
           #print(p2Koordinatı)
           #uzunluk, bilgi, cerceve= tespit.findDistance(p1Koordinatı,p2Koordinatı,cerceve)
           #print(uzunluk)
           #print(bilgi)
           #print(cerceve)
           x1, y1 = p1Koordinatı
           x2, y2 = p2Koordinatı
           x3, y3 = p2Koordinatı
           derece = int(math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1-y2,x1-x2))) 
           if derece<0:
                derece +=360    
          
           
           if baslangicMesafe is None:
                uzunluk, bilgi, cerceve= tespit.findDistance(p1Koordinatı,p2Koordinatı,cerceve) # iki konum arasındaki mesafeyi bulma
                uzunluk, bilgi, cerceve= tespit.findDistance(birinciEl["center"],ikinciEl["center"],cerceve) # iki merkez arasındaki mesafeyi bulma    
                
                
                baslangicMesafe = uzunluk
           uzunluk, bilgi, cerceve= tespit.findDistance(p1Koordinatı,p2Koordinatı,cerceve)  
           uzunluk, bilgi, cerceve= tespit.findDistance(birinciEl["center"],ikinciEl["center"],cerceve)    
           deger = int((uzunluk-baslangicMesafe)//2)
           xmerkez,ymerkez = bilgi[4:]
           #print(deger)
           
        elif (tespit.fingersUp(elGoruntusu[0])==[0,0,0,0,0] and tespit.fingersUp(elGoruntusu[1])==[0,0,0,0,0]):
            deger = 0
            #xmerkez = 300
            #ymerkez = 300
            derece = 360
        else:
            baslangicMesafe = None   
            
    try:
        yukseklik1, genislik1, _= resim.shape       
        yeniYukseklik, yeniGenislik = ((yukseklik1+deger)//2)*2, ((genislik1+deger)//2)*2
        resim1 = cv.resize(resim,(yeniYukseklik,yeniGenislik))
        m = cv.getRotationMatrix2D((yeniYukseklik//2, yeniGenislik//2),derece,1)
        d = cv.warpAffine(resim1,m,(yeniYukseklik,yeniGenislik),cv.INTER_LINEAR,borderMode=cv.BORDER_CONSTANT,borderValue=(255,255,255))
           #print("lm1:",p1)
           #print("lm2:",p2)
        cerceve[ymerkez-yeniYukseklik//2:ymerkez+yeniYukseklik//2,xmerkez-yeniGenislik//2:xmerkez+yeniGenislik//2] = d
        #cerceve[ymerkez-yeniYukseklik//2:ymerkez+yeniYukseklik//2,xmerkez-yeniGenislik//2:xmerkez+yeniGenislik//2]= resim1 
    except:
        pass
          
    

    cv.imshow("Goruntu",cerceve)
    if cv.waitKey(1) & 0XFF == ord("q"):
     break
cv.destroyAllWindows()

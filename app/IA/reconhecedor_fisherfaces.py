import cv2

def reconhecedorFisherFaces(lista):
    detectorFace = cv2.CascadeClassifier("app/IA/haarcascade_frontalface_default.xml")
    reconhecedor = cv2.face.FisherFaceRecognizer_create()
    reconhecedor.read("app/IA/classificadorFisher.yml")
    largura, altura = 220, 220
    font = cv2.FONT_HERSHEY_COMPLEX_SMALL
    camera = cv2.VideoCapture(0)           

    while (True):
        conectado, imagem = camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imagemCinza,
                                                        scaleFactor=1.5,
                                                        minSize=(30,30))
        for (x, y, l, a) in facesDetectadas:
            imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,0,255), 2)
            id, confianca = reconhecedor.predict(imagemFace)
            nome = ""
            for released in lista:
                if id == released.id:
                    nome = released.name

                    #liberacao()
                    print("ACESSO LIBERADO!")
                    break
            
            cv2.putText(imagem, nome, (x,y +(a+30)), font, 2, (0,0,255))
            cv2.putText(imagem, str(confianca), (x,y + (a+50)), font, 1, (0,0,255))

        cv2.imshow("Face", imagem)
        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()
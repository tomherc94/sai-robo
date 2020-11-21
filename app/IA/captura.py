import cv2
import numpy as np

def captura(released_id):

    classificador = cv2.CascadeClassifier("app/IA/haarcascade_frontalface_default.xml")
    classificadorOlho = cv2.CascadeClassifier("app/IA/haarcascade_eye.xml")


    camera = cv2.VideoCapture(0)
    amostra = 1
    numeroAmostras = 25
    id = released_id
    largura, altura = 220, 220 #tamanho da imagem em pixels
    print("Capturando as faces ...")

    status = "ok"
    execucao = True
    while(execucao):
        conectado, imagem  = camera.read()
        imagemCinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
        #print(np.average(imagemCinza))
        facesDetectadas = classificador.detectMultiScale(imagemCinza,scaleFactor=1.5,minSize=(100,100))

        for(x, y, l, a) in facesDetectadas:
            cv2.rectangle(imagem, (x,y), (x+l, y+a), (0,0,255), 2)
            regiao = imagem[y:y + a, x:x + l]
            regiaoCinzaOlho = cv2.cvtColor(regiao, cv2.COLOR_BGR2GRAY)
            olhosDetectados = classificadorOlho.detectMultiScale(regiaoCinzaOlho)
            for(ox, oy, ol, oa) in olhosDetectados:
                cv2.rectangle(regiao, (ox, oy), (ox + ol, oy + oa), (0, 255, 0), 2)

                if cv2.waitKey(1) & 0xFF ==ord('q'):
                    #if np.average(imagemCinza) > 110:
                    imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
                    cv2.imwrite("app/IA/fotos/pessoa." + str(id) + "." + str(amostra) + ".jpg", imagemFace)
                    print("[foto " + str(amostra) + " capturada com sucesso]")
                    amostra += 1
            if cv2.waitKey(1) & 0xFF ==ord('e'):
                execucao = False
                status = "fail"
                break

        #imS = cv2.resize(imagem, (700, 600)) 
        cv2.imshow("Face", imagem)
        cv2.waitKey(1) 
        if (amostra >= numeroAmostras + 1):
            break

    print("Faces capturadas com sucesso!")

        

    camera.release()
    cv2.destroyAllWindows()

    return status


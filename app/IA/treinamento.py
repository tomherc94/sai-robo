from posixpath import abspath
import cv2
import os
import numpy as np

def treinamento():

    #eigenface = cv2.face.EigenFaceRecognizer_create()
    fisherface = cv2.face.FisherFaceRecognizer_create()
    lbph = cv2.face.LBPHFaceRecognizer_create()
    qtd_release = 0
    def getImagemComId():
        caminhos = [os.path.join('app/IA/fotos', f) for f in os.listdir('app/IA/fotos/')]     
        caminhos.sort()
        caminhos.pop(0)
        print(caminhos)
        faces = []
        ids = []
        for caminhoImagem in caminhos:
            if caminhoImagem != None:
                img = cv2.imread(caminhoImagem,0)
                print(caminhoImagem)
                #imagemFace = cv2.cvtColor(img)
                #id = int(os.path.split(caminhoImagem)[-1].split('.')[1])
                id = int(caminhoImagem.split('.')[-3])
                #print(id)
                ids.append(id)
                faces.append(img)
                #cv2.imshow("Face", imagemFace)
                #cv2.waitKey(10)
        
        
        return np.array(ids), faces
    
    ids, faces = getImagemComId()
    qtd_release = len(ids)
    print("QTD_RELEASE="+str(qtd_release))
    if qtd_release >= 50:
        print("Treinando...")
        #eigenface.train(faces, ids)
        #eigenface.write('app/IA/classificadorEigen.yml')

        fisherface.train(faces, ids)
        fisherface.write('app/IA/classificadorFisher.yml')

        lbph.train(faces, ids)
        lbph.write('app/IA/classificadorLBPH.yml')

        print("Treinamento realizado com sucesso!")
    else:
        print("Pasta fotos vazia!")
import cv2
import os
import numpy as np

def treinamento():

    eigenface = cv2.face.EigenFaceRecognizer_create()
    fisherface = cv2.face.FisherFaceRecognizer_create()
    lbph = cv2.face.LBPHFaceRecognizer_create()

    def getImagemComId():
        caminhos = [os.path.join('app/IA/fotos', f) for f in os.listdir('app/IA/fotos')]
        #print(caminhos)
        faces = []
        ids = []
        for caminhoImagem in caminhos:
            imagemFace = cv2.cvtColor(cv2.imread(caminhoImagem), cv2.COLOR_BGR2GRAY)
            id = int(os.path.split(caminhoImagem)[-1].split('.')[1])
            #print(id)
            ids.append(id)
            faces.append(imagemFace)
            #cv2.imshow("Face", imagemFace)
            #cv2.waitKey(10)
        return np.array(ids), faces

    ids, faces = getImagemComId()

    if len(ids) >= 2:
        print("Treinando...")
        eigenface.train(faces, ids)
        eigenface.write('app/IA/classificadorEigen.yml')

        fisherface.train(faces, ids)
        fisherface.write('app/IA/classificadorFisher.yml')

        lbph.train(faces, ids)
        lbph.write('app/IA/classificadorLBPH.yml')

        print("Treinamento realizado com sucesso!")
    else:
        print("Pasta fotos vazia!")
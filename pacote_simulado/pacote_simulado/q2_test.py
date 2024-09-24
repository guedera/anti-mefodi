import cv2
from math import *
import numpy as np

# Carregar a imagem
imagem_crua = cv2.imread('pacote_simulado/pacote_simulado/imagens/exemplo5.png')
imagem = imagem_crua.copy()
cv2.imshow('imagem crua', imagem)
cv2.waitKey()
cv2.destroyAllWindows()

# Converter a imagem para HSV
img_hsv = cv2.cvtColor(imagem, cv2.COLOR_BGR2HSV)

# Definir os limites da máscara (intervalo de cores em HSV)
menor = (13, 62, 181)
maior = (19, 116, 241)
mask = cv2.inRange(img_hsv, menor, maior)

# Aplicar operações morfológicas para limpar a máscara
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

# Encontrar os contornos
contornos, _ = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

# Ordenar os contornos por área e pegar o maior (ou o primeiro de interesse)
contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
contorno_deinteresse = contornos[0]  # Selecionar o maior contorno

# Desenhar o contorno de interesse na imagem original
cv2.drawContours(imagem, [contorno_deinteresse], -1, [255, 0, 0], 2)
cv2.imshow('imagem tab', imagem)
cv2.waitKey()
cv2.destroyAllWindows()

# Obter as coordenadas do retângulo delimitador
x, y, w, h = cv2.boundingRect(contorno_deinteresse)

# Canto superior esquerdo
top_left = (x, y)

# Canto inferior direito
bottom_right = (x + w, y + h)

# Criar uma máscara preta do mesmo tamanho da imagem original
mask_preta = np.zeros_like(imagem)

# Desenhar um retângulo branco (parte que será mantida) na região do tabuleiro
cv2.rectangle(mask_preta, top_left, bottom_right, (255, 255, 255), -1)

# Aplicar a máscara invertida (manter o tabuleiro e pintar de preto o restante)
imagem_mascarada = cv2.bitwise_and(imagem, mask_preta)

# Mostrar o resultado final
cv2.imshow('imagem mascarada', imagem_mascarada)
cv2.waitKey()
cv2.destroyAllWindows()

# Imprimir coordenadas dos cantos
print(f"Canto superior esquerdo: {top_left}")
print(f"Canto inferior direito: {bottom_right}")

tamanho_tabuleiro = int(bottom_right[0])-int(top_left[0])-2

xi = int(top_left[0])
yi = int(top_left[1])

print(xi)
print(yi)

passo_casa = (tamanho_tabuleiro // 8)

linha = []
tabela = []
preto = 0

# Definir os limites de cores para azul, amarelo e vermelho
# Azul: mais no canal B (Blue) e menos nos outros
limite_baixo_azul = np.array([220, 140, 0])
limite_alto_azul = np.array([255, 200, 10])

# Amarelo: mais no canal R e G, e menos no canal B
limite_baixo_amarelo = np.array([0, 190, 200])
limite_alto_amarelo = np.array([20, 230, 255])

# Vermelho: mais no canal R (Red) e menos nos outros
limite_baixo_vermelho = np.array([0, 0, 240])
limite_alto_vermelho = np.array([10, 15, 255])

for i in range(8):
    linha = []
    for j in range(8):
        roi = imagem_crua[yi+(i)*passo_casa:(yi+(i+1)*passo_casa),(xi+(j)*passo_casa):(xi+(j+1)*passo_casa)]
        roi_gray = cv2.cvtColor(roi,cv2.COLOR_BGR2GRAY)
        total_pixels = roi_gray.size
        pixels_pretos = np.count_nonzero(roi_gray == preto)
        percentual_pretos = (pixels_pretos/total_pixels)*100
        if percentual_pretos > 0:
            mascara_azul = cv2.inRange(roi, limite_baixo_azul, limite_alto_azul)
            mascara_amarelo = cv2.inRange(roi, limite_baixo_amarelo, limite_alto_amarelo)
            mascara_vermelho = cv2.inRange(roi, limite_baixo_vermelho, limite_alto_vermelho)
            if percentual_pretos > 10:
                if np.any(mascara_azul):
                    if np.any(mascara_amarelo):
                        print('bispo P')
                        linha.append('BB')
                        
                    elif np.any(mascara_vermelho):
                        print('cavalo P')
                        linha.append('BC')
                    else:
                        print('dama P')
                        linha.append('BQ')
                elif np.any(mascara_amarelo):
                    print('torre P')
                    linha.append('BT')
                elif np.any(mascara_vermelho):
                    print('rei P')
                    linha.append('BK')
                else:
                    print('peao P')
                    linha.append('BP')
            if np.any(pixels_pretos) and percentual_pretos < 10:
                if np.any(mascara_azul):
                    if np.any(mascara_amarelo):
                        print('bispo B')
                        linha.append('WB')
                    elif np.any(mascara_vermelho):
                        print('cavalo B')
                        linha.append('WC')
                    else:
                        print('dama B')
                        linha.append('WQ')
                elif np.any(mascara_amarelo):
                    print('torre B')
                    linha.append('WT')
                elif np.any(mascara_vermelho):
                    print('rei B')
                    linha.append('WK')
                else:
                    print('peao B')
                    linha.append('WP')
            cv2.imshow('imagem mascarada', roi)
            cv2.waitKey()
            cv2.destroyAllWindows()
        else:
            print('vazio')
            linha.append('__')
    tabela.append(linha)

for i in range(8):
    print(tabela[i])
import cv2
from math import *
import numpy as np

class ImageNode:

    def __init__(self, image_path):
        # Carregar a imagem
        self.imagem_crua = cv2.imread(image_path)
        self.imagem = self.imagem_crua.copy()
        self.top_left = None
        self.bottom_right = None
        self.tabela = []

    def show_raw_image(self):
        cv2.imshow('imagem crua', self.imagem)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def process_image(self):
        # Converter a imagem para HSV
        img_hsv = cv2.cvtColor(self.imagem, cv2.COLOR_BGR2HSV)

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
        contornos = sorted(contornos, key=cv2.contourArea, reverse=True)
        contorno_deinteresse = contornos[0]  # Selecionar o maior contorno

        # Desenhar o contorno de interesse na imagem original
        cv2.drawContours(self.imagem, [contorno_deinteresse], -1, [255, 0, 0], 2)
        cv2.imshow('imagem tab', self.imagem)
        cv2.waitKey()
        cv2.destroyAllWindows()

        # Obter as coordenadas do retângulo delimitador
        x, y, w, h = cv2.boundingRect(contorno_deinteresse)

        # Canto superior esquerdo
        self.top_left = (x, y)

        # Canto inferior direito
        self.bottom_right = (x + w, y + h)

    def mask_board(self):
        # Criar uma máscara preta do mesmo tamanho da imagem original
        mask_preta = np.zeros_like(self.imagem)

        # Desenhar um retângulo branco (parte que será mantida) na região do tabuleiro
        cv2.rectangle(mask_preta, self.top_left, self.bottom_right, (255, 255, 255), -1)

        # Aplicar a máscara invertida (manter o tabuleiro e pintar de preto o restante)
        imagem_mascarada = cv2.bitwise_and(self.imagem, mask_preta)

        # Mostrar o resultado final
        cv2.imshow('imagem mascarada', imagem_mascarada)
        cv2.waitKey()
        cv2.destroyAllWindows()

    def detect_pieces(self):
        # Definir os limites de cores para azul, amarelo e vermelho
        limite_baixo_azul = np.array([220, 140, 0])
        limite_alto_azul = np.array([255, 200, 10])
        limite_baixo_amarelo = np.array([0, 190, 200])
        limite_alto_amarelo = np.array([20, 230, 255])
        limite_baixo_vermelho = np.array([0, 0, 240])
        limite_alto_vermelho = np.array([10, 15, 255])

        xi = int(self.top_left[0])
        yi = int(self.top_left[1])

        tamanho_tabuleiro = int(self.bottom_right[0]) - int(self.top_left[0])-2
        passo_casa = tamanho_tabuleiro // 8
        preto = 0

        for i in range(8):
            linha = []
            for j in range(8):
                roi = self.imagem_crua[yi+(i)*passo_casa:(yi+(i+1)*passo_casa), (xi+(j)*passo_casa):(xi+(j+1)*passo_casa)]
                roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                total_pixels = roi_gray.size
                pixels_pretos = np.count_nonzero(roi_gray == preto)
                percentual_pretos = (pixels_pretos / total_pixels) * 100

                if percentual_pretos > 0:
                    mascara_azul = cv2.inRange(roi, limite_baixo_azul, limite_alto_azul)
                    mascara_amarelo = cv2.inRange(roi, limite_baixo_amarelo, limite_alto_amarelo)
                    mascara_vermelho = cv2.inRange(roi, limite_baixo_vermelho, limite_alto_vermelho)
                    if percentual_pretos > 10:
                        if np.any(mascara_azul):
                            if np.any(mascara_amarelo):
                                linha.append('BB')  # Bispo Preto
                            elif np.any(mascara_vermelho):
                                linha.append('BC')  # Cavalo Preto
                            else:
                                linha.append('BQ')  # Dama Preta
                        elif np.any(mascara_amarelo):
                            linha.append('BT')  # Torre Preta
                        elif np.any(mascara_vermelho):
                            linha.append('BK')  # Rei Preto
                        else:
                            linha.append('BP')  # Peão Preto
                    elif percentual_pretos < 10:
                        if np.any(mascara_azul):
                            if np.any(mascara_amarelo):
                                linha.append('WB')  # Bispo Branco
                            elif np.any(mascara_vermelho):
                                linha.append('WC')  # Cavalo Branco
                            else:
                                linha.append('WQ')  # Dama Branca
                        elif np.any(mascara_amarelo):
                            linha.append('WT')  # Torre Branca
                        elif np.any(mascara_vermelho):
                            linha.append('WK')  # Rei Branco
                        else:
                            linha.append('WP')  # Peão Branco
                else:
                    linha.append('__')  # Vazio
            self.tabela.append(linha)

    def print_board(self):
        for linha in self.tabela:
            print(linha)


def main(args=None):
    image_node = ImageNode('pacote_simulado/pacote_simulado/imagens/exemplo1.png')
    image_node.show_raw_image()
    image_node.process_image()
    image_node.mask_board()
    image_node.detect_pieces()
    image_node.print_board()


if __name__ == '__main__':
    main()

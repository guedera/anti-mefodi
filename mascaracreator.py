import cv2
import numpy as np

def calcular_mascara_hsv(rgb):
    # Converter RGB para BGR (OpenCV utiliza BGR)
    bgr_cor = np.uint8([[rgb[::-1]]])  # Inverte RGB para BGR

    # Converter BGR para HSV
    hsv_cor = cv2.cvtColor(bgr_cor, cv2.COLOR_BGR2HSV)
    h, s, v = hsv_cor[0][0]
    print(f"HSV da cor de entrada: H={h}, S={s}, V={v}")

    # Definir limites para H
    margem_h = 10
    lower_h = max(0, h - margem_h)
    upper_h = min(179, h + margem_h)

    # Definir limites fixos para S e V
    lower_s = 50
    upper_s = 230

    lower_v = 150
    upper_v = 255

    mascara_inferior = np.array([lower_h, lower_s, lower_v], dtype=np.uint8)
    mascara_superior = np.array([upper_h, upper_s, upper_v], dtype=np.uint8)

    print("Máscara HSV inferior:", mascara_inferior)
    print("Máscara HSV superior:", mascara_superior)

# Exemplo com a entrada fornecida
rgb_cor = (200, 205, 105)
calcular_mascara_hsv(rgb_cor)

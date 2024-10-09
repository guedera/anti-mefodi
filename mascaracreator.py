import cv2
import numpy as np

def calcular_mascara_hsv(rgb):
    # Converter RGB para BGR (OpenCV utiliza BGR)
    bgr_cor = np.uint8([[rgb[::-1]]])  # Inverte RGB para BGR

    # Converter BGR para HSV
    hsv_cor = cv2.cvtColor(bgr_cor, cv2.COLOR_BGR2HSV)
    h, s, v = hsv_cor[0][0]
    print(f"HSV da cor de entrada: H={h}, S={s}, V={v}")

    # Definir margens para H
    margem_h = 10
    lower_h = max(0, h - margem_h)
    upper_h = min(179, h + margem_h)

    # Calcular margens dinâmicas para S e V (porcentagem do valor original)
    percentual_margem_s = 0.4  # Você pode ajustar esse valor conforme necessário
    percentual_margem_v = 0.4  # Você pode ajustar esse valor conforme necessário

    margem_s = s * percentual_margem_s
    margem_v = v * percentual_margem_v

    # Calcular limites inferior e superior para S
    lower_s = max(0, s - margem_s)
    upper_s = min(255, s + margem_s)

    # Calcular limites inferior e superior para V
    lower_v = max(0, v - margem_v)
    upper_v = min(255, v + margem_v)

    # Converter valores para inteiros
    lower_s = int(lower_s)
    upper_s = int(upper_s)
    lower_v = int(lower_v)
    upper_v = int(upper_v)

    mascara_inferior = np.array([lower_h, lower_s, lower_v], dtype=np.uint8)
    mascara_superior = np.array([upper_h, upper_s, upper_v], dtype=np.uint8)

    print("Máscara HSV inferior:", mascara_inferior)
    print("Máscara HSV superior:", mascara_superior)

# Exemplo com a entrada fornecida
rgb_cor = (200, 205, 105)
calcular_mascara_hsv(rgb_cor)

import cv2
import numpy as np

def calcular_mascara_hsv(rgb):
    bgr_cor = np.uint8([[rgb[::-1]]])

    hsv_cor = cv2.cvtColor(bgr_cor, cv2.COLOR_BGR2HSV)
    h, s, v = hsv_cor[0][0]
    print(f"HSV da cor de entrada: H={h}, S={s}, V={v}")

    margem_h = 10
    lower_h = max(0, h - margem_h)
    upper_h = min(179, h + margem_h)

    percentual_margem_s = 0.4
    percentual_margem_v = 0.4

    margem_s = s * percentual_margem_s
    margem_v = v * percentual_margem_v

    
    lower_s = max(0, s - margem_s)
    upper_s = min(255, s + margem_s)

    
    lower_v = max(0, v - margem_v)
    upper_v = min(255, v + margem_v)

    
    lower_s = int(lower_s)
    upper_s = int(upper_s)
    lower_v = int(lower_v)
    upper_v = int(upper_v)

    mascara_inferior = np.array([lower_h, lower_s, lower_v], dtype=np.uint8)
    mascara_superior = np.array([upper_h, upper_s, upper_v], dtype=np.uint8)

    print("Máscara HSV inferior:", mascara_inferior)
    print("Máscara HSV superior:", mascara_superior)


rgb_cor = (250, 100, 1) #mudar valor pra cor que vc quer achar a mask
calcular_mascara_hsv(rgb_cor)
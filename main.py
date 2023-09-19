import sys
import timeit
import cv2
import numpy as np

####################################################

INPUT_IMAGE =  'GT2.bmp'
QTD_GAUSSIAN = 5
IS_GAUSSIAN = False #Usar como true para fazer o blurr gaussiano e false para box_blurr (imitando gaussian blurr)

#################################################################
def box_blurr_gaussian(img, janela):
    for x in range (QTD_GAUSSIAN):
        img = cv2.blur(img, (janela, janela))
    return img


def main():
    imagem = cv2.imread(INPUT_IMAGE)

    # Converter para HSL
    imagem_hsl = cv2.cvtColor(imagem, cv2.COLOR_BGR2HLS)

    # Extrair o canal de luminosidade (L)
    canal_luminosidade = imagem_hsl[:, :, 1]

    # Definir o limiar para identificar os valores mais "escuros"
    limiar_escuro = 129  # Ajuste esse valor conforme necessário

    # Criar uma máscara binária com base no limiar
    mascara_escuro = canal_luminosidade < limiar_escuro

    # Substituir os pixels correspondentes na imagem original por preto
    imagem_resultado = imagem.copy()
    imagem_resultado[mascara_escuro] = [0, 0, 0]  # Pixels pretos (0, 0, 0)

    if IS_GAUSSIAN:
        imagem_borrada1 = cv2.GaussianBlur(imagem_resultado, (0, 0), 5)
        imagem_borrada2 = cv2.GaussianBlur(imagem_resultado, (0, 0), 15)
        imagem_borrada3 = cv2.GaussianBlur(imagem_resultado, (0, 0), 45)
        imagem_borrada4 = cv2.GaussianBlur(imagem_resultado, (0, 0), 75)
    else:
        imagem_borrada1 = box_blurr_gaussian(imagem_resultado, 6)
        imagem_borrada2 = box_blurr_gaussian(imagem_resultado, 16)
        imagem_borrada3 = box_blurr_gaussian(imagem_resultado, 45)
        imagem_borrada4 = box_blurr_gaussian(imagem_resultado, 75)

    imagem_borrada_total = imagem_borrada1.astype(np.uint16) + imagem_borrada2.astype(np.uint16) + imagem_borrada3.astype(np.uint16) + imagem_borrada4.astype(np.uint16)

    # Limitar os valores máximos a 255
    imagem_borrada_total[imagem_borrada_total > 255] = 255

    # Converter de volta para uint8 (8 bits por canal) para exibir a imagem
    imagem_borrada_total = imagem_borrada_total.astype(np.uint8)

    imagem_com_bloom = (imagem_borrada_total.astype(np.uint16) * 0.5) + (imagem.astype(np.uint16) * 0.75)

    imagem_com_bloom[imagem_com_bloom > 255] = 255

    imagem_com_bloom = imagem_com_bloom.astype(np.uint8)

    # Exibir a imagem resultante
    cv2.imshow('Imagem Com Bloom', imagem_com_bloom)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    cv2.imwrite('03 - imagem_com_bloom.png', imagem_com_bloom)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
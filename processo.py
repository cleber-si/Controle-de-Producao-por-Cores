import cv2 as cv
import matplotlib.pyplot as plt
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasAgg
import io

def cria_canais_modelo(imagem):
    img0 = cv.imread(imagem)
    img = cv.cvtColor(img0, cv.COLOR_RGB2BGR)

    fig , ax = plt.subplots(2, 2, figsize = (3.1, 3.1))

    verm = img.copy()
    # verm = cv.bitwise_not(verm)
    verm[:, :, 2] = 0
    verm[:, :, 1] = 0

    verde = img.copy()
    verde[:, :, 0] = 0
    verde[:, :, 2] = 0

    azul = img.copy()
    azul[:, :, 1] = 0
    azul[:, :, 0] = 0

    tupla = [(0, 0, 'Padrão', img),
            (0, 1, 'Vermelho', verm),
            (1, 0, 'Verde', verde),
            (1, 1, 'Azul', azul)]

    for i, j, cor, pic in tupla:
        ax[i][j].imshow(pic)
        ax[i][j].axis('off')
        ax[i][j].set_title(cor, fontsize=8)

    return fig

def cria_canais_cam(frame, cor='Padrão'):
    if cor == 'Padrão':
        imgbytes = cv.imencode('.png', frame)[1].tobytes()

    elif cor == 'vermelho':
        verm = frame.copy()
        verm[:, :, 0] = 0
        verm[:, :, 1] = 0
        imgbytes = cv.imencode('.png', verm)[1].tobytes()
    
    elif cor == 'verde':
        verde = frame.copy()
        verde[:, :, 0] = 0
        verde[:, :, 2] = 0
        imgbytes = cv.imencode('.png', verde)[1].tobytes()

    elif cor == 'azul':
        azul = frame.copy()
        azul[:, :, 1] = 0
        azul[:, :, 2] = 0
        imgbytes = cv.imencode('.png', azul)[1].tobytes()

    else:
        raise Exception("Cor inválida.")

    return imgbytes

def imprime_figs(elemento, figura):
    plt.close('all')
    canv = FigureCanvasAgg(figura)
    buf = io.BytesIO()
    canv.print_figure(buf, format = 'png')
    if buf is not None:
        buf.seek(0)
        elemento.update(data=buf.read())
        return canv
    else:
        return None

# Função para printar e salvar os resultados do processo ao mesmo tempo
# O arquivo deve ser aberto e fechado fora dela
def printa_exibe(arq, *argumentos):
    printar = ' '.join([str(argumento) for argumento in argumentos])
    print(printar)
    arq.write(printar + '\n')

def processamento(imagem_pad, imagem_prod, ncapturas, dpadrao, fpadrao, conf, arq, scan=False):
    # OBTENDO AS IMAGENS

    img0 = cv.imread(imagem_pad)
    img = cv.cvtColor(img0, cv.COLOR_BGR2RGB)

    """ 
    Como o OpenCV já carrega a imagem da webcam no formato em que ele trabalha,
    se a imagem vier da câmera então não precisa ler um arquivo com o cv.imread().
    """
    if not scan:
        img20 = cv.imread(imagem_prod)
        img2 = cv.cvtColor(img20, cv.COLOR_BGR2RGB)
    else:
        img20 = imagem_prod
        img2 = imagem_prod

    #INICIALIZA ARGUMENTOS  PARA CALCULAR OS HISTOGRAMAS
    h_bins = 50
    s_bins = 60
    histSize = [h_bins, s_bins]
    h_ranges = [0, 180]
    s_ranges = [0, 256]
    ranges = h_ranges + s_ranges
    channels = [1 ,2]

    # Cria histograma para a imagem modelo
    hist_base = cv.calcHist([img], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

    # Cria histograma para a imagem alvo
    hist_test1 = cv.calcHist([img2], channels, None, histSize, ranges, accumulate=False)
    cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)

    # TESTE DE SEMELHANÇA
    # Recebe a semelhança entre os histogramas das imagens
    semelhanca = cv.compareHist(hist_base, hist_test1, 0)

    # Avalia se a semelhança é menor ou maior/igual que o nível de confiança exigido
    if semelhanca*100 < conf :
        printa_exibe(arq, '-'*50)
        printa_exibe (arq, 'FORA DO PADRÃO', " POIS A SEMELHANÇA  É DE APENAS:",
                round(semelhanca*100, 2),"%")
        fpadrao += 1
        printa_exibe(arq, 'percentual de erros:', round((fpadrao/ncapturas)*100, 2), "%")  
        ncapturas += 1
    else:
        # INCREMENTA CONTADOR DE DENTRO DO PADRÃO
        dpadrao += +1

        # COMPARA CADA CANAL
        # Canal Azul
        channels = [0,0]
        hist_base3 = cv.calcHist([img0], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        hist_test4 = cv.calcHist([img20], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        canal_azul = cv.compareHist(hist_base3, hist_test4, 0)

        # Canal Verde
        channels = [1,1]
        hist_base3 = cv.calcHist([img0], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        hist_test4 = cv.calcHist([img20], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        canal_verde = cv.compareHist(hist_base3, hist_test4, 0)

        # Canal Vermelho
        channels = [2,2]
        hist_base3 = cv.calcHist([img0], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hist_base, hist_base, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        hist_test4 = cv.calcHist([img20], channels, None, histSize, ranges, accumulate=False)
        cv.normalize(hist_test1, hist_test1, alpha=0, beta=1, norm_type=cv.NORM_MINMAX)
        canal_vermelho = cv.compareHist(hist_base3, hist_test4, 0)

        # Informa a semelhança da imagem atual
        print('-'*50, file=arq)
        printa_exibe(arq, 'Semelhança com o modelo:', round(semelhanca*100, 2))
        
        # Checa se a a comparação do histograma do canal azul é maior que a confiança
        if canal_azul > conf/100:
            printa_exibe(arq, "TONALIDADE AZUL DENTRO DO PADRÃO")
        else: 
            printa_exibe(arq, "TONALIDADE AZUL FORA DO PADRÃO",)

        # Checa se a a comparação do histograma do canal azul é maior que a confiança
        if canal_verde > conf/100:
            printa_exibe(arq, "TONALIDADE VERDE DENTRO DO PADRÃO")
        else: 
            printa_exibe(arq, "TONALIDADE VERDE FORA DO PADRÃO")

        # Checa se a a comparação do histograma do canal azul é maior que a confiança
        if canal_vermelho > conf/100:
            printa_exibe(arq, "TONALIDADE VERMELHA DENTRO DO PADRÃO")
        else: 
            printa_exibe(arq, "TONALIDADE VERMELHA FORA DO PADRÃO")

        resposta = [round(canal_azul, 2), round(canal_verde, 2), round(canal_vermelho, 2)]
        printa_exibe(arq, resposta)
            
        ncapturas += 1

    #INDICADORES DE PERFORMANCE
    printa_exibe(arq, "Nº de amostras dentro do padrão: ", dpadrao,)
    printa_exibe(arq, "Nº de amostras fora do padrão: ", fpadrao)
    printa_exibe(arq, "Produtos Conformes:", round((dpadrao/(dpadrao+fpadrao))*100, 2),
                    "%", '\n')

    return ncapturas, dpadrao, fpadrao
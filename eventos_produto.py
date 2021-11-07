# Código para as funcionalidades relativas ao produto alvo

import PySimpleGUI as sg
import contorno
import processo
import cv2 as cv
import numpy as np


def caixa_prod(janela, valores, camera_Altura, ncapturas, dpadrao, fpadrao):
    # Garante que a camera esteja desligada
    grav_prod = False
    # Recebe o local do arquivo selecionado
    arq_prod = valores['caixa_prod']
    try:
        # Levanta um alerta caso não haja uma imagem modelo definida
        if len(valores['caixa_mod']) == 0:
            sg.popup('Defina uma imagem modelo primeiro.', title='Aviso')
            pass
        
        else:
            img0 = cv.imread(arq_prod)

            # Altera a escala da impressão da imagem selecionada
            escala_porcent = camera_Altura/img0.shape[0]
            img_largura = int(img0.shape[1]*escala_porcent)
            escala = (img_largura, camera_Altura)
            img = cv.resize(img0, escala)

            # Exibe imagem padrão
            janela['cam0'].update(data=processo.cria_canais_cam(img))
            # Exibe canal vermelho
            janela['cam1'].update(data=processo.cria_canais_cam(img, cor='vermelho'))
            # Exibe canal verde
            janela['cam2'].update(data=processo.cria_canais_cam(img, cor='verde'))
            # Exibe canal azul
            janela['cam3'].update(data=processo.cria_canais_cam(img, cor='azul'))

            #processo.processamento(valores['caixa_mod'], arq_prod)

            ncapturas, dpadrao, fpadrao = processo.processamento(valores['caixa_mod'],
                                                arq_prod, ncapturas, dpadrao, fpadrao,
                                                valores['confianca'])
            # janela.FindElement('output').Update('')
            # processo.imprime_figs(janela['imagem_mod'], processo.cria_canais_modelo(arq_mod))
    except Exception as E:
        # Retorna a excessão/erro, caso algo dê errado
        print(f'Erro: {E}.')
        pass

    return grav_prod, arq_prod, ncapturas, dpadrao, fpadrao


def escanear_prod(arq_mod, grav_prod):
    # Se a camera já estiver ligada
    if grav_prod == True:
        try:
            # Desliga a câmera
            grav_prod = False

        except Exception as E:
            # Retorna a excessão/erro, caso algo dê errado
            print(f'Erro: {E}.\n')
            pass
    
    # Se a câmera estiver desligada
    else:
        # Levanta um alerta caso não haja uma imagem modelo definida
        if len(arq_mod) == 0:
            sg.popup('Defina uma imagem modelo primeiro.', title='Aviso')
            
        # Liga a câmera
        else:
            #sg.FolderBrowse
            grav_prod = True
    
    return grav_prod


def gravar_prod(janela, captura, tamanhoFrame, valores, y, y_ref, controle_altura,
                cont, x_ref1, x_ref2, arq_mod, ncapturas, dpadrao, fpadrao):
    _, frameOrig = captura.read()
    frame = cv.resize(frameOrig, tamanhoFrame)

    try:
        imgContour = frame.copy()

        imgBlur = cv.GaussianBlur(frame, (7, 7), 1)
        imgGray = cv.cvtColor(imgBlur, cv.COLOR_BGR2GRAY)

        limite1 = 30 #cv2.getTrackbarPos("Limite1", "Parametros")
        limite2 = 52 #cv2.getTrackbarPos("Limite2", "Parametros")
        imgCanny = cv.Canny(imgGray, limite1, limite2)

        kernel = np.ones((5,5))
        imgDil = cv.dilate(imgCanny, kernel, iterations=1)
        
        y = contorno.getContours(imgDil, imgContour, valores['areaMin'], y)

        if y <= y_ref and controle_altura:
            cont += 1
            controle_altura = False
            #print(cont, "- Bazinga!")
            try:
                with open(valores['caixa_salva'] + '/log.txt', 'a') as arq:
                    # Esses prints só irão para o arquivo
                    print('-'*50, file = arq)
                    print('Produto', cont, file = arq)

                    # Processa os canais de cores
                    ncapturas, dpadrao, fpadrao = processo.processamento(arq_mod, frame,
                                                    ncapturas, dpadrao, fpadrao,
                                                    valores['confianca'], arq, scan=True)

                # Recebe o nome do arquivo da imagem para ser salva de cada produto
                arq_prod = valores['caixa_salva'] + '/produto_' + str(cont) + '.png'
                # Salva a imagem
                cv.imwrite(arq_prod, frameOrig)
                # Limpa as informações printadas na tela
                #janela.FindElement('output').Update('')
            except Exception as E:
                print(f'Erro: {E}.\n')
                pass
        else:
            cont += 0

        cv.line(imgContour, (x_ref1, y_ref), (x_ref2, y_ref), (0,0,255), 1)

        # Exibe imagem padrão
        janela['cam0'].update(data=processo.cria_canais_cam(imgContour))
        
    except Exception as E:
        print(f'Erro: {E}.\n')
        pass

    # Exibe imagem padrão
    #janela['cam0'].update(data=processo.cria_canais_cam(frame))

    # Exibe canal vermelho
    janela['cam1'].update(data=processo.cria_canais_cam(frame, cor='vermelho'))
    #janela['cam1'].update(data=processo.cria_canais_cam(imgCanny))

    # Exibe canal verde
    janela['cam2'].update(data=processo.cria_canais_cam(frame, cor='verde'))

    # Exibe canal azul
    janela['cam3'].update(data=processo.cria_canais_cam(frame, cor='azul'))

    #arq_prod = valores['caixa_prod']

    return cont, controle_altura, y, ncapturas, dpadrao, fpadrao
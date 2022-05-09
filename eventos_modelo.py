# Código para as funcionalidades relativas ao produto modelo

import PySimpleGUI as sg
import processo
import cv2 as cv

# Evento para quando o operador inserir uma imagem modelo manualmente (por aquivo)
def caixa_mod(janela, valores):
    # Garante que a camera esteja desligada
    grav_mod = False

    # Recebe o local do arquivo selecionado
    arq_mod = valores['caixa_mod']
    try:
        # Imprime a imagem com seus filtros de cores
        processo.imprime_figs(janela['imagem_mod'], processo.cria_canais_modelo(arq_mod))
        
        bloqueia_chaves = False
        janela['pasta_salva'].update(disabled=False)
        #janela['arquivo_prod'].update(disabled=False)
        #janela['escanear_prod'].update(disabled=False)
    except Exception as E:
        # Retorna a excessão/erro, caso algo dê errado
        bloqueia_chaves = False
        print(f'Erro: {E}.')
        pass
    
    return grav_mod, bloqueia_chaves, arq_mod


# Evento para quando o operador escanear o modelo pela câmera
def escanear_mod(janela, grav_mod, bloqueia_chaves, frame):
    # Se a camera já estiver ligada
    if grav_mod == True:
        try:
            # Desliga a câmera
            grav_mod = False

            # Salva a captura e a tranforma em um arquivo .png
            arq_mod = sg.popup_get_file('Selecione o local para salvar', save_as=True)
            arq_mod += '.png'
            # valores['caixa_mod'] = arq_mod
            cv.imwrite(arq_mod, frame)

            # Cria um evento para 'caixa_mod'
            """ 
            O programa cria um evento que direciona o fluxo de execução para
            o caso do evento 'caixa_mod', pois com esse eventos, as imagens
            do modelo são plotadas e imprimidas na tela.
            """
            bloqueia_chaves = False
            janela['pasta_salva'].update(disabled=False)

            janela.write_event_value('caixa_mod', arq_mod)

        except Exception as E:
            # Retorna a excessão/erro, caso algo dê errado
            print(f'Erro: {E}.\n')
            pass
    
    # Se a câmera estiver desligada
    else:
        # Liga a câmera
        grav_mod = True
        """ 
        A função precisa retornar arq_mod, mas nesta etapa ainda não o temos.
        Retornamos None para não atribuir nenhum valor inválido.
        """
        arq_mod = None

    return grav_mod, arq_mod, bloqueia_chaves


# Quando grav_mod = True (camera ligada), a captura começa, de fato
def gravar_mod(captura, tamanhoFrame, janela):
    # Lê e armazena (na variável) cada frame originalmente vindo da câmera
    _, frameOrig = captura.read()
    # Redimensiona o frame com base no tamanho pré-estabelecido em 'tamanhoFrame'
    frame = cv.resize(frameOrig, tamanhoFrame)
    # Define o formato da imagem
    imgbytes = cv.imencode('.png', frame)[1].tobytes()
    # Atualiza a janela com o novo frame processado
    """ 
    Um vídeo é uma sucessão de imagens, frames neste caso, e essas
    atualizações constantes geram o que entendemos por vídeo.
    """
    janela['imagem_mod'].update(data=imgbytes)

    return frame


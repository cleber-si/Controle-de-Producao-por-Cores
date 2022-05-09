'''
Controle de Produção: atualização de 09 de maio de 2022

Modificações:
  Correção no bloqueio da chave ao chamar a função evMod.caixa_mod;
  Correções na leitura de um produto por meio de arquivo;
  Adição do registro de data e hora na leitura de um produto.
  
Aviso: Não use pastas ou arquivos cujo nome carrega caracteres especiais.
'''

import PySimpleGUI as sg
import layout
import cv2 as cv
import eventos_modelo as evMod
import eventos_produto as evProd

""" 
Os sufixos mod e prod fazem menção a 'modelo' e 'produto', respectivamente.
"""

# Carrega a interface gráfica
janela = layout.carrega_layout()

# Redimensiona o tamanho da imagem (um tamanho menor aumenta a performance)
camera_Largura  = 240 # 320 # 480 # 640 # 1024 # 1280
camera_Altura = 180 # 240 # 320 # 480 # 780  # 960

# Indica a captura da webcam
captura = cv.VideoCapture(1)
#captura.set(3, camera_Largura)
#captura.set(4, camera_Altura)

# Tupla contendo as informações do tamanho da imagem
tamanhoFrame = (camera_Largura, camera_Altura)

# Indicadores de gravação (se True, o programa liga a câmera)
grav_mod = False
grav_prod = False

bloqueia_chaves = True
lista_chaves = ['caixa_mod', 'caixa_prod', 'arquivo_prod', 'escanear_prod', 'pasta_salva']

#Declarando variaveis
ncapturas = 1
dpadrao = 0
fpadrao = 0
cont = 0
y = 0

while True:
    # Extrair os dados da tela (timeout é a taxa de atualização da janela)
    evento, valores = janela.Read(timeout=0.1)

    x_ref1 = 0
    x_ref2 = 500
    y_ref = int(valores['contY'])

    controle_altura = True if y > y_ref else False

    # Bloqueia os botões para produto
    if bloqueia_chaves:
        for chave in lista_chaves:
            janela[chave].update(disabled=True)

    # Ação necessária para finalizar o programa quando fechar a janela
    if evento == sg.WIN_CLOSED:
        break
    
    # Evento para quando o operador inserir uma imagem modelo manualmente (por aquivo)
    if evento == 'caixa_mod':
        grav_mod, bloqueia_chaves, arq_mod = evMod.caixa_mod(janela, valores)
    
    # Evento para quando o operador escanear o modelo pela câmera
    if evento == 'escanear_mod':
        print(valores['caixa_mod'])
        """ 
        O programa só vai ter um frame válido se grav_mod == True,
        mas como a função requere algo para essa variável, se grav_mod == False,
        passamos None só por completeza.
        """
        if grav_mod:
            grav_mod, arq_mod, bloqueia_chaves = evMod.escanear_mod(janela,
                                                          grav_mod, bloqueia_chaves, frame)
        else:
            grav_mod, arq_mod, bloqueia_chaves = evMod.escanear_mod(janela,
                                                          grav_mod, bloqueia_chaves, None)
        print(valores['caixa_mod'])

    # Quando grav_mod = True (camera ligada), a captura começa, de fato
    if grav_mod:
        frame = evMod.gravar_mod(captura, tamanhoFrame, janela)

    if evento == 'caixa_salva':
        janela['arquivo_prod'].update(disabled=False)
        janela['escanear_prod'].update(disabled=False)
        print(valores['caixa_salva'])

    # Evento para quando o operador inserir uma imagem do produto manualmente (por aquivo)
    if evento == 'caixa_prod':
        grav_prod, arq_prod, ncapturas, dpadrao, fpadrao = evProd.caixa_prod(janela,
                                                           valores, camera_Altura, 
                                                           ncapturas, dpadrao, fpadrao)

    # Evento para quando o operador escanear o produto pela câmera
    if evento == 'escanear_prod':
        grav_prod = evProd.escanear_prod(arq_mod, grav_prod)

    if grav_prod:
        cont, controle_altura, y, ncapturas, dpadrao, fpadrao = evProd.gravar_prod(janela, 
                                                      captura, tamanhoFrame,
                                                      valores, y, y_ref, controle_altura,
                                                      cont, x_ref1, x_ref2, arq_mod,
                                                      ncapturas, dpadrao, fpadrao)

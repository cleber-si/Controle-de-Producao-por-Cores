import PySimpleGUI as sg

def carrega_layout():
    # Layout
    col1 = sg.Column([
        # Frame do modelo
        [sg.Frame('Modelo',[
            [sg.Text("Procurar Modelo")],
            [sg.Input(enable_events=True, key='caixa_mod', size = (19,1), visible=False),
                sg.FilesBrowse("Procurar", key = 'arquivo_mod'),
                sg.Button('Captura', button_color='red', key = 'escanear_mod')],
            [sg.Text("Imagem Modelo")],
            [sg.Column([[sg.Image(key='imagem_mod')]], justification = 'center')]
        ])],
        [sg.Text("Área Mínima", s=(18,1)), sg.Slider(range=(200,10000),
            orientation='h', size=(27,15), key='areaMin', change_submits=True)],
        [sg.Text("Altura da Detecção", s=(18,1)), sg.Slider(range=(1,200),
            orientation='h', size=(27,15), key='contY', change_submits=True)],
        [sg.Text("Confiança Mínima", s=(18,1)), sg.Slider(range=(0,100),
            orientation='h', size=(27,15), key='confianca', change_submits=True)]
    ])
    
    col2 = sg.Column([
        #[sg.Text("Output")]
        [sg.Frame('Informações de Processamento', [[sg.Output(key = 'output', size=(120, 10))]])]
    ])

    cam0_layout = [
        [sg.Text('Padrão', justification='center')],
        [sg.Image(filename='', key='cam0')]
    ]
    cam0 = sg.Column(cam0_layout, element_justification='center')

    cam1_layout = [
        [sg.Text('Vermelho', justification='center')],
        [sg.Image(filename='', key='cam1')]
    ]
    cam1 = sg.Column(cam1_layout, element_justification='center')

    cam2_layout = [
        [sg.Text('Verde', justification='center')],
        [sg.Image(filename='', key='cam2')]
    ]
    cam2 = sg.Column(cam2_layout, element_justification='center')

    cam3_layout = [
        [sg.Text('Azul', justification='center')],
        [sg.Image(filename='', key='cam3')]
    ]
    cam3 = sg.Column(cam3_layout, element_justification='center')

    cams = sg.Column([
        [sg.Column([[cam0, cam1]])],
        [sg.Column([[cam2, cam3]])]
    ])

    col3 = sg.Column([
        [sg.Frame('Produção',[
            [sg.Text("Selecionar Produção"),
                sg.Input(enable_events = True, key = 'caixa_prod', visible = False),
                sg.FilesBrowse("Procurar", key = 'arquivo_prod')],
                
            [sg.Input(enable_events = True, key = 'caixa_salva', visible = False),
                sg.FolderBrowse('Selecionar Pasta para Salvar', button_color = 'darkorange3',
                            key='pasta_salva'),
                sg.Button('Iniciar Varredura', button_color = 'red', key = 'escanear_prod')],
            [cams]
        ])]
    
    ])

    aba1 = [
        [col1, col3],
        [col2]
    ]

    aba2 = [
        [sg.Text("Ajuste de Parâmetro"), sg.Input(enable_events=True, key='ajuste')]
    ]

    aba3 = [
        [sg.Text("Aqui estarão as instruções de uso.")]
    ]

    layout = [aba1
        #[sg.TabGroup([
        #    [sg.Tab('Análise', aba1), sg.Tab('Ajustes', aba2), sg.Tab('Instruções', aba3)]
        #])]
    ]
    
    # Janela
    janela = sg.Window("Controle de Produção").layout(layout)

    return janela

    #[sg.Input(enable_events = True, key = 'caixa_salva', visible = False),
    #           sg.FolderBrowse('Selecionar Pasta para Salvar', button_color = 'darkorange3',
    #                        key='pasta_salva')],
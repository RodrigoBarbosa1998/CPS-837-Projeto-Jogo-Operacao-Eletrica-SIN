import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random
from PIL import Image, ImageTk

# Configurações do jogo
intervalo_atualizacao_carga = 3  # 3 segundos para atualizar a carga
intervalo_atualizacao_patamar = 30  # 30 segundos para mudar de patamar
custos = {"hidraulica 1": 200, 
          "hidraulica 2": 200, 
          "hidraulica 3": 200,
          "hidraulica 4": 200,
          
          "eolica 1": 100, 
          "eolica 2": 100, 
          "eolica 3": 100, 
          "eolica 4": 100, 
          
          "solar 1": 50, 
          "solar 2": 50,
          "solar 3": 50,
          "solar 4": 50,
          
          "termica 1": 1000, 
          "termica 2": 1000,
          "termica 3": 1000,
          "termica 4": 1000,
          
          "nuclear 1": 500,
          "nuclear 2": 500}  # R$/MWh

velocidade_jogo = 1  # Velocidade padrão do jogo

# Limites de geração conforme potência instalada atual no Brasil (em MW)
limites_geracao = {
    "hidraulica 1": 100000,
    "hidraulica 2": 100000,
    "hidraulica 3": 100000,
    "hidraulica 4": 100000,
    
    "eolica 1": 25000,
    "eolica 2": 25000,
    "eolica 3": 25000,
    "eolica 4": 25000,
    
    "solar 1": 18000,
    "solar 2": 18000,
    "solar 3": 18000,
    "solar 4": 18000,
    
    "termica 1": 35000,
    "termica 2": 35000,
    "termica 3": 35000,
    "termica 4": 35000,
    
    "nuclear 1": 2000,
    "nuclear 2": 2000
}

fontes_sistema = {
          "hidraulica 1", 
          "hidraulica 2", 
          "hidraulica 3",
          "hidraulica 4",
          
          "eolica 1", 
          "eolica 2", 
          "eolica 3", 
          "eolica 4", 
          
          "solar 1", 
          "solar 2",
          "solar 3",
          "solar 4",
          
          "termica 1", 
          "termica 2",
          "termica 3",
          "termica 4",
          
          "nuclear 1",
          "nuclear 2"}  


# Carga média em MW para cada patamar (48 patamares para 24h)
carga_media = [
    74000, 72000, 70000, 67000, 66000, 65000, 65000, 64000, 64000, 62000, 62000, 65000,  # Madrugada
    67000, 68000, 70000, 70000, 71000, 72000, 73000, 74000, 74000, 72000, 75000, 75000,  # Manhã
    73000, 73000, 74000, 75000, 72000, 73000, 74000, 75000, 78000, 78000, 80000, 82000,  # Tarde
    84000, 90000, 92000, 90000, 87000, 80000, 80000, 75000, 75000, 74000, 78000, 74000   # Noite
]


geracao_hidraulica = [
    67680, 63360, 59040, 57600, 54720, 54720, 53280, 54720, 51840, 53280, 54720, 57600,  # Madrugada
    60480, 57600, 56160, 54720, 54720, 51840, 50400, 50400, 50400, 50400, 47520, 46080,  # Manhã
    48960, 50400, 54720, 61920, 64800, 67680, 72000, 77760, 79200, 79200, 82080, 83520,  # Tarde
    83520, 82080, 79200, 77760, 76320, 76320, 73440, 72000, 72000, 69120, 69120, 67680   # Noite
]


geracao_eolica = [
    20400, 20400, 21600, 22800, 21600, 24000, 21600, 21600, 20400, 19200, 20400, 19200,  # Madrugada
    19200, 18000, 19200, 20400, 24000, 21600, 21600, 18000, 12000, 12000, 9600, 12000,  # Manhã
    9600, 9600, 12000, 13200, 13200, 15600, 14400, 15600, 18000, 18000, 20400, 19200,  # Tarde
    19200, 18000, 19200, 20400, 20400, 21600, 21600, 20400, 19200, 19200, 21600, 21600   # Noite
]



geracao_solar = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 300, 600,  # Madrugada
    2400, 8400, 14400, 19200, 22800, 25200, 27600, 30000, 31200, 33600, 34800, 36000,  # Manhã
    36000, 36000, 34800, 33600, 31200, 30000, 27600, 25200, 22800, 19200, 14400, 8400,  # Tarde
    2400, 600, 300, 0, 0, 0, 0, 0, 0, 0, 0, 0   # Noite
]



geracao_termica = [
    12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000,  # Madrugada
    12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000, 12000,  # Manhã
    12000, 12000, 12000, 12000, 13200, 13920, 14400, 14400, 15600, 15600, 16800, 16800,  # Tarde
    16800, 16800, 18000, 18000, 16800, 15600, 15600, 14400, 14400, 12000, 12000, 12000   # Noite
]


geracao_nuclear = [
    2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000,  # Madrugada
    2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000,  # Manhã
    2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000,  # Tarde
    2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000, 2000,   # Noite
]

def interpolar_pontos(dados, num_pontos=2):
    dados_interpolados = []
    for i in range(len(dados) - 1):
        dados_interpolados.append(dados[i])
        step = (dados[i + 1] - dados[i]) / (num_pontos + 1)
        for j in range(1, num_pontos + 1):
            dados_interpolados.append(dados[i] + j * step)
    dados_interpolados.append(dados[-1])
    return dados_interpolados

# Interpolando os pontos
carga_media = interpolar_pontos(carga_media)
geracao_hidraulica = interpolar_pontos(geracao_hidraulica)
geracao_eolica = interpolar_pontos(geracao_eolica)
geracao_solar = interpolar_pontos(geracao_solar)
geracao_termica = interpolar_pontos(geracao_termica)
geracao_nuclear = interpolar_pontos(geracao_nuclear)

# Horários correspondentes a cada patamar
horarios = [h for h in range(1, 143)]

# Inicialização de variáveis
patamar_atual = 0
custo_total = 0
custo_total_total = 0
despacho_atual = {"hidraulica 1": 0, 
                  "hidraulica 2": 0, 
                  "hidraulica 3": 0,
                  "hidraulica 4": 0,
                  
                  "eolica 1": 0, 
                  "eolica 2": 0,
                  "eolica 3": 0,
                  "eolica 4": 0,
                  
                  "solar 1": 0, 
                  "solar 2": 0,
                  "solar 3": 0,
                  "solar 4": 0,
                  
                  "termica 1": 0,
                  "termica 2": 0,
                  "termica 3": 0,
                  "termica 4": 0,
                  
                  "nuclear 1": 0,
                  "nuclear 2": 0}
carga_atual = carga_media[patamar_atual]

# Dicionário para armazenar os widgets Scale
scales = {}

geracao = {
    "hidraulica 1": geracao_hidraulica,
    "hidraulica 2": geracao_hidraulica,
    "hidraulica 3": geracao_hidraulica,
    "hidraulica 4": geracao_hidraulica,
    
    "eolica 1": geracao_eolica,
    "eolica 2": geracao_eolica,
    "eolica 3": geracao_eolica,
    "eolica 4": geracao_eolica,
    
    "solar 1": geracao_solar,
    "solar 2": geracao_solar,
    "solar 3": geracao_solar,
    "solar 4": geracao_solar,
    
    "termica 1": geracao_termica,
    "termica 2": geracao_termica,
    "termica 3": geracao_termica,
    "termica 4": geracao_termica,
    
    "nuclear 1": geracao_nuclear,
    "nuclear 2": geracao_nuclear
}

# Limites de cada barra
limites_fonte = {   
    "hidraulica 1": 0.35,
    "hidraulica 2": 0.30,
    "hidraulica 3": 0.20,
    "hidraulica 4": 0.15,
    
    "eolica 1": 0.40,
    "eolica 2": 0.30,
    "eolica 3": 0.20,
    "eolica 4": 0.10,
    
    "solar 1": 0.35,
    "solar 2": 0.25,
    "solar 3": 0.25,
    "solar 4": 0.15,
    
    "termica 1": 0.35,
    "termica 2": 0.25,
    "termica 3": 0.25,
    "termica 4": 0.15,
    
    "nuclear 1": 0.67,
    "nuclear 2": 0.33
}

violacao_amarela = 0
violacao_vermelha = 0

# Função para atualizar a carga de forma aleatória
def atualizar_carga():
    if patamar_atual >= len(carga_media):
        print("\nFim do Jogo!")
    else:
        return int(random.randint(int(carga_media[patamar_atual]) - 50, int(carga_media[patamar_atual]) + 50))

# Função para atualizar a carga atual a cada 3 segundos
def atualizar_carga_atual():
    global carga_atual
    carga_atual = atualizar_carga()
    carga_atual_label.config(text=f"Carga Atual: {carga_atual} MW")
    root.after(int((intervalo_atualizacao_carga * 250)/velocidade_jogo), atualizar_carga_atual)

# Função para atualizar o custo total, déficit e superávit a cada 3 segundos
def atualizar_dados():
    global custo_total, custo_total_total

    # Atualizar limites de geração conforme o patamar
    atualizar_limites_geracao()

    # Verificar despacho
    energia_despachada = sum(despacho_atual.values())

    if energia_despachada < carga_atual:
        deficit = carga_atual - energia_despachada
        deficit_superavit_label.config(text=f"Déficit de Energia: {deficit} MWh")
    elif energia_despachada > carga_atual:
        superavit = energia_despachada - carga_atual
        deficit_superavit_label.config(text=f"Superávit de Energia: {superavit} MWh")
    else:
        deficit_superavit_label.config(text=f"Ponto Ótimo 60 Hz")

    # Calcular o custo
    custo_patamar = sum(despacho_atual[fonte] * custos[fonte] for fonte in despacho_atual)
    custo_total = custo_patamar
    custo_label.config(text=f"Custo Atual: R$ {round((custo_total/1000000),2)} Milhões")
    
    custo_total_total = custo_total_total + custo_total
    custo_total_label.config(text=f"Custo Total: R$ {round((custo_total_total*27/1000000000000),2)} Bi")

    root.after(int((intervalo_atualizacao_carga * 250)/velocidade_jogo), atualizar_dados)

# Função para atualizar o gráfico e avançar o patamar
def atualizar_grafico():
    global patamar_atual, custo_total_total

    if patamar_atual >= len(carga_media):
        resultado_label.config(text=f"Simulação concluída! Custo total: R$ {round((custo_total_total*27/1000000000000),2)} Bi\nViolações de Alerta: {violacao_amarela}\nViolações de Emergência: {violacao_vermelha}")
        return

    # Atualizar gráfico de Previsão de Carga
    plot_carga.clear()
    plot_carga.plot(horarios, carga_media, marker='o', label="Carga Prevista", markersize=3)
    plot_carga.plot(horarios[patamar_atual], carga_atual, marker='o', color='red', markersize=10, label="Patamar Atual")
    plot_carga.set_title("Previsão de Carga ao Longo do Dia")
    plot_carga.set_xlabel("Patamares (dia)")
    plot_carga.set_ylabel("Carga (MW)")
    plot_carga.legend()

    # Atualizar gráfico de Disponibilidade de Geração
    plot_disponibilidade.clear()
    plot_disponibilidade.plot(horarios, geracao_hidraulica, label="Hidráulica", color='blue', marker='o', markersize=3)
    plot_disponibilidade.plot(horarios, geracao_eolica, label="Eólica", color='green', marker='o', markersize=3)
    plot_disponibilidade.plot(horarios, geracao_solar, label="Solar", color='yellow', marker='o', markersize=3)
    plot_disponibilidade.plot(horarios, geracao_termica, label="Térmica", color='black', marker='o', markersize=3)
    plot_disponibilidade.plot(horarios, geracao_nuclear, label="Nuclear", color='orange', marker='o', markersize=3)
    plot_disponibilidade.axvline(x=horarios[patamar_atual], color='red', linestyle='--', label="Patamar Atual")
    plot_disponibilidade.set_title("Disponibilidade de Geração")
    plot_disponibilidade.set_xlabel("Patamares (dia)")
    plot_disponibilidade.set_ylabel("Geração (MW)")
    plot_disponibilidade.legend()

    canvas_plot.draw()

    # Avançar para o próximo patamar
    patamar_atual += 1

# Função para ajustar o despacho de cada fonte
def ajustar_despacho(fonte, valor):
    despacho_atual[fonte] = valor

# Função para ajustar o despacho de cada fonte - Variação normal das fontes  
def ajustar_despacho_interminentes():
    for fonte in fontes_sistema:
        if despacho_atual.get(fonte, 0) > 0:
            if 'hidraulica' in fonte:
                despacho_atual[fonte] = max(0, despacho_atual[fonte] + random.randint(-10, 10))
            elif 'eolica' in fonte:
                despacho_atual[fonte] = max(0, despacho_atual[fonte] + random.randint(-100, 100))
            elif 'solar' in fonte:
                despacho_atual[fonte] = max(0, despacho_atual[fonte] + random.randint(-50, 50))
            elif 'termica' in fonte:
                despacho_atual[fonte] = max(0, despacho_atual[fonte] + random.randint(-10, 10))
            elif 'nuclear' in fonte:
                despacho_atual[fonte] = max(0, despacho_atual[fonte] + random.randint(-5, 5))
            
            # Atualiza o valor da escala existente
            if fonte in scales:
                scales[fonte].set(despacho_atual[fonte])

    root.after(500, ajustar_despacho_interminentes)
    
# Função para atualizar o relógio
def atualizar_relogio():
    global horas, minutos
    
    minutos += 1
    if minutos == 60:
        minutos = 0
        horas += 1
        if horas == 24:
            horas = 0
            
    if minutos == 10:
        atualizar_grafico()
    elif minutos == 20:
        atualizar_grafico()
    elif minutos == 30:
        atualizar_grafico()        
    elif minutos == 40:
        atualizar_grafico() 
    elif minutos == 50:
        atualizar_grafico() 
    elif minutos == 0:
        atualizar_grafico()
    
    tempo_atual = f"{horas:02}:{minutos:02}"
    relogio_label.config(text=f"Hora Atual: {tempo_atual}")
    root.after(int(1000/velocidade_jogo), atualizar_relogio)

def atualizar_limites_geracao():
    for fonte, scale in scales.items():
        limite_atual = geracao[fonte][patamar_atual] * limites_fonte[fonte]  # Obter o limite do patamar atual
        scale.config(to=limite_atual)
    
# Função para alternar a velocidade do jogo
def alternar_velocidade():
    global velocidade_jogo
    velocidade_jogo = 10 if velocidade_jogo == 7 else (7 if velocidade_jogo == 5 else (5 if velocidade_jogo == 2 else (2 if velocidade_jogo == 1 else 1)))
    botao_velocidade.config(text=f"Velocidade: {velocidade_jogo}x")

x_data = list(range(50))
y_data = [60.0] * 50  # Inicialmente, todos os pontos estão em 60 Hz

# Função para atualizar o gráfico
def atualizar_grafico_frequencia():
    global violacao_amarela, violacao_vermelha
    
    energia_despachada = sum(despacho_atual.values())
    delta_energia = energia_despachada - carga_atual
    
    # Calcular a nova frequência
    frequencia = 60.0 + (delta_energia / 1000)
    
    # Adicionar a nova frequência à lista de dados
    y_data.append(frequencia)
    y_data.pop(0)
    
    # Atualizar os dados do gráfico
    line_freq.set_ydata(y_data)
    canvas_freq.draw()
    
    if frequencia > 61.5 or frequencia < 58.5:
        violacao_vermelha += 1
        violacao_vermelha_label.config(text=f"Violações de Emergência: {violacao_vermelha}")
        
    elif frequencia > 60.5 or frequencia < 59.5:
        violacao_amarela += 1
        violacao_amarela_label.config(text=f"Violações de Alerta: {violacao_amarela}")
        

    # Chamar a função novamente após 1 segundo
    root.after(100, atualizar_grafico_frequencia)

# Função para criar e exibir o modal de introdução
def mostrar_modal_intro():
    modal = tk.Toplevel(root)
    modal.title("Bem-vindo!")
    modal.geometry("1000x600")

    # Mensagens do modal
    mensagens = [
        '''Bem-vindo!\n\n\n
        Você agora é um Operador do Sistema Elétrico!\n\n
        Sua missão é garantir que o balanço entre energia gerada e carga seja sempre igual a zero.\n
        Para isso, você precisará ajustar a produção de diferentes fontes de energia para atender à demanda\n\n\n.
        Na parte superior, você encontrará dois gráficos:\n
        Gráfico de Carga Prevista: Este gráfico mostra a previsão de consumo de energia ao longo do tempo. \nOs valores de carga seguirão aproximadamente essa curva.\n
        Gráfico de Geração Disponível: Aqui, você verá a disponibilidade de geração das diferentes fontes de energia, \nincluindo hidrelétricas, eólicas, solares, térmicas e nucleares.\n\n\n
        Na parte inferior, estão as barras de despacho de energia. \nEste é o painel onde você, como jogador, deve controlar quanto de energia cada fonte irá fornecer para equilibrar a carga.\n\n\n''',
        
        '''Nota Importante: \nAs fontes de energia eólica e solar, por serem intermitentes, 
        \napresentam uma variação de geração maior em comparação com as outras fontes. 
        \nIsso tornará o controle dos limites de frequência mais desafiador, exigindo sua atenção constante.\n\n\n
        Monitoramento de Violações: \nPara verificar a eficácia da sua operação, há dois contadores que acompanham as violações:\n
        Contador de Violações de Alerta: Indica situações de alerta que requerem sua atenção.\n
        Contador de Violações de Emergência: Indica situações críticas que precisam ser evitadas a todo custo.\n\n
        Seu objetivo final é terminar o dia sem nenhuma violação, mantendo a operação do sistema dentro dos limites seguros.\n\n\n''',
        
        '''Custo de Operação 
        \n\nOutro objetivo seu é garantir o menor custo global de operação, uma das metas do ONS. \nAbaixo estão as fontes de energia classificadas pelo custo: \n
        Solares: As mais baratas, mas indisponíveis à noite.\n
        Fotovoltaicas: Também baratas, mas altamente intermitentes, tornando seu controle mais difícil.\n
        Hidrelétricas: Fontes seguras e estáveis, com custos moderados.\n
        Nucleares: Fontes confiáveis, porém com custos mais elevados.\n
        Térmicas: Muito caras, mas essenciais em situações de alta demanda.\n\n\n
        Equilibrar esses fatores será crucial para garantir a eficiência do sistema e manter o custo de operação o mais baixo possível.''',
        
        '''Diagrama Unifilar\n\n\n
        Há uma segunda tela, um diagrama unifilar, onde é possível ver a distribuição das usinas geradoras, \ndas cargas e das linhas de transmissão.\n
        Deve-se respeitas as tensões nos barramentos, realizando o controle de tensão, \ne o controle no fluxo nas linhas de transmissão, por meio do redespacho de geração!\n
        Esses limites não podem ser violados por muito tempo, o que contabilizará penalizações em sua pontuação final.''',
        
        '''Instruções Iniciais\n\n\n
        Observe a Carga Atual: Antes de começar, verifique o valor da carga atual exibido na tela.\n
        Despacho de Geração: Ajuste as barras de despacho de energia de forma que a soma das gerações iguale o valor da carga atual.\n
        Iniciar o Jogo: Quando estiver pronto, clique no botão "Start" para começar a simulação.\n
        Ajuste a Velocidade: Se achar o desafio fácil, experimente acelerar o jogo clicando no botão de velocidade.''',
    ]

    # Índice para rastrear a mensagem atual
    indice_mensagem = [0]

    # Label para exibir as mensagens
    label_mensagem = tk.Label(modal, text=mensagens[indice_mensagem[0]], font=("Arial", 12))
    label_mensagem.pack(pady=20)

    # Função para avançar para a próxima mensagem
    def proximo():
        indice_mensagem[0] += 1
        if indice_mensagem[0] < len(mensagens):
            label_mensagem.config(text=mensagens[indice_mensagem[0]])
        else:
            modal.destroy()  # Fecha o modal após a última mensagem

    # Botão para avançar
    botao_proximo = ttk.Button(modal, text="Próximo", command=proximo)
    botao_proximo.pack(pady=10)

    # Desativa interações com a janela principal enquanto o modal está aberto
    modal.transient(root)
    modal.grab_set()
    root.wait_window(modal)
 
# Função para abrir a nova janela com o mapa e os valores de geração
def abrir_mapa():
    # Criar uma nova janela
    mapa_window = tk.Toplevel(root)
    mapa_window.title("Mapa de Gerações e Cargas")

    # Carregar a imagem
    image = Image.open("mapaGeracoesCargas.png")

    # Redimensionar a imagem para 50% do tamanho original
    original_width, original_height = image.size
    new_width, new_height = original_width // 2, original_height // 2
    image_resized = image.resize((new_width, new_height), Image.LANCZOS)

    # Converter a imagem para o formato compatível com Tkinter
    photo = ImageTk.PhotoImage(image_resized)

    # Ajustar a janela ao tamanho da imagem redimensionada
    # mapa_window.geometry(f"{photo.width()}x{photo.height()}")
    
    # Desativar o redimensionamento da janela
    mapa_window.resizable(False, False)

    # Exibir a imagem em um label
    label_mapa = tk.Label(mapa_window, image=photo)
    label_mapa.image = photo  # Necessário para evitar que a imagem seja coletada pelo garbage collector
    label_mapa.pack()
    
    # Limites de cada barra
    posicoes_originais  = {   
        "hidraulica 1": (50, 610),
        "hidraulica 2": (550, 525),
        "hidraulica 3": (275, 1260),
        "hidraulica 4": (650, 1650),
        
        "eolica 1": (1175, 165),
        "eolica 2": (1400, 300),
        "eolica 3": (1575, 400),
        "eolica 4": (1450, 610),
        
        "solar 1": (850, 215),
        "solar 2": (875, 725),
        "solar 3": (1050, 470),
        "solar 4": (1260, 740),
        
        "termica 1": (50, 250),
        "termica 2": (400, 200),
        "termica 3": (600, 875),
        "termica 4": (1050, 975),
        
        "nuclear 1": (1230, 1250),
        "nuclear 2": (1000, 1350)
    }
    
    # Criar labels para os valores de geração e armazená-los em um dicionário
    labels = {}
    for fonte in fontes_sistema:
        label_text = f"{fonte}: {despacho_atual[fonte]} MW"
        original_x, original_y = posicoes_originais[fonte]
        new_x = int(original_x * new_width / original_width)
        new_y = int(original_y * new_height / original_height)
        label_valor = tk.Label(mapa_window, text=label_text, bg="white")
        label_valor.place(x=new_x, y=new_y)
        labels[fonte] = label_valor

    # Função para atualizar as posições dos textos ao redimensionar a janela
    def atualizar_posicoes(event=None):        
        for fonte in fontes_sistema:
            label_text = f"{fonte}: {despacho_atual[fonte]} MW"
            original_x, original_y = posicoes_originais[fonte]
            new_x = int(original_x * new_width / original_width)
            new_y = int(original_y * new_height / original_height)
            label_valor = tk.Label(mapa_window, text=label_text, bg="white")
            label_valor.place(x=new_x, y=new_y)
            
        # Repetir a cada 1 segundo
        mapa_window.after(500, atualizar_posicoes)

    # Iniciar a atualização contínua das posições dos textos
    atualizar_posicoes()
    
                
# Função que será chamada ao clicar no botão Start
def iniciar_jogo():
    atualizar_relogio()
    ajustar_despacho_interminentes()
    atualizar_grafico_frequencia()
       
# Interface gráfica usando Tkinter
root = tk.Tk()
root.geometry("800x600")  # Definindo o tamanho da janela principal
root.title("Operador do Sistema Elétrico")

# Configuração do grid para o root
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Canvas para rolagem
canvas = tk.Canvas(root)
canvas.grid(row=0, column=0, sticky='nsew')

# Barras de rolagem
vertical_scrollbar = tk.Scrollbar(root, orient='vertical', command=canvas.yview)
vertical_scrollbar.grid(row=0, column=1, sticky='ns')

horizontal_scrollbar = tk.Scrollbar(root, orient='horizontal', command=canvas.xview)
horizontal_scrollbar.grid(row=1, column=0, sticky='ew')

# Frame dentro do Canvas
frame = tk.Frame(canvas)

# Adicionar o Frame ao Canvas
canvas.create_window((0, 0), window=frame, anchor='nw')

# Configurar as barras de rolagem
canvas.configure(yscrollcommand=vertical_scrollbar.set, xscrollcommand=horizontal_scrollbar.set)

# Atualizar a região rolável do Canvas
def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

frame.bind("<Configure>", on_frame_configure)

# Função para rolar o canvas com a bolinha do mouse
def scroll_canvas(event):
    if event.delta > 0:
        canvas.yview_scroll(-1, 'units')
    else:
        canvas.yview_scroll(1, 'units')

canvas.bind_all("<MouseWheel>", scroll_canvas)

# Botão para alternar a velocidade (apenas inclusão, sem alterar o comportamento do jogo)
botao_velocidade = ttk.Button(frame, text=f"Velocidade: {velocidade_jogo}x", command=alternar_velocidade)
botao_velocidade.pack()

# Botão Start
botao_start = ttk.Button(frame, text="Start", command=iniciar_jogo)
botao_start.pack()

resultado_label = tk.Label(frame, text="")
resultado_label.pack()

# Label de carga atual
carga_atual_label = tk.Label(frame, text=f"Carga Atual: {carga_atual} MW")
carga_atual_label.pack()

# Labels de resultado
custo_label = tk.Label(frame, text="Custo Atual: R$ 0")
custo_label.pack()

custo_total_label = tk.Label(frame, text="Custo Total: R$ 0")
custo_total_label.pack()

deficit_superavit_label = tk.Label(frame, text="Déficit de Energia: 0 MWh")
deficit_superavit_label.pack()

violacao_amarela_label = tk.Label(frame, text="Violações de Alerta: 0")
violacao_amarela_label.pack()

violacao_vermelha_label = tk.Label(frame, text="Violações de Emergência: 0")
violacao_vermelha_label.pack()

# Gráfico de previsão de carga e disponibilidade de geração
fig = Figure(figsize=(14, 4), dpi=100)  # Diminui a altura do gráfico

# Subplot para Previsão de Carga
plot_carga = fig.add_subplot(1, 2, 1)
plot_carga.set_xlabel("Horário")
plot_carga.set_ylabel("Carga (MW)")

# Subplot para Disponibilidade de Geração
plot_disponibilidade = fig.add_subplot(1, 2, 2)
plot_disponibilidade.set_xlabel("Horário")
plot_disponibilidade.set_ylabel("Geração (MW)")

canvas_plot = FigureCanvasTkAgg(fig, master=frame)
canvas_plot.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Label do relógio
relogio_label = tk.Label(frame, text="Hora Atual: 00:00")
relogio_label.pack()

# Labels e inputs para despacho
tk.Label(frame, text="Despacho de Energia (MWh)").pack()

# Divisão das fontes de energia em categorias
categorias = {
    'Hidraulicas': [fonte for fonte in limites_geracao if 'hidraulica' in fonte],
    'Eolicas': [fonte for fonte in limites_geracao if 'eolica' in fonte],
    'Fotovoltaicas': [fonte for fonte in limites_geracao if 'solar' in fonte],
    'Termicas': [fonte for fonte in limites_geracao if 'termica' in fonte],
    'Nucleares': [fonte for fonte in limites_geracao if 'nuclear' in fonte],
}

# Criação das colunas
for i, (categoria, fontes) in enumerate(categorias.items()):
    coluna_frame = tk.Frame(frame)
    coluna_frame.pack(side='left', padx=5, pady=5, fill='y')

    tk.Label(coluna_frame, text=categoria).pack(pady=(0, 10))

    for fonte in fontes:
        limite = limites_geracao[fonte]
        tk.Label(coluna_frame, text=f"{fonte.capitalize()}:").pack()
        scale = tk.Scale(coluna_frame, from_=0, to=limite, orient="horizontal", length=150, 
                         command=lambda val, f=fonte: ajustar_despacho(f, int(val)))
        scale.pack()
        scales[fonte] = scale

# Gráfico de frequência
fig_freq = Figure(figsize=(6, 4), dpi=100)  # Figura para o gráfico de frequência
ax_freq = fig_freq.add_subplot(111)
ax_freq.set_ylim(57, 63)
ax_freq.set_xlabel("Tempo (s)")
ax_freq.set_ylabel("Frequência (Hz)")

# Linhas vermelhas para limites de 58.5 Hz e 61.5 Hz
ax_freq.axhline(y=58.5, color='red', linestyle='--')
ax_freq.axhline(y=61.5, color='red', linestyle='--')

ax_freq.axhline(y=59.5, color='yellow', linestyle='--')
ax_freq.axhline(y=60.5, color='yellow', linestyle='--')

# ax_freq.axhline(y=60.0, color='green', linestyle='--')

# Plot inicial da frequência (será atualizado dinamicamente)
line_freq, = ax_freq.plot(x_data, y_data, color='blue')

canvas_freq = FigureCanvasTkAgg(fig_freq, master=frame)
canvas_freq.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Inicializar o tempo do relógio
horas, minutos = 0, 0

atualizar_carga_atual()
atualizar_dados()
atualizar_grafico()

# Exibir o modal de introdução após carregar o jogo
mostrar_modal_intro()
abrir_mapa()

# Ajustar o Canvas e a interface
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

root.mainloop()

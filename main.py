import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from threading import Thread
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import warnings
from svm import analisar_sentimentos
import os
import sys

diretorio = os.path.dirname(os.path.abspath(sys.argv[0]))

# Settings the warnings to be ignored
warnings.filterwarnings('ignore')

def resultado_analise():
    # Leia o arquivo CSV de dados do Twitter com o uso do pandas
    try:
        dados_twitter = pd.read_csv(diretorio + '/dados_twitter.csv', encoding='utf-8', sep=';')
    except FileNotFoundError:
        print("Arquivo 'dados_twitter.csv' não encontrado.")
        return
    
    # Dicionário de mapeamento para substituição
    mapeamento = {
        'Repugnancia': 'Repugnância',
        'Discurso de odio': 'Discurso de ódio'
    }

    # Aplica a substituição na coluna "Classificacao"
    dados_twitter['Classificacao'] = dados_twitter['Classificacao'].replace(mapeamento)

    # Crie uma janela para exibir o gráfico de pizza
    janela_resultado = tk.Toplevel(root)
    janela_resultado.title("Resultado da Análise")

    # Aumente a largura da janela
    janela_resultado.geometry("1200x600")  # Ajuste a largura conforme necessário

    # Título "Frequência de sentimentos"
    fonte_titulo = ("Arial", 12, "bold")
    titulo = tk.Label(janela_resultado, text="Frequência de sentimentos", font=fonte_titulo)
    titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=2)  # Use o gerenciador de geometria grid

    # Calcule a contagem de cada categoria de classificação
    contagem_classificacoes = dados_twitter['Classificacao'].value_counts()

    # Dados para o gráfico de pizza
    labels = contagem_classificacoes.index.tolist()
    sizes = contagem_classificacoes.tolist()

    # Cores associadas às categorias em português
    colors = ['green', 'red', 'blue', 'purple', 'orange', 'gray']  # Adicione mais cores, se necessário
    traducao_cores = {
        'green': 'Verde',
        'red': 'Vermelho',
        'blue': 'Azul',
        'purple': 'Roxo',
        'orange': 'Laranja',
        'gray': 'Cinza'
    }

    # Mapeie as cores em português
    cores_em_portugues = [traducao_cores[color] for color in colors]

    # Crie um gráfico de pizza
    fig, ax = plt.subplots()
    fig.set_facecolor((240/255, 240/255, 240/255))  # Defina a cor de fundo da figura para cinza ou a cor desejada
    wedges, texts, autotexts = ax.pie(
        sizes, labels=None, autopct='%1.1f%%', startangle=90,
        textprops=dict(color="w", fontsize=6), colors=colors, pctdistance=0.85)  # Configure a cor do texto e as cores das fatias

    # Crie uma legenda separada à direita com cores em português e porcentagens
    legend_texts = ['{} - {} ({:.1f}%)'.format(label, cor, size / sum(sizes) * 100) for label, cor, size in zip(labels, cores_em_portugues, sizes)]
    legend_label = tk.Label(janela_resultado, text="\n".join(legend_texts), justify='left')
    legend_label.grid(row=1, column=0, padx=20, pady=10, columnspan=2)  # Use o gerenciador de geometria grid

    # Calcule as médias das colunas
    media_pos_score = dados_twitter['pos_score'].mean()
    media_neg_score = dados_twitter['neg_score'].mean()
    media_obj_score = dados_twitter['obj_score'].mean()

    # Crie rótulos para as médias em negrito e formate-os
    fonte_negrito = ("Arial", 10, "bold")
    media_label_pos = tk.Label(janela_resultado, text=f"Positividade: {media_pos_score:.2f}", font=fonte_negrito, justify='left')
    media_label_neg = tk.Label(janela_resultado, text=f"Negatividade: {media_neg_score:.2f}", font=fonte_negrito, justify='left')
    media_label_obj = tk.Label(janela_resultado, text=f"Neutro: {media_obj_score:.2f}", font=fonte_negrito, justify='left')

    # Posicione os rótulos centralizados na metade do eixo X
    media_label_pos.grid(row=2, column=0, padx=10, pady=1, columnspan=2)
    media_label_neg.grid(row=3, column=0, padx=10, pady=1, columnspan=2)
    media_label_obj.grid(row=4, column=0, padx=10, pady=1, columnspan=2)

    # Calcule a contagem de cada categoria de classificação
    contagem_classificacoes = dados_twitter['Classificacao'].value_counts()

    # Obtenha as categorias mais e menos frequentes
    categorias_mais_frequentes = contagem_classificacoes.index[:2]  # Top 2 categorias
    categoria_menos_frequente = contagem_classificacoes.idxmin()  # Categoria menos frequente

    # Crie um rótulo com o título "Resumo"
    titulo_resumo = tk.Label(janela_resultado, text="Resumo", font=("Arial", 14, "bold"))
    titulo_resumo.grid(row=5, column=0, padx=20, pady=(10, 0), columnspan=2)  # Use o gerenciador de geometria grid

    # Texto com as informações
    texto_info_sentimentos = f"    O top 2 sentimentos que o usuário mais apresenta em sua rede social são {categorias_mais_frequentes[0]} e {categorias_mais_frequentes[1]}.\n    Em contrapartida, o sentimento que ele menos demonstrou é {categoria_menos_frequente}."

    # Crie um rótulo para exibir o texto das informações dos sentimentos
    info_label = tk.Label(janela_resultado, text=texto_info_sentimentos, justify='left', wraplength=400, font=("Arial",12))
    info_label.grid(row=6, column=0, padx=20, pady=10, columnspan=2)  # Use o gerenciador de geometria grid

    # Crie um objeto FigureCanvasTkAgg para exibir o gráfico na janela do tkinter
    canvas = FigureCanvasTkAgg(fig, master=janela_resultado)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.grid(row=0, column=2, rowspan=6, padx=20, pady=10)  # Use o gerenciador de geometria grid


def carregamento(perfil_usuario, data_inicio, data_final):
    def atualizar_texto():
        nonlocal animacao_index
        loading_label.config(text=animacao[animacao_index])
        animacao_index = (animacao_index + 1) % len(animacao)
        loading_label.after(500, atualizar_texto)  # Atualiza o texto a cada 500 ms

    animacao_index = 0  # Defina a variável animacao_index localmente

    # Cria uma janela de espera para exibir durante o processamento
    loading_window = tk.Toplevel(root)
    loading_window.title("Por favor, aguarde...")
    loading_window.geometry("300x100")  # Ajuste o tamanho da janela conforme necessário

    loading_label = ttk.Label(loading_window, text="Analisando perfil.", font=("Arial", 12))
    loading_label.pack(pady=20)

    animacao = ["Analisando perfil.", "Analisando perfil..", "Analisando perfil..."]
    atualizar_texto()

    # Crie uma thread para o processamento -> Essa função irá chamar o SVM
    thread_processamento = Thread(target=processamento, args=(loading_window, perfil_usuario, data_inicio, data_final))
    thread_processamento.start()

def processamento(loading_window, perfil_usuario, data_inicio, data_final):
    # Simule o processamento (chamada do SVM)
    sleep(2)
    analisar_sentimentos(perfil_usuario,data_inicio,data_final)

    # Feche a janela de espera quando o processamento estiver concluído
    loading_window.destroy()

    # Chame a função resultado_analise após fechar a janela de espera
    resultado_analise()

# Função para tratar o clique do botão "Enviar"
def enviar():
    # Captura os valores da entrada e envia para a tela de carregamento
    perfil_usuario = perfil_usuario_entry.get()
    data_inicio = data_inicio_entry.get_date()
    data_final = data_final_entry.get_date()

    # Chama a tela de carregamento (Ela irá rodar o SVM)
    carregamento(perfil_usuario, data_inicio, data_final)

# Função para abrir o calendário ao clicar no campo de data
def abrir_calendario(event):
    event.widget.calendar_popup()

# Função para limpar o valor de exemplo quando a entrada é clicada
def limpar_valor_exemplo(event, widget):
    if widget.get() == widget.placeholder:
        widget.delete(0, tk.END)
        widget.configure(foreground='black')

# Função para restaurar o valor de exemplo se a entrada estiver vazia quando a entrada perde o foco
def restaurar_valor_exemplo(event, widget):
    if not widget.get():
        widget.insert(0, widget.placeholder)
        widget.configure(foreground='gray')

# Configuração da janela principal
root = tk.Tk()
root.title("Análise de rede social")

# Definir o tamanho da janela
root.geometry("600x400")  # Largura x Altura

# Rótulo e entrada para o perfil do usuário
perfil_usuario_label = ttk.Label(root, text="Perfil do usuário:")
perfil_usuario_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky=tk.W)  # Ajuste aqui
perfil_usuario_entry = ttk.Entry(root)
perfil_usuario_entry.grid(row=1, column=0, padx=10, pady=(0, 5), sticky=tk.W)  # Ajuste aqui
perfil_usuario_entry.placeholder = "Exemplo: FEI_online"
perfil_usuario_entry.insert(0, perfil_usuario_entry.placeholder)
perfil_usuario_entry.configure(foreground='gray')
perfil_usuario_entry.bind("<FocusIn>", lambda event, widget=perfil_usuario_entry: limpar_valor_exemplo(event, widget))
perfil_usuario_entry.bind("<FocusOut>", lambda event, widget=perfil_usuario_entry: restaurar_valor_exemplo(event, widget))

# Adicione uma linha vazia para criar espaço
linha_vazia = ttk.Label(root, text="")
linha_vazia.grid(row=2, column=0)

# Título "Período para avaliar" com a mesma fonte do título "Rede social"
fonte_titulo = ("Helvetica", 16, "bold")
periodo_label = ttk.Label(root, text="Período para avaliar", font=fonte_titulo)
periodo_label.grid(row=3, column=0, padx=10, pady=5, columnspan=2, sticky=tk.W)

# Cria um frame para os campos de data
data_frame = ttk.Frame(root)
data_frame.grid(row=4, column=0, padx=10, pady=5, columnspan=2, sticky=tk.W)

# Campo de data de início
data_inicio_label = ttk.Label(data_frame, text="Data de início:")
data_inicio_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky=tk.W)
data_inicio_entry = Calendar(data_frame, date_pattern="yyyy-mm-dd")  # Defina o formato aqui
data_inicio_entry.grid(row=1, column=0, padx=10, pady=(0, 5), sticky=tk.W)
data_inicio_entry.bind("<Button-1>", abrir_calendario)

# Campo de data final
data_final_label = ttk.Label(data_frame, text="Data final:")
data_final_label.grid(row=0, column=1, padx=10, pady=(5, 0), sticky=tk.W)
data_final_entry = Calendar(data_frame, date_pattern="yyyy-mm-dd")  # Defina o formato aqui
data_final_entry.grid(row=1, column=1, padx=10, pady=(0, 5), sticky=tk.W)
data_final_entry.bind("<Button-1>", abrir_calendario)

# Botão de envio (centralizado)
enviar_button = ttk.Button(root, text="Enviar", command=enviar)
enviar_button.grid(row=5, column=0, columnspan=2, padx=10, pady=(10, 0), sticky=tk.W + tk.E)  # Centralizar horizontalmente

# Rótulo abaixo do botão Enviar
analise_label = ttk.Label(root, text="**Análise realizada para a rede social Twitter.", font=("Helvetica", 8, "italic"))
analise_label.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky=tk.W)
root.mainloop()


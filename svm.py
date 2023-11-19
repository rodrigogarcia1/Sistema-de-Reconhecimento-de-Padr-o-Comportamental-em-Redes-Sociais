def analisar_sentimentos(usuario,data_inicial,data_final):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from webdriver_manager.chrome import ChromeDriverManager
    import os, time, pandas as pd, pyautogui, warnings
    from bs4 import BeautifulSoup
    import re
    from nltk.tokenize import TweetTokenizer
    from nltk.stem import PorterStemmer
    import unicodedata
    import string
    import nltk
    from nltk.corpus import sentiwordnet
    from googletrans import Translator
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    from nltk import pos_tag
    import pandas as pd
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import SVC
    import os
    import sys
    from selenium.webdriver.common.action_chains import ActionChains

    warnings.filterwarnings("ignore")
    diretorio = os.path.dirname(os.path.abspath(sys.argv[0]))

    # # **1. Extração de dados**

    # Inicializa o navagedor

    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--window-size=1920,1080")
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()

    # Abrindo o Twitter
    driver.get('https://twitter.com')

    # Aguardando o carregamento da página
    time.sleep(5)

    # Faz login no twitter

    # Vai até o botão de entrar
    login = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[1]/div/div/div[3]/div[5]/a')
    login.click() 

    # Realiza um clique na posição atual do mouse
    time.sleep(5)

    # Preenchendo o nome de usuário
    username_field = driver.find_element(By.XPATH,'/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
    username_field.send_keys('rodrigo1rodrigo.rg@gmail.com')

    # Aguardando um pequeno intervalo de tempo
    time.sleep(1)

    # Pressionando a tecla "Enter" usando PyAutoGUI
    username_field.send_keys(Keys.RETURN)
    #pyautogui.press('enter')

    # Aguardando um pequeno intervalo de tempo
    time.sleep(5)

    #Caso seja solicitado o nome de usuário
    try:
        #Preenche nome de usuário
        user_field = driver.find_element(By.XPATH,'/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input')
        user_field.send_keys('perfil1_tccrh')

        # Aguardando um pequeno intervalo de tempo
        time.sleep(1)

        # Pressionando a tecla "Enter" usando PyAutoGUI
        user_field.send_keys(Keys.RETURN)
        #pyautogui.press('enter')

        # Aguardando um pequeno intervalo de tempo
        time.sleep(5)

        #Preenche a senha
        password_field = driver.find_element(By.XPATH,'/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password_field.send_keys('tccrhfei')

        # Aguardando um pequeno intervalo de tempo
        time.sleep(1)

        # Pressionando a tecla "Enter" usando PyAutoGUI
        password_field.send_keys(Keys.RETURN)
        #pyautogui.press('enter')

    #Caso não seja pedido o nome de usuário
    except:
        #Preenche a senha
        password_field = driver.find_element(By.XPATH,'/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
        password_field.send_keys('tccrhfei')

        # Aguardando um pequeno intervalo de tempo
        time.sleep(1)

        # Pressionando a tecla "Enter" usando PyAutoGUI
        password_field.send_keys(Keys.RETURN)
        #pyautogui.press('enter')

    # Tempo para carregar a página
    time.sleep(10)

    # Realiza a busca do perfil
    user = usuario
    since = data_inicial
    until = data_final

    # Faz a busca
    search_field = driver.find_element(By.XPATH,'/html/body/div[1]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
    search_field.send_keys('(from:' + user + ') since:' + since + ' until:' + until)

    # Tempo para pressionar 'enter'
    time.sleep(1)

    # Pressionando a tecla "Enter" usando PyAutoGUI
    search_field.send_keys(Keys.RETURN)
    #pyautogui.press('enter')

    time.sleep(10)

    # Pega os tweets da página

    # Variável de tweets
    tweets = []
    conteudo = ''

    altura_nova = None
    altura_anterior = 1
    encerrar = False

    actions = ActionChains(driver)
    while True:

        # Verifica se o loop é encerrado
        if encerrar == True:
            # Analisar o HTML com BeautifulSoup
            soup = BeautifulSoup(conteudo, 'html.parser')

            # Encontrar todas as tags <div> com data-testid="tweetText"
            divs_tweet_text = soup.find_all('div', attrs={'data-testid': 'tweetText'})

            # Inicializar uma lista para armazenar o conteúdo das tags <span>
            span_contents_list = []

            # Iterar sobre as ocorrências de <div> com data-testid="tweetText" e adicionar o conteúdo de todas as tags <span> à lista
            for div_tweet_text in divs_tweet_text:
                span_contents = div_tweet_text.find_all('span')
                if span_contents:
                    for span_content in span_contents:
                        span_contents_list.append(span_content.text)

            for elementos in span_contents_list:
                if elementos not in tweets:
                    tweets.append(elementos)

            # Fecha a janela
            driver.quit()
            break
        
        #Verifica se a página não desce mais
        if altura_nova == altura_anterior:
            # Executando um script JavaScript para rolar a página até o final
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            encerrar = True

            # Obtendo o código HTML da página
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # Encontrando a div com o id "react-root"
            div_react_root = soup.find('div', id='react-root')

            # Verificando se a div foi encontrada
            if div_react_root:
                # Encontrando a div filha específica
                div_filha = div_react_root.find('div', class_='css-1dbjc4n r-18u37iz r-13qz1uu r-417010')

                # Verificando se a div filha foi encontrada
                if div_filha:
                    conteudo = conteudo + str(div_filha)

                else:
                    print("Div filha não encontrada")
            else:
                print("Div com o id 'react-root' não encontrada")

        time.sleep(5)

        #Verifica se toda a página já foi carregada    
        altura_anterior = driver.execute_script("return document.body.scrollHeight") # Obtenha a altura inicial da página

        #Desce a página do twitter
        
        #pyautogui.moveTo(936, 429) # Mover o cursor para a posição desejada
        #pyautogui.click()
        time.sleep(1)

        for elementos in range(17):
            actions.send_keys(Keys.ARROW_DOWN).perform() # Simular pressionar a tecla Arrow Down
            time.sleep(0.5)

        time.sleep(1)
        
        altura_nova = driver.execute_script("return document.body.scrollHeight") # Obtenha a nova altura da página

        #Verifica se a página não desce mais
        if altura_nova != altura_anterior:
            encerrar = False

    # Coloca em um dataframe o conteúdo extraído
    tweets_df = pd.DataFrame(tweets, columns=['content'])

    # Exporta arquivo para CSV
    tweets_df.to_csv(diretorio + '/dados_twitter.csv', sep=';', index=False, encoding='utf-8')

    # # **2. Pré-processamento de dados**

    # 2.1 Faz a tokenização, removendo usuários mencionados (começam com '@') e url's

    # criar um objeto TweetTokenizer
    tknzr = TweetTokenizer()

    # definir a expressão regular para encontrar menções a usuários (@user)
    mention_regex = re.compile(r'@[a-zA-Z0-9_]+')

    # definir a expressão regular para encontrar URLs (http(s)://...)
    url_regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # criar uma nova coluna com a coluna 'content' tokenizada e palavras indesejadas removidas
    def preprocess_tweet_content(content):
        content = mention_regex.sub('', content)  # remove menções a usuários
        content = url_regex.sub('', content)  # remove URLs
        tokens = tknzr.tokenize(content)  # tokeniza o texto
        return tokens

    tweets_df['content_preProcessed'] = tweets_df['content'].apply(preprocess_tweet_content)

    # 2.2 Faz o stemming, trazendo a palavra para o seu radical

    # criar um objeto PorterStemmer para o idioma português
    stemmer = PorterStemmer()

    # função para aplicar stemming em uma lista de tokens
    def stem_tokens(tokens):
        return [stemmer.stem(token) for token in tokens]

    # aplicar stemming na coluna 'content_preProcessed'
    tweets_df['content_preProcessed'] = tweets_df['content_preProcessed'].apply(stem_tokens)

    # 2.3 Faz a normalização, removendo a pontuação e deixando todas as letras em minúsculo

    # remover pontuação
    translator = str.maketrans('', '', string.punctuation)
    tweets_df['content_preProcessed'] = tweets_df['content_preProcessed'].apply(lambda tokens: [token.translate(translator) for token in tokens])

    # remover acentuação e colocar em minúsculo
    tweets_df['content_preProcessed'] = tweets_df['content_preProcessed'].apply(lambda tokens: [unicodedata.normalize('NFKD', token).encode('ASCII', 'ignore').decode('utf-8').lower() for token in tokens])

    # 2.4 Faz a remoção de stopwords

    #nltk.download('punkt')
    #nltk.download('stopwords')

    # definir a lista de stopwords
    stop_words = ['o', 'os', 'a', 'as', 'um','uns', 'uma', 'umas', 'a', 
                'ante','apos','ate','com','contra','desde','em','entre',
                'para','per','perante','por','sem','sob','sobre','tras',
                'afora','acomo','conforme','durante','exceto','mediante',
                'menos','salvo','segundo','visto','e','nem','contudo',
                'entretanto','mas','porem','todavia','ja','ou','ora',
                'quer','assim','entao','logo','pois','por conseguinte',
                'por isso','portanto','porquanto','porque','que','como',
                'que','embora','conquanto','se','caso','quando','conforme',
                'como','segundo','consoante','quando','apenas','mal','que',
                'qual','acaso', 'porventura','possivelmente','provavelmente','quiça','talvez',
                'abaixo', 'acima','adiante','ai','alem','ali','aquem','atras',
                'atraves','ca','defronte','dentro','detras','fora',
                'junto','la','longe','onde','perto','assim','bem','debalde',
                'depressa','devagar','não','tampouco',
                'agora','ainda','amanha','anteontem','antes','breve','cedo',
                'depois','entao','hoje','ja','jamais','logo','logo','nunca',
                'ontem','outrora','sempre','tarde','aqui','entao','agora',
                'onde','como','quando', 'eu', 'tu', 'ele', 'ela', 'nós',
                'vós', 'eles', 'elas', 'meu', 'teu', 'seu', 'sua', 'nosso',
                'vosso', 'seus', 'suas', 'me', 'te', 'se', 'o', 'a', 'lhe',
                'nos', 'vos', 'os', 'as', 'lhes', 'meus', 'teus', 'seus', 'suas',
                'nossos', 'vossos', 'suas', 'minha', 'tua', 'sua', 'nossa', 'vossa',
                'suas', 'este', 'esse', 'aquele', 'esta', 'essa', 'aquela', 'isto',
                'isso', 'aquilo', 'mim', 'ti', 'si', 'consigo', 'connosco', 'convosco',
                'si', 'mesmo', 'mesma', 'mesmos', 'mesmas', 'nada', 'ninguém', 'outro',
                'outra', 'outros', 'outras', 'pouco', 'pouca', 'poucos', 'poucas', 'tanto',
                'tanta', 'tantos', 'tantas', 'algum', 'alguma', 'alguns', 'algumas',
                'alguma coisa', 'algumas coisas', 'outrem']

    # função para remover stopwords de uma lista de tokens
    def remove_stopwords(tokens):
        return [token for token in tokens if token.lower() not in stop_words]

    # remover stopwords na coluna 'content_preProcessed'
    tweets_df['content_preProcessed'] = tweets_df['content_preProcessed'].apply(remove_stopwords)

    #Remove tokens vazios
    tweets_df['content_preProcessed'] = tweets_df['content_preProcessed'].apply(lambda tokens: [token for token in tokens if token])

    # Remover linhas com lista vazia na coluna 'conteudo'
    tweets_df = tweets_df[tweets_df['content_preProcessed'].apply(lambda x: x != [])]

    # Refazer os índices
    tweets_df = tweets_df.reset_index(drop=True)

    # Função para unir elementos de uma lista em uma string
    def unir_lista(lista):
        return ' '.join(lista)

    # Aplicar a função à coluna 'coluna_lista' para criar uma nova coluna 'coluna_unida'
    tweets_df['content_preProcessed'] = tweets_df['content_preProcessed'].apply(unir_lista)

    # Exporta arquivo para CSV
    tweets_df.to_csv(diretorio + '/dados_twitter.csv', sep=';', index=False, encoding='utf-8')

    # # **3. Processamento de dados**

    # 3.1 Aplicação do sentiword

    nltk.download('sentiwordnet')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

    # Tradutor de inglês para português

    def translate_sentence(sentence):
        try:
            if pd.isnull(sentence) or not isinstance(sentence, str) or sentence.strip() == "":
                return ""

            translator = Translator(service_urls=['translate.google.com'])
            translation = translator.translate(sentence, src='pt', dest='en')
            return translation.text
        except:
            return sentence

    # Cria uma coluna com o tweet em inglês
    tweets_df['translated_content'] = tweets_df['content'].apply(translate_sentence)

    # Função que aplica o sentiword na sentença em inglês

    def get_sentiment_score(word, pos):
        try:
            synsets = list(sentiwordnet.senti_synsets(word, pos))
            if synsets:
                sentiment = synsets[0]
                return sentiment.pos_score(), sentiment.neg_score(), sentiment.obj_score()
            else:
                return None, None, None
        except KeyError:
            return None, None, None

    def calculate_sentence_sentiment(sentence):
        # Tokenização da sentença
        tokens = word_tokenize(sentence.lower())

        # Remoção das stopwords
        stop_words = set(stopwords.words('english'))
        filtered_tokens = [token for token in tokens if token not in stop_words]

        # Determinação da parte do discurso (POS)
        tagged_tokens = pos_tag(filtered_tokens)

        sentiment_scores = []
        for token, pos in tagged_tokens:
            pos = pos.lower()
            sentiment_score = get_sentiment_score(token, pos)
            sentiment_scores.append(sentiment_score)

        # Cálculo da média dos sentimentos da sentença
        pos_scores = [score[0] for score in sentiment_scores if score[0] is not None]
        neg_scores = [score[1] for score in sentiment_scores if score[1] is not None]
        obj_scores = [score[2] for score in sentiment_scores if score[2] is not None]

        if pos_scores and neg_scores:
            pos_average = sum(pos_scores) / len(pos_scores)
            neg_average = sum(neg_scores) / len(neg_scores)
            obj_average = sum(obj_scores) / len(obj_scores)
            return pos_average, neg_average, obj_average
        else:
            return None, None, None

    # Cria as colunas com positivade, negatividade e neutro
    tweets_df[['pos_score', 'neg_score', 'obj_score']] = tweets_df['translated_content'].apply(calculate_sentence_sentiment).apply(pd.Series)

    # Exporta arquivo para CSV
    tweets_df.to_csv(diretorio + '/dados_twitter.csv', sep=';', index=False, encoding='utf-8')

    # 3.2 Aplicação do SVM

    # Faz o pré-processamento dos dados de treino e transforma as colunas uma lista

    # Use a função read_csv do pandas com o parâmetro sep especificado como ponto e vírgula (;)
    df_treino = pd.read_csv(diretorio + '/frases_sentimentos.csv', encoding='ISO-8859-1', sep=';')

    # Faz a tokenização, removendo usuários mencionados (começam com '@') e url's

    # criar um objeto TweetTokenizer
    tknzr = TweetTokenizer()

    # definir a expressão regular para encontrar menções a usuários (@user)
    mention_regex = re.compile(r'@[a-zA-Z0-9_]+')

    # definir a expressão regular para encontrar URLs (http(s)://...)
    url_regex = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

    # criar uma nova coluna com a coluna 'content' tokenizada e palavras indesejadas removidas
    def preprocess_tweet_content(content):
        content = mention_regex.sub('', content)  # remove menções a usuários
        content = url_regex.sub('', content)  # remove URLs
        tokens = tknzr.tokenize(content)  # tokeniza o texto
        return tokens

    df_treino['frases_preProcessed'] = df_treino['Frases'].apply(preprocess_tweet_content)

    # Faz o stemming, trazendo a palavra para o seu radical
    from nltk.stem import PorterStemmer

    # criar um objeto PorterStemmer para o idioma português
    stemmer = PorterStemmer()

    # função para aplicar stemming em uma lista de tokens
    def stem_tokens(tokens):
        return [stemmer.stem(token) for token in tokens]

    # aplicar stemming na coluna 'content_preProcessed'
    df_treino['frases_preProcessed'] = df_treino['frases_preProcessed'].apply(stem_tokens)

    # Faz a normalização, removendo a pontuação e deixando todas as letras em minúsculo

    # %%
    import unicodedata
    import string

    # %%
    # remover pontuação
    translator = str.maketrans('', '', string.punctuation)
    df_treino['frases_preProcessed'] = df_treino['frases_preProcessed'].apply(lambda tokens: [token.translate(translator) for token in tokens])

    # remover acentuação e colocar em minúsculo
    df_treino['frases_preProcessed'] = df_treino['frases_preProcessed'].apply(lambda tokens: [unicodedata.normalize('NFKD', token).encode('ASCII', 'ignore').decode('utf-8').lower() for token in tokens])

    # Faz a remoção de stopwords

    # função para remover stopwords de uma lista de tokens
    def remove_stopwords(tokens):
        return [token for token in tokens if token.lower() not in stop_words]

    # remover stopwords na coluna 'content_preProcessed'
    df_treino['frases_preProcessed'] = df_treino['frases_preProcessed'].apply(remove_stopwords)

    #Remove tokens vazios
    df_treino['frases_preProcessed'] = df_treino['frases_preProcessed'].apply(lambda tokens: [token for token in tokens if token])

    # Remover linhas com lista vazia na coluna 'conteudo'
    df_treino = df_treino[df_treino['frases_preProcessed'].apply(lambda x: x != [])]

    # Refazer os índices
    df_treino = df_treino.reset_index(drop=True)

    # Faz o join na coluna tokenizada

    # Função para unir elementos de uma lista em uma string
    def unir_lista(lista):
        return ' '.join(lista)

    # Aplicar a função à coluna 'coluna_lista' para criar uma nova coluna 'coluna_unida'
    df_treino['frases_preProcessed'] = df_treino['frases_preProcessed'].apply(unir_lista)

    # Converte para lista
    frases = df_treino['frases_preProcessed'].tolist()
    sentimento = df_treino['Sentimento'].tolist()

    # Realiza o treino

    # Crie um vetorizador TF-IDF para converter texto em recursos numéricos
    vectorizer = TfidfVectorizer()

    # Ajuste o vetorizador aos seus dados de treinamento e transforme os dados de treinamento em vetores
    X_train = vectorizer.fit_transform(frases)

    # Crie um classificador SVM e ajuste-o aos dados de treinamento
    svm = SVC(kernel='linear', C=1)
    svm.fit(X_train, sentimento)

    # Aplica o SVM no dataframe

    # Transforme o texto de entrada em vetores usando o mesmo vetorizador
    X_test = vectorizer.transform(tweets_df['content_preProcessed'])

    # Faça a previsão da classe para a frase
    classe_predita = svm.predict(X_test)

    # Adicione a coluna de classes preditas ao dataframe original
    tweets_df['Classificacao'] = classe_predita

    # Exporta arquivo para CSV
    tweets_df.to_csv(diretorio + '/dados_twitter.csv', sep=';', index=False, encoding='utf-8')

#Testar o código
#analisar_sentimentos('iam_AsE1','2023-01-01','2023-01-31')
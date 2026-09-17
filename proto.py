import tools
from random import random, choice, randint, choices
from json import load

class ProtoLingua:
    """
    FUNCAO
    Classe ProtoLingua desenvolve a primeira língua base, a proto-língua, que começa com sons iniciais, palavras, gramática geral
    e ordem do sistema (SVO, SOV, etc.).
    #
    INPUTS
    quantidade_palavras -> Referente a quantas palavras serão geradas na proto-língua - só aceita números inteiros.
    #
    RETORNO
    None
    #
    EXEMPLO
    >>>var = ProtoLingua(100)
    - Vai formar a língua inicial, e desenvolverá 100 palavras, podendo repetir os mesmos conceitos.
    """
    def __init__(self, quantidade_palavras:int):
        self.proto_vogais = self._criar_vogais()
        self.proto_consoantes = self._criar_consoantes()
        self.proto_ordem = self.gerar_estrutura_da_lingua()
        self.proto_posicao = self.sistema_posicional()
        self.proto_tonica = self.gerar_tonicidade()
        self.proto_lingua = self.criar_proto_lingua(quantidade_palavras)

    ###DICIONARIO PROTO-LINGUA
    def criar_proto_lingua(self, quantidade_palavras:int)->dict[str, dict[str|int, str|list[str]|dict[str, list[str]|float|str]]]:
        """
        FUNCAO

        INPUTS
        quantidade_palavras -> Quantidade de neologismos iniciais desejados
        #
        RETURN
        dict[str, dict[str|int, str|list[str]|float]]
        EXEMPLO
        >>>class.criar_proto_lingua(100)

        """
        proto_lingua:dict[str, dict[str, str|list[str]]] = {
            "sons":{
                "vogais":self.proto_vogais,
                "consoantes":self.proto_consoantes
            },
            "gramatica":{
                "estrutura":self.proto_ordem,
                "silaba_tonica":self.proto_tonica,
                "posicao":self.proto_posicao,
            },
            "configuracao":{
                "metata":0.0,
                "epentese":0.0,
                "harmonia":0.0,

                "aferese":0.0,
                "sincope":0.0,
                "apocope":0.0,

                "assimilacao":0.0,
                "lenicao":0.0,
                "palatalizacao":0.0,

                "reducao_vocal":0.0,
                "nasalizacao":0.0,
            },
            "lingua":{},
        }

        termos:dict[str, dict[str, list[str]|str]] = self.gerar_significado("", True)
        index:int = 0
        for classe_gramatical in termos.keys():
            for generico in termos[classe_gramatical]:
                for significado in termos[classe_gramatical][generico]:
                    proto_lingua["lingua"][index] = {
                    "palavra" : self.criar_palavra(),
                    "classe" : classe_gramatical,
                    "significado" : [significado],
                    "generico" : [generico],
                    "indices" : [],
                    "uso":1.0,
                    }
                    index+=1

        for _ in range(quantidade_palavras):
            classe_gramatical:str = choice(["adjetivo", "substantivo", "verbo"])
            significado, generico = self.gerar_significado(classe_gramatical, False)
            proto_lingua["lingua"][index] = {
                "palavra" : self.criar_palavra(),
                "classe" : classe_gramatical,
                "significado" : [significado],
                "generico" : generico,
                "indices" : [],
                "uso":1.0,
            }
            index+=1

        self.verificar_ausencia(proto_lingua)
        return proto_lingua

    ### CONFIGURACAO SONS
    def _criar_vogais(self)->list[str]:
        """
        FUNCAO
            Seleciona aleatoriamente vogais para a lingua-mae. As vogais selecionadas
            foram as consideradas comuns ou quase comuns. Tambem tem as exoticas,
            mas que abrangem uma quantidade consideravel de troncos linguisticos.
        #
        INPUTS
        None
        #
        RETORNO
        list[str]
        #
        EXEMPLO
        >>>var._criar_vogais()
        ['a', 'i', 'u', 'o', 'ʌ']
        """
        # exoticas:list[str] = ['ɶ', 'æ', 'ʌ', 'œ', 'ø', 'ɤ', 'ɯ']
        vogais_listadas:list[str]=['a', 'i', 'u']
        if(random()>0.5):
            vogais_listadas.extend(['e', 'o'])
            if(random()>0.9):
                secundarias:list[str] = ['ä', 'ɑ', 'ɛ', 'ɔ', 'ɨ']
                index:int = 0
                while(index < randint(1, len(secundarias)-1)):
                    vogais_listadas.append(secundarias.pop(randint(0, len(secundarias)-1)))
                    index+=1
        return vogais_listadas

    def _criar_consoantes(self)->list[str]:
        """
        FUNCAO
        Sorteia as consoantes iniciais para a proto-língua. Por considerar universal, por padrão
        os sons /p/, /t/, /k/, /w/ e /j/ sempre sairão.
        INPUTS
        None
        #
        RETORNO
        list[str]
        #
        EXEMPLO
        >>>class._criar_consoantes()
        ['p', 't', 'k', 'w', 'j','s','r','m','n','g']
        """
        consoantes_listadas:list[str]=['p', 't', 'k', 'w', 'j', 'm', 'n', 's', 'ɾ']
        # incomuns = ['ʔ', 'r', 'x', 'q', 'ŋ', 'ɲ', 'z', 'ʃ', 'ʒ', 'ɢ', 'ɣ']
        # raras = ['ʈ', 'ɖ', 'ɽ', 'ʂ', 'ʐ', 'ɳ', 'χ', 'ʁ', 'ʀ', 'ɬ', 'ɮ', 'ɸ', 'β', 'ɹ', 'ɻ', 'ʋ', 'ɺ']
        if(random()>0.6):
            comuns = ['h', 'b', 'd', 'g', 'l']
            index:int = 0
            while(index< randint(1, len(comuns)-1)):
                consoantes_listadas.extend(comuns.pop(randint(0, len(comuns)-1)))
                index+=1
        return consoantes_listadas

    def conta_vogal_consoante(self, estrutura:list[str], tipo:str)->int:
        if(isinstance(estrutura, str) and isinstance(tipo, str)):
            conta:int = 0
            for index in estrutura:
                if(index==tipo.upper()):
                    conta+=1
        else:
            if(not isinstance(estrutura, list)):
                raise ValueError(f"tipo deveria ser string, mas recebeu {type(tipo)}")
            raise ValueError(f"estrutura deveria ser list, mas recebeu {type(estrutura)}")

        return conta

    def implementar_efeitos(self, word:str)->str: # nao adiciona na funcao surtir_efeito
            """
            Faz passo a passo do processo de desenvolvimento de uma palavra. Função semelhante a surtir_efeito(),
            mas sem o uso de localizadores (loc_1, loc_2).
            Args:
                - lingua (str)
                - word (str)
            Return:
                str
            Exemple:
                >>> implementar_efeitos(lingua_a, word = "anpagtop")
                "ampaktop"
            """
            if(isinstance(word, list)):
                word = "".join(word)
            if(random()<0.1):
                word = tools.devoicing(word)
            # word = ajuste_diacritico(word, vowels)
            effects:list[callable] = [tools.esquecer, tools.rotica_probida, tools.filtro_fonetico]
            for function in effects:
                word = function(word)
            word = tools.retornar_palavra_atona(word, self.proto_tonica)
            return word

    def harmonia_vocalica(self, num_vogais:int, vogais:list[str])->list[str]:
        vogal_posterior:bool = False
        sequencia_vogais:list[str] = []
        vogal_primaria:str = choice(vogais)
        classe_primaria:list[str] = tools.verificar_classe(vogal_primaria)
        sequencia_vogais.append(vogal_primaria)
        while(len(sequencia_vogais)<num_vogais):
            proxima_vogal:str = choice(vogais)
            classe_secundaria:list[str] = tools.verificar_classe(vogal_primaria)
            if(classe_primaria[0]==classe_secundaria[0] or classe_primaria[2]==classe_secundaria[2]):
                sequencia_vogais.append(proxima_vogal)
                classe_primaria = classe_secundaria
        return sequencia_vogais

    def hierarquia_consoantes(self, num_consoantes:int, consoantes:list[str])->list[str]:
        fonotatica_consonantal:dict[int,list[str]] = {
            1: ["oclusiva", "surda"],
            2: ["oclusiva", "sonora"],
            3: ["fricativa", "surda"],
            4: ["fricativa", "sonora"],
            5: ["africada", "surda"],
            6: ["africada", "sonora"],
            7: ["nasal", "sonora"],
            8: ["trill", "sonora"],
            9: ["tap", "sonora"],
            10: ["lateral", "sonora"],
            11: ["aproximante", "sonora"]
        }
        tamanho:int = len(fonotatica_consonantal)
        consoante_posta:bool = False
        index_fonotatico:int = 1
        index_usado:int = 1
        consoantes_lista:list[str] = []
        while(len(consoantes_lista)<num_consoantes):
            c_:str = choice(consoantes)
            index_fonotatico = randint(index_fonotatico,tamanho)
            # print(index_fonotatico)
            if(tools.verificar_classe(c_)[1:] == fonotatica_consonantal[index_fonotatico] and consoante_posta == False):
                # print(consoante, consoante_posta)
                consoantes_lista.append(c_)
                consoante_posta = True
                index_usado = index_fonotatico
            elif(tools.verificar_classe(c_)[1:] == fonotatica_consonantal[index_fonotatico] and consoante_posta == True and index_fonotatico>=index_usado):
                # print(consoante, consoante_posta)
                consoantes_lista.append(c_)
                index_usado = index_fonotatico
                consoante_posta = False
            else:
                index_fonotatico = 1
        return consoantes_lista

    def gerar_estrutura_palavra(self)->str:
        """
        FUNCAO
        Gera a ordem das palavras, como CVC, VC, CVCV, etc.
        INPUTS
        None
        RETORNO
        str
        >>>gerar_estrutura_palavra()
        'CVCV'
        """
        return choice(tools.regra_fonetica["estrutura"])


    def criar_palavra(self)->list[str]:
        # print("Criar Palavra")
        consoantes:list[str] = self.proto_consoantes.copy()
        vogais:list[str] = self.proto_vogais.copy()
        estrutura:str = self.gerar_estrutura_palavra()

        num_consoantes:int = self.conta_vogal_consoante(estrutura, "C")
        num_vogais:int = self.conta_vogal_consoante(estrutura, "V")
        consoantes:list[str] = self.hierarquia_consoantes(num_consoantes, consoantes)
        vogais:list[str] = self.harmonia_vocalica(num_vogais, vogais)
        ultima_consoante_inserida:str = '' #para evitar sequencia de consoantes
        vezes_ultima_adicionada:int = 0
        word:str = ""
        for _, letra in enumerate(estrutura):
            if letra == 'C':
                if(consoantes[0] != ultima_consoante_inserida):
                    ultima_consoante_inserida = consoantes[0]
                    vezes_ultima_adicionada = 0
                    word+=consoantes.pop(0)
                    # word.append(consoantes.pop(0))
                else:
                    vezes_ultima_adicionada+=1
                    if(vezes_ultima_adicionada>2):
                        consoante = choice(consoantes)
                        word+=consoante
                        # word.append(consoante)

            else:
                # word.append(vogais.pop(0))
                word+=vogais.pop(0)
        word = self.implementar_efeitos(word)
        return word

    ### REFINAMENTO DA ESTRUTURA
    def gerar_afixos_pronomes(self, fim:int, consoantes:list[str], vogais:list[str], inicio:int = 0)->list[str]:
        """
        """
        afixo:list[str] = []
        foi_consoante:bool = False
        for som in choice(list(tools.regra_fonetica['estrutura'][inicio:fim])):
            if(som=="C" and not foi_consoante):
                foi_consoante = True
                afixo.append(choice(consoantes))
            else:
                foi_consoante = False
                afixo.append(choice(vogais))
        return afixo

    def gerar_estrutura_da_lingua(self)->list[str]:
        """
        FUNCAO
        Escolhe aleatoriamente induzido uma ordem para o sistema inicial da língua
        #
        INPUTS
        None
        #
        RETORNO
        list[str]
        #
        EXEMPLO
        >>>class.gerar_estrutura_da_lingua()
        ['S', 'O', 'V']
        """
        estruturas_frasais:list[str] = ["SOV", "SVO", "VSO", "VOS", "OVS", "OSV"]
        estruturas_comuns:list[float] = [0.45, 0.42, 0.09, 0.03, 0.009, 0.001]
        estrutura_frasal_selecionada:list = choices(population= estruturas_frasais, weights=estruturas_comuns, k=1)[0]
        return estrutura_frasal_selecionada

    def gerar_tonicidade(self):
        """
        RESUMO
        Define a sílaba tônica inicial da língua.
        #
        INPUTS
        None
        #
        RETORNO
        str
        #
        EXEMPLO
        >>>class.gerar_tonicidade()
        "oxitona"
        """
        syllables:list[str] = ['oxitona', 'paroxitona', 'proparoxitona']
        chances:list[int] = [50, 40, 10]
        return choices(population = syllables, weights = chances, k = 1)[0]

    def sistema_posicional(self): # <============== ainda estou aqui
        estrutura:list = self.proto_ordem
        if(estrutura == 'SOV'):
            return 'posposicao' if(random()>0.1) else 'preposicao'
        else:
            return 'preposicao' if(random()>0.1) else 'posposicao'

    def ordem_gramatical(self, sistema:str)->str:
        """
        RESUMO
        Apesar de a ordem geral ser determinada antes, eventualmente a posição pode mudar.
        #
        INPUTS
        sistema -> se o afixo geral é 'preposicao', 'posposicao' ou se 'nao_contem'.
        #
        RETORNO
        str
        #
        EXEMPLO
        >>>class.ordem_gramatical('posposicao')
        'posposicao'
        >>>class.ordem_gramatical('preposicao')
        'preposicao'
        >>>class.ordem_gramatical("nao_contem")
        'nao_contem'
        #
        obs.: Mesmo que retorne o mesmo item inserido em sistema:str, em algumas outras iterações
        na classe _dialetos_() pode mudar a ordem dos afixos, incluindo a sua perda.
        """
        if(random()>0.4):
            if(sistema=="preposicao"):
                return "preposicao" if(random()>0.2) else "posposicao"
            else:
                return "posposicao" if(random()>0.2) else "posposicao"
        else:
            return "nao_contem"

    def qual_a_regra(self, classe_gramatical:str)->dict[str, str]|str:
        """
        FUNCAO
        Verifica se a classe_gramatical selecionada é posposição, preposição ou se não existe.
        INPUTS
        RETORNO

        EXEMPLO
        >>>class.qual_a_regra(lingua = "okt", "conjugacao")
        "preposicao"
        >>>class.qual_a_regra(lingua = "okt", "casos")
        "nao_contem"

        'posposicao' -> existe na língua, e o afixo vem depois da raiz;
        'preposicao' -> existe na língua, e o afixo vem antes da raiz;
        'nao_contem' -> significa que não existe essa gramática na língua.
        """
        regra:dict|str = self.proto_lingua['gramatica'][classe_gramatical]
        return regra["regra"] if isinstance(regra, dict) else regra

    def gerar_significado(self, classe_gramatical:str, retornar_dicionario:bool)->str:
        """
        RESUMO
        Gera significado para cada palavra. Na classe class.criar, vai ter apenas palavras básicas
        INPUT
        RETORNO

        EXEMPLO
        """
        # tentei pegar todas as raizes primordiais de cada familia linguistica que conheco,
        # tambem to seguir a "lista de swidesh"
        with open("biblioteca/significados.json", "r", encoding="utf-8") as arquivo:
            significados:dict[str, str] = load(arquivo)
        arquivo.close()

        if(retornar_dicionario):
            return significados
        else:
            significado:str = ""
            generico:str = ""
            if(classe_gramatical == "substantivo"):
                generico = choice(list(significados["substantivo"].keys()))
                significado = choice(significados["substantivo"][generico])
            elif(classe_gramatical == "verbo"):
                generico = choice(list(significados["verbo"].keys()))
                significado = choice(significados["verbo"][generico])
            elif(classe_gramatical == "adjetivo"):
                generico = choice(list(significados["adjetivo"].keys()))
                significado = choice(significados["adjetivo"][generico])
            return significado, generico

    def verificar_ausencia(self, lingua)->None:
        """
        Verifica se algum som foi "criado" em uma palavra devido a encontro consonantal novo,
        e adiciona esse novo som para seu acervo de possibilidades.
        """
        dicionario = lingua['lingua']
        acervo_consoante = lingua['sons']['consoantes']
        for p in dicionario.keys():
            palavra = dicionario[p]['palavra']
            for s in palavra:
                if(s not in acervo_consoante and tools.eh_consoante(s)):
                    acervo_consoante.append(s)

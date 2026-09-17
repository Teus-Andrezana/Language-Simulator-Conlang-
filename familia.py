import tools
from random import random, choice, randint, choices, shuffle, uniform
import copy
import pandas as pd
from re import sub

class FamiliaLinguistica:
    """
        Desenvolve dialetos ou línguas filhas a partir de uma língua-mãe.
        Cria novas palavras, altera os sons existentes, realiza aglutinações para
        novos sentidos e aplica regras de mudanças fonológicas nestas palavras.

        Args:
            quantidade_dialetos (int): Número de dialetos (chaves no dicionário) a serem criados.
            proto_lingua (dict): O dicionário da língua base. Pode ser a língua original ou a
                reutilização de um dialeto gerado anteriormente.
            geracao (int): O nível de geração a qual pertencem esses dialetos na árvore evolutiva.
            lingua_mae (str): Pode ser o nome dado pela língua mãe ou criada.

        Exemplo:
            >>> proto_dialetos = FamiliaLinguistica(quantidade_dialetos = 4, proto_lingua = lingua_mae, geracao = 0)
            >>> ramo_1 = FamiliaLinguistica(quantidade_dialetos = 3, proto_lingua = proto_dialetos["ʐeɦʊ"], geracao = 1)
            >>> ramo_2 = FamiliaLinguistica(random.randint(0,5), proto_dialetos['ryrɐg'], geracao = 1)
            >>> ramo_1_1 = FamiliaLinguistica(quantidade_dialetos=2, proto_lingua=ramo_1["undrɐ"], geracao=2)

        from random import randint, random, choice, choices, shuffle
    """
    def __init__(self, quantidade_dialetos:int, proto_lingua:str, lingua_mae:str, geracao:int):
        # self.lingua_originaria = ramo_originario (vai ter que ser um dicionario)
        self.proto_lingua = proto_lingua
        self.consoantes_especificas = self.proto_lingua["sons"]["consoantes"]
        self.vogais_especificas = self.proto_lingua["sons"]["vogais"]
        self.vogais_gerais:list = list(tools.regra_fonetica['vogal'].keys())
        self.consoantes_gerais:list = list(tools.regra_fonetica['consoante'].keys())
        self.iteracoes:int = 1
        self.geracao:int = geracao
        self.linguas_nao_mutaveis:list[str] = ['original']
        self.nome_lingua_mae:str = lingua_mae
        self.dialetos_criados:dict=self.criar_dialetos(quantidade_dialetos, proto_lingua)

    def nao_mutaveis(self, proto_lingua:str)->None:
        """
        Faz com que a língua selecionada não se altere mais.
        """
        self.linguas_nao_mutaveis.append(proto_lingua)


    # cria os dialetos
    def criar_dialetos(self, quantidade_dialetos:int, proto_lingua)->dict:
        """
        FUNCAO
        Gera novos dialetos tendo base o "original".
        INPUTS
        quantidade_dialetos(int) -> define quantos dialetos serao criados
        classe_lingua            -> eh a classe criar(). Precisa ser definida antes de rodar esta classe FamiliaLinguistica
        RETORNO
        Essa funcao retorna um dicionario com as novas linguas recebendo cada uma um nome na lingua original.
        """
        def criar_afixos(lingua:str)->None:
            dialetos_desenvolvidos[lingua]['gramatica']['afixos'] = {}
            afixos:dict = dialetos_desenvolvidos[lingua]['gramatica']['afixos']
            proto_mae = proto_lingua['lingua']
            afixos['cargo'] = proto_mae[self.retornar_indice('original', choice(["homem", "pessoa", "coisa", "semelhante"]))]['palavra']
            afixos['locativo'] = proto_mae[self.retornar_indice('original', choice(["local", "chao", "terra", "centro", "intestino", "barriga"]))]['palavra']
            afixos['dativo'] = proto_mae[self.retornar_indice('original', choice(["fazer", "dar"]))]['palavra']
            afixos['acusativo'] = proto_mae[self.retornar_indice('original', choice(["outro", "junto", "partir"]))]['palavra']
            afixos['instrumental'] = proto_mae[self.retornar_indice('original', choice(["mao", "usar"]))]['palavra']
            afixos['genitivo'] = proto_mae[self.retornar_indice('original', choice(["relativo", "vir", "vincular"]))]['palavra']

        dialetos_desenvolvidos:dict={}
        idioma_original = "original"
        dialetos_desenvolvidos[idioma_original]=proto_lingua

        palavras_originarias:list[int] = list(proto_lingua["lingua"].keys())
        for _ in range(quantidade_dialetos):
            nome_dialeto = "".join(proto_lingua["lingua"][choice(palavras_originarias)]["palavra"])
            dialetos_desenvolvidos[nome_dialeto]=copy.deepcopy(dialetos_desenvolvidos[idioma_original])
        if("afixos" not in dialetos_desenvolvidos['original']['gramatica'].keys()):
            for nome in dialetos_desenvolvidos.keys():
                if(nome != 'original'):
                    criar_afixos(nome)
                    dialetos_desenvolvidos = self.gerar_palavras_base(nome, dialetos_desenvolvidos)
        return dialetos_desenvolvidos

    def encontrar_palavra_pelo_som(self, lingua, palavra)->None:
        """
        """
        dicionario = self.dialetos_criados[lingua]["lingua"]
        indices:list[int] = dicionario.keys()
        for i in indices:
            palavra_encontrada:list[str] = dicionario[i]
            if(palavra_encontrada["palavra"]==palavra):
                return palavra_encontrada

    def buscar_palavra(self, lingua:str, encontrar_palavra:str)->dict:
        """
        Procura a palavra inserida no dicionario da lingua escolhida. Se colocado "agua"
        a funcao vai retornar qual palavra corresponde a "agua".
        """
        dicionario = self.dialetos_criados[lingua]["lingua"]
        indices_existentes:list[int] = list(dicionario.keys())
        correspondentes_encontradas:dict = {}
        for i in indices_existentes:
            if(encontrar_palavra in dicionario[i]['significado']):
                correspondentes_encontradas[i] = dicionario[i]
        if(len(correspondentes_encontradas.keys())==0):
            return "Sem correspondentes"
        return correspondentes_encontradas

    def buscar_palavra_todas_linguas(self, encontrar_palavra:str)->dict:
        """
        Procura a mesma palavra em todas as liguas da familia. Caso nao encontre,
        vai retornar uma mensagem de "Sem correspondentes".
        Args:
            - encontrar_palavras (str) : recebe somente valores string, procura pela palavra inserida
        Exemples:
            >>> buscar_palavra_todas_linguas(encontrar_palavra = "comida")
        """
        # dicionario que organiza em lingua as palavras que foram encontradas
        palavras_encontradas:dict = {}
        linguas:list[str] = list(self.dialetos_criados.keys())
        for i in linguas:
            palavras_encontradas[i] = self.buscar_palavra(i, encontrar_palavra)
        return palavras_encontradas

    def buscar_indice_fundo(self, lingua:str, indice:int)->list[int]:
        """
        Busca pelo indice inserido, mesmo que a chave do índice já não exista, buscando por
        índices usados em aglutinações.
        Args:
            - lingua (str) : uma chave/língua existente no dicionário
        Exemplo:
        >>> class.buscar_indice_fundo(lingua = 'arkut', indice = 10)
        [520, 665, 670, 701]

        Isso indica que, mesmo que o indice 10 já não exista como uma palavra própria,
        ela está contida em outras palavras.

        >>> class.buscar_indice_fundo(lingua = 'arkut', indice = 43)
        [43]

        Então apenas a palavra inserida existe, sem ter sido agrupada a neologismos.
        """
        lingua:dict[int, dict[str|list[int]]] = self.dialetos_criados[lingua]['lingua']

        indices:list[int] = []
        for i in lingua.keys():
            if(i==indice or indice in lingua[i]['indices']):
                indices.append(i)
        return indices

    def retornar_indice(self, lingua:str, buscar_palavra:str)->int:
        """
        Procura pela palavra inserida e retorna a chave dela no dicionário.
        """
        if(lingua == 'original'):
            indices = list(self.proto_lingua['lingua'].keys())
            for i in indices:
                if(buscar_palavra in self.proto_lingua['lingua'][i]['significado']):
                    return i
        else:
            indices = list(self.dialetos_criados[lingua]['lingua'].keys())
            for i in indices:
                if(buscar_palavra in self.dialetos_criados[lingua]['lingua'][i]['significado']):
                    return i

    def gerar_palavras_base(self, lingua:str, dicionario_base:dict)->None:
        """
        Insere mais palavras básicas que são criadas através de outras palavras.
        Método mais direto e menos dependente de sorte.
        Args:
            lingua (str): Nome da língua (chave) que esteja contida na classe.
        """
        def com_afixos(lingua, c2, palavra):
            c1 = (palavra+palavra) if(isinstance(palavra, str)) else lingua[palavra]['palavra']
            return c1 + c2 if(proto_posicao == 'posposicao') else c2 + c1
        def juntar_compostas(c1, c2, estrutura):
            return c1 + c2 if(estrutura) else c2 + c1

        lingua_mae:dict[str, list[str]|str|list[int]] = self.proto_lingua['lingua']
        proto_gramatica = self.proto_lingua['gramatica']
        proto_posicao = proto_gramatica['posicao']
        estrutura = proto_gramatica['estrutura'] in ['SOV', 'OSV']
        afixos:dict[str,list[str]] = dicionario_base[lingua]['gramatica']['afixos']
        raizes = {
            'pai': self.retornar_indice('original', choice(["sol", "proteger", "cobrir"])) if random() > 0.5 else choice(['da','ta','pa']),
            'mae': choice(['ma', 'na', 'ha']),
            'filho': self.retornar_indice('original', choice(["pedaco", "proteger", "semente", "gerar"])),
            'crianca': (self.retornar_indice('original', 'homem'), self.retornar_indice('original', 'pequeno')),
            'cabeca': choice([
                (self.retornar_indice('original', 'membro'), self.retornar_indice('original', 'alto')),
                (self.retornar_indice('original', 'membro'), self.retornar_indice('original', 'redondo')),
                (self.retornar_indice('original', 'membro'), self.retornar_indice('original', 'topo')),
            ]),
            'olho': choice([
                (self.retornar_indice('original', 'membro'), self.retornar_indice('original', 'semente')),
                (self.retornar_indice('original', 'semelhante'), self.retornar_indice('original', 'semente')),
            ]),
            'estrela': (self.retornar_indice('original', 'topo'), self.retornar_indice('original', 'pedra')),
            # (self.retornar_indice('original', 'topo'), self.retornar_indice('original', 'olho')),
            'ceu': choice([
                (self.retornar_indice('original', 'topo'), self.retornar_indice('original', 'cobrir')),
                (self.retornar_indice('original', 'grande'), self.retornar_indice('original', 'azul')),
                (self.retornar_indice('original', 'alto'), self.retornar_indice('original', 'deus')),
                (self.retornar_indice('original', 'alto'), self.retornar_indice('original', 'arvore')),
            ])
        }
        selecao = {
            0:[com_afixos(lingua_mae, afixos['cargo'], raizes['pai']),
                'substantivo', 'familia'],
            1:[com_afixos(lingua_mae, afixos['cargo'], raizes['mae']),
                'substantivo', 'familia'],
            2:[com_afixos(lingua_mae, afixos['genitivo'], raizes['filho']),
                'substantivo', 'familia'],
            3:[juntar_compostas(lingua_mae[raizes['crianca'][0]]['palavra'], lingua_mae[raizes['crianca'][1]]['palavra'], estrutura),
                'substantivo', 'social'],
            4:[juntar_compostas(lingua_mae[raizes['cabeca'][0]]['palavra'], lingua_mae[raizes['cabeca'][1]]['palavra'], estrutura),
                'substantivo', 'corpo'],
            5:[juntar_compostas(lingua_mae[raizes['olho'][0]]['palavra'], lingua_mae[raizes['olho'][1]]['palavra'], estrutura),
                'substantivo', 'corpo'],
            6:[juntar_compostas(lingua_mae[raizes['estrela'][0]]['palavra'], lingua_mae[raizes['ceu'][1]]['palavra'], estrutura),
                'substantivo', 'natureza'],
            7:[juntar_compostas(lingua_mae[raizes['ceu'][0]]['palavra'], lingua_mae[raizes['ceu'][1]]['palavra'], estrutura),
                'substantivo', 'natureza'],
        }
        if(self.geracao < 1):
            for index, raiz in enumerate(raizes.keys()):
                maximo = max(dicionario_base[lingua]['lingua'].keys())
                nova_palavra:list[str] = selecao[index][0]
                # nova_palavra = tools.iterar_efeitos(nova_palavra, [tools.harmonia_vocal])
                dicionario_base[lingua]['lingua'][maximo+1] = {
                    'palavra':nova_palavra,
                    'classe':selecao[index][1],
                    'significado':[raiz],
                    'generico': [selecao[index][2]],
                    'indices':[raizes[raiz]] if isinstance(raizes[raiz], int) else [],
                    'uso':1.0,
                }

        return dicionario_base

    def gerar_pronomes(self)->None:
        """
        Gera os pronomes basicos iniciais apos determinada quantidade de geracoes/iteracoes.
        Escolhe uma palavra para representar os pronomes.
        É esperado que seja uma família de apenas UMA língua, assim representando
        uma comunidade de falantes em comum inicial.
        Args:
            None
        Retorno:
            None
        """
        def gerar_nos(pronomes, ordem:float)->list[str]:
                return (
                    pronomes['voce'] + pronomes['eu'] if ordem>0.5 else pronomes['eu'] + pronomes['voce']
                )
        def gerar_aquele_genero(dicionario, lingua:str, termo:str)->tuple[list[str] ,list[str]]:
            lista_generos:list[str] = [self.retornar_indice(lingua, 'homem'), self.retornar_indice(lingua, 'mulher')]
            idx_termo:int = self.retornar_indice(lingua, termo)
            return tuple(dicionario[idx_termo]['palavra'] + dicionario[g]['palavra'] for g in lista_generos)
        def gerar_nos_gen(pronomes, ordem)->tuple[list[str], list[str]]:
            lista_pronomes = [pronomes['aquele_h'], pronomes['aquele_m']]
            return tuple(g + pronomes['eu'] if ordem>0.5 else pronomes['eu'] + g for g in lista_pronomes)
        def gerar_plural_gen(pronomes, ordem)->tuple[list[str], list[str]]:
            lista_gen = [pronomes['aquele_h'], pronomes['aquele_m']]
            return tuple(g + pronomes['voce'] if ordem>0.5 else pronomes['voce'] + g for g in lista_gen)

        nome = self.nomes().copy()
        dialetos_gerais = self.dialetos_criados
        dialetos = dialetos_gerais[nome[1]]
        dicionario = dialetos['lingua']
        dialetos['gramatica']['pronomes'] = {}
        pronomes = dialetos['gramatica']['pronomes']
        ordem = random()
        genero = False
        termos_gerais = self.retornar_palavras_do_ramo(nome[1])

        pronomes['eu'] = (
            dicionario[self.retornar_indice(nome[1], choice(['homem', 'coisa', 'cabeca']))]['palavra']
            if('cabeca' in termos_gerais)
            else dicionario[self.retornar_indice(nome[1], choice(['homem', 'coisa']))]['palavra']
        )

        pronomes['voce'] = dicionario[self.retornar_indice(nome[1], choice(['pessoa', 'local']))]['palavra']
        if(random()>0.5):
            pronomes['aquele'] = dicionario[self.retornar_indice(nome[1], choice(['relativo', 'outro']))]['palavra']
        else:
            genero = True
            termo = choice(['relativo', 'outro'])
            pronomes['aquele_h'], pronomes['aquele_m'] = gerar_aquele_genero(dicionario, nome[1], termo)
        if(random()>0.5):
            if(genero):
                if(random()>0.5):
                    pronomes['nos_h'], pronomes['nos_m'] = gerar_nos_gen(pronomes, ordem)
                else:
                    pronomes['nos'] = gerar_nos(pronomes, ordem)
            else:
                pronomes['nos'] = gerar_nos(pronomes, ordem)

        else:
            if(genero):
                aquele = choice(['aquele_h', 'aquele_m'])
                pronomes['nos_inclusivo'] = (
                    pronomes['voce'] + pronomes['eu'] if random()>0.5 else pronomes['eu'] + pronomes['voce']
                )
                pronomes['nos_exclusivo'] = (
                    dialetos['gramatica']['pronomes'][aquele] + pronomes['eu'] if random()>0.5 else pronomes['eu'] + dialetos['gramatica']['pronomes'][aquele]
                )
            else:
                dialetos['gramatica']['pronomes']['nos_inclusivo'] = (
                    pronomes['voce'] + pronomes['eu'] if ordem>0.5 else pronomes['eu'] + pronomes['voce']
                )
                dialetos['gramatica']['pronomes']['nos_exclusivo'] = (
                    pronomes['aquele'] + pronomes['eu'] if ordem>0.5 else pronomes['eu'] + pronomes['aquele']
                )
        if(random()>0.8):
            if(genero):
                pronome_sorteado = choice(['voces', 'dual'])
                pronomes[pronome_sorteado+"h"], pronomes[pronome_sorteado+"m"] = gerar_plural_gen(pronomes, ordem)
            else:
                pronomes[choice(['voces', 'dual'])] = (
                    pronomes['aquele'] + pronomes['voce'] if ordem>0.5 else pronomes['voce'] + pronomes['aquele']
                )

    def nomes(self):
        return list(self.dialetos_criados.keys())

    def sortear_lingua(self):
        return choice(self.nomes())

    def _ver_sons_dialetos(self):
        nomes_dialetos:list= self.nomes()
        dialetos:dict = self.dialetos_criados
        print("Quantidade de dialetos: {}".format(len(nomes_dialetos)-1))
        for nd in nomes_dialetos:
            print(nd, dialetos[nd]['sons']['vogais'])
            print(nd, dialetos[nd]['sons']['consoantes'])

    def atualizar_configuracao(self, lingua)->None:
        """
        Atualiza as probabilidade de uma mudança acontecer, como metatase, epentese, silaba, etc.
        Args:
            - lingua (str) : sequencia de caracteres contido em familia.
        Exemplo:
            >>> class.atualizar_configuracao(lingua_a)
        """
        configuracao:dict[str, float] = self.dialetos_criados[lingua]["configuracao"]
        lista_efeitos:list[str] = list(configuracao.keys())
        for e in lista_efeitos:
            valor_inicial:float = configuracao[e] 
            valor_final:float = uniform(-0.15, 0.15)
            if((valor_final - valor_inicial)<=0.0):
                configuracao[e] = 0.0
            else:
                configuracao[e] = valor_final

    def _desenvolver_acervo_dialeto_(self)->None:
        """
        Atualiza as listas de consoantes e vogais de cada lingua-filha,
        adicionando ou subtraindo os sons de suas línguas.
        Args:
            None
        Retorno:
            None
        """
        dialetos:dict = self.dialetos_criados
        for d in dialetos:
            if(d not in self.linguas_nao_mutaveis):
                vogais:list = dialetos[d]["sons"]["vogais"]
                lista_vogais:list[str] = []
                for vogal in vogais:
                    if(tools.eh_vogal(vogal) and random()<0.1):
                        possibilidades:list = tools.regra_fonetica['vogal'][vogal]['possibilidades']
                        chances:list = tools.regra_fonetica['vogal'][vogal]['chances']
                        nova_vogal:str = choices(population = possibilidades, weights = chances, k = 1)[0]
                        while(tools.eh_consoante(nova_vogal)):
                            nova_vogal = choices(population = possibilidades, weights = chances, k = 1)[0]
                        if(nova_vogal not in vogais and len(nova_vogal)>0):
                            lista_vogais.append(nova_vogal)
                            if(all(i in tools.verificar_classe(vogal) for i in ['fechada', 'aberta']) and (vogal not in vogais)):
                                classe_passe:list[str] = [
                                    ['posterior', 'fechada', 'nao-arredondada'],
                                    ['anterior', 'fechada', 'nao-arredondada'],
                                    ['posterior', 'fechada', 'nao-arredondada'],
                                ]
                                if(tools.verificar_classe(vogal) in classe_passe):
                                    lista_vogais.append(vogal)

                self.dialetos_criados[d]['sons']['vogais'].extend(lista_vogais)
                if(random()<0.1):
                    try:
                        self.dialetos_criados[d]['sons']['vogais'].pop(randint(6,len(self.dialetos_criados[d]['sons']['vogais'])))
                    except:
                        pass

                consoantes:list = dialetos[d]['sons']['consoantes']
                lista_consoantes:list[str] = []
                for consoante in consoantes:
                    if(tools.eh_consoante(consoante) and random()<0.1):
                        possibilidades:list = tools.regra_fonetica['consoante'][consoante]['possibilidades']
                        chances:list = tools.regra_fonetica['consoante'][consoante]['chances']
                        nova_consoante:str = "".join(choices(population = possibilidades, weights=chances, k=1))
                        if(nova_consoante not in consoantes and len(nova_consoante)>0):
                            if(len(nova_consoante)>1):
                                # print(f"L{d}: Consoante {consoante} eh um difono nao registrado")
                                consoante_um:str = nova_consoante[0]
                                if(consoante_um not in consoantes):
                                    # print(f"que teve sua [0] adicionada")
                                    lista_consoantes.append(consoante_um)
                            else:
                                lista_consoantes.append(nova_consoante)
                                # print(f"L{d}: Consoante {consoante} registrado")
                consoantes.extend(lista_consoantes)
                if(random()<0.1):
                    try:
                        consoantes.pop(randint(8,len(consoantes)))
                    except:
                        pass

    def implementar_efeitos(self, lingua:str, word:str)->str:
        """
        Faz passo a passo do processo de desenvolvimento de uma palavra. Função semelhante a tools.surtir_efeito(),
        mas sem o uso de localizadores (loc_1, loc_2).
        Args:
            - lingua (str) : 
            - word (str) : 
        Return:
            str
        Exemple:
            >>> implementar_efeitos(lingua_a, word = "anpagtop")
            "ampaktop"
        """
        silaba_tonica:str = self.dialetos_criados[lingua]["gramatica"]["silaba_tonica"]
        config:dict[str, float] = self.dialetos_criados[lingua]["configuracao"]
        if(isinstance(word, list)):
            word = "".join(word)
        if(random()<0.1):
            word = tools.devoicing(word)
        word = tools.apocope(config["apocope"], silaba_tonica, word)
        word = tools.epenthesis(config["epentese"], word)
        effects:list[callable] = [tools.esquecer, tools.rotica_probida, tools.filtro_fonetico]
        for function in effects:
            word = function(word)
        word = tools.mudancas_w_j(word, self.dialetos_criados[lingua]["sons"]["consoantes"])
        word = tools.assimilar(config['assimilacao'], word)
        word = tools.sandhi(word)
        word = tools.filtro_fonetico(word)
        word = tools.implementar_harmonia(config["harmonia"], word)
        word = tools.retornar_palavra_atona(word, silaba_tonica)
        return word

    def especificacoes_palavra(self, lingua, index)->None:
        """
        Desmetaforiza/especifica palavras.
        Exemplo:
        >>>class.especificacoes_palavra(lingua = "sa", index = 146)
        antes -> {
        'palavra': ['m', 'a', 'ɾ', 'p', 'ʊ', 'ɾ', 'u', 'j', 'ɐ', 'w'],
        'classe': 'substantivo',
        'significado': ['outro', 'chao'],
        'generico': ['quantidade', 'local'],
        'indices': [43, 132],
        'uso': 0.9090128565131315
        }
        depois -> {
        'palavra': ['m', 'a', 'ɾ', 'p', 'ʊ', 'ɾ', 'u', 'j', 'ɐ', 'w'],
        'classe': 'substantivo',
        'significado': ['territorio'],
        'generico': ['politica'],
        'indices': [43, 132],
        'uso': 0.9090128565131315
        }
        """
        especificacoes = self.dialetos_criados[lingua]['lingua'][index]
        sig:list[str] = especificacoes['significado']
        gen:list[str] = especificacoes['generico']

        REGRAS_NEOLOGICAS = [
            #bebida
            {
                'CONDICAO': lambda sig,gen: 'beber' in sig and 'sensorial' in gen,
                'ACAO': lambda sig,gen: ([choice(["bebida", "cha", "alcool", "medicina"])],['bebida'])
            },{
                'CONDICAO': lambda sig,gen: 'beber' in sig and 'tamanho' in gen,
                'ACAO': lambda sig,gen: (['recipiente'],['objeto']),
            },{
                'CONDICAO': lambda sig,gen: 'beber' in sig and any(i in ['caracteristica','carater'] for i in gen),
                'ACAO': lambda sig,gen: ([choice(['cha','alcool','medicina'])], ['comida'])
            },
            #comida
            {
                'CONDICAO': lambda sig,gen: 'comer' in sig and 'corpo' in gen,
                'ACAO': lambda sig,gen: (['carnivo'],['animal'])
            },
            {
                'CONDICAO': lambda sig,gen: 'comer' in sig and 'semente' in gen,
                'ACAO': lambda sig,gen: (['grao'],['comida']) if gen=='semente' else (['herbivoro'],['animal'])
            }, # GRAO
            {
                'CONDICAO': lambda sig,gen: 'grao' in sig and any(i in ['frio','gelo'] for i in gen),
                'ACAO': lambda sig,gen: (['granizo'],['natureza'])
            },
            #bicho
            {
                'CONDICAO': lambda sig,gen: 'bicho' in sig and 'sensorial' in gen,
                'ACAO': lambda sig,gen: (['entidade'],['religiao'])
            },{
                'CONDICAO': lambda sig,gen: 'bicho' in sig and 'aspecto' in gen,
                'ACAO': lambda sig,gen: (['tipo-animal'], ['animal'])
            },{
                'CONDICAO': lambda sig,gen: 'bicho' in sig and 'novo' in gen,
                'ACAO': lambda sig,gen: (['cria'], ['animal'])
            },{
                'CONDICAO': lambda sig,gen: 'bicho' in sig and 'carnivoro' in gen,
                'ACAO': lambda sig,sen: (['canino-felino'], ['animal'])
            },
            {   # PEDRA
                'CONDICAO': lambda sig,gen: 'pedra' in sig and 'gelo' in gen,
                'ACAO': lambda sig,gen: (['granizo'], ['natureza'])
            },{
                'CONDICAO': lambda sig,gen: 'pedra' in sig and 'fogo' in gen,
                'ACAO': lambda sig,gen: (['magma'],['natureza'])
            },{
                'CONDICAO': lambda sig,gen: 'pedra' in sig and ('aspecto' in gen or 'caracteristica' in gen),
                'ACAO': lambda sig,gen: (['tipo-minerio'],['minerio'])
            },{
                'CONDICAO': lambda sig,gen: 'pedra' in sig and 'frio' in gen,
                'ACAO': lambda sig,gen: (['gelo'],['natureza'])
            },
            {   # MEMBRO
                'CONDICAO': lambda sig,gen: 'membro' in sig and 'longo' in gen,
                'ACAO': lambda sig,gen: ([choice(['braco','perna'])], ['corpo'])
            },
            {   # ALTO
                'CONDICAO': lambda sig,gen: 'alto' in sig and 'ceu' in gen,
                'ACAO': lambda sig,gen: ([choice(['pico', 'cordilheira'])],['natureza'])
            },{
                'CONDICAO': lambda sig,gen: 'alto' in sig and 'agua' in gen,
                'ACAO': lambda sig,gen: ([choice(["onda", "mar", "oceano"])],['natureza'])
            },
            { #arvore
                'CONDICAO': lambda sig,gen: 'arvore' in sig and 'corpo' in gen,
                'ACAO': lambda sig,gen: (['tronco'],['botanica'])
            },{
                'CONDICAO': lambda sig,gen: 'arvore' in sig and 'braco' in gen,
                'ACAO': lambda sig,gen: (['galho'],['botanica'])
            },{
                'CONDICAO': lambda sig,gen: 'arvore' in sig and 'perna' in gen,
                'ACAO': lambda sig,gen: ([choice(['raiz','ramo'])],['botanica'])
            },{
                'CONDICAO': lambda sig,gen: 'arvore' in sig and any(i in ['animal', 'natureza', 'tamanho'] for i in gen),
                'ACAO': lambda sig, gen: (['tipo-arvore'],['botanica'])
            },{
                'CONDICAO': lambda sig,gen: 'arvore' in sig and 'familia' in gen,
                'ACAO': lambda sig, gen: (['arvore-sagrada'],['cultura','botanica'])
            },{
                'CONDICAO': lambda sig,gen: 'arvore' in sig and 'quantidade' in gen,
                'ACAO': lambda sig, gen: ([choice(['bosque', 'floresta'])],['natureza'])
            },
            { #planta
                'CONDICAO': lambda sig,gen: 'planta' in sig and 'filho' in gen,
                'ACAO': lambda sig,gen: ([choice(['flor','ramo','semente'])],['botanica'])
            },
            { #outro
                'CONDICAO': lambda sig,gen: 'outro' in sig and any(i in ['chao','terra'] for i in gen),
                'ACAO': lambda sig,gen: (['territorio'], ['politica'])
            },
            { #carne
                'CONDICAO': lambda sig,gen: 'carne' in sig and 'aspecto' in gen,
                'ACAO': lambda sig,gen: ([choice(["doente", "podre", "ferida", "inflamacao"])], ['estado'])
            },{ #agora
                'CONDICAO': lambda sig,gen: 'agora' in sig and 'mao' in gen,
                'ACAO': lambda sig,gen: ([choice(["apoio", "ajuda", "auxilio", "soco", "golpe", "agilidade", "segurar"])], ['social'])
            },{ #vento
                'CONDICAO': lambda sig,gen: 'vento' in sig and any(i in ['agua', 'molhado'] for i in gen),
                'ACAO': lambda sig,gen: ([choice(['chuva', 'tormenta', 'tempestade', 'umidade'])], ['tempo'])
            },{ #cair
                'CONDICAO': lambda sig,gen: 'cair' in sig and any(i in ['agua', 'molhado'] for i in gen),
                'ACAO': lambda sig,gen: ([choice(['chuva', 'tormenta', 'tempestade', 'vendaval'])], ['tempo']) if(random()>0.5) else (['cachoeira'],['natureza'])
            },{ #agua
                'CONDICAO': lambda sig,gen: 'agua' in sig and 'frio' in gen,
                'ACAO': lambda sig,gen: (['gelo'],['natureza'])
            },
            {
                'CONDICAO': lambda sig,gen: 'agua' in sig and any(i in ['filho', 'nascer'] for i in gen),
                'ACAO': lambda sig,gen: ([choice(["riacho", "nascente", "fonte"])],['natureza'])
            },
            {
                'CONDICAO': lambda sig,gen: 'agua' in sig and 'local' in gen,
                'ACAO': lambda sig,gen: ([choice(["rio", "fonte", "lago"])],['natureza'])
            },
            {
                'CONDICAO': lambda sig,gen: 'agua' in sig and any(i in ['noite', 'dia', 'espirito'] for i in gen),
                'ACAO': lambda sig,gen: (['espirito-agua'],['religiao'])
            },
            {
                'CONDICAO': lambda sig,gen: 'agua' in sig and any(i in ["deus", "pai", "mae", "avo", "anciao"] for i in gen),
                'ACAO': lambda sig,gen: ([choice(["deus-agua", "divindade-agua"])],['religiao'])
            },
            {
                'CONDICAO': lambda sig,gen: 'agua' in sig and any(i in ['pedra','terra','chao'] for i in gen),
                'ACAO': lambda sig,gen: (['lama'],['natureza'])
            },{
                'CONDICAO': lambda sig,gen: 'agua' in sig and 'grande' in gen,
                'ACAO': lambda sig,gen: ([choice(['mar','rio','lago','enchente'])],['natureza'])
            },{ #TODO
                'CONDICAO': lambda sig,gen: 'todo' in sig and 'terra' in gen,
                'ACAO': lambda sig,gen: ([choice(["territorio", "vila", "nacao"])],['politica']) if(random()>0.5) else ([choice(["local", "plano", "chao"])], ['politica'])
            },{
                'CONDICAO': lambda sig,gen: 'todo' in sig and 'social' in gen,
                'ACAO': lambda sig,gen: ([choice(['reuniao', 'motim', 'ritual', 'musica', 'evento', 'festival', 'grupo'])],['social'])
            },{
                'CONDICAO': lambda sig,gen: 'todo' in sig and 'bicho' in gen,
                'ACAO': lambda sig,gen: (['rebanho'],['bicho'])
            },{
                'CONDICAO': lambda sig,gen: 'todo' in sig and 'tipo-animal' in gen,
                'ACAO': lambda sig,gen: ([f'coletivo-de-{"".join(especificacoes['palavra'])}'],['bicho'])
            },{ #COISA
                'CONDICAO': lambda sig,gen: 'coisa' in sig and 'morder' in gen,
                'ACAO': lambda sig,gen: (['bicho'], ['animal'])
            },{
                'CONDICAO': lambda sig,gen: 'coisa' in sig and any(i in ['natureza', 'botanica'] for i in gen),
                'ACAO': lambda sig,gen: (['simbolo-religioso'], ['religiao'])
            },{
                'CONDICAO': lambda sig,gen: 'coisa' in sig and any(i in ["animal", "corpo", "familia"] for i in gen),
                'ACAO': lambda sig,gen: (['criatura-mitologia'], ['religiao'])
            },{
                'CONDICAO': lambda sig,gen: 'espirito' in sig and 'vento' in gen,
                'ACAO': lambda sig,gen: ([choice(["criatura-mitologica", 'espirito-vento'])], ['religiao'])
            },{
                'CONDICAO': lambda sig,gen: 'coisa' in sig and any(i in ['so', 'unico'] for i in gen),
                'ACAO': lambda sig,gen: (['um'], ['quantidade'])
            },
            { #CORPO
                'CONDICAO': lambda sig,gen: 'corpo' in sig and 'mole' in gen,
                'ACAO': lambda sig,gen: (['fraco'],['caracteristica'])
            },
            { # DEDO
                'CONDICAO': lambda sig,gen: 'dedo' in sig and any(i in ['so', 'unico'] for i in gen),
                'ACAO': lambda sig,gen: (['um'], ['quantidade'])
            },
            { #FOGO
                'CONDICAO': lambda sig,gen: 'fogo' in sig and 'corpo' in gen,
                'ACAO': lambda sig,gen: ([choice(["doente", "ferida", "inflamacao", "febre", "dor", "queimadura"])], ['estado'])
            },{
                'CONDICAO': lambda sig,gen: 'fogo' in sig and 'corpo' in gen,
                'ACAO': lambda sig,gen: ([choice(["sol", "estrela", "cometa", "aurora"])], ['natureza']) if(random()>0.5) else (['caminho'],['local'])
            },{
                'CONDICAO': lambda sig,gen: 'fogo' in sig and any(i in ['noite','dia', 'espirito'] for i in gen),
                'ACAO': lambda sig,gen: (['espirito-fogo'],['religiao'])
            },{
                'CONDICAO': lambda sig,gen: 'fogo' in sig and any(i in ["deus", "pai", "mae", "avo", "anciao"] for i in gen),
                'ACAO': lambda sig,gen: ([choice(["deus-fogo", "divindade-fogo"])],['religiao'])
            },{
                'CONDICAO': lambda sig,gen: 'fogo' in sig and any(i in ["beber", "bebida"] for i in gen),
                'ACAO': lambda sig,gen: ([choice(["sopa", "cha", "alcool"])],['bebida'])
            },{
                'CONDICAO': lambda sig,gen: 'fogo' in sig and any(i in ["comer", "comida"] for i in gen),
                'ACAO': lambda sig,gen: ([choice(["tipo-pimenta", "tipo-comida"])],['comida'])
            },{
                'CONDICAO': lambda sig,gen: 'fogo' in sig and 'carne' in gen,
                'ACAO': lambda sig,gen: (['churrasco'],['comida'])
            },{
                'CONDICAO': lambda sig,gen: 'fogo' in sig and 'bicho' in gen,
                'ACAO': lambda sig,gen: ([choice(['bicho-quente','bicho-pelado'])],['animal'])
            },{ #FRIO
                'CONDICAO': lambda sig,gen: 'frio' in sig and 'bicho' in gen,
                'ACAO': lambda sig,gen: ([choice(["bicho-frio", "bicho-peludo"])],['animal'])
            },{
                'CONDICAO': lambda sig,gen: 'frio' in sig and any(i in ['homem', 'mulher', 'espirito'] for i in gen),
                'ACAO': lambda sig,gen: (['espirito-frio','criatura-mitologica'],['religiao']) if random()>0.5 else ([choice(['insulto', 'jeito'])],['social'])
            },{
                'CONDICAO': lambda sig,gen: 'frio' in sig and any(i in ['pessoa', 'povo'] for i in gen),
                'ACAO': lambda sig,gen: ([choice(['povo-frio', 'gelados'])], ['politica'])
            },{
                'CONDICAO': lambda sig,gen: 'frio' in sig and 'corpo' in gen,
                'ACAO': lambda sig,gen: ([choice(["paralisia", "congelado", "derrame", "travado"])],['estado'])
            },{ #VELHO
                'CONDICAO': lambda sig,gen: 'velho' in sig and any(i in ["noite", "dia"] for i in gen),
                'ACAO': lambda sig,gen: ([choice(["ontem", "passado"])],['tempo'])
            },{
                'CONDICAO': lambda sig,gen: 'velho' in sig and any(i in ["pai", "mae"] for i in gen),
                'ACAO': lambda sig,gen: (['avo'],['familia']) if(random()>0.5) else ([choice(["anciao", "cura", "xama", "mago"])],['social'])
            },{ #NOVO
                'CONDICAO': lambda sig,gen: 'novo' in sig and any(i in ["noite", "dia"] for i in gen),
                'ACAO': lambda sig,gen: ([choice(["amanha", "futuro"])],['tempo'])
            },{ #NOITE
                'CONDICAO': lambda sig,gen: 'noite' in sig and 'caracteristica' in gen,
                'ACAO': lambda sig,gen: ([choice(["criatura-noite","espirito-noite"])],['religiao'])
            },{ #HOMEM E MULHER
                'CONDICAO': lambda sig,gen: 'homem' in sig and 'mole' in gen,
                'ACAO': lambda sig,gen: (['fraco'],['caracteristica']) if(random()>0.5) else (['doente'],['estado'])
            },{
                'CONDICAO': lambda sig,gen: 'mulher' in sig and any(i in ['vermelho','fluido','sangue'] for i in gen),
                'ACAO': lambda sig,gen: (['menstruacao'],['corpo'])
            },{
                'CONDICAO': lambda sig,gen: any(i in ['homem','mulher'] for i in sig) and any(i in ['frio','quente'] for i in gen),
                'ACAO': lambda sig,gen: ([choice(["doente", "ferida", "inflamacao", "febre", "queimadura"])],['estado'])
            },{ #FAZER
                'CONDICAO': lambda sig,gen: 'fazer' in sig and 'nascer' in gen,
                'ACAO': lambda sig,gen: (['criar'],['manipulacao'])
            },{
                'CONDICAO': lambda sig,gen: 'fazer' in sig and 'dormir' in gen,
                'ACAO': lambda sig,gen: ([choice(['desmaiar','matar'])],['manipulacao'])
            },{
                'CONDICAO': lambda sig,gen: 'fazer' in sig and 'morrer' in gen,
                'ACAO': lambda sig,gen: (['matar'],['manipulacao'])
            },{ #PARTIR
                'CONDICAO': lambda sig,gen: 'partir' in sig and any(i in ['pele','cabeca','pescoco'] for i in gen),
                'ACAO': lambda sig,gen: ([choice(['matar','esfolar'])],['manipulacao'])
            },
            {   # DIVIDIR
                'CONDICAO': lambda sig,gen: 'dividir' in sig and 'organizar' in gen,
                'ACAO': lambda sig,gen: (['contar'],['necessidade'])
            },{
                'CONDICAO': lambda sig,gen: 'dividir' in sig and 'agua' in gen,
                'ACAO': lambda sig,gen: (['afluente'],['natureza']) if random()>0.3 else (['desvio'], ['local'])
            },
            {
                'CONDICAO':lambda sig,gen: 'dividir' in sig and 'dividir' in gen,
                'ACAO': lambda sig,gen: (['fracao'],['conceito'])
            },
            {   # NUMERO
                'CONDICAO': lambda sig,gen: 'dois' in sig and 'mao' in gen,
                'ACAO': lambda sig,gen: (['sete'],['quantidade'])
            },{
                'CONDICAO': lambda sig,gen: any(i in ['varios','muito','mao_outro','mao'] for i in sig) and 'mao' in gen,
                'ACAO': lambda sig,gen: (['dez'],['quantidade']),
            },{ # COR
                'CONDICAO': lambda sig,gen: 'fluido' in sig and any(i in ["pele", "corpo"] for i in gen),
                'ACAO': lambda sig,gen: ([choice(['suor','sangue'])], ['corpo']) if random()>0.5 else ([choice(['vermelho'])], ['aspecto']),
            },{
                'CONDICAO': lambda sig,gen: 'agua' in sig and 'agua' in gen,
                'ACAO': lambda sig,gen: (['azul'], ['aspecto']) if random()>0.5 else (['mar', 'rio'], ['natureza']),
            },
            {   # SEMELHANTE
                'CONDICAO': lambda sig,gen: 'semelhante' in sig and 'ceu' in gen,
                'ACAO': lambda sig,gen: ([choice(['agua','mar','oceano'])], ['natureza']),
            },{
                'CONDICAO': lambda sig,gen: 'semelhante' in sig and 'outro' in gen,
                'ACAO': lambda sig,gen: (['diferente'], ['quantidade']),
            },{
                'CONDICAO': lambda sig,gen: 'semelhante' in sig and 'pai' in gen,
                'ACAO': lambda sig,gen: (['tio'], ['familia']),
            },{
                'CONDICAO': lambda sig,gen: 'semelhante' in sig and 'mae' in gen,
                'ACAO': lambda sig,gen: (['tia'], ['familia']),
            },{
                'CONDICAO': lambda sig,gen: 'semelhante' in sig and 'sangue' in gen,
                'ACAO': lambda sig,gen: (['vermelho'], ['cor']),
            },
            { # EXISTIR
                'CONDICAO': lambda sig,gen: 'existir' in sig and any(i in ['so', 'unico'] for i in gen),
                'ACAO': lambda sig,gen: (['um'], ['quantidade']),
            },
            {   # SEMENTE
                'CONDICAO': lambda sig,gen: 'semente' in sig and 'relativo' in gen,
                'ACAO': lambda sig,gen: (['grao'], ['comida'])
            },
        ]

        iter = 0
        for r in REGRAS_NEOLOGICAS:
            if(r['CONDICAO'](sig,gen)):
                especificacoes['significado'],especificacoes['generico'] = r['ACAO'](sig,gen)
                break
            elif(r['CONDICAO'](gen,sig)):
                especificacoes['significado'],especificacoes['generico'] = r['ACAO'](gen,sig)
                break
            elif(r['CONDICAO'](sig,sig)):
                especificacoes['significado'],especificacoes['generico'] = r['ACAO'](sig,sig)
                break
            elif(r['CONDICAO'](gen,gen)):
                especificacoes['significado'],especificacoes['generico'] = r['ACAO'](gen,gen)
            iter+=1
        if(iter>=len(REGRAS_NEOLOGICAS)):
            del especificacoes

    """
    Nao faz sentido criar toda hora palavras aleatórias.
    Vale a pena induzir as esoclhas de forma que faça sentido.
    Bicho+chao=terrestre
    Bicho+pote=nao deveria existir
    """

    def gerar_nova_palavra(self, lingua:str, iter:int)->None:
        """
        """

        def aglutinar(estrutura, dicionario_palavra:list[str], palavra_par:list[str])->list[str]:
            if(estrutura in ["SVO", "SOV", "OSV"]):
                p_1 = dicionario_palavra['palavra']
                p_2 = palavra_par['palavra']
                return (p_2 + p_1, 'verbo') if(dicionario_palavra['classe'] == 'verbo') else (p_1 + p_2, palavra_par['classe'])
            elif(estrutura in ["OVS", "VSO","VOS"]):
                p_1 = dicionario_palavra['palavra']
                p_2 = palavra_par['palavra']
                return (p_1 + p_2, 'verbo') if(dicionario_palavra['classe'] == 'verbo') else (p_2 + p_1, dicionario_palavra['classe'])

        dicionario_de_pares:dict[str,list[str]] = {
            'agora':('mao'),
            'agua':('familia','nascer','local','anciao','pedra','terra','chao','grande','dividir','alto'),
            'alto':('terra','ceu','agua'),
            'arvore':('corpo','braco','perna','animal','natureza','tamanho','familia','quantidade'),
            'beber':('sensorial','tamanho','caracteristica','carater'),
            'bicho':('sensorial','aspecto','novo','todo'),
            'carne':('aspecto'),
            'cair':('molhado','agua'),
            'ceu':('alto', 'semelhante'),
            'coisa':('natureza','botanica','animal','corpo','familia','morder', 'so', 'unico'),
            'corpo':('fio','chao','mole', 'mao'),
            'comer':('corpo','botanica'),
            'dedo': ('so', 'unico'),
            'dividir':('organizar', 'dividir'),
            'fazer':('nascer','dormir','morrer'),
            'fogo':('corpo','ceu','noite','dia','familia','anciao','comida','comer','bebida','beber'),
            'frio':('pessoa','corpo','animal','grao'),
            'gelo':('grao','pedra'),
            'grao':('frio','gelo'),
            'manipulacao':('pele','morrer'),
            'mao':('agora', 'corpo'),
            'membro':('alto', 'topo','longo'),
            'mudar':('corpo','natureza'),
            'organizar':('dividir'),
            'nascer':('agua','fazer'),
            'pedra':('gelo','ceu','fogo','aspecto', 'agua'),
            'relativo':('semente'),
            'semelhante':('ceu','sangue','agua','mae','pai'),
            'semente':('relativo'),
            'terra':('alto', 'todo', 'agua'),
            'tipo-bicho':('todo'),
            'todo':('social','terra','bicho','tipo-bicho'),
            'vento':('agua','molhado'),

        }
        dicionario = self.dialetos_criados[lingua]['lingua']
        indices = list(dicionario.keys())
        indices_limitados = indices[:len(self.dialetos_criados['original']['lingua'].keys())]

        for _ in range(iter):
            shuffle(indices_limitados)
            index = choice(indices_limitados)
            dicionario_palavra = dicionario[index]
            contador = 0
            while((dicionario_palavra['significado'][0] or dicionario_palavra['generico'][0]) not in dicionario_de_pares.keys()):
                index = indices_limitados[contador]
                dicionario_palavra = dicionario[index]
                contador+=1
            significado = dicionario_palavra['significado'][0]
            combinacoes:list[str] = list(dicionario_de_pares[significado])

            shuffle(indices_limitados)
            palavra_par:dict[str,list[str]] = {}
            index_2:int = 0
            for i in indices_limitados:
                dic_palavra_temporaria:dict[str,list[str]] = dicionario[i]
                if(any(i in dic_palavra_temporaria['significado'] for i in combinacoes) or any(i in dic_palavra_temporaria['generico'] for i in combinacoes)):
                    palavra_par = dic_palavra_temporaria
                    index_2 = i
                    break
            if(len(palavra_par.keys())>0):
                estrutura:list[str] = self.dialetos_criados[lingua]['gramatica']['estrutura']
                aglutinacao, classe_gramatical = aglutinar(estrutura, dicionario_palavra, palavra_par)
                significado = dicionario_palavra['significado'] + palavra_par['significado']
                generico = dicionario_palavra['generico'] + palavra_par['generico']
                silaba_tonica:str = self.dialetos_criados[lingua]['gramatica']['silaba_tonica']
                aglutinacao = self.implementar_efeitos(lingua, aglutinacao)
                # aglutinacao = iterar_efeitos(aglutinacao, [harmonia_vocal])
                self.dialetos_criados[lingua]['lingua'][max(indices)+1] = {
                    'palavra': aglutinacao,
                    'classe': classe_gramatical,
                    'significado': significado,
                    'generico': generico,
                    'indices': [index, i],
                    'uso': 1.0,
                }
                self.especificacoes_palavra(lingua, max(indices)+1)

    def assimilar_gramatica(self, sistema_linguistico:dict, gramatica:str)->None:
        """
        RESUMO
            Verifica alguma similaridade fonetica na gramatica, podendo fundir
            casos, generos, pronomes...
        PARAMETRO
            gramatica -> espera uma string "casos", "pronomes" e "generos"
        RETORNO
            None
        EXEMPLO
        >>>assimilar_gramatica(class.dialetos_criados, "pronomes")
        """
        # deletar declinações iguais
        if(self.qual_a_regra('original', gramatica) != "nao_contem"):
            # print("É um dicionario")
            for dialeto in sistema_linguistico.keys():
                if(dialeto!="original"):
                        casos = sistema_linguistico[dialeto]["gramatica"][gramatica]
                        nomes = [n for n in sistema_linguistico[dialeto]["gramatica"][gramatica].keys() if n!="regra"]
                        # print(casos, nomes)
                        i:int = 0
                        while(i < len(nomes)):
                            caso_um = nomes[i]
                            # print(caso_um)
                            j:int=0
                            while(j < len(nomes)):
                                caso_dois = nomes[j]
                                # print(caso_dois)
                                if(caso_um!=caso_dois):
                                    if(any(i in [caso_um, caso_dois] for i in sistema_linguistico[dialeto]["gramatica"][gramatica].keys())):
                                        try:
                                            c1 = casos[caso_um]
                                            c2 = casos[caso_dois]
                                            semelhanca:float = self._semelhanca_de_palavras_(c1, c2)
                                            if(semelhanca>0.85):
                                                if(caso_dois in casos):
                                                    del casos[caso_dois]
                                                nomes.pop(i+1)
                                        except:
                                            # print("erro ignorado")
                                            pass

                                j+=1
                            i+=1

    def _adaptar_gramatica_(self, lingua_alvo:dict): # <============
        """
        FUNCAO
        INPUTS
        RETORNO

        EXEMPLO
        >>>
        """
        conjunto:list = list(self.dialetos_criados[lingua_alvo]["gramatica"].keys())
        vogais:list[str] = list(self.dialetos_criados[lingua_alvo]['sons']['vogais'])
        consoantes:list[str] = list(self.dialetos_criados[lingua_alvo]['sons']['consoantes'])
        for materia in conjunto:
            gramatica:dict = self.dialetos_criados[lingua_alvo]["gramatica"][materia]
            if(isinstance(gramatica, dict)):
                silaba_tonica:str = self.dialetos_criados[lingua_alvo]['gramatica']['silaba_tonica']
                for assunto in gramatica:
                    index:int = 0
                    if(assunto != "regra"):
                        palavra:str = gramatica.get(assunto) # <============== parei aqui
                        palavra:list[str] = tools.corrigir_palavra(list(palavra))
                        # print(palavra)
                        for letra, som_antigo in enumerate(palavra):
                            if(tools.eh_vogal(som_antigo)):
                                som_max_vogal:float=0.0
                                sons_parecidos_sorteados:list[str] = []
                                chances:list[float] = []
                                som_novo:str=""
                                for som_novo in vogais: ## ele vê letra por letra da palavra
                                    if(som_novo!=som_antigo):
                                        semelhanca_vogais:float = tools.semelhanca_entre_sons(som_antigo, som_novo)
                                        if(semelhanca_vogais>=som_max_vogal): # use o som_max_vogal para substituir o valor
                                            som_max_vogal = semelhanca_vogais
                                            sons_parecidos_sorteados.append(som_novo)
                                            chances.append(1/2 if(len(sons_parecidos_sorteados)==1) else chances[-1]/2)
                                        index+=1
                                # checa no mesmo loop cada som que tem no acervo e então muda para o novo som
                                sons_parecidos_sorteados.insert(0, som_antigo)
                                chances.insert(0, 1.0)
                                palavra[letra] = choices(population = sons_parecidos_sorteados, weights = chances)[0]

                            elif(tools.eh_consoante(som_antigo)):
                                if(len(som_antigo)>0):
                                    if(som_antigo not in self.consoantes_gerais):
                                        if(random()>0.4):
                                            som_max_consoante:float = 0.0
                                            som_novo:str = ""
                                            consoantes_sorteadas:list = []
                                            for som_novo in consoantes:
                                                semelhanca_consoantes:float = tools.semelhanca_entre_sons(som_antigo, som_novo)
                                                if(semelhanca_consoantes>=som_max_consoante): # use o som_max_consoante para substituir o valor
                                                    if(semelhanca_consoantes>som_max_consoante):
                                                        som_max_consoante = semelhanca_consoantes
                                                        consoantes_sorteadas = []
                                                        consoantes_sorteadas.append(som_novo)
                                                    else:
                                                        consoantes_sorteadas.append(som_novo)
                                                index+=1
                                            palavra[letra] = choice(consoantes_sorteadas)

                                        else:
                                            if(len(som_antigo)>1):
                                                som_novo = som_antigo[0]
                                                possibilidades:list = tools.regra_fonetica['consoante'][som_antigo]['possibilidades']
                                                chances:list = tools.regra_fonetica['consoante'][som_antigo]['chances']
                                                som_escolhido = "".join(choices(population=possibilidades, weights=chances, k=1))
                                                palavra[letra] = f"{som_escolhido}{som_antigo[1]}"
                                            else:
                                                possibilidades:list = tools.regra_fonetica['consoante'][som_antigo]['possibilidades']
                                                chances:list = tools.regra_fonetica['consoante'][som_antigo]['chances']
                                                palavra[letra] = "".join(choices(population=possibilidades, weights=chances, k=1))
                                            continue
                                    else:
                                        som_max_consoante:float=0.0
                                        som_novo:str = ""
                                        consoantes_sorteadas:list = []
                                        for som_novo in consoantes:
                                            semelhanca_consoantes:float = tools.semelhanca_entre_sons(som_antigo, som_novo)
                                            if(semelhanca_consoantes>=som_max_consoante): # use o som_max_consoante para substituir o valor
                                                if(semelhanca_consoantes>som_max_consoante):
                                                    som_max_consoante = semelhanca_consoantes
                                                    consoantes_sorteadas.clear()
                                                    consoantes_sorteadas.append(som_novo)
                                                else:
                                                    consoantes_sorteadas.append(som_novo)
                                            index+=1
                                            palavra[letra] = choice(consoantes_sorteadas)
                        palavra = tools.retornar_palavra_atona(
                            "".join(palavra),
                            silaba_tonica
                        )
                        self.dialetos_criados[lingua_alvo]["gramatica"][materia][assunto] = palavra

    def _perder_significado_(self):
        """
        FUNCAO
        INPUTS
        RETORNO

        EXEMPLO
        >>>
        """
        for i in self.dialetos_criados.keys():
            for j in self.dialetos_criados[i]['lingua']:
                if(j in self.dialetos_criados[i]['lingua']):
                    significados = self.dialetos_criados[i]['lingua'][j]['significado']
                    quantidade_significados:int = len(significados)
                    if(quantidade_significados>2):
                        # print(f"Antigo: {i}, {j}, {self.dialetos_criados[i]['lingua'][j]['significado']}")
                        if(random()>(1.8/quantidade_significados)):
                            index:int = 0
                            # print(significados)
                            while(index<randint(1,len(significados)-1) or len(significados)>3):
                                significados.pop(randint(0,len(significados)-1))
                                index+=1
                            # print(f"Novo: {self.dialetos_criados[i]['lingua'][j]['significado']}\n")

        """
        preciso fazer com que, se houver um som novo clusterizado, no novo acervo adicione sua versão não clusterizada.
        provavelmente terei de criar uma class ou def para tratar essas situações dialetos e mudanças sonoras.
        --------
        pode ser interessante fazer um sistema de escolha, onde, apesar de alguns sons retornarem 1.0, sorteia entre aqueles que também deram o valor máximo

        """

    def lenicao_gramatical(self)->None:
        """
        Intensifica as chances de lenicionar.
        Considerando a ideia que palavras cotidianas que estão se gramaticalizando
            sofrem muito mais erosão que as demais palavras.
        """
        def por_efeito(lingua:str, palavra:str, silaba_tonica)->list[str]:
            vogais:list[str] = "".join(list(tools.regra_fonetica['vogal'].keys()))
            lista_efeitos = [
                (r'p$', 'b'), (r'k$', 'g'), (r't$', 'd'), (r'[hmn]$', ''),
                (r's$', 'z'), (rf'[bdg]$|(?=[{vogais}])[bdg]|[bdg](?<=[{vogais}])', ''),
                (r'[aäʌɑæ]', 'ɐ'), (r'[ie]', 'ɪ'), (r'[ɐɪʊə]$', ''),
                (r'[u]', 'ʊ'), (r'[øɶ]', 'œ'), (r'[ø]', 'ə'), (r'[y]', 'ʏ'),
                (r'[ɞ]', 'ɵ'), (r'[ɤ]', 'ʌ'),
            ]
            efeito = choice(lista_efeitos)
            palavra = "".join(palavra)
            palavra = sub(efeito[0], efeito[1], palavra)
            palavra = tools.corrigir_palavra(list(palavra))
            palavra = self.implementar_efeitos(lingua, palavra)
            palavra = tools.sandhi(palavra)
            palavra = tools.retornar_palavra_atona(palavra, silaba_tonica)
            return palavra

        for nome in self.nomes():
            if(nome not in self.linguas_nao_mutaveis):
                gramatica = self.dialetos_criados[nome]['gramatica']
                for assunto in gramatica.keys():
                    if(assunto not in ['estrutura', 'silaba_tonica', 'posicao']):
                        # print(assunto)
                        for pessoa in gramatica[assunto]:
                            if(len(gramatica[assunto][pessoa])>1):
                                gramatica[assunto][pessoa] = por_efeito(nome, gramatica[assunto][pessoa], gramatica['silaba_tonica'])

    def adaptar_palavras(self)->None:
        """

        """
        def retornar_semelhante(lingua:str, som_antigo:str)->str:
            """
            """
            som_selecionado:list[str] = []
            chances:list[float] = []

            tipo = "vogais" if(tools.eh_vogal(som_antigo)) else "consoantes"
            for novo_som in self.dialetos_criados[lingua]['sons'][tipo]:
                if(novo_som != som_antigo):
                    similaridade:float = tools.semelhanca_entre_sons(som_antigo[0], novo_som[0])
                    proximos:list[str] = tools.regra_fonetica["vogal" if tipo == "vogais" else "consoante"][som_antigo[0]]["possibilidades"]
                    if(similaridade>=0.5 and novo_som in proximos):
                        som_selecionado.append(novo_som)
                        chances.append(1/6 if(len(som_selecionado)==1) else round(chances[-1]/6, 4))
            som_selecionado.insert(0, som_antigo)
            chances.insert(0, 1.0)
            return choices(population = som_selecionado, weights = chances)[0]

        def ajustar_palavra(lingua:str, palavra:str)->str:
            """
            """
            nova_palavra:list[str] = []
            palavra = tools.corrigir_palavra(list(palavra))
            for som_antigo in palavra:
                nova_palavra.append(retornar_semelhante(lingua, som_antigo))
            return "".join(nova_palavra)
        
        linguas = self.dialetos_criados
        for nome in linguas.keys():
            if(nome not in self.linguas_nao_mutaveis):
                descritivo = linguas[nome]
                dicionario = descritivo["lingua"]
                # silaba_tonica:str = descritivo["gramatica"]["silaba_tonica"]
                for i in dicionario.keys():
                    palavra = dicionario[i]["palavra"]
                    palavra = ajustar_palavra(nome, palavra)
                    dicionario[i]["palavra"] = self.implementar_efeitos(nome, palavra)
                self.gerar_nova_palavra(nome, 100)
    
    def desenvolver_filhas(self, loops:int)->None: # iteracoes
        """
        classe -> precisa da variável proveniente da classe FamiliaLinguistica
        """
        for i in range(loops):
            self._desenvolver_acervo_dialeto_()
            self.adaptar_palavras()
            # esse if eh mais para dar algum tempo em que os casos gramaticais se fundem
            """
            if(self.iteracoes%3==0):
                casos:list[str] = ["casos", "genero", "conjugacao"]
                for caso in casos:
                    # print(caso)
                    self.assimilar_gramatica(self.dialetos_criados, caso)
            """
            if(self.iteracoes>=2 and "pronomes" not in self.dialetos_criados['original']['gramatica'].keys()):
                self.gerar_pronomes()

            if(any(i in ['pronomes', 'conjugacao', 'afixos'] for i in self.dialetos_criados['original']['gramatica'].keys())):
                self.lenicao_gramatical()
            self._perder_significado_()
            self._ver_sons_dialetos()
            self.iteracoes+=1

    def contar_significados(self, lingua:str, buscar_palavra:str)->int:
        """
        Conta quantos buscar_palavra tem no dicionario da lingua.

        Parametros:
            lingua (str): o nome de uma lingua que esteja contida na classe inserida
            buscar_palavra (str): palavra que deseja buscar
        Exemplo:
        >>> contar_significados_lexico(lingua = 'ozga', buscar_palavra = 'comer')
        3
        """
        contador:int = 0
        dicionario:dict[str,list[str]] = self.dialetos_criados[lingua]['lingua']
        indices:set[int] = set(self.dialetos_criados[lingua]['lingua'].keys())
        for i in indices:
            if(buscar_palavra in dicionario[i]['significado']):
                contador+=1
        return contador

    def _substantivo_(self, nomes_dialetos:list[str], substantivos:list[str], significados_substantivos:list[str], numero:int, index:str)->str:
        """
        FUNCAO
        INPUTS
        RETORNO

        EXEMPLO
        >>>
        """
        regra:str = self.qual_a_regra(nomes_dialetos[numero], "afixos")
        substantivo_escolhido:str = choice(substantivos)
        significado:str = significados_substantivos[substantivos.index(substantivo_escolhido)]
        if(regra!="nao_contem"):
            caso:str; lista_casos:list[str]
            lista_casos = list(self.dialetos_criados[nomes_dialetos[numero]]["gramatica"]["afixos"].keys())
            if(index=="S"):
                caso = "nominativo" if "ergativo" not in lista_casos else choice(["nominativo", "ergativo"])
            else:
                caso = choice(lista_casos)
                while(caso in ['nominativo', 'ergativo']):
                    caso = choice(lista_casos)
            declinacao:list = self.dialetos_criados[nomes_dialetos[numero]]["gramatica"]["casos"][caso]
            #   print(regra)
            if(regra=="preposicao"):
                print(f"declinacao: {declinacao} |")
                print(f" substantivo {substantivo_escolhido}")
                # print(f"declinacao: {declinacao} | substantivo {substantivo_escolhido}")
                som_sujeito_ajustado:list = tools.regra_de_sandhi(declinacao + substantivo_escolhido, len(declinacao)-1, 0)
                palavra = "".join(som_sujeito_ajustado)
            elif(regra=="posposicao"):
                print(f"substantivo {substantivo_escolhido} | declinacao: {declinacao}")
                som_sujeito_ajustado:list = tools.regra_de_sandhi(substantivo_escolhido + declinacao, len(substantivo_escolhido)-1, 0)
                palavra = "".join(som_sujeito_ajustado)
        else:
            palavra = "".join(substantivo_escolhido)
        return palavra, significado

    def _verbo_(self, nomes_dialetos:list[str], verbos:list[str], significados_verbos:list[str], numero:int)->str:
        """
        FUNCAO
        INPUTS
        RETORNO

        EXEMPLO
        >>>class._verbo_(nomes_dialetos = "Original", verbos = "")
        """
        regra:dict = self.qual_a_regra(nomes_dialetos[numero], "conjugacao")
        verbo_escolhido:str = choice(verbos)
        significado:str = significados_verbos[verbos.index(verbo_escolhido)]
        verbo:str; significado:str
        if(regra!="nao_contem"):
            pessoas:list = list(self.dialetos_criados[nomes_dialetos[numero]]["gramatica"]["conjugacao"].keys())
            pessoas.remove("regra")
            if(regra!="nao_contem"):
                verbo_flexionado:list = self.dialetos_criados[nomes_dialetos[numero]]["gramatica"]["conjugacao"][choice(pessoas)]
                if(regra=="preposicao"):
                    som_verbo_adaptado:list = tools.regra_de_sandhi(verbo_flexionado + verbo_escolhido, len(verbo_flexionado)-1, 0)
                    verbo = "".join(som_verbo_adaptado)
                elif(regra=="posposicao"):
                    som_verbo_adaptado:list = tools.regra_de_sandhi(verbo_escolhido + verbo_flexionado, len(verbo_escolhido)-1, 0)
                    verbo = "".join(som_verbo_adaptado)
            else:
                verbo = "".join(verbo_escolhido)
        else:
            verbo = "".join(verbo_escolhido)
        return verbo, significado

    def _semelhanca_de_palavras_(self, som_x:list, som_y:list)->float:
        """
        FUNCAO
        INPUTS
        RETORNO

        EXEMPLO
        >>>
        """
        calculo:float = 0.0
        total:int = max(len(som_x), len(som_y))
        for i in range(len(som_x)):
            if(len(som_y)==i):
                break
            calculo+= tools.semelhanca_entre_sons(som_x[i], som_y[i])
        return calculo/total

    def _inteligibilidade_(self, dialeto_um:dict, dialeto_dois:dict)->float: # refazer, a língua de menor lexico devia ser a divisor
        """
        FUNCAO
        INPUTS
        RETORNO

        EXEMPLO
        >>>
        """
        calculo:float = 0.0
        total:int = max(len(dialeto_um), len(dialeto_dois))
        for i in range(len(dialeto_um)):
            if(len(dialeto_dois)==i):
                break
            if(i not in dialeto_um or i not in dialeto_dois):
                continue
            for j in range(len(dialeto_um[i])):
                if(len(dialeto_dois[i])==j):
                    break
                calculo+=self._semelhanca_de_palavras_(dialeto_um[i]['palavra'], dialeto_dois[i]['palavra'])
        return (calculo/total)/3

    def _ver_inteligibilidade_(self)->None:
        """
        FUNCAO
        Mostra a inteligibilidade entre as linguas
        INPUTS
        None
        RETORNO
        None

        EXEMPLO
        >>>class._ver_inteligibilidade()
        Intelegibilidade entre original e jejaqso: 0.9726727513227531
        Intelegibilidade entre original e zoŋeŋe: 0.8874084656084648
        ...
        """
        nomes_dialetos:list =  self.nomes()
        for i in nomes_dialetos:
            for j in nomes_dialetos:
                if(i!=j and j!= "original"):
                    print(f"Intelegibilidade entre {i} e {j}: {self._inteligibilidade_(self.dialetos_criados[i]['lingua'], self.dialetos_criados[j]['lingua'])}")

    def qual_a_regra(self, lingua:str, classe_gramatical:str)->dict[str, list[str]]|str:
        """
        FUNCAO
        Verifica se a classe_gramatical selecionada é posposição, preposição ou se não existe.
        INPUTS
        Retorno
        dict[str, list[str]]|str
        Exemplo:
        >>>class.qual_a_regra(lingua = "okt", "conjugacao")
        "preposicao"
        >>>class.qual_a_regra(lingua = "okt", "conjugacao")
        "nao_contem"
        """
        regra:dict|str = self.dialetos_criados[lingua]['gramatica'][classe_gramatical]
        return regra["regra"] if isinstance(regra, dict) else regra

    def sortear_pronome(self, lingua:str="Original")->str:
        """
        Sorteia um tipo de pronome (eu, voce, nos, nos_inclusivo, etc).
        Por padrão, o argumento lingua** está recebendo "Original"
        Args:
            lingua (str): precisa receber o nome de uma das linguas para que retorne um verbo
        Retorno:
        str
        Exemplo:
        >>>class.sortear_pronome(lingua = "Original")
        "eu"
        >>>class.sortear_pronome(lingua = "Original")
        "voce"
        """
        return choice(list(self.dialetos_criados[lingua]['gramatica']['pronomes'].keys()))

    def buscar_indices(self, lingua:str, indice:int, ja_encontrados:list[int] = [])->list[int]:
        """
        FUNCAO
        Procura por indices existentes nos dicionarios das linguas. Pode acontecer de uma determinada lingua perder a raiz da palavra,
        mas preservar a mesma raiz em outras palavras por processos aglutinativos/fixais.
        INPUTS
            lingua (str): é preciso colocar algum nome que seja filha da lingua mãe.
            indice (int): insere um numero inteiro válido do dicionário da língua e que tenha tido descendentes ou homofonia,
                caso contrário diz que não tem correspondente.
            ja_encontrados (list[int]): orienta quais indices ja foram visitados
        RETORNO
        list[int]

        Exemplo:
        >>>class.buscar_indices(lingua = "onʷɔn", indice = 25)
            536 : Palavra:ogbʉhoto
                Classe: substantivo
                Significados: tocar | velho
                Semelhante a: [468, 25]
            25 : Palavra:ihodɵtɵ
                Classe: adjetivo
                Significados: velho
                Semelhante a: []
        """
        encontrado:bool = False
        dicionario:dict = self.dialetos_criados[lingua]['lingua']
        lista_encontrados:list[int] = []

        for index in dicionario.keys():
            if(lingua!='original'):
                for palavra in dicionario[index]['indices']:
                    if(indice == palavra and not index in ja_encontrados):
                        # print(f"Index {index} passou")
                        encontrado = True
                        palavra:list[str] = dicionario[index]['palavra']
                        classe_gramatical:str = dicionario[index]['classe']
                        lista_significado:list[str] = dicionario[index]['significado']
                        lista_index:list[int] = dicionario[index]['indices']
                        print(f"\t\t{index} : Palavra:{"".join(palavra)}\n\t\t\tClasse: {classe_gramatical}\n\t\t\tSignificados: {" | ".join(lista_significado)}\n\t\t\tSemelhante a: {lista_index}")
                        lista_encontrados.append(index)
        if(((encontrado and indice in list(dicionario.keys())) and (indice not in ja_encontrados)) or ((lingua=='original' and indice in list(dicionario.keys())))):
            # print(f"Indice {indice} passou")
            palavra:str = dicionario[indice]['palavra']
            classe_gramatical:str = dicionario[indice]['classe']
            lista_significado:list[str] = dicionario[indice]['significado']
            lista_index:list[int] = dicionario[indice]['indices']
            print(f"\t\t{indice} : Palavra:{"".join(palavra)}\n\t\t\tClasse: {classe_gramatical}\n\t\t\tSignificados: {" | ".join(lista_significado)}\n\t\t\tSemelhante a: {lista_index}")
            lista_encontrados.append(indice)
        elif(not encontrado):
            print(f"\t\tSem correspondentes para o indice {indice}")
        return lista_encontrados

    def mostrar_desenvolvimento_palavra_linguas(self, indices:list[int])->None:
            """
            Utiliza a funcao buscar_indices() mostrando as variações de cada palavra em cada língua.
            Args:
                indices (list[int]): recebe somente números que estejam contidos no dicionário.
            Retorno:
            None
            Exemplo:
            >>>class.mostrar_desenvolvimento_palavra_linguas(indices = [25, 42])
            ========================= ANALISE HOMOFONICA E/OU AGLUTINATIVA DA LINGUA original =========================
                25 : Palavra:ɨhɔnotʊ
                    Classe: adjetivo
                    Significados: velho
                    Semelhante a: []
                42 : Palavra:ib
                    Classe: substantivo
                    Significados: boca
                    Semelhante a: []


            ========================= ANALISE HOMOFONICA E/OU AGLUTINATIVA DA LINGUA onʷɔn =========================
                536 : Palavra:ogbʉhoto
                    Classe: substantivo
                    Significados: tocar | velho
                    Semelhante a: [468, 25]
                25 : Palavra:ihodɵtɵ
                    Classe: adjetivo
                    Significados: velho
                    Semelhante a: []
                Sem correspondentes para o indice 42
            """
            for i in self.nomes():
                lista_encontrados:list[int] = []
                print("="*25, f"ANALISE HOMOFONICA E/OU AGLUTINATIVA DA LINGUA {i}", "="*25)
                for n in indices:
                    lista_encontrados.extend(self.buscar_indices(i, n, lista_encontrados))
                print('\n')

    """
    RETORNO
    """
    def retornar_pronome(self, lingua:str, buscar_pronome:str, retorno:str = 'str')->str|list[str]:
        """
        Retorna o pronome correspondente na lingua escolhida.
        Args:
            lingua (str): nome chave que contenha a palavra buscada;
            buscar_palavra (str): a palavra que deseja encontrar a correspondente;
            retorno (str): se quer que o retorno seja em formato str ou list;
        Retorno:
            str|list[str]
        Exemplo:
        >>>retornar_pronome(lingua = lingua = 'ʊmij', buscar_pronome = 'eu', retorno = 'str')
        ʏɾɪjʊ
        >>>retornar_pronome(lingua = lingua = 'ʊmij', buscar_pronome = 'voce', retorno = 'list')
        ['n', 'ɪ', 'w', 'ɪ', 'j']
        """
        pronome = self.dialetos_criados[lingua]['gramatica']['pronomes'][buscar_pronome]
        return "".join(pronome) if(retorno == 'str') else pronome


    def retornar_verbo(self, lingua:str, buscar_palavra:str, conjugacao:bool|str = False, retorno:str = 'str', aviso:bool = False)->str|list[str]:
        """
        Busca pelo verbo inserido e retorna somente a palavra da língua.
        Args:
            lingua (str): nome chave que contenha a palavra buscada;
            buscar_palavra (str): a palavra que deseja encontrar a correspondente;
            conjugacao (bool|str): retorna a palavra conjugada caso True, podendo
                especificar qual conjugacao deseja (eu, voce, nos, nos_h, voces, etc.);
            retorno (str): se quer que o retorno seja em formato str ou list;
            aviso (false): se quer que avise que encontrou mais de um correspondente,
                caso falso, vai retornar um ALEATORIO.
        Retorno:
            str|list[str]
        Exemplo:
        >>>retornar_palavra(lingua = 'ʊmij', buscar_palavra = 'comer', conjugacao = False, retorno = 'str', aviso = False)

        """
        def conjugar(gramatica, pessoa, retorno)->str|list[str]:
            try:
                conjugacao = gramatica['conjugacao']
                if(pessoa in conjugacao.keys()):
                    conjugado = conjugacao[pessoa]
                else:
                    conjugado = conjugacao[choice(list(conjugacao.keys()))]
                return "".join(conjugado) if(retorno=='str') else conjugado
            except KeyError:
                return ""

        try:
            descritivo = self.dialetos_criados[lingua]
            dicionario = descritivo['lingua']
            palavras_encontradas:list[str] = []
            encontrados:int = 0
            for index in dicionario.keys():
                detalhes = dicionario[index]
                if(buscar_palavra in detalhes['significado']):
                    encontrados+=1
                    palavras_encontradas.append("".join(detalhes['palavra']) if(retorno.lower().startswith('s')) else detalhes['palavra'])
                    if(aviso and encontrados>1):
                        print(f'== Mais de {encontrados} foram encontrados **')

            if(conjugacao):
                gramatica = descritivo['gramatica']
                posicao = gramatica['posicao']
                conjugado = conjugar(gramatica, conjugacao, retorno)
                if(posicao=='preposicao'):
                    return conjugado + palavras_encontradas if(aviso) else conjugado + choice(palavras_encontradas)
                return palavras_encontradas + conjugado if(aviso) else choice(palavras_encontradas) + conjugado
            return palavras_encontradas if(aviso) else choice(palavras_encontradas)
        except IndexError:
            print(f"Palavra '{buscar_palavra}' não foi encontrada.")

    def retornar_palavra(self, lingua:str, buscar_palavra:str, declinacao:bool|str = False, retorno:str = 'str', aviso:bool = False)->str|list[str]:
        """
        Busca pela palavra inserida e retorna somente a palavra da língua.
        Args:
            lingua (str): nome chave que contenha a palavra buscada;
            buscar_palavra (str): a palavra que deseja encontrar a correspondente;
            declinacao (bool|str): retorna a palavra declinada caso True, podendo
                especificar qual declinacao deseja (nominativo, acusativo, dativo, etc.);
            retorno (str): se quer que o retorno seja em formato str ou list;
            aviso (false): se quer que avise que encontrou mais de um correspondente,
                caso falso, vai retornar um ALEATORIO.
        Retorno:
            str|list[str]
        Exemplo:
        >>>retornar_palavra(lingua = 'ʊmij', buscar_palavra = 'homem', declinacao = False, retorno = 'str', aviso = False)
        ʏji
        """
        def declinar(gramatica, declinacao, retorno)->str|list[str]:
            afixos = gramatica['afixos']
            if(declinacao == 'nominativo'):
                afixo_escolhido = [""]
            elif(declinacao in afixos.keys()):
                afixo_escolhido = afixos[declinacao]
            else:
                afixo_escolhido = afixos[choice(list(afixos.keys()))]
            return "".join(afixo_escolhido) if(retorno=='str') else afixo_escolhido

        try:
            descritivo = self.dialetos_criados[lingua]
            dicionario = descritivo['lingua']
            palavras_encontradas:list[str] = []
            encontrados:int = 0
            for index in dicionario.keys():
                detalhes = dicionario[index]
                if(buscar_palavra in detalhes['significado']):
                    encontrados+=1
                    palavras_encontradas.append("".join(detalhes['palavra']) if(retorno.lower().startswith('s')) else detalhes['palavra'])
                    if(aviso and encontrados>1):
                        print(f'== Mais de {encontrados} foram encontrados **')

            if(declinacao):
                gramatica = descritivo['gramatica']
                posicao = gramatica['posicao']
                declinacao = declinar(gramatica, declinacao, retorno)
                if(posicao=='preposicao'):
                    return declinacao + palavras_encontradas if(aviso) else declinacao + choice(palavras_encontradas)
                return palavras_encontradas + declinacao if(aviso) else choice(palavras_encontradas) + declinacao

            return palavras_encontradas if(aviso) else choice(palavras_encontradas)
        except IndexError:
            print(f"Palavra '{buscar_palavra}' não foi encontrada.")

    def retornar_indices(self, buscar_palavra:str, lingua:str='original', tipo:str='todos')->list[int]:
        """
        Retorna todos os indices do tipo inserido.
        Args:
            lingua (str):
            tipo (str): por padrão retorna 'todos' os tipos, mas aceita somente 'substantivo', 'verbo' e 'adjetivo';
        Retorno:
            list[int]
        Exemplo:
        """
        dicionario = self.dialetos_criados[lingua]['lingua']
        if(tipo=='todos'):
            return list(dicionario.keys())
        else:
            lista_indices:list[int] = [
                i for i in dicionario.keys()
                if(dicionario[i]['classe'] == tipo and buscar_palavra.lower() in dicionario[i]['significado'])
            ]
            return lista_indices

    """
    VERIFICACAO
    """
    def eh_pronome(self, lingua:str, pronome:str)->bool:
        """
        Exemplo:
        >>>eh_pronome(gramatica = ramo_2.dialetos_criados['umat']['gramatica'], pronome = 'eu')
        True
        >>>eh_pronome(gramatica = ramo_2.dialetos_criados['umat']['gramatica'], pronome = 'ela')
        False
        >>>eh_pronome(gramatica = ramo_2.dialetos_criados['umat']['gramatica'], pronome = 'nos_exclusivo')
        False
        """
        return pronome.lower() in self.dialetos_criados[lingua]['gramatica']['pronomes'].keys()

    def eh_verbo(self, lingua, verbo)->bool:
        """
        Exemplo:
        >>>eh_verbo(classe = ramo_a, lingua = 'ibeg', verbo = 'comer')
        True
        >>>eh_verbo(classe = ramo_a, lingua = 'ibeg', verbo = 'montanha')
        False
        """
        return len(self.retornar_indices(self, verbo, lingua, 'verbo'))>0

    def eh_substantivo(self, lingua, substantivo)->bool:
        """
        Exemplo:
        >>>eh_substantivo(classe = ramo_a, lingua = 'ibeg', substantivo = 'cacar')
        False
        >>>eh_substantivo(classe = ramo_a, lingua = 'ibeg', substantivo = 'espirito')
        True
        """
        return len(self.retornar_indices(self.classe, substantivo, lingua, 'substantivo'))>0

    """
    RETORNO
    """
    def retornar_da_gramatica(self, lingua:str, tipo:str):
        """
        RESUMO
        Busca todos os indices que tenham o tipo inserido.
        INPUTS
        tipo -> recebe somente "substantivo", "adjetivo" e "verbo"
        RETORNO
        list[int]

        EXEMPLO
        >>>retornar_da_gramatica(class, 'original', "substantivo")
        [2,6,7,8,10,18,19,27,30,...]
        """
        indices:list[int] = self.dialetos_criados[lingua]["lingua"].keys()
        tipos_encontrados:list[int] = []
        for i in indices:
            if(self.dialetos_criados[lingua]["lingua"][i]['classe']==tipo):
                tipos_encontrados.append(i)
        return tipos_encontrados

    """
    SORTEAR
    """
    def sortear_indice(self, lingua:str, tipo:str)->int:
        """
        FUNCAO
        Retorna somente um numero inteiro
        INPUTS
        classe -> a class que contém os dicionários
        lingua -> uma língua que pertença a classe
        tipo -> "substantivo", "adjetivo" ou "verbo"
        EXEMPLO
        >>>sortear_indice(class, 'uɾɵʔuʔ', 'verbo')
        392
        """
        return choice(self.retornar_da_gramatica(lingua, tipo))

    def sortear_palavras(self, quantidade_palavras:int)->list[str]:
        """
        FUNCAO
        Sorteia uma ou mais palavras. Usado mais para output de dados, principalmente se não souber que palavra
        colocar ou qual palavra existe nas classe. É utilizado a função
        retornar_palavras_do_ramo('original').
        #
        INPUTS
        classe -> class que contenha as informações da/s língua/s.
        quantidade_palavras -> número inteiro de palavras que quer receber
        #
        RETORNO
        list[str]
        #
        EXEMPLO
        >>>sortear_palavras(class, 10)
        ['passado', 'arvore', 'felino', 'seco', 'eterno', 'objeto', 'mar', 'olho', 'roedor', 'cruel']
        >>>sortear_palavras(class, 1)
        ['forma']
        """
        try:
            lingua:str = self.sortear_lingua()
            palavras:list[str] = self.retornar_palavras_do_ramo(lingua)
            palavras_sorteadas:list[str] = []
            index:int = 0
            while index<quantidade_palavras:
                p:str = choice(palavras)
                contador:int = 0
                while(p in palavras_sorteadas or contador<10):
                    p = choice(palavras)
                    contador+=1
                palavras_sorteadas.append(p)
                index+=1
            return palavras_sorteadas
        except ValueError:
            raise ValueError('Tipo errado inserido. Verificar:\n\t\tclasse e número inserido.')

    """
    MOSTRAR/VER
    """
    def inserir_sinal_tonico(self, word:str, tonico:str, retorno:str)->list[str] | str:
        """
        Insere a apostrofe para indicar onde se encontra a sílaba tônica na word.
        Parameters:
        word (str) : sequencia de caracteres, como ['t', 'ɨ', 't', 'p', 'i']
        tonico (str) : se é uma lingua ou word oxitona, paroxitona ou proparoxitona
        retorno (str) : se o retorno é em 'lista' ou em 'string'
        Returns:
        list[str] | str : the word as string or an array
        Exemple:
        >>> self.inserir_sinal_tonico(['t','a','x', 'a', 'r', 'o'], 'oxitona', lista)
        ['t','a','x', 'a', "'r", 'o']
        >>> self.inserir_sinal_tonico(['t', 'ɨ', 't', 'p', 'i'], 'paroxitona', string)
        /'tɨt.pi./
        """
        stressed_syllable, tonico_posto, passou_por_consoante, passou_por_vogal = False,False,False,False
        count_vowels, count_consonants, index = 0, 0, 0
        list_word = list(word)
        list_word = list_word[::-1]
        word_reserva = list_word
        while(len(word_reserva)>index):
            letra = list_word[index] # o programa olha a 'colinha' para nao se perder
            if(tools.eh_vogal(letra)):
                # print("É vogal")
                count_vowels+=1
                if(index==0):
                    word_reserva[index] = f"{word_reserva[index]}."
                try:
                    if(tools.eh_consoante(list_word[index+1][0])):
                        # print(word_reserva[index])
                        if((tonico == 'oxitona' and count_vowels == 1) or (tonico in ['paroxitona', 'proparoxitona'] and len(list_word)<=4) and (not stressed_syllable)):
                            # print("É oxítona")
                            word_reserva[index+1] = f"'{word_reserva[index+1]}"
                            stressed_syllable = True
                        elif((tonico == 'paroxitona' or tools.contar_vogais(list_word)<3) and (not stressed_syllable)
                        and count_vowels>1 and count_consonants>=1):
                            # print("É paroxítona")
                            word_reserva[index+1] = f"'{word_reserva[index+1]}"
                            stressed_syllable = True
                        elif(tonico == 'proparoxitona' and not stressed_syllable and count_vowels>2 and count_consonants>1):
                            # print("É proparoxítona, {}".format(word_reserva[index]))
                            word_reserva[index+1] = f"'{word_reserva[index+1]}"
                            stressed_syllable = True
                except IndexError:
                    # print("Erro de index na condição VOGAL")
                    if(tonico in ['oxitona', 'paroxitona', 'proparoxitona'] and not stressed_syllable):
                        word_reserva[index] = f"'{word_reserva[index]}"
                passou_por_vogal = True
                passou_por_consoante = False

            elif(tools.eh_consoante(letra)):
                count_consonants+=1
                try:
                    if(index==0):
                        word_reserva[index] = f"{word_reserva[index]}."
                    elif(tools.eh_vogal(word[index+1]) and not passou_por_consoante):
                        # print("Proximo NÃO é consoante")
                        word_reserva[index+1] = f"{word_reserva[index+1]}."
                    elif(len(word)-1==index+1):
                        pass
                    elif(not passou_por_consoante):
                        # print("Proxima é consoante")
                        word_reserva[index+1] = f"{word_reserva[index+1]}."
                except IndexError:
                    # print("Erro de index na condição CONSOANTE")
                    # word_reserva[index] = f"{word_reserva[index]}."
                    pass
                passou_por_consoante = True
                passou_por_vogal = False

            index+=1
        # print(word)
        list_word = word_reserva[::-1]
        return list_word if retorno.lower() in ['lista', 'list'] else ''.join(list_word)

    def ver_gramatica(self, topico="todos")->None:
        """
        Args:
        Exemplo:
        >>> ver_gramatica(classe = class, topico = "pronomes")

        """
        assuntos:dict[str,list[str]] = {
            'p':'pronomes', 'a':'afixos', 'c':'conjugacao',
        }
        dialetos:dict = self.dialetos_criados
        complemento:str = self.retornar_palavra(lingua = 'original', buscar_palavra = 'lingua')
        for i in dialetos.keys():
            print("="*20, f"{"Língua" if(i=='original') else complemento} {i}", "="*20)
            for gramatica in dialetos[i]["gramatica"]:
                if(isinstance(dialetos[i]["gramatica"][gramatica], dict)):
                    if(topico=="todos"):
                        print(":"*10, f"{gramatica}")
                        for conteudo in dialetos[i]["gramatica"][gramatica]:
                            print("||", " "*10, f"{conteudo}  :::  {"".join(dialetos[i]["gramatica"][gramatica][conteudo])}")
                        print("||")
                    else:
                        if(gramatica==assuntos.get(topico[0]) or gramatica == topico):
                            print(":"*10, f"{gramatica}")
                            for conteudo in dialetos[i]["gramatica"][gramatica]:
                                print("||", " "*10, f"{conteudo}  :::  {"".join(dialetos[i]["gramatica"][gramatica][conteudo])}")
                            print("||")

    def ver_gramatica_detalhada(self, lingua, topico, modelo)->None:
        """
        """
        lingua_dict = self.dialetos_criados[lingua]
        if(topico.startswith("s") or topico.startswith("p") or topico.startswith("c")):
            indice_sorteado:int = choice(self.retornar_da_gramatica(lingua, 'substantivo'))
            gramatica = lingua_dict['gramatica']['afixos']
        elif(topico.startswith("v")):
            indice_sorteado:int = choice(self.retornar_da_gramatica(lingua, 'verbo'))
            gramatica = lingua_dict['gramatica']['conjugacao']

        tabela:list[list[str]] = [['', 'AFIXO', 'CONJUGACAO']]

        if(isinstance(gramatica, dict)):
            regra = gramatica['regra']
            for g in gramatica.keys():
                if(gramatica[g]!=regra):
                    particula:list[str] = []
                    if(modelo == "tabela"):
                        print(f"{g}", end=" | ")
                        if(regra=='posposicao'):
                            print(f"-{"".join(gramatica[g])}", end=" | ")
                            print("".join(lingua_dict['lingua'][indice_sorteado]['palavra']+gramatica[g]))
                        elif(regra == 'preposicao'):
                            print(f'{gramatica[g]}-', end=" | ")
                            print("".join(gramatica[g]+lingua_dict['lingua'][indice_sorteado]['palavra']))
                    else:
                        particula.append(f"{g}")
                        if(regra=='posposicao'):
                            particula.append(f"-{"".join(gramatica[g])}")
                            particula.append("".join(lingua_dict['lingua'][indice_sorteado]['palavra']+gramatica[g]))
                        elif(regra == 'preposicao'):
                            particula.append(f'{gramatica[g]}-')
                            particula.append("".join(gramatica[g]+lingua_dict['lingua'][indice_sorteado]['palavra']))
                        tabela.append(particula)
        if(modelo!="tabela"):
            df = pd.DataFrame(data=tabela[1:], columns=tabela[0])
            # df.fillna("", inplace=True, )
            print(df)
        else:
            print(f"{lingua} não contém casos")

    def organizar_frase(self, ordem:list[str], lingua:str, indices:list[int])->list[int]:
        """
        Organiza a frase na ordem da língua.
        EXEMPLO
        >>>organizar_frase(dialetos.dialetos_criados, 'SVO', "original", [120, 15, 401])
        [15, 401, 120]
        """
        frase_organizada:list[int] = []
        dicionario = self.dialetos_criados[lingua]["lingua"]
        nova_ordem = list(ordem)
        nova_ordem[nova_ordem.index('O')] = "S"
        for o in nova_ordem:
            for i in indices:
                if(dicionario[i]['classe'][0].upper() == o):
                    frase_organizada.append(i)
                    indices.pop(indices.index(i))
                    break
        return frase_organizada

    def conjugar_pessoa(self, lingua:str, pessoa:str, verbo:list[str])->list[str]:
        """
        Junta o verbo com a pessoa verbal
        """
        conjugacao = self.dialetos_criados[lingua]['gramatica']['conjugacao']
        regra:str = conjugacao['regra']
        if(regra=='preposicao'):
            return conjugacao[pessoa] + verbo
        elif(regra=='posposicao'):
            return verbo + conjugacao[pessoa]
        return verbo

    def conjugar_verbo(self, lingua:str, verbo_indice:int=None)->None:
        """
        RESUMO
        Monta uma tabela com o verbo inserido em verbo_indice
        INPUTS
        verbo_indice -> precisa receber um índice que seja verbo no dicionário da língua/dialeto
        RETORNO

        EXEMPLO
        >>>conjugar_verbo(class.dialetos_criados, "", )
        Verbo proibir
        asuʂ diɾœ
        u diɾœ
        ʊɣi diɾœ
        ɖaj diɾœ
        ilʊ diɾœ
        ʊʂ diɾœ
        """

        def conjugar(self, lingua:str, pessoa:str, verbo:list[str], silaba_tonica:str)->list[str]:
            """
            """
            verbo_conjugado = self.conjugar_pessoa(lingua, pessoa, palavra['palavra'])
            verbo_conjugado = tools.retornar_palavra_atona(verbo_conjugado, silaba_tonica)
            verbo_conjugado = tools.filtro_fonetico(verbo_conjugado)
            verbo_conjugado = self.inserir_sinal_tonico(
                verbo_conjugado,
                silaba_tonica, "lista"
            )
            return verbo_conjugado

        def montar_conjugacao(palavra, significado, pronomes):
            print(f"Verbo {"".join(significado)}")
            for _, p in enumerate(pronomes):
                if(gramatica["estrutura"] in ["SOV", "OSV", "SVO"]):
                    conjugacao_pronta:list[str] = tools.filtro_fonetico(pronomes[p] + palavra)
                    conjugacao_pronta = tools.retornar_palavra_atona(conjugacao_pronta, silaba_tonica)
                    conjugacao_pronta = tools.corrigir_palavra(list(conjugacao_pronta))
                    conjugacao_pronta[:len(pronomes[p])] = self.inserir_sinal_tonico(
                        conjugacao_pronta[:len(pronomes[p])],
                        silaba_tonica, "lista"
                    )
                    conjugacao_pronta[len(pronomes[p]):] = self.inserir_sinal_tonico(
                        conjugacao_pronta[len(pronomes[p]):],
                        silaba_tonica, "lista"
                    )
                    conjugacao_pronta.insert(len(pronomes[p]), '‿')
                    print(f"{p}:/{"".join(conjugacao_pronta)}/")
                else:
                    conjugacao_pronta:list[str] = tools.filtro_fonetico(palavra + pronomes[p])
                    conjugacao_pronta = tools.retornar_palavra_atona(conjugacao_pronta, silaba_tonica)
                    conjugacao_pronta = tools.corrigir_palavra(list(conjugacao_pronta))
                    conjugacao_pronta[:len(palavra)] = self.inserir_sinal_tonico(
                        conjugacao_pronta[:len(palavra)],
                        silaba_tonica, "lista"
                    )
                    conjugacao_pronta[len(palavra):] = self.inserir_sinal_tonico(
                        conjugacao_pronta[len(palavra):],
                        silaba_tonica, "lista"
                    )
                    conjugacao_pronta.insert(len(palavra), '‿')
                    print(f"{p}:/{"".join(conjugacao_pronta)}/")

        try:
            verbo = verbo_indice if(isinstance(verbo_indice, int)) else self.sortear_indice(lingua, "verbo")
            DC = self.dialetos_criados[lingua]
            palavra = DC["lingua"][verbo]
            gramatica:dict = DC["gramatica"]
            silaba_tonica:str = gramatica["silaba_tonica"]
            posicao:str = gramatica["posicao"]
            pronomes:list[str] = list(gramatica["pronomes"].keys())
            conjugacao:dict[str,str] | str = gramatica["conjugacao"]
            if(isinstance(conjugacao, str)):
                montar_conjugacao(palavra["palavra"], palavra["significado"], gramatica["pronomes"])

            # eu não pretendo por '‿' nos conjugaveis, pois se tratam com afixos
            elif(isinstance(conjugacao, dict)):
                afixos:list[str] = list(conjugacao.keys())
                # regra:str = afixos.pop(0) # VER ISSO!!!!
                # por alguma razão, as regras dentro de afixos e conjugação estão sendo alteradas, colando a alteração anterior.
                if(posicao=="posposicao"):
                    print(f"Verbo {"".join(palavra["significado"])} ({"".join(palavra["palavra"])}-)")
                    for i, pessoa in enumerate(pronomes):
                        # print(conjugacao[afixos[i]])
                        verbo_conjugado = conjugar(lingua, pessoa, palavra['palavra'], silaba_tonica)
                        print(f"{afixos[i]} {"".join(palavra["significado"])}:/{"".join(verbo_conjugado)}/")
                elif(posicao=="preposicao"):
                    print(f"Verbo {"".join(palavra["significado"])} (-{"".join(palavra["palavra"])})")
                    for i, pessoa in enumerate(pronomes):
                        # print(conjugacao[afixos[i]])
                        verbo_conjugado = conjugar(lingua, pessoa, palavra['palavra'], silaba_tonica)
                        print(f"{afixos[i]} {"".join(palavra["significado"])}:/{"".join(verbo_conjugado)}/")
        except KeyError:
            if(any(i in ['pronomes', 'conjugacao'] for i in gramatica)):
                montar_conjugacao(palavra["palavra"], palavra["significado"], gramatica["pronomes"])
            else:
                print(f"Verbo {"".join(palavra["significado"])}")
                print(f"/{"".join(palavra["palavra"])}/")

        except UnboundLocalError:
            print(f"Verbo {"".join(palavra["significado"])}")
            print(f"/{"".join(palavra["palavra"])}/")

        except IndexError:
            print("Erro de index")

    def retornar_nome_lingua(self)->list[str]:
        """
        Retorna especificamente os nomes
        """
        nomes:list[str] = []
        significados:list[str] = []
        try:
            lingua_mae = self.encontrar_palavra_pelo_som(self.dialetos_criados, "original", self.nome_lingua_mae) #tools.corrigir_palavra(list(self.nome_lingua_mae))
            nomes.append(lingua_mae.get('palavra'))
            significados.append(lingua_mae.get('significado'))
        except:
            print('Mae nao encontrada?')

        for nome in self.nomes():
            if(nome!="original"):
                detalhe_palavra:dict[str, list[str]]= self.encontrar_palavra_pelo_som("original", nome) #tools.corrigir_palavra(list(nome))
                nomes.append(detalhe_palavra['palavra'])
                significados.append(detalhe_palavra.get('significado'))

        return nomes, significados

    def montar_frase(self, lingua:str="original", mostrar_declinacao:bool=False, mostrar_conjugacao:bool=False)->None:
        """
        RESUMO
        Args:
            lingua (str): nome ou chave existente em classe
            mostrar_declinacao (bool): se mostra como as declinações com a raiz
        RETORNO
            None
        Exemplo:
        >>> montar_frase(ramo_1, "aʧɪɐw", False)
        Tradução: ['neto'] ['cidade'] ['morder']
        /ɾajɾmuɾɪmwʊiɪw/
        Palavras usadas: [['ɾ', 'a', 'j', 'ɾ'], ['m', 'u', 'ɾ', 'ɪ', 'm', 'w', 'ʊ'], ['i', 'ɪ', 'w']]
        """

        def retornar_caso(self, regra, lingua, palavra, caso)->list[str]:
            """
            """
            if(len(self.dialetos_criados[lingua]["gramatica"]["afixos"][caso])>0):
                return self.dialetos_criados[lingua]["gramatica"]["afixos"][caso] + palavra if(regra=="preposicao") else palavra + self.dialetos_criados[lingua]["gramatica"]["afixos"][caso]
            return palavra


        num_substantivo = self.sortear_indice(lingua, "substantivo")
        num_objeto = self.sortear_indice(lingua, "substantivo")
        num_verbo = self.sortear_indice(lingua, "verbo")
        descritivo = self.dialetos_criados[lingua]
        ordem:str = descritivo['gramatica']['estrutura']
        frase_organizada:list[int] = self.organizar_frase(ordem, lingua, [num_substantivo, num_objeto, num_verbo])
        print(frase_organizada)

        dicionario = descritivo['lingua']
        print(f"Tradução: {dicionario[frase_organizada[0]]["significado"]} {dicionario[frase_organizada[1]]["significado"]}", end=" ")
        print(f"{dicionario[frase_organizada[2]]["significado"]}")
        gramatica:dict[str,dict[str,str]] = descritivo["gramatica"]
        frase_base:list[str] = [
            dicionario[frase_organizada[0]]["palavra"],
            dicionario[frase_organizada[1]]["palavra"],
            dicionario[frase_organizada[2]]["palavra"]
            ]
        if("afixos" in gramatica.keys()):
            afixos:dict[str,str]|str = gramatica["afixos"]
            ### ==> criar uma função para afixos, em que usa a regra_de_sandhi e modificar_sonora_ou_surda
            pronomes:dict[str, str] = gramatica["pronomes"]
            if(isinstance(afixos, dict) and mostrar_declinacao):
                # frase = []
                # afixos_lista = list(afixos.keys())
                if(all(i in ['nominativo', 'absolutivo'] for i in afixos.keys())):
                    frase_base[ordem.index("S")] = retornar_caso(afixos["regra"], lingua, frase_base[ordem.index("S")], choice(["nominativo", "absolutivo"]))
                else:
                    frase_base[ordem.index("S")] = retornar_caso(afixos["regra"], lingua, frase_base[ordem.index("S")], "nominativo")
                if(all(i in ['acusativo', 'dativo'] for i in afixos.keys())):
                    frase_base[ordem.index("O")] = retornar_caso(afixos["regra"], lingua, frase_base[ordem.index("O")], choice(["acusativo", "dativo"]))
                elif('acusativo' in afixos.keys()):
                    frase_base[ordem.index("O")] = retornar_caso(afixos["regra"], lingua, frase_base[ordem.index("O")], "acusativo")
                else:
                    frase_base[ordem.index("O")] = retornar_caso(afixos["regra"], lingua, frase_base[ordem.index("O")], "dativo")

            if(isinstance(pronomes, dict) and mostrar_conjugacao):
                frase_base[ordem.index("V")] = self.conjugar_pessoa(lingua, 'aquele', frase_base[ordem.index("V")])

        silaba_tonica = gramatica['silaba_tonica']
        for i in range(len(frase_base)):
            frase_base[i] = tools.retornar_palavra_atona(frase_base[i], silaba_tonica)
        descricao = tools.filtro_fonetico(frase_base[0]+frase_base[1]+frase_base[2])
        print("/"+"".join(descricao)+"/")


        print("Palavras usadas: ", end="")
        for palavra in frase_base:
            print("".join(palavra), end=" ")

    def dar_titulo(self, lingua:str)->None:
        """
        Pega um substantivo e um adjetivo para dar um 'título' ou uma característica ao objeto
        >>>dar_titulo()
        """
        substantivo:int = self.sortear_indice(lingua, "substantivo")
        adjetivo:int = self.sortear_indice(lingua, "adjetivo")
        DC = self.dialetos_criados[lingua]
        palavra_substantivo:dict[str,list[str]] = DC['lingua'][substantivo]
        palavra_adjetivo:dict[str,list[str]] = DC['lingua'][adjetivo]
        silaba_tonica:str = DC['gramatica']['silaba_tonica']
        if(DC["gramatica"]["estrutura"] in ["SOV", "OSV"]):
            palavra:list[str] = tools.filtro_fonetico(palavra_adjetivo["palavra"] + palavra_substantivo["palavra"])
            palavra = tools.retornar_palavra_atona(palavra, silaba_tonica)
            palavra = tools.corrigir_palavra(list(palavra))
            palavra[:len(palavra_adjetivo['palavra'])] = self.inserir_sinal_tonico(palavra[:len(palavra_adjetivo['palavra'])], silaba_tonica, "lista")
            palavra[len(palavra_adjetivo['palavra']):] = self.inserir_sinal_tonico(palavra[len(palavra_adjetivo['palavra']):], silaba_tonica, "lista")
            palavra.insert(len(palavra_adjetivo['palavra']), '‿')
            print(f"/{"".join(palavra)}/")
            print(f"Tradução* \nAdjetivo:{" ".join(palavra_adjetivo["significado"])} ({"".join(palavra_adjetivo["palavra"])})\
            \nSubstantivo:{"".join(palavra_substantivo["significado"])} ({"".join(palavra_substantivo["palavra"])})")
        # elif(classe[lingua]["gramatica"]["estrutura"] in ["SVO", "VSO", "VOS", "OVS"]):
        else:
            palavra:list[str] = tools.filtro_fonetico(palavra_substantivo["palavra"] + palavra_adjetivo["palavra"])
            palavra = tools.retornar_palavra_atona(palavra, silaba_tonica)
            palavra = tools.corrigir_palavra(list(palavra))
            palavra[:len(palavra_substantivo['palavra'])] = self.inserir_sinal_tonico(palavra[:len(palavra_substantivo['palavra'])], silaba_tonica, "lista")
            palavra[len(palavra_substantivo['palavra']):] = self.inserir_sinal_tonico(palavra[len(palavra_substantivo['palavra']):], silaba_tonica, "lista")
            palavra.insert(len(palavra_substantivo['palavra']), '‿')
            print(f"/{"".join(palavra)}/")
            print(f"Tradução* \nSubstantivo:{" ".join(palavra_substantivo["significado"])} ({"".join(palavra_substantivo['palavra'])})\
            \nAdjetivo:{"".join(palavra_adjetivo["significado"])} ({"".join(palavra_adjetivo["palavra"])})")

    """
    esta célula está sendo testada para encontrar palavras de uma língua ou várias

    além disso, estou tentando melhorar o output para melhor visualizar as mudanças
        em cada língua

    Muitas das vezes eu vou me referir a 'dicionário' como sendo os dicionários das línguas e não necessariamente ao dicionario/dict (tipo de variável)
    """

    def retornar_palavras_do_ramo(self, lingua:str)->list[str]:
        """
        Retornar todas as palavras e termos que a língua tem
        """
        lista_palavras:list[str] = []
        indices = self.dialetos_criados[lingua]['lingua']
        for palavra in list(indices.keys()):
            significado:str = indices[palavra]['significado']
            if(significado not in lista_palavras):
                lista_palavras.extend(significado)
        return lista_palavras

    def mostrar_palavra_mais_descritiva(self, lingua:str, encontrar_palavra:str, apresentar_casos:bool, transcricao_fonetica:bool=False)->None:
        """
        RESUMO
        Faz um output da funcao buscar_palavra (busca de apenas uma lingua) mais legivel
        e mostrando uso da palavra, alem de explica-la melhor. Ex.:
        'significado: agua
            | gramatica: substantivo
            | declinacoes:
                | nominativo - agua
                | acusativo  - agua
                ...
        INPUTS
        lingua             -> nome da língua ("original", "æʔt", etc.). É importante saber quais línguas constam nas suas classes
        encontrar_palavra  -> uma palavra que esteja contida em pelo menos um dicionário da língua
        apresentar_casos   -> escolhe se vai mostrar os casos gramaticais (nominativo, acusativo,
        dativo, genitivo, etc.), se não tiver casos, nenhum caso vai aparecer
        transcricao_fonetica -> habilita ou não transcrição fonética, seguindo o IPA. Mostra as sílabas átonas e tônicas se *True*
        RETORNO
        None

        EXEMPLO
        >>>mostrar_palavra_mais_descritiva(class.dialetos_criados, "original", "forma", True, False)
        """
        try:
            correspondentes = self.buscar_palavra(lingua, encontrar_palavra)
            if(isinstance(correspondentes, str)):
                return correspondentes
            descritivo = self.dialetos_criados[lingua]
            gramatica:dict[str,list[str,list[str,str]]] = descritivo['gramatica']
            # print("Erro:", gramatica)
            if('afixos' in gramatica.keys()):
                casos:dict[str,str]|str = gramatica['afixos']
            else:
                casos = "sem_afixo"
            silaba_tonica:str = gramatica['silaba_tonica']
            print(f"Língua {lingua}")
            if(isinstance(casos, str) or not apresentar_casos): #or eh_verbo(classe, lingua)
                for i in list(correspondentes.keys()):
                    classe_gramatical = correspondentes[i]['classe']
                    outros_significados = list(correspondentes[i]['significado'])
                    outros_significados.pop(outros_significados.index(encontrar_palavra))
                    palavra = correspondentes[i]["palavra"]
                    palavra = tools.sandhi(palavra)
                    palavra = tools.retornar_palavra_atona(palavra, silaba_tonica)
                    if(transcricao_fonetica):
                        palavra = self.inserir_sinal_tonico(palavra, silaba_tonica, 'lista')
                    print("="*50)
                    print(f"significado: {encontrar_palavra}\n\t| gramatica: {classe_gramatical}\n\t| palavra: /{"".join(palavra)}/\
                    \n\t| outros significados: {", ".join(outros_significados)}\n\t| Usabilidade: {descritivo['lingua'][i]['uso']:.2f}")
                print("="*50)

            elif(isinstance(casos, dict)):
                regra = gramatica["posicao"]
                for i in list(correspondentes.keys()):
                    gramatica = correspondentes[i]['classe']
                    outros_significados = list(correspondentes[i]['significado'])
                    outros_significados.pop(outros_significados.index(encontrar_palavra))
                    correspondente = self.inserir_sinal_tonico(correspondentes[i]["palavra"], silaba_tonica, 'lista')
                    print("="*50)
                    print(f"| significado: {encontrar_palavra}\n\t| gramatica: {gramatica}\n\t| palavra: /{"".join(correspondente)}/\
                    \n\t| posicao: {regra}\n\tCasos gramaticais:")
                    for c in casos:
                        if(c!="regra"):
                            palavra = correspondentes[i]["palavra"]
                            # print("Erro:", casos[c], regra)
                            if(len(casos[c])>0):
                                palavra = palavra + casos[c] if(regra=='posposicao') else casos[c] + palavra
                            if(regra=="posposicao"):
                                tmnh_p = len(palavra)
                                palavra = tools.filtro_fonetico(palavra)
                            elif(regra=="preposicao"):
                                tmnh_c = len(casos[c])
                                palavra = tools.filtro_fonetico(palavra)
                            palavra = tools.sandhi(palavra)
                            palavra = tools.retornar_palavra_atona(palavra, silaba_tonica)
                            if(transcricao_fonetica):
                                palavra = self.inserir_sinal_tonico(palavra, silaba_tonica, 'lista')
                            print(f"\t\t| {c}: /{"".join(palavra)}/")
                    print(f"\t| outros significados: {", ".join(outros_significados)}\n\t| Usabilidade: {descritivo['lingua'][i]['uso']:.2f}")
                print("="*50)
        except IndexError:
            print(f"Não existe correspondente para língua {lingua}")

    def mostrar_palavra_todas_linguas(self, encontrar_palavra:str, transcricao_fonetica:bool, melhorar_visual:bool = False)->list[str]|None:
        """
        Faz o output da funcao buscar_palavra_todas_linguas mais legivel. Retorna os indices em que
        o termo inserido em encontrar_palavra está presente.
        Args:
            encontrar_palavra (str) : espera uma string que tenha no dicionario de uma lingua
            transcricao_fonetica (bool) : habilita ou nao a transcrição em IPA
            melhorar_visual (bool) : muda o output de print(True) para display(False). *Funciona somente com jupyter!* Por padrão está True
        Return:
            list[str]
        Exemple
        >>>mostrar_palavra_todas_linguas(class.dialetos_criados, "mao", False, False)
        mao original    ɔt        æʔt tɨɣidɣ     hijaɸ
        64     ɛpxʊ  epeŋ       ʌbɦɨ    ɛbi        ap
        277      sɔn   sɔt        sɵd    tɔn       son
        487 mɨmɨɪnrɨ meʣrɯ      mɨdɨr  minɾi   meʊnɤʣe
        500                            itɛbʊ
        502                sɛtːumɛpχɨ
        510                              häb
        524                           tɔnänɾ
        532                                  mɯnɤʣeneh
        """
        palavras_encontradas:dict = self.buscar_palavra_todas_linguas(encontrar_palavra)
        linguas:list[str] = list(palavras_encontradas.keys())
        try:
            indices:list[str] = []
            for i in palavras_encontradas:
                indices_reserva = list(palavras_encontradas[i].keys())
                for j in indices_reserva:
                    if(j not in indices):
                        indices.append(j)
            indices.sort()

            palavras:list[str] = [linguas]
            palavras[0].insert(0, encontrar_palavra) # vai considerar o encontrar_palavra como lingua. palavras[0][2:] é o ideal para "esconder"
            # talvez dê para fazer uma função decorativa
            for i in indices:
                lista_provisoria:list[str] = [i]
                for lingua in linguas:
                    if(lingua==encontrar_palavra):
                        continue
                    try:
                        if(transcricao_fonetica):
                            palavra_fonada:list[str] = self.inserir_sinal_tonico(
                                palavras_encontradas[lingua][i]["palavra"],
                                self.dialetos_criados[lingua]['gramatica']['silaba_tonica'],
                                "lista"
                            )
                            lista_provisoria.append("/"+"".join(palavra_fonada)+"/")
                        else:
                            lista_provisoria.append("".join(palavras_encontradas[lingua][i]["palavra"]))
                    except:
                        lista_provisoria.append("---")
                palavras.append(lista_provisoria)
            df = pd.DataFrame(data=palavras[1:], columns=palavras[0])

            # Preenche os valores vazios para não quebrar a formatação
            df.fillna("", inplace=True, )
            try:
                print(df.to_string(index=False)) if melhorar_visual else display(df)
            except:
                print("Erro ao usar display.")
                print(df.to_string(index=False))
            return indices
        except:
            print("Não é um correspondente em nenhuma das línguas")

    def mostrar_tabela(self):
        """
        Mostra um dataframe de todos os indices da classe
        """
        dicionario = {}
        coluna = [n for n in self.nomes()]
        palavras = []
        indices = []
        for c in coluna:
            dicionario[c] = {}
            for i in self.dialetos_criados[c]['lingua'].keys():
                if(i not in indices):
                    indices.append(i)
        for c in coluna:
            for i in indices:
                try:
                    dicionario[c][i] = f"{"".join(self.dialetos_criados[c]['lingua'][i]['palavra'])} ({"_".join(self.dialetos_criados[c]['lingua'][i]['significado'])})"
                except:
                    dicionario[c][i] = ""
        df = pd.DataFrame(data = dicionario, index=indices , columns = coluna)
        return df

    def mostrar_(self, option:str)->None:
        """
        Mostra exemplos de conjugações, declinações, frases e títulos (dar um adjetivo a algo).
        Args:
            var (class): uma variavel var que contenha a(s) lingua(s)
            option (str): Recebe 'substantivo', 'verbo', 'frase' e 'titulo'
        Retorno:
            None

        Exemplo:
        >>>class.mostrar_('subs')
        Língua original
        ==================================================
        significado: medo
            | gramatica: adjetivo
            | palavra: /sun/
            | outros significados:
            | Usabilidade: 1.00
        ==================================================

        Língua amɐ
        ==================================================
        | significado: medo
            | gramatica: adjetivo
            | palavra: /'sun./
            | posicao: preposicao
            Casos gramaticais:
                | cargo: /nuɾsʊn/
                | locativo: /esʊnɘksʊn/
                | dativo: /ɪpusʊn/
                | acusativo: /utsʊn/
                | instrumental: /nisʊn/
                | genitivo: /ɾisʊn/
            | outros significados:
            | Usabilidade: 1.00
        ==================================================
        [...]

        >>>mostrar_(var = ramo_1, option = 't')
        Língua original:
        /o.'kej.‿'mo.ɾes./
        Tradução*
        Substantivo:lama (oke)
        Adjetivo:preto (ɪmoɾes)

        Língua ɪmoɾes:
        /ɪ.'ɾʊj.‿'mu.ɾʊn./
        Tradução*
        Substantivo:arvore rapido (iɾʊ)
        Adjetivo:livre (ɪmuɾʊn)

        * Note que a sequencia de palavras pode não ser muito concruente, a escolha
        de palavras também é aleatória

        >>>mostrar_(var = ramo_1, option = 'frase')

        """
        # print(self.dialetos_criados['original']['gramatica']['estrutura'])

        if(option.lower().startswith('s')):
            p_sorteado = self.sortear_palavras(1)[0]
            for l in self.nomes():
                self.mostrar_palavra_mais_descritiva(l, p_sorteado, True, False)
                print('')
        elif(option.lower().startswith('v')):
            indice = self.sortear_indice("original", "verbo")
            print(f"Indice: {indice}")
            for l in self.nomes():
                print(f"Língua {l}")
                self.conjugar_verbo(l, indice)
                print("")
        elif(option.lower().startswith('t')):
            for lingua in self.nomes():
                print(f"Língua {lingua}:")
                self.dar_titulo(lingua)
                print('')
        elif(option.lower().startswith('f')):
            print("-".join(self.dialetos_criados['original']['gramatica']['estrutura']))
            print("="*50)
            for lingua in self.nomes():
                print(f"Língua {lingua}:")
                self.montar_frase(lingua, True, True)
                print("")
                print("="*50)
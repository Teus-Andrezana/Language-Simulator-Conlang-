from random import randint, choice, choices, random, uniform, shuffle
import re
import json

with open(file='biblioteca/fonetica.json', mode='r', encoding='utf-8') as file:
    regra_fonetica = json.load(file)
file.close()

global_consonants_str:str = "".join(list(regra_fonetica['consoante'].keys()))
global_vowels_str:str = "".join(list(regra_fonetica['vogal'].keys()))

"""
CHECAGEM/VERIFICAR
"""

def verificar_classe(som:str)->str | list[str]:
    """
    Verifica as definições do som inserido.
    Args:
        som (str): uma letra/som que pertença ao dicionário regra_fonetica.
    Retorno:
        str | None | list[str]
    Exemplo:
    >>>verificar_classe(som = "k")
    ['velar', 'oclusiva', 'surda']
    >>>verificar_classe(som = "â")
    â
    """
    if(len(som)>0 and not eh_diacritico(som[0])):
        # print(f"Som: {som} e tamanho: {len(som)}")
        if(eh_vogal(som) or eh_consoante(som[0])):
            classe:list[str] = list(regra_fonetica[verificar_som(som[0])][som[0]]["classe"])
        return classe
    return som

def verificar_som(som:str)->str:
    """
    Verifica se a string eh uma vogal ou uma consoante.
    Args:
        som (str) : espera uma consoante ou vogal
    Return:
        str
    Exemple:
    >>> verificar_som("s")
    consoante
    >>> verificar_som("a")
    vogal
    """
    # tipo_som:str=""
    # if(eh_vogal(som)):
    #     tipo_som = "vogal"
    # elif(eh_consoante(som)):
    #     tipo_som = "consoante"
    # return tipo_som
    return "vogal" if(eh_vogal(som)) else "consoante"

def contar_vogais(palavra:str)->int:
    """
    Conta quantas vogais tem em uma palavra
    EXEMPLO
    contar_vogais(['a','k','a','n','a'])
    3
    """
    quantidade:int = 0
    for letra in palavra:
        if(eh_vogal(letra)):
            quantidade+=1
    return quantidade

def eh_rotica(som:str)->bool:
    """
    RESUMO
        Verifica se o som eh uma rotica, retornando um valor booleano.
    PARAMETROS
        som -> espera uma string
    RETORNO
        bool
    >>>eh_rotica("r")
    True
    >>>eh_rotica("f")
    False
    """
    if(isinstance(som, str)):
        return som in ['r', 'h', 'ʁ', 'ɻ', 'ɾ', 'ɹ', 'ʀ', 'ɽ', 'x', 'χ', 'ɦ']
    return False

def eh_consoante(som:str)->bool:
    """
    RESUMO
        Verificar se o parametro eh uma consoante.
    PARAMETRO
        som -> espera uma string
    RETORNO
        bool
    """
    # print(f"{som} acessou eh_consoante()")
    if isinstance(som, str):
        if len(som) == 1:
            return som in regra_fonetica['consoante']
        return som[0] in regra_fonetica['consoante']
    return False

def eh_vogal(som:str)->bool:
    """
    RESUMO
        Verificar se o parametro eh uma vogal.
    PARAMETRO
        som -> espera uma string
    RETORNO
        bool
    """
    # print(f"{som} acessou eh_vogal()")
    if isinstance(som, str):
        if len(som) == 1:
            return som in regra_fonetica['vogal']
        return som[0] in regra_fonetica['vogal']
    return False

def eh_semivogal(som:str)->bool:
    """
    RESUMO
        Verifica se o som eh uma semivogal, retornando um valor booleano.
    PARAMETROS
        som -> espera uma string
    RETORNO
        bool
    """
    if(isinstance(som, str)):
        return som in ['w', 'j']

def eh_diacritico(som:str)->bool:
    """
    RESUMO
        Verifica se o som eh um diacritico, retornando um valor booleano.
    PARAMETROS
        som -> espera uma string
    RETORNO
        bool
    """
    if(isinstance(som, str)):
        letra = "ø̞"
        return som in ['ʷ', 'ʲ', 'ʰ', '~', letra[1], 'ː']

def eh_retroflexa(som:str)->bool:
    '''
    FUNCAO
    Usada principalmente para identificar se o som inserido é uma retroflexa. Em outros contextos, é usado
    para ver se o som anterior ao inserido também é uma retroflexa, e, caso não seja, vai tentar convertê-lo
    em um som de mesmo tipo.
    #
    INPUTS
    som -> é um argumento do tipo string. É esperado que seja uma string pertencente ao
    dicionário regras_foneticas
    #
    RETORNO
    bool
    #
    EXEMPLO
    >>>eh_retroflexa('a')
    False
    >>>eh_retroflexa("ꭧ")
    True
    >>>eh_retroflexa('ʂ')
    True
    '''
    return som in ["ʈ", "ꭧ", "ɖ", "ɽ", "ʂ", "ʐ", "ɳ", "ɻ"] or verificar_classe(som)[0] == 'retroflexa'

def corrigir_palavra(palavra:list[str])->list[str]:
    """
    Garante que nomes com a grafia "ː" e outras que se separam de seus fonemas por conta do list()
    não se dividam
    Args:
        palavra (list[str]): conjunto de caracteres com ou sem problemas
    Retorno:
        list[str]
    Exemplo:
    >>> corrigir_palavra(list(['tʊnaːbwɛ'))
    ['t', 'ʊ', 'n', 'aː', 'b', 'w', 'ɛ']
    >>> corrigir_palavra(list(['äɾɐw'))
    ['ä', 'ɾ', 'ɐ', 'w']
    """
    index:int = 0
    while(index<len(palavra)):
        if(palavra[index]=='ː'):
            palavra.pop(index)
            palavra[index-1] = f'{palavra[index-1]}ː'
        index+=1
    return palavra

"""
ESTRUTURA SEM REGEX, COM WHILE
"""
def retornar_palavra_atona(palavra:str, silaba_tonica:str)->str:
    """
    Enfraquece as vogais atonas, deixando apenas a tonica como estava.
    Args:
        palavra (str): sequencia de caracteres
        silaba_tonica (str): se é 'oxitona', 'paroxitona' ou 'proparoxitona'
    >>>retornar_palavra_atonca(['p', 'u', 'm', 'i'], "oxitona")
    ['p', 'ʊ', 'm', 'i']
    """
    leni = [
        (r'[aäʌɑæ]', 'ɐ'), (r'[uʉɯ]', 'ʊ'), (r'[i]', 'ɪ'), (r'[ɞ]', 'ɵ'), (r'y', 'ʏ'),
        (r'ɶø', 'œ'), (r'ɤ', 'ʌ')
    ]
    #sem muita precisao
    lenicao:dict[str,str] = {
        'a':'ɐ',
        'i':'ɪ',
        'u':'ʊ',
        'ɶ':'œ',
        'ø':'ə',
        'y':'ʏ',
        'ʌ':'ɐ',
        'ä':'ɐ',
        'ɤ':'ʌ',
        'ø':'œ',
        'ɞ':'ɵ',
        'ɑ':'ɐ',
        'æ':'ɐ',
        'ʉ':'ʊ',
        'ɯ':'ʊ',
    }
    fortificacao:dict[str,str|list[str]] = { #vai precisar ter informação das vogais da língua para decidir para qual som fortificar ou leniçionar
        'ɐ':'a',
        'ɪ':'i',
        'ʊ':'u',
        'ə':'ɐ',
        'œ':'ɶ',
        'ʏ':'y',
        'ɵ':'ɞ',
        'ɑ':choice([['a','ʊ'], 'ɔ', 'ɑː', ['ɑ','ɪ']])
    }
    lista_fracas:list[str] = list(lenicao.keys())
    lista_fortes:list[str] = list(fortificacao.keys())
    harmonized_word:list[str] = corrigir_palavra(list(palavra))[::-1]
    qntd_consoantes:int = 0
    qntd_vogais:int = 0
    calculo_vogais:int = contar_vogais(palavra)
    tonica_encontrada:bool = False
    index:int = 0
    while len(harmonized_word)>index:
        letra = harmonized_word[index]
        if(eh_vogal(letra)):
            # print(f'[1] {letra} é uma vogal')
            qntd_vogais +=1
            if(not tonica_encontrada):
                # print('\t[2] Tônica não encontrada')
                if(silaba_tonica == 'proparoxitona' and qntd_vogais>2 or qntd_consoantes>2):
                    # print('\t\t[3] Sílaba tônica encontrada: proparoxitona')
                    tonica_encontrada = True
                    if(letra in lista_fortes):
                        fortificado:str|list[str] = fortificacao[letra]
                        # print(fortificado)
                        if(isinstance(fortificado, str)):
                            harmonized_word[index] = fortificado
                        else:
                            harmonized_word[index] = fortificado[0]
                            harmonized_word.insert(index, fortificado[1])
                elif(((silaba_tonica in 'paroxitona' or (calculo_vogais<3 and silaba_tonica=='proparoxitona')) and (qntd_vogais>1 or qntd_consoantes>1))):
                    # print('\t\t[3] Sílaba tônica encontrada paroxítona')
                    tonica_encontrada = True
                    if(letra in lista_fortes):
                        fortificado:str|list[str] = fortificacao[letra]
                        # print(fortificado)
                        if(isinstance(fortificado, str)):
                            harmonized_word[index] = fortificado
                        else:
                            harmonized_word[index] = fortificado[0]
                            harmonized_word.insert(index, fortificado[1])
                elif(silaba_tonica=='oxitona' or contar_vogais(palavra)==1):
                    # print('\t\t[3] Sílaba tônica encontrada oxítona')
                    tonica_encontrada = True
                    if(letra in lista_fortes):
                        fortificado:str|list[str] = fortificacao[letra]
                        # print(fortificado)
                        if(isinstance(fortificado, str)):
                            harmonized_word[index] = fortificado
                        else:
                            harmonized_word[index] = fortificado[0]
                            harmonized_word.insert(index, fortificado[1])
                else:
                    # print(f'\t\t[3] Enfraquecendo {letra}')
                    if(letra in lista_fracas):
                        harmonized_word[index] = lenicao[letra]
            else:
                # print(f'\t[2] Sílaba tônica já encontrada. Lenicionar...')
                if(letra in lista_fracas):
                    # print(f'\t\t[3] Vogal {letra} consta na lista das fracas. Lenicionando...')
                    harmonized_word[index] = lenicao[letra]
        elif(eh_consoante(letra)):
            # print(f'[1] {letra} é uma consoante')
            qntd_consoantes+=1
        index+=1
    palavra = harmonized_word[::-1]
    return "".join(palavra)

def palatalizar(palavra:list[str], loc_1:int, loc_2:int)->list[str]:
    """
    Permite a palatalização. Não é garantia de que isso vai acontecer.
    Analisa quantas vogais altas fechadas estão próximas da consoante, o que
    pode aumentar as chances de palatalização.

    EXEMPLO
    >>>palatalizar(['s', 'j', 'ɪ', 's', 'ɪ', 'u', 't', 'ʊ'])
    ['s', 'j', 'ɪ', 'ʃ', 'ɪ', 'u', 't', 'ʊ']
    """
    def eh_vogal_gatilho(v:str)->bool:
        return eh_vogal(v) and not any(i in ['aberta', 'posterior'] for i in verificar_classe(v))

    def aplicar_traco(loc:int)->list[str]:
        traco:str = f'pos-{verificar_classe(palavra[loc])[0]}'
        palavra[loc] = retornar_aproximante(palavra[loc], traco, 0)

    if(eh_consoante(palavra[loc_1])):
        if(eh_vogal_gatilho(palavra[loc_2])):
            if(loc_1-1>=0 and eh_vogal_gatilho(palavra[loc_1-1])):
                aplicar_traco(loc_1)
            elif(random()>0.6):
                aplicar_traco(loc_1)

    elif(eh_vogal_gatilho(palavra[loc_1])):
        if(eh_consoante(palavra[loc_2])):
            if(loc_2+1<len(palavra) and eh_vogal_gatilho(palavra[loc_2+1])):
                aplicar_traco(loc_2)
            elif(random()>0.6):
                traco:str = f'pos-{verificar_classe(palavra[loc_2])[0]}'
                palavra[loc_2] = retornar_aproximante(palavra[loc_2], traco, 0)
    return palavra

def excesso_ditongo(palavra:list[str], loc_1:int, loc_2:int)->list[str]:
    """
    RESUMO
        Verifica se existe uma sequencia de vogais, se existir, retira
        a vogal do meio.
    PARAMETROS
        palavra -> espera uma lista de strings
    RETORNO
        list[str]
    """
    if(loc_2+1<len(palavra)):
        vogais:list[str] = [palavra[loc_1], palavra[loc_2], palavra[loc_2+1]]
        if(all(eh_vogal(v) for v in vogais)):
            palavra.pop(choice([loc_1, loc_2+1]))
    return palavra

def shwa_errado(palavra:list[str], loc_1:int, loc_2:int)->list[str]:
    """
    """
    l1:str=palavra[loc_1]
    l2:str=palavra[loc_2]
    if(all(eh_vogal(v) for v in [l1, l2]) and "ə" in [l1, l2]):
        if(any(i in verificar_classe(l1) for i in ['aberta', 'fechada']) or any(i in verificar_classe(l2) for i in ['aberta', 'fechada'])):
            palavra.pop(loc_1) if l1=="ə" else palavra.pop(loc_2)
        else:
            if(l1=="ə"):
                palavra.pop(loc_1)
    return palavra

def regra_de_sandhi(palavra:list[str], loc_1:int, loc_2:int):
    """
    Funde dois sons vizinhos que se assemelham.
    Args:
        palavra (list[str]):
        loc_1 (int):
        loc_2 (int):
    Exemplo:
    >>> regra_de_sandhi(['n', 'æ', 'g', 'k', 'ɔ', 'ɾ', 'i'], 2, 3)
    ['n', 'æ', 'kː', 'ɔ', 'ɾ', 'i']
    """
    p1:str = palavra[loc_1]
    p2:str = palavra[loc_2]
    if(semelhanca_entre_sons(p1, p2)>0.83):
        classe_verificada:list[str] = verificar_classe(p1)
        if(classe_verificada[:2]==verificar_classe(p2)[:2]):
            palavra.pop(loc_1)
            palavra[loc_1] = p1+'ː'
        elif(classe_verificada[0]=="alveolar"):
            if(classe_verificada[1]=="oclusiva"):
                if(classe_verificada[2] == "surda"):
                    palavra.pop(loc_1)
                    palavra[loc_1] = "ʦ"
                elif(classe_verificada[2] == "sonora"):
                    palavra.pop(loc_1)
                    palavra[loc_1] = "ʣ"
        elif(eh_vogal(p2)):
            palavra.pop(loc_1)
            palavra[loc_1] = p1+'ː'
    return palavra


def modificar_sonora_ou_surda(palavra:list[str], loc_1:int, loc_2:int): #, tipo:str
    """
    RESUMO
    Verifica se a consoante seguinte a outra é uma surda. Caso a anterior seja sonora, converte em surda.
    INPUTS
    tipo -> recebe somente "fortificar" ou "enfraquecer"
    EXEMPLO
    >>>modificar_sonora_ou_surda(['n', 'æ', 'd', 'k', 'ɔ', 'ɾ', 'i'], 2, 3, "fortificar")
    ['n', 'æ', 't', 'k', 'ɔ', 'ɾ', 'i']
    """
    # print(palavra)
    classe_verificada_1 = verificar_classe(palavra[loc_1])
    classe_verificada_2 = verificar_classe(palavra[loc_2])
    if(not (eh_rotica(palavra[loc_2]) or eh_w_j_h(palavra[loc_2] or palavra[loc_2] not  in ['m', 'n'] or palavra[loc_1] not in ['m', 'n']))):
        valor_um, valor_dois = ("sonora", "surda") if("surda" in classe_verificada_2) else ("surda", "sonora")
        # print(valor_um, valor_dois)
        if(classe_verificada_1[2]== valor_um and classe_verificada_2[2] == valor_dois):
            palavra[loc_1] = retornar_aproximante(palavra[loc_1], valor_dois, 2)[0]
    return palavra

def esquecer(word:str)->str:
    """
    Corta partes do meio da palavra. Corta principalmente dependendo da silaba tonica, se porparoxitona,
    entao corta as ultimas. Se for oxitona, corta as primeras, e, então, se for paroxitona, tende a cortar as bordas.
    INPUTS
    palavra -> precisa de uma lista com caracteres.
    EXEMPLO
    >>>esquecer(['i', 'g', 'i', 'm', 'ʊ', 'x', 'a', 'ʊ', 'j', 'u', 'm', 'a', 'r', 'a', 'ʋ', 'u', 't', 'u', 't', 'x',  'i'], 'proparoxitona')
    ['i', 'g', 'i', 'm', 'ʊ', 'x', 'a', 'ʊ', 'j', 'u', 'm', 'a']
    """
    if(isinstance(word, str)):
        word = list(word)
    if(len(word)>7 and random()>0.8):
        inicio:list[str] = word[:3]
        fim:list[str] = word[-3:]
        word = inicio+fim
    elif(len(word)>10):
        inicio:list[str] = word[:4]
        fim:list[str] = word[-4:]
        word = inicio+fim
    return "".join(word)

def cluster_alveolares(palavra:list[str], loc_1:str, loc_2:str)->str:
    classe_verificada_A:list[str] = verificar_classe(palavra[loc_1])
    classe_verificada_B:list[str] = verificar_classe(palavra[loc_2])
    if([classe_verificada_A[0] == 'alveolar' and classe_verificada_B[0]] == 'alveolar'):
        l1:str = palavra[loc_1]
        l2:str = palavra[loc_2]
        lista_simplificada:list[str] = [l1[0], l2[0]]
        filtro:list = [
            all(i in ["d", "ʣ"] for i in lista_simplificada),
            all(i in ["t", "ʦ"] for i in lista_simplificada),
            all(i in ["s", "z"] for i in lista_simplificada)
        ]
        grupos:list[tuple[str,str]] = [
            ("d", "ʣ"), ("t", "ʦ"), ("s", "z")
        ]
        if(any(all(som in grupo for som in lista_simplificada) for grupo in grupos)):
            palavra.pop(loc_1)
            palavra[loc_1]+= 'ː'
    return palavra

def cluster_fricativas(palavra:list[str], loc_1:int, loc_2:int)->list[str]:
    classe_verificar_A:list[str] = verificar_classe(palavra[loc_1])
    classe_verificar_B:list[str] = verificar_classe(palavra[loc_2])
    if(classe_verificar_A[1] == 'ficativa' and classe_verificar_B[1] == 'fricativa'):
        l1:str = palavra[loc_1]
        l2:str = palavra[loc_2]
        if(all(i in verificar_classe(l1) for i in ['fricativa', 'sonora']) and all(i in verificar_classe(l2) for i in ['fricativa', 'sonora'])):
            lista_efeito:list = [retornar_aproximante(l1, choice(['oclusiva', 'africada']), 1), retornar_aproximante(l1, 'surda', 2)]
            if(loc_1>0):
                if(eh_vogal(palavra[loc_2+1])):
                    palavra.insert(loc_2, palavra.pop(loc_2+1))
                elif(eh_vogal(palavra[loc_1-1])):
                    palavra.insert(loc_1, palavra.pop(loc_1-1))
            else:
                palavra[loc_1] = lista_efeito[randint(0,1)]
                palavra.pop(loc_2)
    return palavra

def assimilacao_silabica(palavra:list[str], loc_1, loc_2)->list[str]:
    """
    RESUMO
        Assimilação de sílabas e ou sons por germinação.
            /sɛʃ/ pode mudar para /ʃɛʃ/ ou /sɛs/. Assim como
            se for /...kogo.../, a aproximação do som /k/ com o som /g/
            podem encurtar as sílabas em uma, dando prioridade a segunda
            sílaba.
    PARAMETROS
    RETORNO
    """
    if(loc_1>0 and loc_2<len(palavra)):
        l1:str = palavra[loc_1]
        loc_2 = loc_2+1
        if(eh_consoante(l1) and len(palavra)>=4 and randint(0,100)>60 and loc_2+1<len(palavra)):
            l3:str = palavra[loc_2]
            if(semelhanca_entre_sons(l1, l3)>0.83):
                palavra[loc_1] = palavra[loc_2]

        if(eh_consoante(l1) and loc_2+1<len(palavra)):
            l2:str = palavra[loc_1+1]
            l3:str = palavra[loc_2]
            if(semelhanca_entre_sons(l2,l3)>0.83):
                palavra.pop(loc_1)
                palavra.pop(loc_1)
    return palavra

def tratamento_erros(func, *args, **kwargs)->list[str]:
    """
    Trata erros de index, type, entre outros.
    Args:
        func: função que vai ser usada
        args/kwargs: os argumentos da função
    Exemplo:
    >>> tratamento_erros(regra_de_sandhi, palavra, loc_1, loc_2)

    Se tiver erro, a função pula sem alterar o valor original.
    """
    try:
        return func(*args, **kwargs)

    except Exception as e:
        if args:
            return args[0]
        elif 'palavra' in kwargs:
            return kwargs['palavra']
        return "" # caso palavra não tenha sido recebida

def iterar_efeitos(palavra:list[str], efeitos:list)->list[str]:
    """
    Altera a palavra a partir dos efeitos escolhidos.
    Args:
        palavra (list[str]): uma sequência de caracteres;
        efeitos (list[callable]): uma lista com os efeitos que vão alterar
            em algum grau a palavra;
    Retorno:
        list[str]
    Exemplo:
    >>>iterar_efeitos(palavra = ['a','g','k','i'], efeitos = [modificar_sonara_ou_surda, regra_de_sandhi])
    ['a', 'kː', 'i']
    """
    loc_1:int = 0
    loc_2:int = 1
    while(loc_1<len(palavra)-1):
        if(loc_2<len(palavra)):
            for f in efeitos:
                palavra = tratamento_erros(f, palavra, loc_1, loc_2)
        loc_1+=1
        loc_2+=1
    return palavra

def surtir_efeitos(palavra:str)->str:
    """
    Faz passo a passo podendo alterar a palavra inserida. A mudança não é sempre garantida.
    Args:
        palavra (str) : string
    Return:
        str
    list[str]

    EXEMPLO
    >>>surtir_efeitos(['a','k','k','u','m','y'], class.dialetos_criados["original"]["gramatica"]["silaba_tonica"])
    ['a','k:','y','m','u']
    """
    efeitos:list = [
        excesso_ditongo, modificar_sonora_ou_surda, cluster_fricativas,
        cluster_alveolares, assimilacao_silabica, palatalizar,
    ]
    palavra = iterar_efeitos(palavra, efeitos)
    return palavra

"""
EFEITOS COM OU SEM REGEX
"""
def verificar_classes_regra_fonetica(classe_fonetica:list[str], tipo:str, exatidao:bool|int)->tuple[list[str], list[str]]:
    """
    Retorna sons com suas respectivas classes, buscando as que batem
        com os termos passados no parametro classe_fonetica.
    Args:
        - classe_fonetica (list[str]) : espera uma lista de strings contendo a classe de um som
        - tipo (str) : espera uma "consoante" ou "vogal"
        - exatidao (bool | int) : espera um True/1 ou False/0 para mostrar os sons que tem
            a exata classe_fonetica ou mostrar todos que tiverem pelo menos um
    Return:
        tuple(list[str], list[list[str]])
    Exemple:
        >>> verificar_classes_regra_fonetica(classe_fonetica = ["plosiva"], tipo = "consoante", exatidao = 0)
        ['p', 'b', 't', 'd', 'c', 'ɟ', 'k', 'g', 'ʔ', 'q', 'ɢ', 'ʈ', 'ɖ', ...], [['bilabial', 'oclusiva', 'surda'],
  ['bilabial', 'oclusiva', 'sonora'], ...]
    """
    sons:list[str] = []
    classes:list[str] = []
    for som in regra_fonetica[tipo]:
        classe_verificada:list[str] = verificar_classe(som)
        if(all(i in classe_verificada for i in classe_fonetica) and exatidao in [True, 1]):
            # print(f"{som} {classe_verificada}")
            sons.append(som)
            classes.append(classe_verificada)
        elif(any(i in classe_verificada for i in classe_fonetica) and exatidao in [False, 0]):
            # print(f"{som} {classe_verificada}")
            sons.append(som)
            classes.append(classe_verificada)
    return sons, classes

def conferir_consoante(som:str, classificacao:list[str])->bool: #verifica se a classe
    """
    RESUMO
    Args:
        som -> espera uma string
        classificacao -> espera uma lista de strings
    Retorno:
        bool
    """
    comparativo:list[str]=list(regra_fonetica['consoante'][som]['classe'])
    for _, item in enumerate(comparativo):
            if(len(comparativo)!=len(classificacao)):
                return False
            if(item not in classificacao):
                return False
    return True

def metatase(configuracao:float, palavra:list[str])->list[str]:
    """
    RESUMO
        Pega uma letra aleatoria e muda de lugar com outra.
    PARAMETRO
        palavra -> espera receber uma lista string
    Retorno:
        list[str]
    """
    if(len(palavra)>3):
        if(random()<configuracao):
            letra:int = randint(0,len(palavra)-1)
            letra_atual:str=palavra[letra]
            if(letra>1):
                if(random()>0.5 and letra<len(palavra)-1):
                    letra_alvo:str=palavra[letra+1]
                    palavra[letra]=letra_alvo
                    palavra[letra+1]=letra_atual
                else:
                    letra_alvo:str=palavra[letra-1]
                    palavra[letra]=letra_alvo
                    palavra[letra-1]=letra_atual
            else:
                letra_alvo:str=palavra[letra+1]
                palavra[letra]=letra_alvo
                palavra[letra+1]=letra_atual
    return palavra

def efeito_separador(palavra:list[str])->list[str]:
    if(len(palavra)>0):
        index:int = 0
        while(index<len(palavra)):
            if(len(palavra[index])>1 and any(eh_diacritico(c) for c in palavra[index])==False):
                palavra.insert(index+1, palavra[index][1])
                palavra[index] = palavra[index][0]
            index+=1
    return palavra

def sons_da_lingua()->tuple[list[str], list[str]]:
    conjunto_de_vogais:list[str]=list(regra_fonetica['vogal'].keys())
    conjunto_de_consoantes:list[str]=list(regra_fonetica['consoante'].keys())
    consoantes_primarias:list[str]=['p','k','t']
    vogais_listadas:list[str]=[]
    consoantes_listadas:list[str]=[]

    for _ in range(randint(5,10)):
        vogal:str=choice(conjunto_de_vogais)
        while(vogal in vogais_listadas):
            vogal=choice(conjunto_de_vogais)
        vogais_listadas.append(vogal)

    for _ in range(randint(5,20)):
        if(len(consoantes_listadas)<2):
            primaria_sorteada:str=choice(consoantes_primarias)
            consoantes_listadas.append(primaria_sorteada)
            consoantes_primarias.remove(primaria_sorteada)
        else:
            consoante:str=choice(conjunto_de_consoantes)
            classe_consoante:list[str]=regra_fonetica['consoante'][consoante]['classe'] # <------------
            while(consoante in consoantes_listadas or "fricativa" in classe_consoante):
                    consoante=choice(conjunto_de_consoantes)
                    classe_consoante=regra_fonetica['consoante'][consoante]['classe']
            consoantes_listadas.append(consoante)
    return vogais_listadas, consoantes_listadas

def retornar_aproximante(som:str, traco:str, posicao:int)->str|list[str]:
    """
    Retorna um som semelhante ao selecionado de acordo com as caracteristica
        modificadas, ex.: /k/, se trocar "surda" por "sonora, vai retornar /g/.
    Args:
        som (str) : espera um som só
        traco (str) : traco a ser substituido
        posicao (int) : qual posicao da lista deseja mudar ou acrescentar
    Retorno:
        str | list[str]
    EXEMPLO
    >>> retornar_aproximante("g", "surdo", 2)
    "k"
    """
    som_base = som[0]
    tipo_de_letra:str = "consoante" if eh_consoante(som_base[0]) else "vogal"
    classe_som:list[str] = regra_fonetica[tipo_de_letra][som_base]["classe"].copy()
    if(len(classe_som)-1<posicao):
        classe_som.append(traco)
    else:
        classe_som[posicao] = traco
    sons_possiveis:list[str] = []
    for s in regra_fonetica[tipo_de_letra]:
        if(regra_fonetica[tipo_de_letra][s]["classe"] == classe_som):
            sons_possiveis.append(s)
    if(len(sons_possiveis)>1):
        return sons_possiveis
    elif(len(sons_possiveis) == 1):
        return sons_possiveis[0]
    else:
        return som
    # return sons_possiveis if len(sons_possiveis) else som

def pegar_difone(consoante:str)->str: # pega uma consoante e junta com um diacrítico, criando uma nova palavra
    diacriticos:list[str]=['ʷ', 'ʲ', 'ʰ']
    return consoante if(eh_semivogal(consoante)) else consoante+choice(diacriticos)

####
# PALATO, ARREDONDAMENTO E ASPIRAÇÃO
####

def se_tem_palatal(palavra:str, som_objetivo:str, loc_letra:int)->str:
  if(random()>=0.5):
    palavra[loc_letra] = som_objetivo.replace('ʲ', '')
    return palavra
  palavra[loc_letra] = som_objetivo.replace('ʲ', '')
  palavra.insert(loc_letra+1, 'ɪ')
  return palavra

def se_tem_arredondamento(palavra:list[str], som_objetivo:str, loc_letra:int)->list[str]:
    if(random()>=0.5):
      palavra[loc_letra] = som_objetivo[0]
      return palavra
    palavra[loc_letra] = som_objetivo[0]
    palavra.insert(loc_letra+1, 'ʊ')
    return palavra

def proibicoes_em_difones(palavra:list[str], som_objetivo:str, loc_letra:int, proibicao:bool)->list[str]:
  if(eh_consoante(som_objetivo)):
    som_objetivo:str=choice(regra_fonetica['consoante'][som_objetivo]['possibilidades'])
    if(proibicao):
      palavra[loc_letra] = som_objetivo[0]
  else:
    print(f"Som /{som_objetivo}/ não encontrado")
    palavra[loc_letra] = som_objetivo.replace('ʲ', '').replace('ʷ', '').replace('ʰ', '')
  return palavra

def rotica_probida(word:str)->str:
    """
    Verifica se existe mais de uma rotica seguidamente, retirando a primeira encontrada.
    """
    word = re.sub(r'([rʁɻɾɹʀɽ])[rʁɻɾɹʀɽ]+', r'\g<1>', word)
    return word

def lateral_proibida(word:str)->str:
    """
    """
    if(isinstance(word, str)):
        word = corrigir_palavra(list(word))
    if(len(word)>2):
        w1:str = word[0]
        w2:str = word[1]
        if(any(i in "lateral" for i in verificar_classe(w1)) and eh_consoante(w2)):
            lateral:str = word[0]
            word[0] = word[1]
            word[1] = lateral
        
    word = "".join(word)
    return word

def eh_w_j_h(som:str)->bool:
    return som in ['w', 'j', 'h']

def deleta_diacriticos_solos(palavra:list[str]):
    index:int=0
    while(index<len(palavra)):
        if(eh_diacritico(palavra[index])):
            palavra.pop(index)
        index+=1
    return palavra

def semelhanca_entre_sons(som_um:str, som_dois:str)->float:
  if(len(som_dois)>0 and len(som_um)>0):
    som_um = som_um[0]
    som_dois = som_dois[0]
    classificacao_1:list = list(verificar_classe(som_um))
    classificacao_2:list = list(verificar_classe(som_dois))
    pontos:int = 0
    total:int = max(len(classificacao_1), len(classificacao_2))
    aproximadas: set = {
        # Fundos da boca
        ("velar", "glotal"),
        ("velar", "uvular"),
        ("uvular", "glotal"),
        ("velar", "palatal"),

        # Frente da boca
        ("bilabial", "labiodental"),
        ("labiodental", "dental"),
        ("dental", "alveolar"),

        # Meio da boca
        ("alveolar", "pos-alveolar"),
        ("pos-alveolar", "palatal"),
        ("pos-alveolar", "retroflexa"),
        ("alveolar", "velarizada"),
        ("velar", "velarizada"),

        # Outras secundárias importantes
        ("palatal", "palatalizada"),
        ("alveolar", "palatalizada"),
        ("bilabial", "labializada"),
        ("velar", "labializada"),

        # Obstruintes
        ("stop", "oclusiva"),
        ("oclusiva", "fricativa"),
        ("fricativa", "africada"),
        ("oclusiva", "africada"),

        # Soantes & Líquidas
        ("lateral", "lateral"),
        ("lateral", "fricativa"),
        ("aproximante", "liquida"),
        ("trill", "tap"),
        ("tap", "flap"),
        ("nasal", "oclusiva"),

        # --- VOZEAMENTO ---
        ("surda", "sonora"),
        ("fechada", "quase-fechada"),
        ("quase-fechada", "semifechada"),
        ("fechada", "semifechada"),

        # Do meio para baixo
        ("semifechada", "media"),
        ("media", "semiaberta"),
        ("semifechada", "semiaberta"),

        # Do fundo (Aberta)
        ("semiaberta", "quase-aberta"),
        ("quase-aberta", "aberta"),
        ("semiaberta", "aberta"),
        ("anterior", "central"),
        ("central", "posterior"),
        ("arredondada", "nao-arredondada"),

    }

    for i in classificacao_1[:]:
      if(i in classificacao_2):
        pontos+=1
        classificacao_1.remove(i)
        classificacao_2.remove(i)

    for i in classificacao_1:
      for j in classificacao_2:
        caracteristica_anterior:str = i
        caracteristica_posterior:str = j
        if((caracteristica_anterior, caracteristica_posterior) in aproximadas or (caracteristica_posterior, caracteristica_anterior) in aproximadas):
          pontos+=0.5
          break

    return pontos/total if pontos!=0 else 0.0
  return 0

# HARMONIA_VOCAL é para ser usada apenas em casos de aglutinações, onde ele readapta os extremos
def harmonia_vocal(palavra: list[str], loc_1: int, loc_2: int) -> list[str]:
    # Movidos para o topo para construir apenas uma vez por chamada
    graus_de_abertura = {
        'aberta': 3, 'semiaberta': 2, 'quase-aberta': 1, 'central': 0,
        'quase-fechada': -1, 'semifechada': -2, 'fechada': -3
    }
    graus_de_garganta = {
        'anterior': 2, 'quase-anterior': 1, 'central': 0,
        'quase-posterior': -1, 'posterior': -2
    }

    def modificar_garganta(classe_s: str, grau_retornado: str) -> str:
        if classe_s == 'anterior' and grau_retornado == 'quase-aberta':
            return retornar_grau(graus_de_garganta, graus_de_garganta.get(classe_s, 0), -1)
        elif classe_s == 'posterior' and grau_retornado == 'quase-fechada':
            return retornar_grau(graus_de_garganta, graus_de_garganta.get(classe_s, 0), 1)
        elif classe_s == 'quase-posterior' and grau_retornado != 'quase-fechada':
            return retornar_grau(graus_de_garganta, graus_de_garganta.get(classe_s, 0), -1) 
        elif classe_s == 'quase-anterior' and grau_retornado != 'quase-fechada':
            return retornar_grau(graus_de_garganta, graus_de_garganta.get(classe_s, 0), 1)   
        return classe_s

    def retornar_grau(dicio: dict, n1: int, n2: int) -> str:
        # Substitui a falha da lambda evitando StopIteration oculto
        for k, v in dicio.items():
            if v == (n1 + n2): return k
        for k, v in dicio.items():
            if v == n1: return k
        return None

    classe_sucessora = verificar_classe(palavra[loc_1])
    classe_antecessora = verificar_classe(palavra[loc_2])

    if eh_vogal(palavra[loc_1]) and eh_vogal(palavra[loc_2]):
        try:
            abertura_ant = graus_de_abertura.get(classe_antecessora[1])
            abertura_suc = graus_de_abertura.get(classe_sucessora[1])

            if abertura_ant is not None and abertura_suc is not None:
                if abertura_ant < abertura_suc:
                    nova_abertura = retornar_grau(graus_de_abertura, abertura_suc, -1)
                    classe_sucessora[1] = nova_abertura if nova_abertura else classe_sucessora[1]
                    classe_sucessora[0] = modificar_garganta(classe_sucessora[0], classe_sucessora[1])
                
                elif abertura_ant > abertura_suc:
                    nova_abertura = retornar_grau(graus_de_abertura, abertura_suc, 1)
                    classe_sucessora[1] = nova_abertura if nova_abertura else classe_sucessora[1]
                    classe_sucessora[0] = modificar_garganta(classe_sucessora[0], classe_sucessora[1])

                resultado_fonema = verificar_classes_regra_fonetica(classe_sucessora, 'vogal', True)
                if resultado_fonema:
                    palavra[loc_1] = resultado_fonema[0][0]

        except Exception:
            # Durante os testes, não use "pass" cego, ou você não verá erros reais de tipagem.
            pass

    return palavra

def implementar_harmonia(config: float, palavra: str) -> str:
    """
    Verifica cada vogal de trás para frente, ajustando a harmonia vocálica.
    """
    if random() >= config:
        return palavra
        
    palavra_lista = corrigir_palavra(list(palavra))
    lista_index = [i for i, letra in enumerate(palavra_lista) if eh_vogal(letra)]
    
    for i in range(len(lista_index) - 1, 0, -1):
        idx_alvo = lista_index[i - 1]
        idx_gatilho = lista_index[i]
        
        palavra_lista = harmonia_vocal(palavra_lista, idx_alvo, idx_gatilho)
        
    return "".join(palavra_lista)

def mudancas_w_j(word:list[str], acervo:list[str])->list[str]:
    """
    Args:
        palavra (list[str]): sequencia de caracteres
        acervo (list[str]): as consoantes existentes na língua para checar se x mudança é possível
    Exemplo:
    >>> mudanca_w_j(['p','a','j','o'], [..., 'ʝ', ...])
    ['p','a','ʝ','o']
    """
    def verificar_e_atualizar(word:str, som:str, mudado:str)->str:
        new_word = re.sub(rf'{som}(?=[{global_vowels_str}])', rf"{mudado}", word)
        return new_word
    try:
        if('j' in word):
            if('ʝ' in acervo): #pode adicionar aquele som de "je"/"ge"
                word = verificar_e_atualizar(word, 'ʝ', 'j')
        elif('w' in word):
            if('β' in acervo):
                word = verificar_e_atualizar(word, 'β', 'w')
    except Exception as e:
        tipo_erro = e.__class__.__name__
        print(f"Erro do tipo [{tipo_erro}]: {e}")
    return word

### EFEITOS POR *REGEX*
def apocope(config:float, tonic_syllable:str, word:str)->str:
    """
    Perde vogal ou consoante nos extremos da palavra, dependendo do tipo de preferência
    de sílaba.
    Args:
        tonic_syllable (str): indica a silaba forte da palavra
        word (str): palavra contida no dicionário da língua
    Retorno:
        str
    Exemplo:
    >>> apocope(dialetos, ['b','ə','k','m','ɐ'])
    ['b','ə','k','m']
    """
    if(random()<config):
        if(tonic_syllable == 'oxitona'):
            word = re.sub(r'^[ɪɐʊəh]', '', word)
        elif(tonic_syllable == 'paroxitona'):
            word = re.sub(r'^[ɪɐʊəh]|[ɪɐʊəh]$', '', word)
        else:
            word = re.sub(r'[ɪɐʊəh]$', '', word)
    return word

def epenthesis(config:float, word:str)->str:
    """
    Adds a vowel or consonant to word, sometimes to make it easy to speak or due to a change on the language
    (like changing the most of the language to syllable).
    Args:
        word (str): word to be changed;
    Retorno:
        str
    """
    if(random()<config):
        help_vowel = choice(['ɪ','ɐ','ʊ','ə']) #pode ser melhor usar as vogais próximas na própria palavra em vez de um som aleatório
        word = re.sub(rf"([{global_consonants_str}])(?=[{global_consonants_str}])", rf'\g<1>{help_vowel}', word)
    return word

def assimilar(config:float, word:str)->str:
    """
    Faz assimilacao entre dois sons proximos, trazendo
        a coda mais proxima da pos-coda ou a vogal mais proxima da outra.
    Args:
        - config (float) : numero decimal em configuracao da lingua (class.dialetos_criados[lingua_a]["configuracao"])
        - word (str) : espera uma lista de strings
    Return:
        str
    Exemple:
        >>> assimilar(word = "anpu")
        "ampu"
    """
    if(random()<config): # aqui é para ser a chance em configuracao da lingua
        sonora = "".join(verificar_classes_regra_fonetica(["sonora"], "consoante", 1)[0])
        surda = "".join(verificar_classes_regra_fonetica(["surda"], "consoante", 1)[0])
        bilabial_oclusiva = "".join(verificar_classes_regra_fonetica(["bilabial", "oclusiva"], "consoante", 1)[0])
        alveolar_oclusiva = "".join(verificar_classes_regra_fonetica(["alveolar", "oclusiva"], "consoante", 1)[0])
        lista_efeitos = [
            (rf"n(?=[{bilabial_oclusiva}])", "m"), (rf"m(?=[{alveolar_oclusiva}])", "n"), 
            (rf"([{surda}])(?=[{sonora}])", lambda match:retornar_aproximante(match.group(1), "sonora", 2)),
            (rf"([{sonora}])(?=[{surda}])", lambda match:retornar_aproximante(match.group(1), "surda", 2)),
            (r"eo", "oː"), (r"oe", "eː")
        ]
        for e in lista_efeitos:
            if(random()>0.5): # para evitar que a mudanca seja uma unica vez
                word = re.sub(e[0], e[1], word)
    return word

def ajuste_diacritico(word:str, vowels:str)->str: # MANUTENCAO *
    """
    Verify ʊ/ɪ position and turn into w/j if followed by other vowels.
    Args:
        word (str): 
    """
    def retornar_padroes(vowel:str)->str:
        if(vowel in ["u", "ʊ"]):
            return "w"
        elif(vowel in ["i", "ɪ"]):
            return "j"
        return vowel
    for v in vowels:
        padrao:str = retornar_padroes(v)
        print(v, padrao)
        # word = re.sub(rf"{v}ː(?=[{v}])", rf"{padrao}", word)
        word = re.sub(rf"{v}(?=[{v}])", rf"{padrao}", word)
    return word

def devoicing(word:str)->str:
    """
    Change the last voiced letter to unvoiced.
    Args:
        word (str): a string sequence, as "bed", "kob", etc.
    Return:
        str
    Exemple:
    >>> devoicing(word = "lamb")
    "lamp"
    >>> devoicing(word = "kaz")
    "kas"
    """
    return re.sub(rf"([{global_consonants_str}])$", lambda l:retornar_aproximante(l.group(1), 'surda', 2), word)

def iter_regex(effect_list:list, word:str)->str:
    """
    Instead of using loops throghout the functions, I tried to make it easier
    using only one FOR. It is particularely for regex functions.
    Args:
        effect_list (list[callable]): a list within functions;
        word (str): sequence of strings that we want to change;
    Return:
        str
    """
    for f in effect_list:
        word = re.sub(f[0], f[1], word)
    return word

def sandhi(word:str)->str:
    """
    """
    def choose(lista:list[str])->str:
        return choice(lista)
    lista_efeitos = [
        (r'dg|gg',choose(['g', 'gː'])), (r'bp|pp', choose(['p','pː'])), (r'dt|tt', choose(['t','tː'])),
        (r'pb|bb', choose(['b','bː'])), (r'dd', choose(['d','dː'])), (r'kk', 'kː'), (r'ts', 'ʦ'),
        (r'dz', 'ʣ'), (r'bm', choose(['mb', 'b', 'm', 'mː'])), (r'pm', choose(['mp', 'm', 'p', 'mː'])),
        (r'nŋ|ŋn', 'ŋ'), (r'n(?=[rɾ])', 'nd'), (r'm(?=[rɾ])', 'mb'), (r'ɾɾ|ɾː|rː', 'r'), (r'mm', 'mː'),
        (r'nn', 'nː'), (r'a[aɐə]|[aɐə]a', choose(['a', 'aː'])), (r'iɪ|ɪi', choose(['ɪ', 'ɪː', 'ij'])),
        (r'[eə]e|e[eə]', 'eː'), (r'uu', choose(['uː', choose(['wu','uw'])])), (r'oo', 'oː'), 
        (r'([ɐə])[ɐə]|[ɐə]([ɐə])', r'\g<1>ː'), (r'ɐe|aɪ', choose(['e', 'ɛ'])),
    ]
    word = iter_regex(lista_efeitos, word)
    return word

def coalescencia()->str:
    """
    Quase o mesmo que sandhi, mas serve exclusivamente para palavras já feitas, ou seja,
        se a lingua já pronunciava "pha", então ela conseguiria distinguir entre "pha" e "pʰa", ficando
        desnecessario a conversao. Entretanto, se fosse uma juncao entre uma palavra "alp" e "hon", então
        sandhi poderia entrar, por serem palavras diferentes, se tornando "alpʰon" ou até "alpon".
    """
    pass

def filtro_fonetico(word:str)->str:
    """
    """
    def choose(lista):
        return choice(lista)
    consonants = re.escape(global_consonants_str)
    vowels = re.escape(global_vowels_str)
    non_aspirated = [c for c in global_consonants_str if 'aspirada' not in verificar_classe(c)]
    effect_list = [
        (rf'([{non_aspirated}])h', r'\g<1>ʰ'), (r'mβ', 'mb'),
        (rf'(?=[{consonants}])wj(?=[{consonants}])', choose(['wɪ', 'ʊj'])),
        (rf'(?=[{consonants}])jw(?=[{consonants}])', choose(['jʊ', 'ɪw'])),
        (rf'(?=[{consonants}])j$', 'ɪ'), (rf'(?=[{consonants}])w$', 'ʊ'),
        (rf'nl(?=[{consonants}])|(?<=[{consonants}])nl', choose(['n', 'l'])),
        (rf'(?<=[{consonants}])wː(?=[{consonants}])', 'ʊː'), (rf'(?<=[{consonants}])w(?=[{consonants}])', 'ʊ'),
        (rf'(?<=[{consonants}])j(?=[{consonants}])', 'ɪ'), (rf'(?<=[{consonants}])jː(?=[{consonants}])', 'ɪː'),
        (rf'(?<=[{vowels}])ɪ|ɪ(?=[{vowels}])', 'j'), (rf'(?<=[{vowels}])ʊ|ʊ(?=[{vowels}])', 'w'),
        (rf'([{vowels}])ww', choose(['wʊ', 'w'])),(rf'ww(?=[{vowels}])', choose(['ʊw', 'w'])),
        (rf'([{vowels}])ww', choose(['jɪ', 'j', 'ɪː'])),(rf'ww(?=[{vowels}])', choose(['ɪj', 'j', 'ɪː'])),
        (rf'ʝ$|(?<=[{consonants}])ʝ|ʝ(?=[{consonants}])', 'j'),
    ]
    word = iter_regex(effect_list, word)
    # for f in effect_list:
    #     word = re.sub(f[0], f[1], word)
    return word

def implementar_correcoes(word:str)->str:
    """
    Checkup function. It must be always used, as word can change throw iteractions.
    Args:
        word (str): 
    Return:
        str
    Exemple:
    >>> apply_fix(word = "arros")
    "aros"
    """

"""
DESENVOLVIMENTO E NEOLOGISMO
"""
def lista_indevida(palavra:list[str,list[str]])->list[str]:
    """
    RESUMO
        Verifica se tem alguma lista em palavra que não deveria estar.
    PARAMETRO
        palavra -> espera uma lista string
    RETORNO
        list[str]
    """
    for index, letra in enumerate(palavra):
        if(isinstance(letra,list)):
            palavra[index] = "".join(letra)
    return palavra

def perde_fracas(palavra:list[str])->list[str]:
    if(len(palavra)>3):
        vogais_fracas:list[str] = ['ɐ', 'ə', 'ɪ', 'ʊ', 'ʏ']
        # procura a primeira e ultima letra e ve se eh "fraca"
        if(palavra[0] in vogais_fracas and random()>0.7):
            # print(palavra)
            palavra.pop(0)
        elif(palavra[-1] in vogais_fracas and random()>0.7):
            # print(palavra)
            palavra.pop(-1)
        index:int = 0
        # ve uma letra fraca entre vogais para torna-las semi-vogais ou retira-las
        while(index<len(palavra)-2):
            letras:list[str] = [palavra[index], palavra[index+1], palavra[index+2]]
            if(all(eh_vogal(v) for v in letras)):
                if(letras[1] == 'ɪ'):
                    palavra[index+1] = 'j'
                elif(letras[1] == 'ʊ'):
                    palavra[index+1] = 'w'
            else:
                consoantes:list[str] = [letras[0], letras[2]]
                if(letras[1] in vogais_fracas):
                    if(all(eh_consoante(c) for c in consoantes)):
                        if(random()>0.6):
                            palavra.pop(index+1)
                            continue
                    if(eh_consoante(letras[0]) or eh_consoante(letras[2])):
                        if(letras[1] == 'ɪ'):
                            palavra[index+1] = 'j'
                        elif(letras[1] == 'ʊ'):
                            palavra[index+1] = 'w'
            index+=1
    # print(palavra)
    return palavra

"""
BUSCAR/PESQUISAR/ENCONTRAR
"""
def ajuda(funcao:str|bool = False)->None:
    """
    Caso esteja perdido sobre qual função usar ou o que x função faz, esta
    função tem como objetivo justamente auxilar sobre as funções no geral.
    """
    funcoes:dict[str, str] = {
        'ENCONTRAR':'\n  | encontrar_palavra_pelo_som',
        'BUSCAR':'\n  | buscar_palavra\n  | buscar_palavras_todas_linguas\n  | buscar_indice_fundo',
        'RETORNAR':'\n  | retornar_pronome\n  | retornar_verbo\n  | retornar_palavra\n  | retornar_indices',
        'VER':'\n  | ver_gramatica\n  | ver_gramatica_detalhada',
        'EH':'\n  | eh_consoante\n  | eh_vogal\n  | eh_diacritico\n  | eh_verbo\n  | eh_pronome\n  | eh_substantivo',
    }
    if(not funcao):
        for k in funcoes.keys():
            print(f"Funções {k}:{funcoes[k]}")
        return

    funcao = funcao.upper()
    if(funcao in funcoes.keys()):
        print(f"Função {funcao}:{funcoes[funcao]}")
    else:
        print(f"Função {funcao} não encontrada. Funções disponíveis: {", ".join(funcoes.keys())}")


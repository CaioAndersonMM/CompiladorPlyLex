import ply.lex as lex


#Fazer regex pois elas terminam em dois pontos no final, precisa de regra!
reservadas = {
    'SOME': 'PALAVRA_RESERVADA',
    'ALL': 'PALAVRA_RESERVADA',
    'VALUE': 'PALAVRA_RESERVADA',
    'MIN': 'PALAVRA_RESERVADA',
    'MAX': 'PALAVRA_RESERVADA',
    'EXACTLY': 'PALAVRA_RESERVADA',
    'THAT': 'PALAVRA_RESERVADA',
    'NOT': 'PALAVRA_RESERVADA',
    'AND': 'PALAVRA_RESERVADA',
    'OR': 'PALAVRA_RESERVADA',
    'Class': 'PALAVRA_RESERVADA',
    'EquivalentTo': 'PALAVRA_RESERVADA',
    'Individuals': 'PALAVRA_RESERVADA',
    'SubClassOf': 'PALAVRA_RESERVADA',
    'DisjointClasses': 'PALAVRA_RESERVADA',
}

# Todas as funções que começam com 't_' são chamadas de regras e são responsáveis por identificar esses tokens
tokens = [
    'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO',
    'CARDINALIDADE', 'TIPO_DADO', 'SIMBOLO_ESPECIAL',
    'DOIS_PONTOS', 'PARA_ABRIR', 'PARA_FECHAR', 'PARENTESES_ABERTO', 'PARENTESES_FECHADO', 'MAIOR_IGUAL', 'MENOR_IGUAL', 'IGUAL'
] + list(set(reservadas.values()))

t_DOIS_PONTOS = r':'
t_PARA_ABRIR = r'\['
t_PARA_FECHAR = r'\]'
t_PARENTESES_ABERTO = r'\('
t_PARENTESES_FECHADO = r'\)'

# Operadores >= e <= e =

# Tipos de dados precisou vim primeiro que as palavras reservadas, pois a regex das palavras reservadas é mais genérica
def t_TIPO_DADO(t):
    r'owl:real|rdfs:domain|xsd:string'
    return t

def t_PALAVRA_RESERVADA(t):
    r'[A-Za-z]+:'
    
    palavra = t.value[:-1]

    if palavra in reservadas:
        t.type = reservadas[palavra]
        return t

def t_IDENTIFICADOR_CLASSE(t):
    r'[A-Z][A-Za-z0-9_]*'   #(começam com letra maiúscula, podem ser compostos e pode terminar com underline)
    t.type = reservadas.get(t.value, 'IDENTIFICADOR_CLASSE')
    return t

def t_IDENTIFICADOR_PROPRIEDADE(t):
    r'(has[A-Za-z0-9]+|is[A-Za-z0-9]+Of|[a-z][A-Za-z0-9]*)' #(começam com 'has' ou 'is', seguidos de letras)
    return t

def t_IDENTIFICADOR_INDIVIDUO(t):
    r'[A-Z][a-z0-9]*[0-9]+' #(começam com letra maiúscula e terminam com número)
    return t

def t_CARDINALIDADE(t):
    r'\d+' #(números inteiros)
    return t

def t_SIMBOLO_ESPECIAL(t):
    r'[\[\]\(\)\{\},<>=>=<]'
    return t

# Ignorar espaços e tabulações
t_ignore = ' \t'

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Erro léxico: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

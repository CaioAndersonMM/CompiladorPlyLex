import ply.lex as lex

reservadas = {
    'SOME': 'SOME',
    'ALL': 'ALL',
    'VALUE': 'VALUE',
    'MIN': 'MIN',
    'MAX': 'MAX',
    'EXACTLY': 'EXACTLY',
    'THAT': 'THAT',
    'NOT': 'NOT',
    'AND': 'AND',
    'OR': 'OR',
    'Class': 'CLASS',
    'EquivalentTo': 'EQUIVALENTTO',
    'Individuals': 'INDIVIDUALS',
    'SubClassOf': 'SUBCLASSOF',
    'DisjointClasses': 'DISJOINTCLASSES',
}

# Todas as funções que começam com 't_' são chamadas de regras e são responsáveis por identificar esses tokens
tokens = [
    'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO',
    'CARDINALIDADE', 'TIPO_DADO', 'SIMBOLO_ESPECIAL',
    'DOIS_PONTOS', 'PARA_ABRIR', 'PARA_FECHAR', 'PARENTESES_ABERTO', 'PARENTESES_FECHADO', 'MAIOR_IGUAL', 'MENOR_IGUAL', 'IGUAL'
] + list(reservadas.values())

t_DOIS_PONTOS = r':'
t_PARA_ABRIR = r'\['
t_PARA_FECHAR = r'\]'
t_PARENTESES_ABERTO = r'\('
t_PARENTESES_FECHADO = r'\)'

# Operadores >= e <= e =

def t_MAIOR_IGUAL(t):
    r'>='
    return t

def t_MENOR_IGUAL(t):
    r'<='
    return t

def t_IGUAL(t):
    r'='
    return t

def t_IDENTIFICADOR_CLASSE(t):
    r'[A-Z][A-Za-z0-9_]*'   #(começam com letra maiúscula, podem ser compostos)
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

# Tipos de dados
def t_TIPO_DADO(t):
    r'owl:real|rdfs:domain|xsd:string'
    return t

def t_SIMBOLO_ESPECIAL(t):
    r'[\[\]\(\)\{\},<>]'
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

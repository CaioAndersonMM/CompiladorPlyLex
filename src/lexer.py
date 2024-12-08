import ply.lex as lex

from src.symbol_table import TabelaSimbolos

reservadas = {
    'some': 'PALAVRA_RESERVADA',
    'all': 'PALAVRA_RESERVADA',
    'value': 'PALAVRA_RESERVADA',
    'min': 'PALAVRA_RESERVADA',
    'max': 'PALAVRA_RESERVADA',
    'exactly': 'PALAVRA_RESERVADA',
    'that': 'PALAVRA_RESERVADA',
    'not': 'PALAVRA_RESERVADA',
    'and': 'PALAVRA_RESERVADA',
    'or': 'PALAVRA_RESERVADA',
    'class': 'PALAVRA_RESERVADA',
    'equivalentto': 'PALAVRA_RESERVADA',
    'individuals': 'PALAVRA_RESERVADA',
    'subclassof': 'PALAVRA_RESERVADA',
    'disjointclasses': 'PALAVRA_RESERVADA',
}

type_dado = [
    'integer', 'real', 'string', 'boolean', 'date', 'time',
    'long', 'language', 'short', 'token', 'byte', 'Name', 'NCName',
]

tokens = [
    'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO',
    'CARDINALIDADE', 'SIMBOLO_ESPECIAL', 'TIPO_DADO', 'NAMESPACE'
] + list(set(reservadas.values()))

tabela_simbolos = TabelaSimbolos()

def adicionar_tabela_simbolos(t):
    tabela_simbolos.add(simbolo=t.value, tipo=t.type, linha=t.lineno)


# Funções de regras de token
def t_NAMESPACE(t):
    r'owl:|rdfs:|xsd:'
    adicionar_tabela_simbolos(t)
    return t

def t_TIPO_DADO(t):
    r'(integer|real|string|boolean|date|time|long|language|short|token|byte|Name|NCName)'

    if t.value in type_dado:
        adicionar_tabela_simbolos(t)
        return t


    adicionar_tabela_simbolos(t)
    return t

def t_PALAVRA_RESERVADA(t):
    r'[A-Za-z]+:'
    
    palavra = t.value[:-1].lower()

    if palavra in reservadas:
        t.type = reservadas[palavra]
        t.value = palavra
        adicionar_tabela_simbolos(t)
        return t
    
def t_IDENTIFICADOR_INDIVIDUO(t):
    r'[A-Z][a-z0-9]*[0-9]+'
    adicionar_tabela_simbolos(t)
    return t

def t_IDENTIFICADOR_CLASSE(t):
    r'[A-Z][A-Za-z0-9_]*'
    
    if t.value.lower() in reservadas:
        t.type = reservadas[t.value.lower()]
    else:
        t.type = 'IDENTIFICADOR_CLASSE'
    
    adicionar_tabela_simbolos(t)
    return t


def t_IDENTIFICADOR_PROPRIEDADE(t):
    r'(has[A-Za-z0-9]+|is[A-Za-z0-9]+Of|[a-z][A-Za-z0-9]*)'
    
    if t.value.lower() in reservadas:
        t.type = reservadas[t.value.lower()]
    else:
        t.type = 'IDENTIFICADOR_PROPRIEDADE'
    
    adicionar_tabela_simbolos(t)
    return t

def t_CARDINALIDADE(t):
    r'\d+'
    adicionar_tabela_simbolos(t)
    return t

def t_SIMBOLO_ESPECIAL(t):
    r'(>=|<=|[\{\},<>=\[\]\(\)\'"])'
    adicionar_tabela_simbolos(t)
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
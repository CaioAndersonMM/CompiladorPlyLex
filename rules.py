import ply.lex as lex

from Symb import TabelaSimbolos

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

namespaces = [
    'integer', 'real', 'string', 'boolean', 'date', 'time',
    'long', 'language', 'short', 'token', 'byte', 'Name', 'NCName',
]

tokens = [
    'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO',
    'CARDINALIDADE', 'TIPO_DADO', 'SIMBOLO_ESPECIAL', 'NAMESPACE',
] + list(set(reservadas.values()))

tabela_simbolos = TabelaSimbolos()

def adicionar_tabela_simbolos(t):
    tabela_simbolos.adicionar(simbolo=t.value, tipo=t.type, linha=t.lineno)


# Funções de regras de token
def t_TIPO_DADO(t):
    r'owl:|rdfs:|xsd:'
    adicionar_tabela_simbolos(t)
    return t

def t_NAMESPACE(t):
    r'(integer|real|string|boolean|date|time|long|language|short|token|byte|Name|NCName)'

    if t.value in namespaces:
        adicionar_tabela_simbolos(t)
        return t


    adicionar_tabela_simbolos(t)
    return t

def t_PALAVRA_RESERVADA(t):
    r'[A-Za-z]+:'
    
    palavra = t.value[:-1]

    if palavra in reservadas:
        t.type = reservadas[palavra]
        t.value = palavra
        adicionar_tabela_simbolos(t)
        return t

def t_IDENTIFICADOR_CLASSE(t):
    r'[A-Z][A-Za-z0-9_]*'
    t.type = reservadas.get(t.value, 'IDENTIFICADOR_CLASSE')
    adicionar_tabela_simbolos(t)
    return t

def t_IDENTIFICADOR_PROPRIEDADE(t):
    r'(has[A-Za-z0-9]+|is[A-Za-z0-9]+Of|[a-z][A-Za-z0-9]*)'
    adicionar_tabela_simbolos(t)
    return t

def t_IDENTIFICADOR_INDIVIDUO(t):
    r'[A-Z][a-z0-9]*[0-9]+'
    adicionar_tabela_simbolos(t)
    return t

def t_CARDINALIDADE(t):
    r'\d+'
    adicionar_tabela_simbolos(t)
    return t

def t_SIMBOLO_ESPECIAL(t):
    r'(>=|<=|[\{\},<>=\[\]\(\)])'
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
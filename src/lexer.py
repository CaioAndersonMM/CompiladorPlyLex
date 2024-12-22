import ply.lex as lex
import ply.yacc as yacc
from src.symbol_table import TabelaSimbolos

# Definindo palavras reservadas
reservadas = {
    'some': 'SOME',
    'all': 'ALL',
    'value': 'VALUE',
    'min': 'MIN',
    'max': 'MAX',
    'exactly': 'EXACTLY',
    'that': 'THAT',
    'not': 'NOT',
    'and': 'AND',
    'or': 'OR',
    'class': 'CLASS',
    'equivalentto': 'EQUIVALENTTO',
    'individuals': 'INDIVIDUALS',
    'subclassof': 'SUBCLASSOF',
    'disjointclasses': 'DISJOINTCLASSES',
    'disjointwith': 'DISJOINTWITH',
}

# Tipos de dados
type_dado = [
    'integer', 'real', 'string', 'boolean', 'date', 'time',
    'long', 'language', 'short', 'token', 'byte', 'Name', 'NCName',
]

# Tokens
tokens = [
    'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO',
    'CARDINALIDADE', 'SIMBOLO_ESPECIAL', 'TIPO_DADO', 'NAMESPACE', 'LPAREN', 'RPAREN',
] + list(set(reservadas.values()))

# Tabela de símbolos
tabela_simbolos = TabelaSimbolos()

# Função para adicionar à tabela de símbolos
def adicionar_tabela_simbolos(t):
    tabela_simbolos.add(simbolo=t.value, tipo=t.type, linha=t.lineno)

# Funções de regras de token
t_LPAREN = r'\('  # Abre parêntese
t_RPAREN = r'\)'  # Fecha parêntese

# Ajuste na captura de NAMESPACE para remover ':'
def t_NAMESPACE(t):
    r'owl:|rdfs:|xsd:'  # Agora captura 'owl:', 'rdfs:', 'xsd:'
    t.value = t.value[:-1]  # Remove o ":" da palavra reservada para evitar problemas no parser
    adicionar_tabela_simbolos(t)
    return t

# Tipos de dados
def t_TIPO_DADO(t):
    r'(integer|real|string|boolean|date|time|long|language|short|token|byte|Name|NCName)'
    if t.value in type_dado:
        adicionar_tabela_simbolos(t)
        return t
    print(f"Erro léxico: {t.value}")
    t.lexer.skip(1)

# Palavras reservadas
def t_PALAVRA_RESERVADA(t):
    r'[A-Za-z]+:'
    palavra = t.value[:-1].lower()  # Remover o ":" ao processar palavras reservadas

    if palavra in reservadas:
        t.type = reservadas[palavra]
        t.value = palavra
        adicionar_tabela_simbolos(t)
        return t
    print(f"Erro léxico: {t.value}")
    t.lexer.skip(1)

# Identificadores de indivíduos
def t_IDENTIFICADOR_INDIVIDUO(t):
    r'[A-Z][a-zA-Z0-9]*[0-9]+'
    adicionar_tabela_simbolos(t)
    return t

# Identificadores de classe
def t_IDENTIFICADOR_CLASSE(t):
    r'[A-Z][A-Za-z_]*(?:_[A-Z][A-Za-z_]*)*'
    if t.value.lower() in reservadas:
        t.type = reservadas[t.value.lower()]
    else:
        t.type = 'IDENTIFICADOR_CLASSE'
    adicionar_tabela_simbolos(t)
    return t

# Identificadores de propriedade
def t_IDENTIFICADOR_PROPRIEDADE(t):
    r'(has[A-Za-z0-9]+|is[A-Za-z0-9]+Of|[a-z][A-Za-z0-9]*)'
    if t.value.lower() in reservadas:
        t.type = reservadas[t.value.lower()]
    else:
        t.type = 'IDENTIFICADOR_PROPRIEDADE'
    adicionar_tabela_simbolos(t)
    return t

# Cardinalidade
def t_CARDINALIDADE(t):
    r'\d+'
    adicionar_tabela_simbolos(t)
    return t

# Símbolos especiais
def t_SIMBOLO_ESPECIAL(t):
    r'(>=|<=|[\{\},<>=\[\]\'"])'  # Removido os parênteses de aqui
    adicionar_tabela_simbolos(t)
    return t

# Ignorar espaços e tabulações
t_ignore = ' \t'

# Nova linha
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Comentário
def t_comment(t):
    r'\#.*'
    pass

# Erro léxico
def t_error(t):
    print(f"Erro léxico: {t.value}")
    t.lexer.skip(1)

# Analisador Sintático

precedence = (
    ('left', 'AND'),
    ('left', 'OR'),
    ('right', 'SOME'),
    ('right', 'VALUE'),
)

# Funções do analisador sintático

def p_declaracao_classe_primitiva(p):
    """declaracao_classe : CLASS IDENTIFICADOR_CLASSE SUBCLASSOF restricoes disjunto individuos"""
    restricoes = p[4] if p[4] else "nenhuma"
    disjunto = p[5] if p[5] else "nenhum"
    print(f"Classe primitiva: {p[2]} é subclasse com restrições {restricoes} e disjunto {disjunto}")

def p_declaracao_classe_definida(p):
    """declaracao_classe : CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO expressao"""
    print(f"Classe definida: {p[2]} é equivalente a {p[4]}")

def p_declaracao_classe_enumerada(p):
    """declaracao_classe : CLASS IDENTIFICADOR_CLASSE DISJOINTCLASSES lista_individuos"""
    print(f"Classe enumerada: {p[2]} contém os indivíduos {p[4]}")

def p_declaracao_classe_coberta(p):
    """declaracao_classe : CLASS IDENTIFICADOR_CLASSE DISJOINTWITH lista_classes"""
    print(f"Classe coberta: {p[2]} é disjunta com as classes {p[4]}")

# Expressão
def p_expressao(p):
    """expressao : IDENTIFICADOR_CLASSE
                 | IDENTIFICADOR_PROPRIEDADE SOME IDENTIFICADOR_CLASSE
                 | expressao AND expressao
                 | expressao SOME IDENTIFICADOR_CLASSE
                 | expressao SOME NAMESPACE TIPO_DADO
                 | LPAREN expressao RPAREN"""
    if len(p) == 4 and p[2] == 'AND':
        print(f"Expressão combinada: {p[1]} and {p[3]}")
        return f"({p[1]} and {p[3]})"
    elif len(p) == 3 and p[2] == 'SOME':
        print(f"Expressão com SOME: {p[1]} some {p[3]}")
        return f"({p[1]} some {p[3]})"
    else:
        return p[1]

# Regras para restrições
def p_restricoes(p):
    """restricoes : IDENTIFICADOR_PROPRIEDADE SOME IDENTIFICADOR_CLASSE
                  | IDENTIFICADOR_PROPRIEDADE SOME IDENTIFICADOR_CLASSE SIMBOLO_ESPECIAL restricoes
                  | IDENTIFICADOR_PROPRIEDADE SOME NAMESPACE TIPO_DADO
                  | IDENTIFICADOR_PROPRIEDADE VALUE TIPO_DADO
                  | IDENTIFICADOR_PROPRIEDADE MIN CARDINALIDADE IDENTIFICADOR_CLASSE
                  | IDENTIFICADOR_PROPRIEDADE MAX CARDINALIDADE IDENTIFICADOR_CLASSE
                  | IDENTIFICADOR_PROPRIEDADE EXACTLY CARDINALIDADE IDENTIFICADOR_CLASSE
                  | IDENTIFICADOR_CLASSE SIMBOLO_ESPECIAL
                  | expressao"""
    print(f"Restrição: {p[1]} com operador {p[2]} para {p[3]}")

# Disjunto
def p_disjunto(p):
    """disjunto : DISJOINTCLASSES IDENTIFICADOR_CLASSE
                | DISJOINTCLASSES IDENTIFICADOR_CLASSE SIMBOLO_ESPECIAL disjunto
                | IDENTIFICADOR_CLASSE SIMBOLO_ESPECIAL disjunto
                | IDENTIFICADOR_CLASSE"""
    disjoint_classes = [item for item in p[1:] if item is not None]
    print(f"DisjointClasses: {disjoint_classes}")

# Indivíduos
def p_individuos(p):
    """individuos : INDIVIDUALS IDENTIFICADOR_INDIVIDUO
                  | INDIVIDUALS IDENTIFICADOR_INDIVIDUO SIMBOLO_ESPECIAL individuos
                  | individuos ',' IDENTIFICADOR_INDIVIDUO
                  | IDENTIFICADOR_INDIVIDUO"""
    individuos = [item for item in p[1:] if item is not None]
    print(f"Indivíduos: {individuos}")

# Regras para lista de classes e indivíduos
def p_lista_classes(p):
    """lista_classes : IDENTIFICADOR_CLASSE
                      | lista_classes ',' IDENTIFICADOR_CLASSE"""
    pass

def p_lista_individuos(p):
    """lista_individuos : IDENTIFICADOR_INDIVIDUO
                         | lista_individuos ',' IDENTIFICADOR_INDIVIDUO"""
    pass

# Erro sintático
def p_error(p):
    if p:
        print(f"Erro sintático: token inesperado '{p.value}', linha {p.lineno}")
    else:
        print("Erro sintático: fim inesperado da entrada.")

# Criando lexer e parser
lexer = lex.lex()
parser = yacc.yacc()

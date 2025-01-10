import ply.lex as lex
import ply.yacc as yacc

# ============================
# LEXER
# ============================

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
    'MAIORIGUAL', 'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO',
    'CARDINALIDADE', 'SIMBOLO_ESPECIAL', 'TIPO_DADO', 'NAMESPACE', 'LPAREN', 'RPAREN',
] + list(set(reservadas.values()))

# Regras de tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'  # Ignorar espaços e tabulações
t_MAIORIGUAL = r'>='

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass  # Ignorar NEWLINE no lexer, será tratado no parser

def t_SOME(t):
    r'some'
    return t
def t_CLASS(t):
    r'[Cc]lass\s*:'  # Permite "Class:" ou "class :" (com espaços opcionais)
    return t

def t_SUBCLASSOF(t):
    r'[Ss]ub[Cc]lass[Oo]f\s*:'  # Permite variações de maiúsculas/minúsculas e espaços opcionais
    return t

def t_EQUIVALENTTO(t):
    r'[Ee]quivalent[Tt]o\s*:'  # Permite variações e espaços opcionais
    return t

def t_AND(t):
    r'and'
    return t

def t_DISJOINTCLASSES(t):
    r'[Dd]isjoint[Cc]lasses\s*:'  # Permite variações e espaços opcionais
    return t

def t_INDIVIDUALS(t):
    r'[Ii]ndividuals\s*:'  # Permite variações e espaços opcionais
    return t

def t_NAMESPACE(t):
    r'owl:|rdfs:|xsd:'
    t.value = t.value[:-1]  # Remove o ":" no final
    return t

def t_TIPO_DADO(t):
    r'(integer|real|string|boolean|date|time|long|language|short|token|byte|Name|NCName)'
    if t.value in type_dado:
        return t

def t_IDENTIFICADOR_INDIVIDUO(t):
    r'[A-Z][a-zA-Z0-9]*[0-9]+'
    return t

def t_IDENTIFICADOR_CLASSE(t):
    r'[A-Z][A-Za-z_]*(?:_[A-Z][A-Za-z_]*)*'
    return t

def t_IDENTIFICADOR_PROPRIEDADE(t):
    r'(has[A-Za-z0-9]+|is[A-Za-z0-9]+Of|[a-z][A-Za-z0-9]*)'
    return t

def t_CARDINALIDADE(t):
    r'\d+'
    return t

def t_SIMBOLO_ESPECIAL(t):
    r'([\{\},\[\]\'"])'
    return t

def t_comment(t):
    r'\#.*'
    pass

def t_error(t):
    print(f"Erro léxico: {t.value}")
    t.lexer.skip(1)

lexer = lex.lex()

# ============================
# PARSER
# ============================


def p_ontologia(p):
    """ontologia : declaracao_classe
                 | declaracao_classe_definida
                 | ontologia declaracao_classe
                 | ontologia declaracao_classe_definida"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_declaracao_classe_definida(p):
    """declaracao_classe_definida : CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO lista_restricoes_definidas corpo_classe
                                  | CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO lista_restricoes_definidas"""
    if len(p) == 6:
        p[0] = ("ClasseDefinida", p[2], p[4], p[5])
    else:
        p[0] = ("ClasseDefinida", p[2], p[4])

def p_declaracao_classe(p):
    """declaracao_classe : CLASS IDENTIFICADOR_CLASSE SUBCLASSOF lista_restricoes corpo_classe
                         | CLASS IDENTIFICADOR_CLASSE SUBCLASSOF lista_restricoes"""
    if len(p) == 6:
        p[0] = ("ClassePrimitiva", p[2], p[4], p[5])
    else:
        p[0] = ("ClassePrimitiva", p[2], p[4])

def p_corpo_classe_primitiva(p):
    """corpo_classe : restricoes disjunto individuos
                    | restricoes disjunto
                    | restricoes individuos
                    | disjunto individuos
                    | restricoes
                    | disjunto
                    | individuos"""
    p[0] = p[1:]

def p_restricoes(p):
    """restricoes : SUBCLASSOF lista_restricoes"""
    p[0] = ("Restricoes", p[2])

def p_lista_restricoes(p):
    """lista_restricoes : restricao
                        | lista_restricoes SIMBOLO_ESPECIAL restricao"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_lista_restricoes_definidas(p):
    """lista_restricoes_definidas : restricao_definidas
                        | lista_restricoes_definidas SIMBOLO_ESPECIAL restricao_definidas"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_restricao(p):
    """restricao : IDENTIFICADOR_PROPRIEDADE SOME IDENTIFICADOR_CLASSE
                 | IDENTIFICADOR_PROPRIEDADE SOME NAMESPACE TIPO_DADO"""
    p[0] = ("Restricao", p[1], p[3])

def p_restricao_definidas(p):
    """restricao_definidas : IDENTIFICADOR_CLASSE AND LPAREN lista_restricoes RPAREN
                           | IDENTIFICADOR_PROPRIEDADE SOME IDENTIFICADOR_CLASSE
                           | IDENTIFICADOR_PROPRIEDADE SOME NAMESPACE TIPO_DADO '[' CARDINALIDADE ']'
                           | IDENTIFICADOR_PROPRIEDADE SOME NAMESPACE TIPO_DADO '[' MAIORIGUAL CARDINALIDADE ']'
                           | IDENTIFICADOR_PROPRIEDADE AND LPAREN lista_restricoes_definidas RPAREN
                           | IDENTIFICADOR_PROPRIEDADE AND NAMESPACE TIPO_DADO '[' MAIORIGUAL CARDINALIDADE ']'
                           | IDENTIFICADOR_PROPRIEDADE AND LPAREN IDENTIFICADOR_PROPRIEDADE SOME IDENTIFICADOR_CLASSE RPAREN
                           | IDENTIFICADOR_CLASSE AND LPAREN IDENTIFICADOR_PROPRIEDADE SOME NAMESPACE TIPO_DADO '[' MAIORIGUAL CARDINALIDADE ']' RPAREN
                           | IDENTIFICADOR_CLASSE AND LPAREN IDENTIFICADOR_PROPRIEDADE SOME NAMESPACE TIPO_DADO SIMBOLO_ESPECIAL MAIORIGUAL CARDINALIDADE SIMBOLO_ESPECIAL RPAREN""" # essa ultima regra cubriu a ultima da classe definida
    if len(p) == 5:  # Caso com parênteses
        p[0] = ("Restricao", p[1], p[4])
    elif len(p) == 8 and p[5] == "MAIORIGUAL":  # Com >=
        p[0] = ("Restricao", p[1], p[3], p[5], p[6])
    else:
        p[0] = ("Restricao", p[1], p[3])


def p_disjunto(p):
    """disjunto : DISJOINTCLASSES lista_classes"""
    p[0] = ("Disjunto", p[2])

def p_lista_classes(p):
    """lista_classes : IDENTIFICADOR_CLASSE
                     | lista_classes SIMBOLO_ESPECIAL IDENTIFICADOR_CLASSE"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_individuos(p):
    """individuos : INDIVIDUALS lista_individuos"""
    p[0] = ("Individuos", p[2])

def p_lista_individuos(p):
    """lista_individuos : IDENTIFICADOR_INDIVIDUO
                        | lista_individuos SIMBOLO_ESPECIAL IDENTIFICADOR_INDIVIDUO"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_error(p):
    if p:
        print(f"Erro sintático no token: {p.type}, valor: '{p.value}', linha: {p.lineno}")
    else:
        print("Erro sintático: fim inesperado da entrada.")

parser = yacc.yacc()

# ============================
# MAIN
# ============================

def main():
    entrada = """
    Class: CheesyPizza
    EquivalentTo:
    Pizza and (hasTopping some CheeseTopping)
    Individuals:
    CheesyPizza1

    Class: HighCaloriePizza
    EquivalentTo:
    Pizza and (hasCaloricContent some xsd:integer[>= 400])
    """
    resultado = parser.parse(entrada, lexer=lexer)
    print("Árvore Sintática:", resultado)

if __name__ == "__main__":
    main()

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
    'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO',
    'CARDINALIDADE', 'SIMBOLO_ESPECIAL', 'TIPO_DADO', 'NAMESPACE', 'LPAREN', 'RPAREN',
] + list(set(reservadas.values()))

# Regras de tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'  # Ignorar espaços e tabulações

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass  # Ignorar NEWLINE no lexer, será tratado no parser

def t_SOME(t):
    r'some'
    return t

def t_CLASS(t):
    r'Class:'
    return t

def t_SUBCLASSOF(t):
    r'SubClassOf:'
    return t

def t_DISJOINTCLASSES(t):
    r'DisjointClasses:'
    return t

def t_INDIVIDUALS(t):
    r'Individuals:'
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
    r'(>=|<=|[\{\},<>=\[\]\'"])'
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

precedence = (
    ('left', 'SIMBOLO_ESPECIAL'),
    ('left', 'CLASS'),
)

def p_ontologia(p):
    """ontologia : declaracao_classe corpo_classe
                 | declaracao_classe"""
    if len(p) == 3:
        p[0] = (p[1], p[2])
    else:
        p[0] = p[1]

def p_declaracao_classe_primitiva(p):
    """declaracao_classe : CLASS IDENTIFICADOR_CLASSE"""
    p[0] = ("ClassePrimitiva", p[2])


def p_corpo_classe(p):
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

def p_restricao(p):
    """restricao : IDENTIFICADOR_PROPRIEDADE SOME IDENTIFICADOR_CLASSE
                 | IDENTIFICADOR_PROPRIEDADE SOME NAMESPACE TIPO_DADO"""
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

def p_classes_definidas(p):
    """classes_definidas : classe_definida
                        | classes_definidas classe_definida"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_classe_definida(p):
    """classe_definida : CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO lista_restricoes"""
    p[0] = ("ClasseDefinida", p[2], p[4])


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
    Class: Pizza
        SubClassOf:
            hasBase some PizzaBase,
            hasCaloricContent some xsd:integer
        DisjointClasses:
            Pizza, PizzaBase, PizzaTopping
        Individuals:
            CustomPizza1, CustomPizza2
    """
    resultado = parser.parse(entrada, lexer=lexer)
    print("Árvore Sintática:", resultado)

if __name__ == "__main__":
    main()

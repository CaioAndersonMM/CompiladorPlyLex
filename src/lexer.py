import ply.lex as lex
import ply.yacc as yacc

# ============================
# LEXER
# ============================

# Definindo palavras reservadas
reservadas = {
    'some': 'SOME',
    'only': 'ONLY',
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
    'MAIORIGUAL', 'MENORIGUAL', 'MAIOR', 'MENOR', 'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO',
    'CARDINALIDADE', 'SIMBOLO_ESPECIAL', 'TIPO_DADO', 'NAMESPACE', 'LPAREN', 'RPAREN',
] + list(set(reservadas.values()))

# Regras de tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_ignore = ' \t'  # Ignorar espaços e tabulações
t_MAIORIGUAL = r'>='
t_MENORIGUAL = r'<='
t_MAIOR = r'>'
t_MENOR = r'<'

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    pass  # Ignorar NEWLINE no lexer, será tratado no parser

def t_SOME(t):
    r'some'
    return t

def t_ONLY(t):
    r'only'
    return t

def t_VALUE(t):
    r'value'
    return t

def t_OR(t):
    r'or'
    return t

def t_MIN(t):
    r'min'
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
                 | ontologia declaracao_classe"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaracao_classe(p):
    """declaracao_classe : declaracao_classe_definida
                        | declaracao_classe_primitiva"""
    p[0] = p[1]



def p_declaracao_classe_definida(p):
    """declaracao_classe_definida : CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO tipo_classe_definida individuals_opcional"""
    p[0] = ["classe definida", p[2], p[4], p[5]]

def p_declaracao_classe_primitiva(p):
    """declaracao_classe_primitiva : CLASS IDENTIFICADOR_CLASSE classe_primitiva_subclass_opcional individuals_opcional"""
    
    retorno = ["classe primitiva", p[2]]
    if p[3] != None:
        retorno = retorno + [p[3]]

    p[0] = retorno + [p[4]]

def p_tipo_classe_definida(p):
    """tipo_classe_definida : classe_enumerada
                             | classe_coberta
                             | classe_aninhada"""
    p[0] = p[1]


def p_classe_primitiva_subclass_opcional(p):
    """classe_primitiva_subclass_opcional : SUBCLASSOF sequencia_subclassof
                             | SUBCLASSOF classe_aninhada
                             | """
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None

def p_sequencia_subclassof(p):
    """sequencia_subclassof : sequencia_subclassof SIMBOLO_ESPECIAL conteudo_aninhamento
                   | conteudo_aninhamento """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_classe_enumerada(p):
    """classe_enumerada : SIMBOLO_ESPECIAL identificadores_classe_sequencia SIMBOLO_ESPECIAL"""
    p[0] = ["enumerada", p[2]]

def p_classe_coberta(p):
    """classe_coberta : identificadores_classe_sequencia"""
    p[0] = ["coberta", p[1]]

def p_classe_aninhada(p):
    """classe_aninhada : IDENTIFICADOR_CLASSE AND aninhamento
                        | AND aninhamento"""
    
    if len(p) == 4:
        p[0] = ["aninhada", p[1], p[3]]
    else:
        p[0] = ["aninhada", p[2]]


def p_aninhamento(p):
    """aninhamento : conteudo_aninhamento_com_parenteses
                   | LPAREN conteudo_aninhamento_com_parenteses OR conteudo_aninhamento_com_parenteses RPAREN
                   | LPAREN aninhamento RPAREN
                   | conteudo_aninhamento_com_parenteses AND aninhamento"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 6:
        p[0] = [["or", p[2]] + [p[4]]]
    elif len(p) == 4 and p[1] == "(":
        p[0] = p[2]
    else:
        p[0] = [[p[1]] + p[3]]

def p_conteudo_aninhamento_com_parenteses(p):
    """conteudo_aninhamento_com_parenteses : LPAREN conteudo_aninhamento RPAREN"""
    p[0] = p[2]

def p_conteudo_aninhamento(p):
    """conteudo_aninhamento :  IDENTIFICADOR_PROPRIEDADE restricao_propriedade conteudo_aninhamento_pos
                             | IDENTIFICADOR_PROPRIEDADE MIN CARDINALIDADE conteudo_aninhamento_pos
                             | IDENTIFICADOR_PROPRIEDADE restricao_propriedade conteudo_aninhamento_com_parenteses"""
    
    if len(p) == 4:
        p[0] = [p[1]] + [p[2]] + [p[3]]
    else:
        p[0] = [p[1]] + [p[2]] + [p[3]] + [p[4]]

def p_conteudo_aninhamento_pos(p):
    """conteudo_aninhamento_pos : IDENTIFICADOR_CLASSE
                                | NAMESPACE TIPO_DADO
                                | LPAREN identificadores_classe_or RPAREN
                                | NAMESPACE TIPO_DADO SIMBOLO_ESPECIAL operador_relacional cardinalidade_com_sem_aspas_simples SIMBOLO_ESPECIAL"""
    if len(p) == 7:
        p[0] = [p[1]] + [p[2]] + [[p[4]] + [p[5]]]
    elif len(p) == 3:
        p[0] = [p[1]] + [p[2]]
    elif len(p) == 4:
        p[0] = ["or"] + [p[2]]
    else:
        p[0] = p[1]

def p_individuals_opcional(p):
    """
    individuals_opcional : INDIVIDUALS identificadores_individuo_sequencia
                         | 
                         | INDIVIDUALS
                         | identificadores_individuo_sequencia
    """
    if len(p) == 3:
        p[0] = ["INDIVIDUALS", p[2]]
    elif len(p) == 2:
        tratamento_personalizado_erros("'Individuals' deve ser seguido de pelo menos um indivíduo.", p)
    else:
        p[0] = ["INDIVIDUALS", []]


# PARSER AUX #

def p_operador_relacional(p):
    """operador_relacional : MAIOR
                            | MENOR
                            | MAIORIGUAL
                            | MENORIGUAL"""
    p[0] = p[1]

def p_cardinalidade_com_sem_aspas_simples(p):
    """cardinalidade_com_sem_aspas_simples : CARDINALIDADE
                                | SIMBOLO_ESPECIAL CARDINALIDADE SIMBOLO_ESPECIAL"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_identificadores_classe_sequencia(p):
    """identificadores_classe_sequencia : IDENTIFICADOR_CLASSE
                                         | identificadores_classe_sequencia SIMBOLO_ESPECIAL IDENTIFICADOR_CLASSE"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_identificadores_classe_or(p):
    """identificadores_classe_or : IDENTIFICADOR_CLASSE
                                | identificadores_classe_or OR IDENTIFICADOR_CLASSE"""
    
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_identificadores_individuo_sequencia(p):
    """identificadores_individuo_sequencia : IDENTIFICADOR_INDIVIDUO
                                         | identificadores_individuo_sequencia SIMBOLO_ESPECIAL IDENTIFICADOR_INDIVIDUO"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_restricao_propriedade(p):
    """restricao_propriedade : ONLY
                            | SOME
                            | VALUE"""
    p[0] = p[1]


def p_error(p):
    if p:
        print(f"Erro sintático no token: {p.type}, valor: '{p.value}', linha: {p.lineno}")
        print(p)
    else:
        print("Erro sintático: fim inesperado da entrada.")

def tratamento_personalizado_erros(message, p):
    print(f"Erro sintático, linha {p.lineno(1)}. {message}")
    exit()

parser = yacc.yacc()

# ============================
# MAIN
# ============================

def main():
    with open('src/entrada_parser.txt', 'r') as file:
        entrada = file.read()

    resultado = parser.parse(entrada, lexer=lexer)
    print("Árvore Sintática:")
    for i in resultado:
        print(i)

if __name__ == "__main__":
    main()

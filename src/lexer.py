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
    # 'disjointclasses': 'DISJOINTCLASSES',
    # 'disjointwith': 'DISJOINTWITH',
}

# Tipos de dados
type_dado = [
    'integer', 'real', 'string', 'boolean', 'date', 'time',
    'long', 'language', 'short', 'token', 'byte', 'Name', 'NCName',
]

# Tokens
tokens = [
    'MAIORIGUAL', 'MENORIGUAL', 'MAIOR', 'MENOR',  'IDENTIFICADOR_CLASSE', 'IDENTIFICADOR_PROPRIEDADE', 'IDENTIFICADOR_INDIVIDUO', 
    'CARDINALIDADE', 'SIMBOLO_ESPECIAL', 'TIPO_DADO', 'NAMESPACE', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', "COMMA", 'OPENKEY', 'DISJOINTCLASSES', 'DISJOINTWITH'
] + list(set(reservadas.values()))

# Regras de tokens
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r'\,'
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

def t_EXACTLY(t):
    r'exactly'
    return t

def t_CLASS(t):
    r'[Cc][Ll][Aa][Ss][Ss]\s*:'
    return t

def t_SUBCLASSOF(t):
    r'[Ss][Uu][Bb][Cc][Ll][Aa][Ss][Ss][Oo][Ff]\s*:'
    return t

def t_EQUIVALENTTO(t):
    r'[Ee][Qq][Uu][Ii][Vv][Aa][Ll][Ee][Nn][Tt][Tt][Oo]\s*:'
    return t

def t_AND(t):
    r'and'
    return t

def t_DISJOINTCLASSES(t):
    r'[Dd][Ii][Ss][Jj][Oo][Ii][Nn][Tt][Cc][Ll][Aa][Ss][Ss][Ee][Ss]\s*:'
    return t

def t_DISJOINTWITH(t):
    r'[Dd][Ii][Ss][Jj][Oo][Ii][Nn][Tt][Ww][Ii][Tt][Hh]\s*:'
    return t

def t_INDIVIDUALS(t):
    r'[Ii][Nn][Dd][Ii][Vv][Ii][Dd][Uu][Aa][Ll][Ss]\s*:'
    return t

def t_NAMESPACE(t):
    r'owl:|rdfs:|xsd:'
    t.value = t.value[:-1]  # Remove o ":" no final
    return t

def t_TIPO_DADO(t):
    r'\b(integer|real|string|boolean|date|time|long|language|short|token|byte|Name|NCName)\b'
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
    r'([\[\]\'"])'
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

types = []
errors = []

def add_new_type(type):
    if type not in types:
        types.append(type)

def p_ontologia(p):
    """ontologia : declaracao_classe
                 | ontologia declaracao_classe"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaracao_classe(p):
    """declaracao_classe : declaracao_classe_definida
                        | declaracao_classe_primitiva
                        | declaracao_classe_errada"""
    
    global types
    types = []
    
    p[0] = p[1]

def p_declaracao_classe_definida(p):
    """declaracao_classe_definida : CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO tipo_classe_definida subclass_opcional individuals_opcional"""
    p[0] = [p[2], ["DEFINIDA", types], p[4]]

def p_declaracao_classe_primitiva(p):
    """declaracao_classe_primitiva : CLASS IDENTIFICADOR_CLASSE SUBCLASSOF tipo_classe_primitiva disjoint_opcional individuals_opcional"""
    p[0] = [p[2], ["PRIMITIVA", types], p[4]]

    if p[5] != None:
        p[0] += [p[5]]
    if p[6] != None:
        p[0] += [p[6]]

def p_declaracao_classe_errada(p):
    """declaracao_classe_errada : CLASS IDENTIFICADOR_CLASSE DISJOINTCLASSES identificadores_classe_sequencia
                                | CLASS IDENTIFICADOR_CLASSE DISJOINTWITH identificadores_classe_sequencia
                                | CLASS IDENTIFICADOR_CLASSE INDIVIDUALS individuals_opcional"""
    tratamento_personalizado_erros("Declaracao incorreta de classe.", p)

def p_tipo_classe_definida(p):
    """tipo_classe_definida : classe_enumerada
                             | classe_coberta
                             | classe_aninhada"""
    p[0] = p[1]

def p_subclass_opcional(p):
    """subclass_opcional : SUBCLASSOF tipo_classe_primitiva
                             | """
    
    p[0] = None

    if len(p) > 1:
        p[0] = p[2]


def p_tipo_classe_primitiva(p):
    """tipo_classe_primitiva : sequencia_subclassof
                             | classe_aninhada
                             | IDENTIFICADOR_CLASSE
                             | IDENTIFICADOR_CLASSE COMMA sequencia_subclassof"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = [p[1], p[3]]

def p_sequencia_subclassof(p):
    """sequencia_subclassof : sequencia_subclassof COMMA aninhamento_ou_conteudo_aninhamento
                   | aninhamento_ou_conteudo_aninhamento """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]

def p_disjoint_opcional(p):
    """disjoint_opcional : DISJOINTCLASSES identificadores_classe_sequencia
                         | DISJOINTWITH identificadores_classe_sequencia
                         | """
    if len(p) == 1:
        p[0] = None
    elif p[1].lower() == 'disjointclasses:':
        p[0] = ["DISJOINT_CLASSES", p[2]]
    elif p[1].lower() == 'disjointwith:':
        p[0] = ["DISJOINT_WITH", p[2]]

def p_classe_enumerada(p):
    """classe_enumerada : LBRACE identificadores_individuo_sequencia RBRACE"""
    p[0] = ["enum", p[2]]
    add_new_type("ENUMERADA")

def p_classe_coberta(p):
    """classe_coberta : identificadores_classe_or"""
    p[0] = ["coberta", p[1]]
    add_new_type("COBERTA")

def p_classe_aninhada(p):
    """classe_aninhada : IDENTIFICADOR_CLASSE AND aninhamento
                        | AND aninhamento"""
    
    if len(p) == 4:
        p[0] = [p[1], "AND", p[3]]
    else:
        p[0] = ["AND", p[2]]


def p_aninhamento(p):
    """aninhamento : conteudo_aninhamento_com_parenteses
                   | conteudo_aninhamento
                   | aninhamento AND aninhamento"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + p[3]

def p_conteudo_aninhamento(p):
    """conteudo_aninhamento :  IDENTIFICADOR_PROPRIEDADE restricao_propriedade conteudo_aninhamento_pos
                             | IDENTIFICADOR_PROPRIEDADE IDENTIFICADOR_PROPRIEDADE restricao_propriedade conteudo_aninhamento_pos
                             | IDENTIFICADOR_PROPRIEDADE restricao_palavra_reservada CARDINALIDADE conteudo_aninhamento_pos
                             | IDENTIFICADOR_PROPRIEDADE IDENTIFICADOR_PROPRIEDADE restricao_palavra_reservada CARDINALIDADE conteudo_aninhamento_pos"""

    if len(p) == 4:
        p[0] = [p[1]] + [p[2]] + [p[3]]

    elif len(p) == 5:
        p[0] = [p[1]] + [p[2]] + [p[3]] + [p[4]]

    else:
        p[0] = [p[1]] + [p[2]] + [p[3]] + [p[4]] + [p[5]]


def p_conteudo_aninhamento_com_parenteses(p):
    """conteudo_aninhamento_com_parenteses : LPAREN conteudo_aninhamento RPAREN
                                            | LPAREN conteudo_aninhamento_com_parenteses or_and conteudo_aninhamento_com_parenteses RPAREN"""
    if len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = [p[3], p[2], p[4]]



def p_conteudo_aninhamento_pos(p):
    """conteudo_aninhamento_pos : IDENTIFICADOR_CLASSE
                                | conteudo_aninhamento_com_parenteses
                                | NAMESPACE TIPO_DADO
                                | LPAREN identificadores_classe_or_and RPAREN
                                | NAMESPACE TIPO_DADO SIMBOLO_ESPECIAL operador_relacional cardinalidade_com_sem_aspas_simples SIMBOLO_ESPECIAL"""
    if len(p) == 7:
        p[0] = [p[1], p[2], [[p[4], p[5]]]]
    elif len(p) == 3:
        p[0] = [p[1], [p[2]]]
    elif len(p) == 4:
        add_new_type("FECHADA")
        p[0] = p[2]
    elif len(p) == 2:
        p[0] = p[1]

        if isinstance(p[1], list):
            add_new_type("ANINHADA")

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
        p[0] = None


# PARSER AUX #

def p_operador_relacional(p):
    """operador_relacional : MAIOR
                            | MENOR
                            | MAIORIGUAL
                            | MENORIGUAL"""
    p[0] = p[1]

def p_or_and(p):
    """or_and : OR
                | AND"""
    if p[1] == "or":
        p[0] = "OR"
    else:
        p[0] = "AND"

def p_cardinalidade_com_sem_aspas_simples(p):
    """cardinalidade_com_sem_aspas_simples : CARDINALIDADE
                                | SIMBOLO_ESPECIAL CARDINALIDADE SIMBOLO_ESPECIAL"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_identificadores_classe_sequencia(p):
    """identificadores_classe_sequencia : IDENTIFICADOR_CLASSE
                                         | identificadores_classe_sequencia COMMA identificadores_classe_sequencia
                                         | identificadores_classe_sequencia identificadores_classe_sequencia"""
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + p[3]
    else:
        tratamento_personalizado_erros("Vírgula não presente na sequência de identificadores de classe.")

def p_identificadores_classe_or(p):
    """identificadores_classe_or : IDENTIFICADOR_CLASSE
                                | identificadores_classe_or OR IDENTIFICADOR_CLASSE"""
    
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_identificadores_classe_or_and(p):
    """identificadores_classe_or_and : IDENTIFICADOR_CLASSE
                                      | identificadores_classe_or_and or_and IDENTIFICADOR_CLASSE"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2], p[3]]

def p_identificadores_individuo_sequencia(p):
    """identificadores_individuo_sequencia : IDENTIFICADOR_INDIVIDUO
                                         | identificadores_individuo_sequencia COMMA identificadores_individuo_sequencia"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + p[3]

def p_restricao_propriedade(p):
    """restricao_propriedade : ONLY
                            | ALL
                            | SOME
                            | VALUE
                            | NOT
                            | THAT"""
    p[0] = p[1]

def p_restricao_palavra_reservada(p):
    """restricao_palavra_reservada : MIN
                            | MAX
                            | SOME
                            | EXACTLY"""
    p[0] = p[1]

def p_aninhamento_ou_conteudo_aninhamento(p):
    """aninhamento_ou_conteudo_aninhamento : aninhamento
                                           | conteudo_aninhamento"""
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Erro sintático no token: {p.type}, valor: '{p.value}', linha: {p.lineno}")
        print(p)
    else:
        print("Erro sintático: fim inesperado da entrada.")

def tratamento_personalizado_erros(message, p):
    errors.append(f"Erro sintático, linha {p.lineno(1)}. {message}")

parser = yacc.yacc(debug=False, write_tables=False, errorlog=yacc.NullLogger())

# ============================
# MAIN
# ============================

def main():
    with open('src/entrada_parser.txt', 'r') as file:
        entrada = file.read()

    resultado = parser.parse(entrada, lexer=lexer)
    resultado = [item for item in resultado if item is not None]

    if resultado is not None:
        print("Árvore Sintática:")
        for i in resultado:
            print(i)
        print("\n" + "="*30)

        if len(errors) == 0:
            print(" " * 10 + "OK!")
        else:
            for i in errors:
                print(i)

        print("="*30 + "\n")

if __name__ == "__main__":
    main()

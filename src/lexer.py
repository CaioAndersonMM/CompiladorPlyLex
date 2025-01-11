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
    """ontologia : declaracao_classe_definida
                 | ontologia declaracao_classe_definida"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_declaracao_classe_definida(p):
    """declaracao_classe_definida : CLASS IDENTIFICADOR_CLASSE EQUIVALENTTO tipo_classe_definida"""
    p[0] = ["classe definida", p[2], p[4]]

def p_tipo_classe_definida(p):
    """tipo_classe_definida : classe_enumerada
                             | classe_coberta
                             | classe_aninhada"""
    p[0] = p[1]

def p_classe_enumerada(p):
    """classe_enumerada : SIMBOLO_ESPECIAL identificadores_classe_sequencia SIMBOLO_ESPECIAL"""
    p[0] = ["enumerada", p[2]]

def p_classe_coberta(p):
    """classe_coberta : identificadores_classe_sequencia"""
    p[0] = ["coberta", p[1]]

def p_classe_aninhada(p):
    """classe_aninhada : IDENTIFICADOR_CLASSE AND aninhamento"""
    p[0] = ["aninhada", p[1], p[3]]


def p_aninhamento(p):
    """aninhamento : conteudo_aninhamento
                   | conteudo_aninhamento AND aninhamento"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_conteudo_aninhamento(p):
    """conteudo_aninhamento : LPAREN IDENTIFICADOR_PROPRIEDADE SOME conteudo_aninhamento_pos RPAREN
                             | LPAREN IDENTIFICADOR_PROPRIEDADE ONLY conteudo_aninhamento_pos RPAREN
                             | LPAREN IDENTIFICADOR_PROPRIEDADE MIN CARDINALIDADE conteudo_aninhamento_pos RPAREN"""
    
    if len(p) == 5:
        p[0] = [p[2]] + [p[3]] + [p[4]]
    else:
        p[0] = [p[2]] + [p[3]] + [p[4]] + [p[5]]

def p_conteudo_aninhamento_pos(p):
    """conteudo_aninhamento_pos : IDENTIFICADOR_CLASSE
                                | NAMESPACE TIPO_DADO
                                | NAMESPACE TIPO_DADO SIMBOLO_ESPECIAL operador_relacional cardinalidade_com_sem_aspas_simples SIMBOLO_ESPECIAL"""
    if len(p) == 7:
        p[0] = [p[1]] + [p[2]] + [[[p[4]] + [p[5]]]]
    elif len(p) == 3:
        p[0] = [p[1]] + [p[2]]
    else:
        p[0] = p[1]

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

def p_error(p):
    if p:
        print(f"Erro sintático no token: {p.type}, valor: '{p.value}', linha: {p.lineno}")
        print(p)
    else:
        print("Erro sintático: fim inesperado da entrada.")

parser = yacc.yacc()

# ============================
# MAIN
# ============================

def main():
    entrada = """
    Class: Spiciness

        EquivalentTo:  {Hot , Medium , Mild}
    Class: Spicinesss
        EquivalentTo:  Hot , Medium , Mild

    Class: CheesyPizza
    EquivalentTo:
        Pizza
        and (purchasedPizza some Pizza)
        and (numberOfPhone some xsd:string)
        and (hasTopping some CheeseTopping)
        and (hasCaloriContent some xsd:integer[>= '400'])
        and (hasTopping min 3 PizzaTopping)
        and (ssn min 1 xsd:string)
        and (hasCaloricContent some xsd:integer[< 400])

    Class: Spicinessss
        EquivalentTo:  Hot , Medium , Mild
    """
    resultado = parser.parse(entrada, lexer=lexer)
    print("Árvore Sintática:")
    for i in resultado:
        print(i)

if __name__ == "__main__":
    main()

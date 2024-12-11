# Lexical Analyzer - PLY Tokenizer

Este repositório contém um analisador léxico desenvolvido com **PLY (Python Lex-Yacc)**. Ele processa arquivos de entrada com sintaxe específica, identifica e classifica tokens conforme regras predefinidas, e armazena as informações em uma tabela de símbolos.

---

## **Sumário**
- [Funcionalidades](#funcionalidades)
- [Instruções de Execução](#instruções-de-execução)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Tokens Reconhecidos](#tokens-reconhecidos)
- [Exemplo de Uso](#exemplo-de-uso)
- [Tabela de Símbolos](#tabela-de-símbolos)

---

## **Funcionalidades**
- Identificação de **palavras reservadas**, **identificadores de classe**, **propriedades**, **cardinalidades**, e **tipos de dados**.
- Validação e classificação de tokens conforme regras sintáticas.
- Registro de tokens identificados na tabela de símbolos com informações de tipo e linha.

---

## **Instruções de Execução**
- O projeto inclui um arquivo denominado entrada.txt, localizado na pasta /data. Este arquivo pode ser editado para testar diferentes entradas de código.
- Certifique-se de que o Python esteja corretamente instalado em sua máquina. Caso não tenha o Python, você pode baixá-lo através do seguinte link: https://www.python.org/downloads/.
- No terminal, instale a dependência PLY utilizando o comando: `pip install ply`
- Em seguida, execute o arquivo main.py, localizado na raiz do projeto.
- Para visualizar os resultados, consulte os arquivos gerados na pasta /data, os quais têm nomes iniciados por "saida". Esses arquivos contêm o sumário da execução, a tabela de símbolos e os tokens gerados.
---

## **Estrutura do Repositório**
```plaintext
data/
├── entrada.txt                    # Arquivo de entrada com o código fonte
├── saida_tokens.txt               # Arquivo de saída com todos os tokens identificados
├── saida_sumario.txt              # Arquivo de saída com quantitativo de palavras e tipos
├── saida_tabela_simbolos.txt      # Arquivo de saída que exibirá a tabela de símbolos
src/
├── symbol_table.py         # Implementação da Tabela de Símbolos
├── lexer.py                # Analisador léxico principal, contendo as regras e definições do lex
main.py                     # Arquivo principal que deverá ser executado
```
---

## **Tokens Reconhecidos**
O analisador léxico é capaz de reconhecer os seguintes tipos de tokens
#### Palavras Reservadas
Estas palavras são pré-definidas e têm um significado específico dentro da sintaxe. As palavras reservadas incluem:
```plaintext
some, all, value, min, max, exactly, that, not, and, or, class, equivalentto, individuals, subclassof, disjointclasses.
```
### Identificadores
Identificadores são usados para nomear classes, propriedades e indivíduos. As regras para formatação dos identificadores são:

- Identificadores de Classe: Devem começar com uma letra maiúscula, podendo conter letras, números e sublinhados.
```plaintext
Exemplos: Pizza, Vegetarian_Pizza.
````
-  Identificadores de Propriedade: Normalmente começam com letra minúscula e podem ter prefixos como has, is, ou usar um formato camelCase.
```plaintext
Exemplos: hasTopping, isPartOf, topping.
````
-  Identificadores de Indivíduo: Começam com uma letra maiúscula, seguidas por letras, números e devem terminar com um número.
```plaintext
Exemplos: Pizza1, VegetarianPizza2.
````
-  Cardinalidades: São representadas por números inteiros e indicam a quantidade de elementos. 
```plaintext
Exemplos: 3, 400, 1
````

-  Tipos de Dados: Os tipos de dados suportados são:
```plaintext
integer, real, string, boolean, date, time, long, language, short, token, byte, Name, NCName e outros a serem definidos.
```
-  Namespace: Namespaces usuais definidos e seguidos de dois pontos, como:
```plaintext
Exemplos: owl:, rdfs:, xsd:
````
-  Símbolos Especiais: Incluem caracteres como:
```plaintext
Exemplos: {, }, >=, <=, etc.
```

---

## **Exemplos de Uso**
Suponha que o arquivo entrada.txt contenha o seguinte código:

```plaintext
Class: Customer
    EquivalentTo:
        Person
        and (purchasedPizza some Pizza)
        and (numberOfPhone some xsd:string)
````
Ao executar o script main.py, o analisador identificará os seguintes tokens e preencherá todos os arquivos de saída:
```plaintext
#saida_tokens.txt

Token(PALAVRA_RESERVADA, 'class')
Token(IDENTIFICADOR_CLASSE, 'Customer')
Token(PALAVRA_RESERVADA, 'equivalentto')
Token(IDENTIFICADOR_CLASSE, 'Person')
Token(PALAVRA_RESERVADA, 'and')
Token(SIMBOLO_ESPECIAL, '(')
Token(IDENTIFICADOR_PROPRIEDADE, 'purchasedPizza')
Token(PALAVRA_RESERVADA, 'some')
Token(IDENTIFICADOR_CLASSE, 'Pizza')
Token(SIMBOLO_ESPECIAL, ')')
Token(PALAVRA_RESERVADA, 'and')
Token(SIMBOLO_ESPECIAL, '(')
Token(IDENTIFICADOR_PROPRIEDADE, 'numberOfPhone')
Token(PALAVRA_RESERVADA, 'some')
Token(NAMESPACE, 'xsd:')
Token(TIPO_DADO, 'string')
Token(SIMBOLO_ESPECIAL, ')')
````

## **Tabela de Símbolos**
A Tabela de Símbolos mantém o controle dos tokens identificados durante o processo de análise léxica. Cada entrada contém informações sobre o símbolo, seu tipo e a linha em que foi encontrado. O objetivo da tabela de símbolos é fornecer um mapeamento detalhado e organizado dos tokens analisados, o que facilita o processo de análise sintática e semântica subsequente.


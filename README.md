# Lexical Analyzer - PLY Tokenizer

Este repositório contém um analisador léxico desenvolvido com **PLY (Python Lex-Yacc)**. Ele processa arquivos de entrada com sintaxe específica, identifica e classifica tokens conforme regras predefinidas, e armazena as informações em uma tabela de símbolos.

---

## **Sumário**
- [Funcionalidades](#funcionalidades)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Tokens Reconhecidos](#tokens-reconhecidos)
- [Como Usar](#como-usar)
  - [Arquivo de Entrada](#arquivo-de-entrada)
  - [Executando o Analisador](#executando-o-analisador)
- [Exemplo de Uso](#exemplo-de-uso)
- [Tabela de Símbolos](#tabela-de-símbolos)
- [Como Baixar e Instalar o PLY](#como-baixar-e-instalar-o-ply)

---

## **Funcionalidades**
- Identificação de **palavras reservadas**, **identificadores de classe**, **propriedades**, **cardinalidades**, e **tipos de dados**.
- Validação e classificação de tokens conforme regras sintáticas.
- Registro de tokens identificados na tabela de símbolos com informações de tipo e linha.

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
main.py                     # Arquivo principal que deverá ser executado (main)
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
````

---
## **Como Usar**
No arquivo chamado entrada.txt dentro da pasta data é onde deve está o código a ser analisado. Exemplo:
```plaintext
Class: InterestingPizza
    EquivalentTo:
        Pizza
        and (hasTopping min 3 PizzaTopping)
```
---
## **Como Baixar e Instalar o PLY**
O PLY (Python Lex-Yacc) é uma biblioteca que facilita a criação de analisadores léxicos e sintáticos em Python. Para utilizar o projeto, você precisará instalar o PLY. Siga os passos abaixo:
- Instalar o PLY com pip
O método mais simples de instalar o PLY é através do pip, o gerenciador de pacotes do Python. Se você não tiver o pip instalado, consulte a documentação oficial do pip para mais informações.
```plaintext
pip install ply
````

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


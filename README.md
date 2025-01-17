# Lexical and Syntax Analyzer - PLY

Este repositório contém um analisador léxico e sintático desenvolvido com PLY (Python Lex-Yacc). Ele processa arquivos de entrada com sintaxe específica, identifica e classifica tokens conforme regras predefinidas, gera uma árvore sintática e armazena as informações em uma tabela de símbolos.
---

## **Sumário**
- [Analise Sintática](#análise-sintática)
- [Funcionalidades](#funcionalidades-léxicas)
- [Instruções de Execução](#instruções-de-execução)
- [Estrutura do Repositório](#estrutura-do-repositório)
- [Tokens Reconhecidos](#tokens-reconhecidos)
- [Exemplo de Uso](#exemplos-de-uso)
- [Tabela de Símbolos](#tabela-de-símbolos)

---

## **Funcionalidades Léxicas**
- Identificação de **palavras reservadas**, **identificadores de classe**, **propriedades**, **cardinalidades**, e **tipos de dados**.
- Validação e classificação de tokens conforme regras sintáticas.
- Registro de tokens identificados na tabela de símbolos com informações de tipo e linha.

---

## **Funcionalidades Sintáticas**
- Identifica e classifica tokens da entrada com base em regras definidas.
- Informa erros, o tipo de erro e a linha.
- Gera uma árvore sintática com base nas produções definidas em YACC.



## **Instruções de Execução**
- O projeto inclui um arquivo denominado entrada.txt e entrada2.txt, localizado na pasta /data. Este arquivo pode ser editado para testar diferentes entradas de código.
- Certifique-se de que o Python esteja corretamente instalado em sua máquina. Caso não tenha o Python, você pode baixá-lo através do seguinte link: https://www.python.org/downloads/.
- No terminal, instale a dependência PLY utilizando o comando: `pip install ply`
- Em seguida, execute o arquivo main.py, localizado na raiz do projeto.
- Para visualizar os resultados, consulte os arquivos gerados na pasta /data, os quais têm nomes iniciados por "saida". Esses arquivos contêm o sumário da execução, a tabela de símbolos e os tokens gerados.
---

![image](https://github.com/user-attachments/assets/272546f1-ca02-4588-9ba4-12eb3a805c04)

---
## **Estrutura do Repositório**
```plaintext
data/
├── entrada.txt                    # Arquivo de entrada com o código fonte
├── entrada2.txt                   # Arquivo de entrada com o código fonte alternativo
├── saida_tokens.txt               # Arquivo de saída com todos os tokens identificados
├── saida_sumario.txt              # Arquivo de saída com quantitativo de palavras e tipos
├── saida_tabela_simbolos.txt      # Arquivo de saída que exibirá a tabela de símbolos
src/
├── symbol_table.py         # Implementação da Tabela de Símbolos
├── principal.py                # Analisador léxico principal, e agora com a nova atualização, está junto do analisador sintático, contendo as regras e definições do lex e as gramáticas e tratamentos.
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

### Mas agora, será retornado a nossa árvore sintática no terminal do usuário, junto com dois novos arvivos:
#### parser.out: Gerado automaticamente pelo PLY durante a execução do analisador sintático. Contém informações detalhadas sobre a gramática, incluindo:
- Produções: Todas as regras sintáticas definidas em YACC.
- Estados do Autômato LR: Representação detalhada dos estados gerados para a análise sintática.
- Tabelas de Análise: Incluem as ações (shift, reduce, goto) para cada estado.
  
#### parsetab: Este arquivo armazena tabelas de análise sintática geradas pelo PLY, otimizando a execução futura. Ele inclui:
- Tabelas de Parsing: Estruturas pré-calculadas para agilizar a análise sintática.
- Cache: Permite evitar o cálculo repetitivo das tabelas, acelerando a inicialização do parser.


![image](https://github.com/user-attachments/assets/3d1d33ee-8fa3-4ab5-98ba-e29a153ddd18)


-------
## **Tabela de Símbolos**
A Tabela de Símbolos mantém o controle dos tokens identificados durante o processo de análise léxica. Cada entrada contém informações sobre o símbolo, seu tipo e a linha em que foi encontrado. O objetivo da tabela de símbolos é fornecer um mapeamento detalhado e organizado dos tokens analisados, o que facilita o processo de análise sintática e semântica subsequente.
- A tabela é implementada como um dicionário Python (self.tabela = {}), onde cada símbolo é a chave, e o valor associado é outro dicionário contendo outras informações.
- Adição de símbolos: add(simbolo, tipo, linha) insere um símbolo na tabela com suas informações, se o símbolo já existir, exibe um aviso para evitar duplicatas.
- Get e Set: get(simbolo) permite buscar informações sobre um símbolo específico e set(simbolo, tipo=None, linha=None) atualiza o tipo ou a linha de um símbolo existente.
- A função show() exibe todos os símbolos armazenados, junto com suas informações.
```plaintext
class: Tipo = PALAVRA_RESERVADA, Linha = 1
Activity: Tipo = IDENTIFICADOR_CLASSE, Linha = 1
subclassof: Tipo = PALAVRA_RESERVADA, Linha = 3
````

-----

## **Análise Sintática**

- Funcionamento Bem-sucedido: Quando a entrada segue corretamente a gramática definida, o programa gera além da árvore sintática correspondente, que estrutura a entrada de forma hierárquica.

````
Uma mensagem clara de "OK!" indicando que a análise foi bem-sucedida.
````
 ![image](https://github.com/user-attachments/assets/c61af515-daf6-4dfc-80a4-231c831550a1)


- Ocorrências de erro: Com base na gramática definida, quando ocorre um erro, é exposto ao usuario a interrupção do código, a linha exata onde o problema ocorreu, a qual token se refere e o tipo de erro.

![image](https://github.com/user-attachments/assets/86f5382a-fff5-4740-8747-8ed236218656)



### Definições da Gramática
- Classe Primitivas: Indivíduos herdam suas propriedades. No entanto, indivíduos externos que possuam tais propriedades não podem ser automaticamente classificados como membros desta classe.
```plaintext
Class: Pizza
SubClassOf:
hasBase some PizzaBase,
hasCaloricContent some xsd:integer
DisjointClasses:
Pizza, PizzaBase, PizzaTopping
Individuals:
CustomPizza1,
CustomPizza2
```
- Classe Definida: Contém condições necessárias e suficientes para descrever a classe. Indivíduos externos que atendam às condições podem ser classificados como membros dessa classe. Geralmente, utiliza o axioma EquivalentTo seguido de descrições.
```plaintext
Class: CheesyPizza
EquivalentTo:
Pizza and (hasTopping some CheeseTopping)
Individuals:
CheesyPizza1
Class: HighCaloriePizza
EquivalentTo:
Pizza and (hasCaloricContent some xsd:integer[>= 400])
```
- Classe com axioma de fechamento (closure axiom): Contém normalmente uma cláusula que “fecha” ou restringe as imagens de suas relações a um conjunto bem definido de classes ou de expressões.
```plaintext
Class: MargheritaPizza
SubClassOf:
NamedPizza,
hasTopping some MozzarellaTopping,
hasTopping some TomatoTopping,
hasTopping only (MozzarellaTopping or TomatoTopping)
```
- Classe com descrições aninhadas: : A imagem de uma propriedade que descreve uma classe pode não ser uma outra classe, mas outra tripla composta de propriedade, quantificador e outra classe
```plaintext
Class: SpicyPizza
EquivalentTo:
Pizza
and (hasTopping some (hasSpiciness value Hot))
```
- Classe enumarada: Representa um conjunto fixo e finito de indivíduos, definidos explicitamente.
```plaintext
Class: Spiciness
EquivalentTo: {Hot1, Medium1, Mild1} // Lista de indivíduos
```
- Classe coberta: Representa uma classe que cobre completamente as opções possíveis para seus membros, utilizando operadores como or.
```plaintext
Class: Spiciness
EquivalentTo: Hot or Medium or Mild // Lista de classes (não indivíduos)
```

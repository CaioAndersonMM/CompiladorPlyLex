from src.principal import lexer, parser, errors, type_dado

RESERVED_WORDS = {"some", "all", "only", "and", "or", "not", "min", "max", "exactly", 'DISJOINT_WITH', 'EQUIVALENT_TO', 'INVERSE_OF', 'SUBCLASS_OF', 'DOMAIN', 'RANGE', 'PRIMITIVA', 'DEFINIDA', 'FECHADA', 'SUBCLASSE', 'INDIVIDUALS', 'DISJOINT_CLASSES', 'ANINHADA', 'ENUMERADA', 'COBERTA', 'coberta'}

NUMERIC_TYPES = {tipo for tipo in type_dado if tipo not in {'string', 'boolean', 'date', 'time', 'language', 'token', 'byte', 'Name', 'NCName'}}

DATA_TYPES = {"xsd:string", "xsd:real", "xsd:integer", "xsd:float", "xsd:boolean", "xsd:dateTime"}.union(type_dado)


def classificar_propriedade(propriedade, sucessor, linha):
    def extrair_tipos(sucessor):
        if isinstance(sucessor, list):
            tipos = []
            for item in sucessor:
                if isinstance(item, list):
                    tipos.extend(extrair_tipos(item))
                elif isinstance(item, str):
                    tipos.append(item)
            return tipos
        elif isinstance(sucessor, str):
            return [sucessor]
        return []

    tipos_extraidos = extrair_tipos(sucessor)

    if any(tipo in DATA_TYPES for tipo in tipos_extraidos):
        tipo = "data property"
    else:
        tipo = "object property"
    return tipo

def analisar_propriedades(classe, class_line):
    if isinstance(classe, (list, tuple)) and len(classe) >= 4:
        _, _, _, class_data = classe[:4]

        def processar_propriedades(data):
            if isinstance(data, list):
                for item in data:
                    # Se for uma lista contendo propriedade, quantificador e sucessor
                    if isinstance(item, list) and len(item) >= 3:
                        propriedade = item[0]
                        quantificador = item[1]

                        if isinstance(quantificador, str) and quantificador in {"some", "only", "min", "max", "exactly"}:
                            sucessor = item[2]
                            # Classifica a propriedade com base no sucessor
                            tipo = classificar_propriedade(propriedade, sucessor, class_line)
                            print(f"Propriedade '{propriedade}' classificada como '{tipo}'.")

                    # Processa itens aninhados
                    processar_propriedades(item)

        processar_propriedades(class_data)


def main():
    print("Escolha o arquivo a ser processado:")
    print("1 - data/entrada")
    print("2 - data/entrada2")
    escolha = input("Digite o número correspondente à sua escolha: ")

    if escolha == '1':
        caminho_arquivo = 'data/entrada'
    elif escolha == '2':
        caminho_arquivo = f'data/entrada{escolha}'
    else:
        print("Opção inválida. Saindo do programa.")
        return

    caminho_arquivo += ".txt"
    try:
        with open(caminho_arquivo, 'r') as file:
            entrada = file.read()
    except FileNotFoundError:
        print(f"Erro: O arquivo {caminho_arquivo} não foi encontrado.")
        return

    resultado = parser.parse(entrada, lexer=lexer)
    resultado = [item for item in resultado if item is not None]
    declared_classes = set()

    if resultado is not None:
        print("Árvore Sintática:")
        print("")
        for classe in resultado:
            class_name = classe[0]
            class_line = classe[1]
            if class_name in declared_classes:
               tratamento_personalizado_erros(f"A classe '{class_name}' já foi declarada.", class_line, destaque=True)
            else:
                declared_classes.add(class_name)
                print(f"Classe: {class_name} (linha {class_line})")

                # Capturando classes mencionadas no restante do conteúdo
                for i in range(2, len(classe)):
                    print(classe[i])
                    if isinstance(classe[i], list):
                        for item in classe[i]:
                            if isinstance(item, list):
                                for sub_item in item:
                                    if isinstance(sub_item, list):
                                        for sub_sub_item in sub_item:
                                            if isinstance(sub_sub_item, str):
                                                if sub_sub_item.lower() in (word.lower() for word in declared_classes) or sub_sub_item.lower() in (word.lower() for word in RESERVED_WORDS):
                                                    continue
                                                else:
                                                    continue
                                    else:
                                        if isinstance(sub_item, str):
                                            if sub_item.lower() in (word.lower() for word in declared_classes) or sub_item.lower() in (word.lower() for word in RESERVED_WORDS):
                                                continue
                                            else:
                                                errors.append(f"Erro semântico, linha {class_line}: A classe '{sub_item}' foi mencionada mas não foi declarada.")
                            else:
                                if isinstance(item, str):
                                    if item.lower() in (word.lower() for word in declared_classes) or item.lower() in (word.lower() for word in RESERVED_WORDS):
                                        continue
                                    else:
                                        errors.append(f"Erro semântico, linha {class_line}: A classe '{item}' foi mencionada mas não foi declarada.")
                    print("-"*90)
            
                print("Classificação de Propriedades:")
                analisar_propriedades(classe, class_line)
                print('\n')
        
        for classe in resultado:
            class_name = classe[0]
            class_line = classe[1]
            class_type = classe[2]
            class_data = classe[3]

            # print(f"{class_name} {class_line}")

            if "FECHADA" in class_type[1]:
                parent_class = class_data[0]
                closure_axiom = class_data[1]


                if isinstance(closure_axiom, list) == False:
                    closure_axiom = class_data[2]

                prop_types = []
                for propriedade in closure_axiom:
                    if (len(propriedade) == 1):
                        propriedade = propriedade[0]

                    if propriedade[1] == "some":
                        prop_types.append(propriedade[2])
                    elif propriedade[1] == "only":
                        prop_fechamento = propriedade[2]
                        
                        if isinstance(prop_fechamento, list) == False:
                            prop_fechamento = [prop_fechamento]



                        index = 0
                        while index < len(prop_fechamento):
                            item = prop_fechamento[index]
                            
                            if item not in prop_types:
                                tratamento_personalizado_erros(f"{item} não foi definido no axioma de fechamento da classe {class_name}.", class_line, destaque=True)

                            index += 2

            verificar_intervalo(classe, class_line)
            verificar_fechamento(classe, class_line)

        print("\n" + "="*30)

        if len(errors) == 0:
            print(" " * 10 + "OK!")
        else:
            for error in errors:
                print(error)

        print("="*30 + "\n")

def verificar_intervalo(classe, class_line):
    if isinstance(classe, (list, tuple)) and len(classe) >= 4:
        _, _, _, class_data = classe[:4]

        def verificar_item(item):
            stack = [item]
            while stack:
                current_item = stack.pop()
                # print('verificando', current_item)
                if isinstance(current_item, list):
                    for sub_item in reversed(current_item):
                        stack.append(sub_item)
                elif isinstance(current_item, str):
                    if current_item.lower() in NUMERIC_TYPES:
                        # Verificar se o próximo item na pilha é um intervalo válido
                        if stack:
                            next_item = stack.pop()
                            if isinstance(next_item, list) and any(isinstance(sub_item, list) and len(sub_item) == 2 and isinstance(sub_item[0], str) and sub_item[0] in [">", "<", ">=", "<=", "=="] for sub_item in next_item):
                                continue
                            else:
                                tratamento_personalizado_erros(f"Erro semântico, linha {class_line}: Tipo numérico '{current_item}' precisa ser seguido por um intervalo.", class_line, destaque=True)
                                stack.append(next_item)  # Recolocar o item na pilha
                        else:
                            tratamento_personalizado_erros(f"Erro semântico, linha {class_line}: Tipo numérico '{current_item}' precisa ser seguido por um intervalo.", class_line, destaque=True)

        for item in class_data:
            verificar_item(item)

def verificar_fechamento(classe, class_line):
    if isinstance(classe, (list, tuple)) and len(classe) >= 4:
        _, _, class_type, class_data = classe[:4]

        # Verifica se a classe é fechada
        if "FECHADA" in class_type[1]:
            propriedades_some = set()
            propriedades_only = set()

            def capturar_propriedades(item):
                if isinstance(item, list) and len(item) > 1:
                    if item[1] == "some":
                        propriedades_some.add(item[0])
                    elif item[1] == "only":
                        propriedades_only.add(item[0])

            for item in class_data:
                if isinstance(item, list):
                    for sub_item in item:
                        if isinstance(sub_item, list):
                            for sub_sub_item in sub_item:
                                capturar_propriedades(sub_sub_item)
                        else:
                            capturar_propriedades(sub_item)
                else:
                    capturar_propriedades(item)

            for prop in propriedades_some:
                if prop not in propriedades_only:
                    tratamento_personalizado_erros(f"Erro semântico, linha {class_line}: Propriedade '{prop}' com 'some' deve ser acompanhada de 'only'.", class_line, destaque=True)

def tratamento_personalizado_erros(message, linha, destaque=False):
    if destaque:
        errors.append(f"\033[91mErro semântico, linha {linha}: {message}\033[0m")
    else:
        errors.append(f"Erro semântico, linha {linha}: {message}")

if __name__ == "__main__":
    main()
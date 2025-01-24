from src.principal import lexer, parser, errors

RESERVED_WORDS = {"some", "all", "only", "and", "or", "not", "min", "max", "exactly", 'DISJOINT_WITH', 'EQUIVALENT_TO', 'INVERSE_OF', 'SUBCLASS_OF', 'DOMAIN', 'RANGE'}

def main():
    print("Escolha o arquivo a ser processado:")
    print("1 - data/entrada")
    print("2 - data/entrada2")
    #escolha = input("Digite o número correspondente à sua escolha: ")
    escolha = "3"

    if escolha == '1':
        caminho_arquivo = 'data/entrada'
    elif escolha == '2' or escolha == '3':
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
    mentioned_classes = set()

    if resultado is not None:
        print("Árvore Sintática:")
        for classe in resultado:
            class_name = classe[0]
            class_line = classe[1]
            if class_name in declared_classes:
                errors.append(f"Erro semântico: A classe '{class_name}' já foi declarada.")
            else:
                declared_classes.add(class_name)
                print(class_name)
                print(classe[1])

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
                    print("---")

        # DUVIDA: POR QUE TEM DUAS VEZES?
        """
        # Verificando classes mencionadas, mas não declaradas
        for mentioned_class in mentioned_classes:
            if mentioned_class not in declared_classes and mentioned_class not in RESERVED_WORDS:
                errors.append(f"Erro semântico: A classe '{mentioned_class}' foi mencionada mas não foi declarada.")
        """


        print("***---***")
        for classe in resultado:
            class_name = classe[0]
            class_line = classe[1]
            class_type = classe[2]
            class_data = classe[3]

            print(f"{class_name} {class_line}")

            if "FECHADA" in class_type[1]:
                parent_class = class_data[0]
                closure_axiom = class_data[1]

                prop_types = []
                for propriedade in closure_axiom:
                    if propriedade[0][1] == "some":
                        prop_types.append(propriedade[0][2])
                    elif propriedade[0][1] == "only":
                        print(prop_types)
                        prop_fechamento = propriedade[0][2]

                        index = 0
                        while index < len(prop_fechamento):
                            item = prop_fechamento[index]
                            
                            if item not in prop_types:
                                tratamento_personalizado_erros(f"{item} não foi definido no axioma de fechamento da classe {class_name}.", class_line)

                            index += 2

        print("\n" + "="*30)

        if len(errors) == 0:
            print(" " * 10 + "OK!")
        else:
            for error in errors:
                print(error)

        print("="*30 + "\n")


def tratamento_personalizado_erros(message, linha):
    errors.append(f"Erro semântico, linha {linha}: {message}")

if __name__ == "__main__":
    main()
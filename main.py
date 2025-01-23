from src.principal import lexer, parser, errors

RESERVED_WORDS = {"some", "all", "only", "and", "or", "not", "min", "max", "exactly", 'DISJOINT_WITH', 'EQUIVALENT_TO', 'INVERSE_OF', 'SUBCLASS_OF', 'DOMAIN', 'RANGE'}

def main():
    print("Escolha o arquivo a ser processado:")
    print("1 - data/entrada")
    print("2 - data/entrada2")
    escolha = input("Digite o número correspondente à sua escolha: ")

    if escolha == '1':
        caminho_arquivo = 'data/entrada'
    elif escolha == '2':
        caminho_arquivo = 'data/entrada2'
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
                                                errors.append(f"Erro semântico: A classe '{sub_item}' foi mencionada mas não foi declarada.")
                            else:
                                if isinstance(item, str):
                                    if item.lower() in (word.lower() for word in declared_classes) or item.lower() in (word.lower() for word in RESERVED_WORDS):
                                        continue
                                    else:
                                        errors.append(f"Erro semântico: A classe '{item}' foi mencionada mas não foi declarada.")
                    print("---")

        # Verificando classes mencionadas, mas não declaradas
        for mentioned_class in mentioned_classes:
            if mentioned_class not in declared_classes and mentioned_class not in RESERVED_WORDS:
                errors.append(f"Erro semântico: A classe '{mentioned_class}' foi mencionada mas não foi declarada.")

        print("\n" + "="*30)

        if len(errors) == 0:
            print(" " * 10 + "OK!")
        else:
            for error in errors:
                print(error)

        print("="*30 + "\n")

if __name__ == "__main__":
    main()
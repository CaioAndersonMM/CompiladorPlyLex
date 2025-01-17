from src.principal import lexer, parser, errors

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

    if resultado is not None:
        print("Árvore Sintática:")
        for classe in resultado:
            print(classe[0])
            print(classe[1])
            
            print("---")
            i = 2
            while i < len(classe):
                print(classe[i])
                i += 1
            print("")

        print("\n" + "="*30)

        if len(errors) == 0:
            print(" " * 10 + "OK!")
        else:
            for i in errors:
                print(i)

        print("="*30 + "\n")

if __name__ == "__main__":
    main()
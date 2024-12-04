import os
from rules import lexer

def main():
    arquivo_entrada = "entrada.txt"
    arquivo_saida_tokens = "saida.txt"
    arquivo_saida_resumo = "saida2.txt"
    
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: Arquivo '{arquivo_entrada}' não encontrado!")
        return
    
    with open(arquivo_entrada, "r", encoding="utf-8") as f:
        conteudo = f.read()
    
    lexer.input(conteudo)

    contador_tokens = {}
    tokens_identificados = []

    for token in lexer:
        tokens_identificados.append(token)
        if token.type not in contador_tokens:
            contador_tokens[token.type] = 0
        contador_tokens[token.type] += 1

    with open(arquivo_saida_tokens, "w", encoding="utf-8") as f:
        f.write("=== Tokens Identificados ===\n")
        for token in tokens_identificados:
            f.write(f"Token({token.type}, '{token.value}')\n")
    
    with open(arquivo_saida_resumo, "w", encoding="utf-8") as f:
        f.write("=== Resumo dos Tokens ===\n")
        f.write(f"{'Token':<20}{'Quantidade':<10}\n")
        f.write("-" * 30 + "\n")
        for token_type, count in contador_tokens.items():
            f.write(f"{token_type:<20}{count:<10}\n")
        
        atributos_interessantes = [
            "IDENTIFICADOR_CLASSE",
            "IDENTIFICADOR_PROPRIEDADE",
            "IDENTIFICADOR_INDIVIDUO",
            "CARDINALIDADE",
        ]
        
        for atributo in atributos_interessantes:
            if atributo in contador_tokens:
                valores_identificados = [
                    token.value for token in tokens_identificados if token.type == atributo
                ]
                f.write(f"\n=== {atributo} ===\n")
                f.write(f"Quantidade: {contador_tokens[atributo]}\n")
                f.write(f"Valores: {', '.join(valores_identificados)}\n")


if __name__ == "__main__":
    main()

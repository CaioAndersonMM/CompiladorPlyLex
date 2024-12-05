class TabelaSimbolos:
    def __init__(self):
        self.tabela = {}

    def adicionar(self, simbolo, tipo, linha):
        if simbolo not in self.tabela:
            self.tabela[simbolo] = {'tipo': tipo, 'linha': linha}
        else:
            print(f"Warning: Símbolo '{simbolo}' já existe na tabela.")

    def get(self, simbolo):
        return self.tabela.get(simbolo, None)

    def set(self, simbolo, tipo=None, linha=None):
        if simbolo in self.tabela:
            if tipo:
                self.tabela[simbolo]['tipo'] = tipo
            if linha:
                self.tabela[simbolo]['linha'] = linha
        else:
            print(f"Warning: Símbolo '{simbolo}' não encontrado na tabela.")

    def imprimir(self):
        for simbolo, info in self.tabela.items():
            print(f"{simbolo}: Tipo = {info['tipo']}, Linha = {info['linha']}")

    def salvar_em_arquivo(self, arquivo_saida):
        with open(arquivo_saida, "w", encoding="utf-8") as f:
            f.write("=== Tabela de Símbolos ===\n")
            for simbolo, info in self.tabela.items():
                f.write(f"{simbolo}: Tipo = {info['tipo']}, Linha = {info['linha']}\n")

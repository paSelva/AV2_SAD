import pandas as pd
import random
import numpy as np

# ======== Função de avaliação dos cromossomos ========
def calcular_fitness(grupo: pd.DataFrame) -> float:
    # Critério 1: média das notas
    notas = grupo[['NU_NOTA_MT', 'NU_NOTA_CN', 'NU_NOTA_LC', 'NU_NOTA_CH']]
    nota_media = notas.mean().mean() / 1000  # normalizado entre 0 e 1

    # Critério 2: diversidade (renda, cor/raça, escolaridade mãe, tipo escola)
    def diversidade(coluna):
        proporcoes = grupo[coluna].value_counts(normalize=True)
        return -sum(p * np.log2(p) for p in proporcoes if p > 0)

    div_q006 = diversidade('Q006')
    div_q002 = diversidade('Q002')
    div_cor = diversidade('TP_COR_RACA')
    div_escola = diversidade('TP_ESCOLA')
    diversidade_media = (div_q006 + div_q002 + div_cor + div_escola) / 4
    diversidade_media /= np.log2(10)  # normalizado

    # Critério 3: cobertura geográfica
    cobertura = grupo['SG_UF_PROVA'].nunique() / 27  # normalizado

    # Função de aptidão
    fitness = 0.5 * nota_media + 0.3 * diversidade_media + 0.2 * cobertura
    return fitness

# ======== Algoritmo Genético ========
def gerar_populacao_inicial(df, tamanho_pop=20, tamanho_grupo=100):
    return [random.sample(range(len(df)), tamanho_grupo) for _ in range(tamanho_pop)]

def selecao(populacao, df, k=5):
    selecionados = random.sample(populacao, k)
    selecionados.sort(key=lambda crom: calcular_fitness(df.iloc[crom]), reverse=True)
    return selecionados[0]

def crossover(pai1, pai2, tamanho_grupo, total_dados):
    ponto = random.randint(1, tamanho_grupo - 2)
    filho = pai1[:ponto] + [g for g in pai2 if g not in pai1[:ponto]]
    while len(filho) < tamanho_grupo:
        gene_extra = random.randint(0, total_dados - 1)
        if gene_extra not in filho:
            filho.append(gene_extra)
    return filho

def mutacao(cromossomo, total_dados, taxa=0.05):
    for i in range(len(cromossomo)):
        if random.random() < taxa:
            novo_gene = random.randint(0, total_dados - 1)
            while novo_gene in cromossomo:
                novo_gene = random.randint(0, total_dados - 1)
            cromossomo[i] = novo_gene
    return cromossomo

def algoritmo_genetico(df, tamanho_pop=20, tamanho_grupo=100, geracoes=100):
    populacao = gerar_populacao_inicial(df, tamanho_pop, tamanho_grupo)
    melhor_cromossomo = None
    melhor_fitness = -1

    for geracao in range(geracoes):
        nova_populacao = []
        for _ in range(tamanho_pop):
            pai1 = selecao(populacao, df)
            pai2 = selecao(populacao, df)
            filho = crossover(pai1, pai2, tamanho_grupo, len(df))
            filho = mutacao(filho, len(df))
            nova_populacao.append(filho)

            fit = calcular_fitness(df.iloc[filho])
            if fit > melhor_fitness:
                melhor_fitness = fit
                melhor_cromossomo = filho

        populacao = nova_populacao
        print(f"Geração {geracao + 1} | Melhor Fitness: {melhor_fitness:.4f}")

    return df.iloc[melhor_cromossomo], melhor_fitness

# ======== Execução principal ========
def main():
    ARQUIVO = "MICRODADOS_ENEM_2023.csv"
    COLUNAS = [
        "NU_INSCRICAO", "NU_NOTA_MT", "NU_NOTA_CN", "NU_NOTA_LC",
        "NU_NOTA_CH", "Q006", "Q002", "TP_COR_RACA",
        "TP_ESCOLA","SG_UF_PROVA"
    ]

    print("Lendo microdados...")
    df = pd.read_csv(ARQUIVO, sep=";", encoding="latin-1", usecols=COLUNAS)

    print("Limpando dados...")
    df.dropna(subset=["NU_NOTA_MT", "NU_NOTA_CN", "NU_NOTA_LC", "NU_NOTA_CH"], inplace=True)
    df.drop_duplicates(subset=["NU_INSCRICAO"], inplace=True)

    print("Rodando algoritmo genético...")
    melhor_grupo, fitness = algoritmo_genetico(df)

    print(f"\nMelhor grupo encontrado com fitness: {fitness:.4f}")
    melhor_grupo.to_excel("Grupo_Selecionado.xlsx", index=False)
    print("Grupo exportado para 'Grupo_Selecionado.xlsx'")

if __name__ == "__main__":
    main()

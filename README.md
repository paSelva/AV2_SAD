# AV2_SAD
TRABALHO AV2 SISTEMA DE APOIO A DECISAO

Este código implementa um algoritmo genético para selecionar um grupo de estudantes (bolsistas) a partir dos microdados do ENEM 2023, considerando três critérios principais: desempenho acadêmico, diversidade e cobertura geográfica.
Funcionamento Geral
O código utiliza técnicas de inteligência artificial (algoritmos genéticos) para encontrar a melhor combinação de estudantes que atenda a múltiplos critérios simultaneamente, otimizando:
1.	Desempenho acadêmico (média das notas)
2.	Diversidade (renda, raça/cor, escolaridade da mãe, tipo de escola)
3.	Cobertura geográfica (representação de diferentes estados)
Componentes Principais
1. Função de Avaliação (Fitness)
calcular_fitness() é a função mais importante, que avalia a qualidade de um grupo de estudantes com base em:
•	Nota média: Média das notas em Matemática, Ciências da Natureza, Linguagens e Códigos, e Ciências Humanas (50% do score)
•	Diversidade: Calculada usando entropia de Shannon para renda (Q006), raça/cor (TP_COR_RACA), escolaridade da mãe (Q002) e tipo de escola (TP_ESCOLA) (30% do score)
•	Cobertura geográfica: Proporção de estados representados no grupo (20% do score)
2. Algoritmo Genético
O algoritmo simula um processo evolutivo com:
•	População inicial: Grupos aleatórios de estudantes
•	Seleção: Escolhe os melhores grupos baseado no fitness
•	Crossover: Combina partes de dois grupos pais para formar filhos
•	Mutação: Introduz pequenas alterações aleatórias para manter diversidade
•	Iterações: Melhora progressivamente a qualidade dos grupos ao longo de gerações
3. Fluxo Principal
1.	Lê e limpa os dados do ENEM 2023
2.	Executa o algoritmo genético
3.	Exporta o melhor grupo encontrado para um arquivo Excel
Por que usar Algoritmo Genético?
Esta abordagem é ideal porque:
•	Permite otimizar múltiplos critérios simultaneamente
•	Lida bem com espaços de busca grandes (muitos candidatos)
•	Encontra soluções balanceadas entre os diferentes objetivos
•	É flexível para ajustar pesos dos critérios conforme necessidade
Saída
O resultado final é um grupo de estudantes que representa um equilíbrio entre excelência acadêmica, diversidade sociodemográfica e representatividade geográfica, exportado para análise em "Grupo_Selecionado.xlsx".

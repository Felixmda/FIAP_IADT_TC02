# Planejamento Financeiro Familiar com Algoritmos Genéticos

## Descrição do Problema

O objetivo deste projeto é utilizar algoritmos genéticos para prever o melhor cenário de planejamento financeiro familiar. Considerando diferentes fontes de renda (salário fixo, rendimentos de investimentos e outras receitas) e classificando os gastos em essenciais e não essenciais, o algoritmo visa maximizar a reserva financeira ao longo de um período definido. A meta é garantir que os gastos não excedam a renda mensal e que a reserva financeira seja composta por investimentos em renda fixa, renda variável e tesouro, respeitando limites definidos pelo usuário.

## Objetivos
Garantir que os gastos essenciais estejam dentro de um intervalo específico.
Garantir que os gastos não essenciais estejam dentro de um intervalo específico.
Maximizar a reserva financeira total após um período definido, considerando possíveis emergências financeiras.
Garantir que a soma dos percentuais dos limites para gastos essenciais, não essenciais e reserva não ultrapasse 100%.

## Estrutura do Projeto

`financial_plan.py`

Este arquivo contém a implementação do algoritmo genético e as funções auxiliares necessárias.

`config.ini`

Este arquivo permite ao usuário definir os parâmetros financeiros e os parâmetros do algoritmo genético.

```ini
[finance]
salario_fixo = 6500
rendimentos_investimentos = 450
outras_receitas = 500
meta_reserva = 30000
num_meses = 12
min_gastos_essenciais = 30
max_gastos_essenciais = 50
min_gastos_nao_essenciais = 10
max_gastos_nao_essenciais = 20
max_reserva = 30

[genetic_algorithm]
population_size = 100
ngen = 50
mutation_rate = 0.1
crossover_rate = 0.5
```

#### Parâmetros do Arquivo de Configuração

 - finance
   - salario_fixo: Salário fixo mensal.
   - rendimentos_investimentos: Rendimentos de investimentos mensais.
   - outras_receitas: Outras receitas mensais.
   - meta_reserva: Meta de reserva financeira a ser alcançada.
   - num_meses: Número de meses para o planejamento.
   - min_gastos_essenciais: Percentual mínimo da renda destinado a gastos essenciais.
   - max_gastos_essenciais: Percentual máximo da renda destinado a gastos essenciais.
   - min_gastos_nao_essenciais: Percentual mínimo da renda destinado a gastos não essenciais.
   - max_gastos_nao_essenciais: Percentual máximo da renda destinado a gastos não essenciais.
   - max_reserva: Percentual máximo da renda destinado à reserva financeira.

- genetic_algorithm
   - population_size: Tamanho da população.
   - ngen: Número de gerações.
   - mutation_rate: Taxa de mutação.
   - crossover_rate: Taxa de crossover.

## Execução do Código

Ajuste os valores no arquivo de configuração `config.ini` e execute o script abaixo

> python financial_plan.py

### Resultado Esperado

Ao final da execução do algoritmo genético, o melhor plano financeiro será exibido, mostrando a distribuição mensal dos gastos essenciais, gastos não essenciais e investimentos em renda fixa, renda variável e tesouro. Além disso, será exibida a reserva financeira total após o período planejado.

Exemplo de Saída:
```plaintext
Mês 1:
  Gastos Essenciais: R$ 2600.00
  Gastos Não Essenciais: R$ 1300.00
  Investimento em Renda Fixa: R$ 600.00
  Investimento em Renda Variável: R$ 700.00
  Investimento em Tesouro: R$ 750.00
...
Total de Reserva após 12 meses: R$ 35000.00
```

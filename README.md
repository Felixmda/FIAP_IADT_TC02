# Problema de Planejamento Financeiro Familiar

## Problema a ser Resolvido

O objetivo é utilizar algoritmos genéticos para otimizar o planejamento financeiro familiar ao longo de 12 meses. Isso inclui distribuir a renda mensal entre gastos essenciais, gastos não essenciais e investimentos em diferentes tipos de reserva financeira (renda fixa, renda variável e tesouro), de modo a atingir uma meta anual de reserva financeira. Além disso, deve-se simular emergências financeiras ao longo do ano que possam consumir parte da reserva, garantindo que a reserva seja suficiente para cobrir essas emergências.

## Variáveis

1. **Renda Mensal Total**:
   - Composta por:
     - Salário fixo
     - Rendimentos de investimentos
     - Outras receitas

2. **Gastos**:
   - **Gastos Essenciais**: Incluem despesas como saúde e alimentação.
   - **Gastos Não Essenciais**: Incluem despesas como serviços de streaming e passeios.

3. **Reserva Financeira**:
   - Dividida em:
     - **Renda Fixa**: Investimento com baixo risco e retorno moderado.
     - **Renda Variável**: Investimento com maior risco e potencial de retorno mais alto.
     - **Tesouro**: Investimento com risco moderado e retorno garantido.

4. **Meta Anual de Reserva Financeira**:
   - Quantidade mínima desejada de reserva financeira a ser acumulada ao longo dos 12 meses.

## Regras

- A soma dos percentuais de gastos essenciais, gastos não essenciais e reserva financeira não pode exceder 100% da renda total.
- Os percentuais de gastos essenciais devem estar entre 30% e 50% da renda total.
- Os percentuais de gastos não essenciais devem estar entre 0% e 20% da renda total.
- O percentual restante deve ser alocado para a reserva financeira, que deve estar entre 30% e 70% da renda total.
- Durante o planejamento, a reserva deve ser ajustada para cobrir possíveis emergências financeiras, simuladas consumindo uma parte da reserva em determinados meses.

## Formato Esperado de Resultado

O resultado do planejamento será uma lista de 12 meses, cada um contendo:

- Gastos Essenciais
- Gastos Não Essenciais
- Montantes a serem investidos em:
  - Renda Fixa
  - Renda Variável
  - Tesouro

Além disso, será exibido o valor total da reserva financeira ao final dos 12 meses, após a consideração de possíveis emergências.

Exemplo de resultado esperado:

```
Mês 1:
Gastos Essenciais: 2000.00
Gastos Não Essenciais: 500.00
Renda Fixa: 1000.00
Renda Variável: 1500.00
Tesouro: 500.00

...

Valor Total da Reserva Financeira: 12000.00
```
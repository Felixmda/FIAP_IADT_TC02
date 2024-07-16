import random

# Parâmetros do problema
Renda_Mensal = {
    'salario_fixo': 5000,
    'rendimentos_investimentos': 500,
    'outras_receitas': 200
}
renda_total = sum(Renda_Mensal.values())

# Meta de reserva financeira
meta_reserva = 10000

# Número de meses
num_meses = 12

# Fatores de risco dos investimentos (desvio padrão)
risco_renda_fixa = 0.01
risco_renda_variavel = 0.05
risco_tesouro = 0.02

# Função para gerar um mês de planejamento
def generate_month():
    while True:
        gastos_essenciais = random.uniform(0.3, 0.5) * renda_total
        gastos_nao_essenciais = random.uniform(0, 0.2) * renda_total
        reserva = renda_total - (gastos_essenciais + gastos_nao_essenciais)
        
        if 0.3 * renda_total <= reserva <= 0.7 * renda_total:
            break
    
    # Distribuir a reserva entre os tipos de investimento
    renda_fixa = random.uniform(0, reserva)
    reserva -= renda_fixa
    renda_variavel = random.uniform(0, reserva)
    tesouro = reserva - renda_variavel
    return [gastos_essenciais, gastos_nao_essenciais, renda_fixa, renda_variavel, tesouro]

# Função para gerar um planejamento de 12 meses
def generate_individual():
    return [generate_month() for _ in range(num_meses)]

# Função para gerar a população inicial
def generate_population(size):
    return [generate_individual() for _ in range(size)]

# Função de mutação
def mutate(individual, mutation_rate=0.1):
    for mes in individual:
        if random.random() < mutation_rate:
            mes[0] = random.uniform(0.3, 0.5) * renda_total
        if random.random() < mutation_rate:
            mes[1] = random.uniform(0, 0.2) * renda_total
        if random.random() < mutation_rate:
            reserva = renda_total - (mes[0] + mes[1])
            mes[2] = random.uniform(0, reserva)
            reserva -= mes[2]
            mes[3] = random.uniform(0, reserva)
            mes[4] = reserva - mes[3]
    return individual

# Função de crossover (crossover de um ponto)
def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

# Função de seleção (torneio)
def select(population, k=3):
    selected = random.sample(population, k)
    selected.sort(key=lambda ind: eval_plano(ind))
    return selected[0]

# Função de avaliação
def eval_plano(plano):
    total_gastos_essenciais = 0
    total_gastos_nao_essenciais = 0
    total_reserva_fixa = 0
    total_reserva_variavel = 0
    total_reserva_tesouro = 0
    
    for mes in plano:
        gastos_essenciais, gastos_nao_essenciais, renda_fixa, renda_variavel, tesouro = mes
        
        # Calcular os gastos totais
        gastos_totais = gastos_essenciais + gastos_nao_essenciais
        
        # Aplicar fator de risco
        renda_fixa *= (1 + random.gauss(0, risco_renda_fixa))
        renda_variavel *= (1 + random.gauss(0, risco_renda_variavel))
        tesouro *= (1 + random.gauss(0, risco_tesouro))
        
        # Calcular a reserva total
        reserva_total = renda_fixa + renda_variavel + tesouro
        
        # Penalizar se os gastos essenciais não estiverem entre 30-50% da renda
        if not (0.3 * renda_total <= gastos_essenciais <= 0.5 * renda_total):
            return float('inf')  # Penalidade alta
        
        # Penalizar se os gastos não essenciais não estiverem entre 0-20% da renda
        if not (0 <= gastos_nao_essenciais <= 0.2 * renda_total):
            return float('inf')  # Penalidade alta
        
        # Penalizar se a reserva não estiver entre 30-70% da renda
        if not (0.3 * renda_total <= reserva_total <= 0.7 * renda_total):
            return float('inf')  # Penalidade alta
        
        # Penalizar se os gastos totais excederem a renda
        if gastos_totais + reserva_total > renda_total:
            return float('inf')  # Penalidade alta
        
        total_gastos_essenciais += gastos_essenciais
        total_gastos_nao_essenciais += gastos_nao_essenciais
        total_reserva_fixa += renda_fixa
        total_reserva_variavel += renda_variavel
        total_reserva_tesouro += tesouro
    
    # Simulação de emergências
    total_reserva = total_reserva_fixa + total_reserva_variavel + total_reserva_tesouro
    for _ in range(random.randint(1, 3)):  # 1 a 3 emergências por ano
        emergencia = random.uniform(0.1, 0.3) * renda_total  # Emergência consome entre 10-30% da renda total
        if emergencia > total_reserva:
            return float('inf')  # Penalidade alta se a reserva não for suficiente
        total_reserva -= emergencia
    
    # Penalizar se a reserva total não atingir a meta
    if total_reserva < meta_reserva:
        return float('inf')  # Penalidade alta
    
    # Objetivo é maximizar a reserva total após emergências
    return -total_reserva

# Parâmetros do algoritmo genético
population_size = 100
ngen = 50
mutation_rate = 0.1
crossover_rate = 0.5

# Gerar população inicial
population = generate_population(population_size)

# Algoritmo genético
for gen in range(ngen):
    new_population = []
    for _ in range(population_size // 2):
        # Seleção
        parent1 = select(population)
        parent2 = select(population)
        
        # Crossover
        if random.random() < crossover_rate:
            child1, child2 = crossover(parent1, parent2)
        else:
            child1, child2 = parent1, parent2
        
        # Mutação
        child1 = mutate(child1, mutation_rate)
        child2 = mutate(child2, mutation_rate)
        
        new_population.extend([child1, child2])
    
    # Substituir a população antiga pela nova
    population = new_population

# Encontrar o melhor indivíduo
best_ind = min(population, key=lambda ind: eval_plano(ind))

# Exibir os resultados
for i, mes in enumerate(best_ind, 1):
    print(f"Mês {i}:")
    print(f"  Gastos Essenciais: {mes[0]:.2f}")
    print(f"  Gastos Não Essenciais: {mes[1]:.2f}")
    print(f"  Renda Fixa: {mes[2]:.2f}")
    print(f"  Renda Variável: {mes[3]:.2f}")
    print(f"  Tesouro: {mes[4]:.2f}")

print(f"Valor Total: {-eval_plano(best_ind)}")

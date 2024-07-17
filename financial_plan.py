import random
import logging
import configparser

# Configuração do logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    
    salario_fixo = config.getfloat('finance', 'salario_fixo')
    rendimentos_investimentos = config.getfloat('finance', 'rendimentos_investimentos')
    outras_receitas = config.getfloat('finance', 'outras_receitas')
    meta_reserva = config.getfloat('finance', 'meta_reserva')
    num_meses = config.getint('finance', 'num_meses')
    min_gastos_essenciais = config.getfloat('finance', 'min_gastos_essenciais') / 100
    max_gastos_essenciais = config.getfloat('finance', 'max_gastos_essenciais') / 100
    min_gastos_nao_essenciais = config.getfloat('finance', 'min_gastos_nao_essenciais') / 100
    max_gastos_nao_essenciais = config.getfloat('finance', 'max_gastos_nao_essenciais') / 100
    max_reserva = config.getfloat('finance', 'max_reserva') / 100

    if max_gastos_essenciais + max_gastos_nao_essenciais + max_reserva > 1.0:
        raise ValueError("A soma dos percentuais dos limites não pode ultrapassar 100%")

    population_size = config.getint('genetic_algorithm', 'population_size')
    ngen = config.getint('genetic_algorithm', 'ngen')
    mutation_rate = config.getfloat('genetic_algorithm', 'mutation_rate')
    crossover_rate = config.getfloat('genetic_algorithm', 'crossover_rate')
    
    Renda_Mensal = {
        'salario_fixo': salario_fixo,
        'rendimentos_investimentos': rendimentos_investimentos,
        'outras_receitas': outras_receitas
    }
    renda_total = sum(Renda_Mensal.values())
    
    return (Renda_Mensal, renda_total, meta_reserva, num_meses, 
            min_gastos_essenciais, max_gastos_essenciais, 
            min_gastos_nao_essenciais, max_gastos_nao_essenciais, 
            max_reserva, population_size, ngen, mutation_rate, crossover_rate)

def generate_month(renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva):
    gastos_essenciais = random.uniform(min_gastos_essenciais, max_gastos_essenciais) * renda_total
    gastos_nao_essenciais = random.uniform(min_gastos_nao_essenciais, max_gastos_nao_essenciais) * renda_total
    reserva = renda_total - (gastos_essenciais + gastos_nao_essenciais)
    
    # Ajustar a reserva para garantir que não exceda o limite máximo
    if reserva > max_reserva * renda_total:
        reserva = max_reserva * renda_total

    # Distribuir a reserva entre os tipos de investimento
    renda_fixa = random.uniform(0, reserva)
    reserva -= renda_fixa
    renda_variavel = random.uniform(0, reserva)
    tesouro = reserva - renda_variavel
    return [gastos_essenciais, gastos_nao_essenciais, renda_fixa, renda_variavel, tesouro]

def generate_individual(num_meses, renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva):
    return [generate_month(renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva) for _ in range(num_meses)]

def generate_population(size, num_meses, renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva):
    return [generate_individual(num_meses, renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva) for _ in range(size)]

def mutate(individual, renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva, mutation_rate=0.1):
    for mes in individual:
        if random.random() < mutation_rate:
            mes[0] = random.uniform(min_gastos_essenciais, max_gastos_essenciais) * renda_total
        if random.random() < mutation_rate:
            mes[1] = random.uniform(min_gastos_nao_essenciais, max_gastos_nao_essenciais) * renda_total
        if random.random() < mutation_rate:
            reserva = renda_total - (mes[0] + mes[1])
            mes[2] = random.uniform(0, reserva)
            reserva -= mes[2]
            mes[3] = random.uniform(0, reserva)
            mes[4] = reserva - mes[3]
    return individual

def crossover(parent1, parent2):
    point = random.randint(1, len(parent1) - 1)
    child1 = parent1[:point] + parent2[point:]
    child2 = parent2[:point] + parent1[point:]
    return child1, child2

def select(population, eval_fn, k=3):
    selected = random.sample(population, k)
    selected.sort(key=eval_fn)
    return selected[0]

def eval_plano(plano, renda_total, risco_renda_fixa, risco_renda_variavel, risco_tesouro, meta_reserva, 
               min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva):
    total_reserva = 0
    
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
        
        # Penalizar se os gastos essenciais estiverem fora dos limites
        if gastos_essenciais < min_gastos_essenciais * renda_total or gastos_essenciais > max_gastos_essenciais * renda_total:
            return float('inf')  # Penalidade alta
        
        # Penalizar se os gastos não essenciais estiverem fora dos limites
        if gastos_nao_essenciais < min_gastos_nao_essenciais * renda_total or gastos_nao_essenciais > max_gastos_nao_essenciais * renda_total:
            return float('inf')  # Penalidade alta
        
        # Penalizar se a reserva exceder o limite
        if reserva_total > max_reserva * renda_total:
            return float('inf')  # Penalidade alta
        
        # Penalizar se os gastos totais excederem a renda
        if gastos_totais > renda_total:
            return float('inf')  # Penalidade alta
        
        total_reserva += reserva_total
    
    # Simulação de emergências
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

def genetic_algorithm(population_size, ngen, mutation_rate, crossover_rate, 
                      renda_total, num_meses, risco_renda_fixa, risco_renda_variavel, risco_tesouro, meta_reserva, 
                      min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva):
    population = generate_population(population_size, num_meses, renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva)
    logging.info('População inicial gerada')
    
    for gen in range(ngen):
        new_population = []
        for _ in range(population_size // 2):
            parent1 = select(population, lambda ind: eval_plano(ind, renda_total, risco_renda_fixa, risco_renda_variavel, risco_tesouro, meta_reserva, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva))
            parent2 = select(population, lambda ind: eval_plano(ind, renda_total, risco_renda_fixa, risco_renda_variavel, risco_tesouro, meta_reserva, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva))
            
            if random.random() < crossover_rate:
                child1, child2 = crossover(parent1, parent2)
            else:
                child1, child2 = parent1, parent2
            
            child1 = mutate(child1, renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva, mutation_rate)
            child2 = mutate(child2, renda_total, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva, mutation_rate)
            
            new_population.extend([child1, child2])
        
        population = new_population
        # logging.info(f'Geração {gen + 1} completada')

    best_ind = min(population, key=lambda ind: eval_plano(ind, renda_total, risco_renda_fixa, risco_renda_variavel, risco_tesouro, meta_reserva, min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva))
    logging.info('Algoritmo genético completado')

    total_reserva = 0
    for i, mes in enumerate(best_ind, 1):
        gastos_essenciais, gastos_nao_essenciais, renda_fixa, renda_variavel, tesouro = mes
        print(f"Mês {i}:")
        print(f"  Gastos Essenciais: R$ {gastos_essenciais:.2f}")
        print(f"  Gastos Não Essenciais: R$ {gastos_nao_essenciais:.2f}")
        print(f"  Investimento em Renda Fixa: R$ {renda_fixa:.2f}")
        print(f"  Investimento em Renda Variável: R$ {renda_variavel:.2f}")
        print(f"  Investimento em Tesouro: R$ {tesouro:.2f}")
        total_reserva += renda_fixa + renda_variavel + tesouro

    print(f"\nTotal de Reserva após {num_meses} meses: R$ {total_reserva:.2f}")

# Parâmetros fixos do risco
risco_renda_fixa = 0.01
risco_renda_variavel = 0.1
risco_tesouro = 0.05

# Obter dados do arquivo de configuração
config_file_path = 'config.ini'
(Renda_Mensal, renda_total, meta_reserva, num_meses, 
 min_gastos_essenciais, max_gastos_essenciais, 
 min_gastos_nao_essenciais, max_gastos_nao_essenciais, 
 max_reserva, population_size, ngen, mutation_rate, crossover_rate) = read_config(config_file_path)

# Executar o algoritmo genético
genetic_algorithm(population_size, ngen, mutation_rate, crossover_rate, 
                  renda_total, num_meses, risco_renda_fixa, risco_renda_variavel, risco_tesouro, meta_reserva, 
                  min_gastos_essenciais, max_gastos_essenciais, min_gastos_nao_essenciais, max_gastos_nao_essenciais, max_reserva)

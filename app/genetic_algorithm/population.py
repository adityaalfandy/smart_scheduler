from app.genetic_algorithm.chromosome import Chromosome
from app.genetic_algorithm.fitness import FitnessCalculator
from app.genetic_algorithm.selection import TournamentSelection
from app.genetic_algorithm.crossover import Crossover
from app.genetic_algorithm.mutation import Mutation

class Population:
    def __init__(self, mata_kuliah_list, dosen_list, ruangan_list, preferensi_dict, population_size=50):
        self.mata_kuliah_list = mata_kuliah_list
        self.dosen_list = dosen_list
        self.ruangan_list = ruangan_list
        self.population_size = population_size
        self.chromosomes = []
        
        # Setup Dictionaries
        self.mata_kuliah_dict = {mk.id: mk for mk in mata_kuliah_list}
        self.dosen_dict = {d.id: d for d in dosen_list}
        self.ruangan_dict = {r.id: r for r in ruangan_list}
        
        # Inisialisasi Helper
        self.fitness_calculator = FitnessCalculator(
            self.mata_kuliah_dict, self.dosen_dict, 
            self.ruangan_dict, preferensi_dict
        )
        self.selector = TournamentSelection(tournament_size=4)
        self.mutation = Mutation(dosen_list, ruangan_list)
    
    def initialize(self):
        self.chromosomes = []
        for _ in range(self.population_size):
            chromosome = Chromosome.create_random(
                self.mata_kuliah_list, self.dosen_list, self.ruangan_list
            )
            self.chromosomes.append(chromosome)
        self.evaluate_fitness()
    
    def evaluate_fitness(self):
        for chromosome in self.chromosomes:
            # Panggil calculate, abaikan return value-nya dulu, ambil dari atribut nanti
            score = self.fitness_calculator.calculate(chromosome)
            chromosome.fitness = score
    
    def run_genetic_algorithm(self, max_generations=100, mutation_rate=0.1):
        self.initialize()
        best_sol = None
        
        for generation in range(max_generations):
            # Elitism: Sort berdasarkan fitness tertinggi
            sorted_pop = sorted(self.chromosomes, key=lambda x: x.fitness, reverse=True)
            best_sol = sorted_pop[0]
            
            # Print progress di console (untuk debug)
            if generation % 10 == 0:
                print(f"Gen {generation}: Best Fitness = {best_sol.fitness}")

            new_population = sorted_pop[:2] # Elitism (Ambil 2 terbaik)
            
            while len(new_population) < self.population_size:
                p1 = self.selector.select(self.chromosomes)
                p2 = self.selector.select(self.chromosomes)
                
                c1, c2 = Crossover.two_point_crossover(p1, p2)
                
                c1 = self.mutation.mutate(c1, mutation_rate)
                c2 = self.mutation.mutate(c2, mutation_rate)
                
                new_population.extend([c1, c2])
            
            self.chromosomes = new_population[:self.population_size]
            self.evaluate_fitness()
            
        # --- BAGIAN PENTING: RETURN 4 VALUE ---
        # Hitung ulang fitness untuk solusi terbaik agar kita dapat detail logs-nya
        best_sol.fitness = self.fitness_calculator.calculate(best_sol)
        
        # Ambil logs dari atribut fitness_details yang diisi oleh fitness.py
        final_logs = getattr(best_sol, 'fitness_details', [])
        
        # Hitung jumlah konflik (log yang mengandung kata BENTROK/KAPASITAS/SALAH)
        # Atau sesuaikan dengan logic di fitness.py Anda
        final_conflicts = len(final_logs) 
        
        return best_sol, best_sol.fitness, final_conflicts, final_logs
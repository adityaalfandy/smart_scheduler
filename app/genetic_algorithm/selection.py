import random

class TournamentSelection:
    """Tournament Selection untuk memilih parent"""
    
    def __init__(self, tournament_size=3):
        self.tournament_size = tournament_size
    
    def select(self, population):
        """Pilih satu parent menggunakan tournament selection"""
        tournament = random.sample(population, min(self.tournament_size, len(population)))
        tournament.sort(key=lambda x: x.fitness, reverse=True)
        return tournament[0]
    
    def select_parents(self, population, num_parents):
        """Pilih beberapa parent"""
        parents = []
        for _ in range(num_parents):
            parent = self.select(population)
            parents.append(parent)
        return parents
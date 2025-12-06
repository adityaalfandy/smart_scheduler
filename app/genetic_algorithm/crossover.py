import random
from app.genetic_algorithm.chromosome import Chromosome, Gene

class Crossover:
    """Crossover operator"""
    
    @staticmethod
    def two_point_crossover(parent1, parent2):
        size = len(parent1.genes)
        
        if size < 2:
            return parent1.copy(), parent2.copy()
        
        point1 = random.randint(0, size - 1)
        point2 = random.randint(point1, size - 1)
        
        child1_genes = []
        child2_genes = []
        
        for i in range(size):
            g1_src = parent1.genes[i]
            g2_src = parent2.genes[i]

            # Tentukan sumber gen (Swap atau Tetap)
            if point1 <= i <= point2:
                # Swap: Child 1 dapat dari Parent 2
                source_for_c1 = g2_src
                source_for_c2 = g1_src
            else:
                # Tetap: Child 1 dapat dari Parent 1
                source_for_c1 = g1_src
                source_for_c2 = g2_src
            
            # Buat Gene Baru (PENTING: Pakai struktur slot)
            c1_gene = Gene(source_for_c1.matkul_id, source_for_c1.dosen_id, source_for_c1.ruangan_id,
                           source_for_c1.time_slot, source_for_c1.sks, source_for_c1.semester, source_for_c1.jenis)
            
            c2_gene = Gene(source_for_c2.matkul_id, source_for_c2.dosen_id, source_for_c2.ruangan_id,
                           source_for_c2.time_slot, source_for_c2.sks, source_for_c2.semester, source_for_c2.jenis)
            
            child1_genes.append(c1_gene)
            child2_genes.append(c2_gene)
        
        return Chromosome(child1_genes), Chromosome(child2_genes)
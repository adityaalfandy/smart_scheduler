import random
from typing import List

class Gene:
    """Representasi satu jadwal mata kuliah (Versi Slot ID)"""
    def __init__(self, matkul_id: int, dosen_id: int, ruangan_id: int, 
                 time_slot: int, sks: int, semester: int, jenis: str):
        self.matkul_id = matkul_id
        self.dosen_id = dosen_id
        self.ruangan_id = ruangan_id
        self.time_slot = time_slot # Slot 1-40
        self.sks = sks
        self.semester = semester
        self.jenis = jenis

    def __repr__(self):
        return f"Gene(M:{self.matkul_id}, D:{self.dosen_id}, T:{self.time_slot})"

class Chromosome:
    """Representasi satu solusi jadwal lengkap"""
    def __init__(self, genes: List[Gene] = None):
        self.genes = genes if genes else []
        self.fitness = 0
        self.fitness_details = []
    
    # --- PENTING UNTUK CROSSOVER ---
    def __len__(self):
        return len(self.genes)
    
    def __getitem__(self, index):
        return self.genes[index]
    
    def __setitem__(self, index, value):
        self.genes[index] = value
    # -------------------------------

    def copy(self):
        """Deep copy kromosom"""
        new_genes = []
        for g in self.genes:
            # Copy semua atribut Gene dengan benar
            new_gene = Gene(g.matkul_id, g.dosen_id, g.ruangan_id, 
                          g.time_slot, g.sks, g.semester, g.jenis)
            new_genes.append(new_gene)
        return Chromosome(new_genes)
    
    @staticmethod
    def create_random(mata_kuliah_list, dosen_list, ruangan_list):
        """Buat kromosom random"""
        genes = []
        time_slots = list(range(1, 41)) # Slot 1-40
        
        for mk in mata_kuliah_list:
            # 1. Pastikan Dosen sesuai Data (Jangan diacak)
            if hasattr(mk, 'dosen_obj'):
                final_dosen_id = mk.dosen_obj.id
            else:
                final_dosen_id = random.choice(dosen_list).id
            
            # 2. Acak Ruangan & Waktu
            ruangan = random.choice(ruangan_list)
            slot = random.choice(time_slots)
            
            # 3. Buat Gene dengan struktur lengkap
            gene = Gene(mk.id, final_dosen_id, ruangan.id, slot, mk.sks, mk.semester, mk.jenis)
            genes.append(gene)
        
        return Chromosome(genes)
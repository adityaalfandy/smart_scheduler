"""import random
import copy
import pandas as pd

class GeneticScheduler:
    def __init__(self, courses_df, rooms_df, population_size=100, mutation_rate=0.2, elitism_size=5):
        self.courses = courses_df.to_dict('records')
        self.rooms = rooms_df.to_dict('records')
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.elitism_size = elitism_size
        self.time_slots = list(range(1, 41)) 

    def create_individual(self):
        individual = []
        for course in self.courses:
            gene = course.copy()
            gene['assigned_time'] = random.choice(self.time_slots)
            gene['assigned_room'] = random.choice(self.rooms)
            individual.append(gene)
        return individual

    def calculate_fitness(self, individual):
        score = 2500
        conflicts = 0
        error_logs = [] # List untuk menyimpan detail error
        
        lecturer_schedule = {} 
        room_usage = {} 

        for gene in individual:
            lecturer = gene['Dosen']
            time = gene['assigned_time']
            room_name = gene['assigned_room']['Nama']
            matkul_name = gene['Nama_MK']
            
            # 1. Cek Bentrok Dosen
            if lecturer not in lecturer_schedule: lecturer_schedule[lecturer] = []
            if time in lecturer_schedule[lecturer]:
                score -= 50; conflicts += 1
                error_logs.append(f"DOSEN: {lecturer} mengajar 2 kelas di Slot {time}.")
            else: lecturer_schedule[lecturer].append(time)

            # 2. Cek Bentrok Ruangan
            key = (room_name, time)
            if key in room_usage:
                score -= 100; conflicts += 1
                error_logs.append(f"RUANGAN: {room_name} dipakai ganda di Slot {time}.")
            else: room_usage[key] = True

            # 3. Cek Kapasitas
            mhs = int(gene.get('Jumlah_Mhs', 40))
            cap = int(gene['assigned_room']['Kapasitas'])
            if mhs > cap:
                score -= 50; conflicts += 1
                error_logs.append(f"KAPASITAS: {matkul_name} ({mhs} Mhs) tidak muat di {room_name} (Kap: {cap}).")

            # 4. Cek Jenis Ruangan
            mk_type = gene.get('Jenis_MK', 'Teori')
            room_type = gene['assigned_room']['Jenis']
            if mk_type == 'Laboratorium' and room_type != 'Laboratorium':
                 score -= 50; conflicts += 1
                 error_logs.append(f"SALAH RUANG: Praktikum {matkul_name} harus di Lab, bukan di {room_name}.")
            elif mk_type == 'Teori' and room_type == 'Laboratorium':
                 score -= 10; 

            # 5. Cek Ketersediaan Waktu Dosen
            try:
                raw_avail = str(gene.get('Waktu_Tersedia', ''))
                if raw_avail and raw_avail.lower() != 'nan':
                    available_slots = raw_avail.split(';')
                    if str(time) not in available_slots:
                        score -= 200; conflicts += 1
                        error_logs.append(f"WAKTU TIDAK BISA: {lecturer} tidak bisa di Slot {time}.")
            except: pass

        return max(score, 0), conflicts, error_logs

    def initialize_population(self):
        return [self.create_individual() for _ in range(self.pop_size)]

    def selection(self, population):
        best = None
        for _ in range(4):
            ind = random.choice(population)
            # calculate_fitness return (score, conflicts, logs), ambil index 0 (score)
            if best is None or self.calculate_fitness(ind)[0] > self.calculate_fitness(best)[0]:
                best = ind
        return best

    def crossover(self, parent1, parent2):
        if random.random() > 0.8: return parent1, parent2
        point = random.randint(1, len(parent1) - 2)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

    def mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.mutation_rate:
                if random.random() < 0.5: individual[i]['assigned_time'] = random.choice(self.time_slots)
                else: individual[i]['assigned_room'] = random.choice(self.rooms)
        return individual

    def run(self, generations=100):
        population = self.initialize_population()
        best_sol, best_fit = None, -1

        for gen in range(generations):
            scored_pop = []
            for ind in population:
                score, conf, _ = self.calculate_fitness(ind) # _ untuk ignore logs saat training
                scored_pop.append((ind, score))
            
            scored_pop.sort(key=lambda x: x[1], reverse=True)

            if scored_pop[0][1] > best_fit:
                best_fit = scored_pop[0][1]
                best_sol = scored_pop[0][0]

            new_pop = [x[0] for x in scored_pop[:self.elitism_size]]
            while len(new_pop) < self.pop_size:
                p1 = self.selection(population)
                p2 = self.selection(population)
                c1, c2 = self.crossover(p1, p2)
                new_pop.append(self.mutate(c1))
                if len(new_pop) < self.pop_size: new_pop.append(self.mutate(c2))
            population = new_pop
        
        # Hitung logs final untuk solusi terbaik
        final_score, final_conflicts, final_logs = self.calculate_fitness(best_sol)
        
        # RETURN 4 VALUE
        return best_sol, final_score, final_conflicts, final_logs """
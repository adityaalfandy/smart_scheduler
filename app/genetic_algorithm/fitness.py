class FitnessCalculator:
    # PERBAIKAN DI SINI: Tambahkan parameter 'preferensi_dict'
    def __init__(self, mata_kuliah_dict, dosen_dict, ruangan_dict, preferensi_dict=None):
        self.mata_kuliah_dict = mata_kuliah_dict
        self.dosen_dict = dosen_dict
        self.ruangan_dict = ruangan_dict
        self.preferensi_dict = preferensi_dict if preferensi_dict else {} # Default kosong jika None
    
    def calculate(self, chromosome):
        score = 2000 # Score awal
        details = [] # Log error untuk ditampilkan di web
        
        # Helper structures
        lecturer_slots = {} 
        room_slots = {}
        lecturer_sks_load = {} 

        # 1. LOOP UTAMA: Cek Per Gen
        for i, gene in enumerate(chromosome.genes):
            
            # --- CEK 1: Bentrok Dosen ---
            if gene.dosen_id not in lecturer_slots: lecturer_slots[gene.dosen_id] = []
            if gene.time_slot in lecturer_slots[gene.dosen_id]:
                score -= 50
                # Ambil nama dosen dari dict
                nama_dosen = self.dosen_dict[gene.dosen_id].nama
                details.append(f"🔴 DOSEN BENTROK: {nama_dosen} di Slot {gene.time_slot}")
            else:
                lecturer_slots[gene.dosen_id].append(gene.time_slot)

            # --- CEK 2: Bentrok Ruangan ---
            key = (gene.ruangan_id, gene.time_slot)
            if key in room_slots:
                score -= 50
                nama_ruang = self.ruangan_dict[gene.ruangan_id].nama
                details.append(f"🔴 RUANGAN BENTROK: {nama_ruang} di Slot {gene.time_slot}")
            else:
                room_slots[key] = True

            # --- CEK 3: Kapasitas & Fasilitas ---
            ruangan = self.ruangan_dict[gene.ruangan_id]
            matkul = self.mata_kuliah_dict[gene.matkul_id]
            
            if matkul.jumlah_mhs > ruangan.kapasitas:
                score -= 20
                details.append(f"⚠️ KAPASITAS: {matkul.nama} ({matkul.jumlah_mhs}) tdk muat di {ruangan.nama} ({ruangan.kapasitas})")
            
            # Smart Check: Lab vs Teori
            if matkul.jenis == 'Laboratorium' and ruangan.jenis != 'Laboratorium':
                score -= 50
                details.append(f"⚠️ SALAH RUANG: Praktikum {matkul.nama} harus di Lab")

            # --- CEK 4: Kelas Paralel (Semester Sama jangan bentrok) ---
            for other_gene in chromosome.genes:
                if gene != other_gene and gene.time_slot == other_gene.time_slot:
                    if gene.semester == other_gene.semester:
                        score -= 10 

            # --- Hitung Beban SKS ---
            if gene.dosen_id not in lecturer_sks_load: lecturer_sks_load[gene.dosen_id] = 0
            lecturer_sks_load[gene.dosen_id] += gene.sks

        # 2. LOOP KEDUA: Cek Beban Dosen
        for dosen_id, total_sks in lecturer_sks_load.items():
            dosen_nama = self.dosen_dict[dosen_id].nama
            if total_sks < 12:
                penalti = (12 - total_sks) * 5
                score -= penalti
                details.append(f"📉 KURANG SKS: {dosen_nama} cuma {total_sks} SKS (Min 12)")
            elif total_sks > 16:
                penalti = (total_sks - 16) * 10
                score -= penalti
                details.append(f"🔥 OVERLOAD: {dosen_nama} beban {total_sks} SKS (Max 16)")

        chromosome.fitness = max(score, 0)
        chromosome.fitness_details = details 
        return score
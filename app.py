import os
import io # <--- PENTING: Library untuk file memory
import pandas as pd
from flask import Flask, render_template, request, send_file, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from fpdf import FPDF

# Import Modul GA
from app.genetic_algorithm.population import Population

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_project_skripsi'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/smart_scheduler_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- GLOBAL CACHE ---
LAST_RESULT = {'schedule': None, 'fitness': 0, 'conflicts': 0, 'logs': []}

# --- DATABASE MODELS ---
class MataKuliah(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    kode_mk = db.Column(db.String(50))
    nama_mk = db.Column(db.String(150))
    sks = db.Column(db.Integer)
    fakultas = db.Column(db.String(100))
    dosen = db.Column(db.String(150))
    waktu_tersedia = db.Column(db.String(255))
    jumlah_mhs = db.Column(db.Integer)
    jenis_mk = db.Column(db.String(50))
    semester = db.Column(db.Integer, default=1)

class Ruangan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_ruangan = db.Column(db.String(50))
    kapasitas = db.Column(db.Integer)
    jenis = db.Column(db.String(50))
    fasilitas = db.Column(db.String(255), default="Standard")

# --- ADAPTER CLASSES ---
class ObjDosen:
    def __init__(self, id, nama): self.id = id; self.nama = nama

class ObjRuangan:
    def __init__(self, id, nama, kapasitas, jenis): 
        self.id = id; self.nama = nama; self.kapasitas = kapasitas; self.jenis = jenis

class ObjMatkul:
    def __init__(self, id, kode, nama, sks, semester, jenis, mhs, dosen_obj, fakultas):
        self.id = id; self.kode = kode; self.nama = nama; self.sks = sks
        self.semester = semester; self.jenis = jenis; self.jumlah_mhs = mhs
        self.dosen_obj = dosen_obj
        self.fakultas = fakultas 

# --- HELPER TIME
def get_readable_time(slot_id):
    try:
        slot = int(slot_id) - 1
        days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat"]
        
        # Update jam agar sesuai dengan Tabel Panduan di website
        times = [
            "07:00 - 08:40",  # Slot 1
            "08:40 - 10:20",  # Slot 2
            "10:20 - 12:00",  # Slot 3
            "13:00 - 14:40",  # Slot 4 (Istirahat Siang 12:00-13:00)
            "14:40 - 16:20",  # Slot 5
            "16:20 - 18:00",  # Slot 6 (Istirahat Sore/Maghrib 18:00-18:30)
            "18:30 - 20:10",  # Slot 7
            "20:10 - 21:50"   # Slot 8
        ]
        
        day_idx = slot // 8
        time_idx = slot % 8
        
        if day_idx < len(days) and time_idx < len(times):
            return days[day_idx], times[time_idx]
        return "Weekend", "Extra"
    except: return "-", "-"

# ================= ROUTES =================

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        upload_type = request.form.get('upload_type')
        file = None

        if upload_type == 'excel':
            file = request.files.get('file_excel')
        elif upload_type in ['csv_matkul', 'csv_ruangan']:
            file = request.files.get('file_csv')

        if file and file.filename != '':
            try:
                # --- KASUS 1: EXCEL ---
                if upload_type == 'excel' and file.filename.endswith('.xlsx'):
                    xls = pd.ExcelFile(file, engine='openpyxl')
                    
                    if 'Matkul' in xls.sheet_names:
                        df_mk = pd.read_excel(xls, 'Matkul')
                        MataKuliah.query.delete()
                        for _, row in df_mk.iterrows():
                            db.session.add(MataKuliah(
                                kode_mk=row['Kode_MK'], nama_mk=row['Nama_MK'], sks=int(row['SKS']),
                                dosen=row['Dosen'], waktu_tersedia=str(row['Waktu_Tersedia']),
                                jumlah_mhs=int(row.get('Jumlah_Mhs', 40)), jenis_mk=row.get('Jenis_MK', 'Teori'),
                                semester=int(row.get('Semester', 1)), fakultas=row.get('Fakultas', '-')
                            ))
                    else: flash('Gagal: Sheet "Matkul" hilang!', 'error')

                    if 'Ruangan' in xls.sheet_names:
                        df_ru = pd.read_excel(xls, 'Ruangan')
                        Ruangan.query.delete()
                        for _, row in df_ru.iterrows():
                            db.session.add(Ruangan(
                                nama_ruangan=row['Nama_Ruangan'], kapasitas=int(row['Kapasitas']), 
                                jenis=row['Jenis']
                            ))
                    else: flash('Gagal: Sheet "Ruangan" hilang!', 'error')
                    
                    db.session.commit()
                    flash('Sukses Import Excel!', 'success')

                # --- KASUS 2: CSV MATKUL ---
                elif upload_type == 'csv_matkul' and file.filename.endswith('.csv'):
                    df = pd.read_csv(file, sep=None, engine='python')
                    df.columns = df.columns.str.strip()
                    MataKuliah.query.delete()
                    for _, row in df.iterrows():
                        db.session.add(MataKuliah(
                            kode_mk=row['Kode_MK'], nama_mk=row['Nama_MK'], sks=int(row['SKS']),
                            dosen=row['Dosen'], waktu_tersedia=str(row['Waktu_Tersedia']),
                            jumlah_mhs=int(row.get('Jumlah_Mhs', 40)), jenis_mk=row.get('Jenis_MK', 'Teori'),
                            semester=int(row.get('Semester', 1)), fakultas=row.get('Fakultas', '-')
                        ))
                    db.session.commit()
                    flash('Sukses Import CSV Matkul!', 'success')

                # --- KASUS 3: CSV RUANGAN ---
                elif upload_type == 'csv_ruangan' and file.filename.endswith('.csv'):
                    df = pd.read_csv(file, sep=None, engine='python')
                    df.columns = df.columns.str.strip()
                    Ruangan.query.delete()
                    for _, row in df.iterrows():
                        db.session.add(Ruangan(
                            nama_ruangan=row['Nama_Ruangan'], kapasitas=int(row['Kapasitas']), 
                            jenis=row['Jenis']
                        ))
                    db.session.commit()
                    flash('Sukses Import CSV Ruangan!', 'success')
                else:
                    flash('Format file salah! Gunakan .xlsx atau .csv.', 'error')

            except Exception as e:
                flash(f'Error: {str(e)}', 'error')

        return redirect('/')

    data_mk = MataKuliah.query.all()
    data_ruangan = Ruangan.query.all()
    stats = {'sks': sum([mk.sks for mk in data_mk]), 'dosen': len(set([mk.dosen for mk in data_mk])), 'ruangan': len(data_ruangan)}
    return render_template('index.html', data=data_mk, rooms=data_ruangan, stats=stats)

@app.route('/run_ga', methods=['POST'])
def run_ga():
    db_matkul = MataKuliah.query.all()
    db_ruangan = Ruangan.query.all()

    if not db_matkul or not db_ruangan:
        flash("Data Kosong! Upload dulu.", 'error')
        return redirect('/')

    dosen_map, dosen_objs, matkul_objs, ruangan_objs = {}, [], [], []

    for r in db_ruangan:
        ruangan_objs.append(ObjRuangan(r.id, r.nama_ruangan, r.kapasitas, r.jenis))
    
    for mk in db_matkul:
        if mk.dosen not in dosen_map:
            d_obj = ObjDosen(len(dosen_map)+1, mk.dosen)
            dosen_map[mk.dosen] = d_obj
            dosen_objs.append(d_obj)
        
        m_obj = ObjMatkul(
            mk.id, mk.kode_mk, mk.nama_mk, mk.sks, mk.semester, 
            mk.jenis_mk, mk.jumlah_mhs, dosen_map[mk.dosen], mk.fakultas
        )
        matkul_objs.append(m_obj)

    try:
        population = Population(matkul_objs, dosen_objs, ruangan_objs, {}, population_size=150)
        best_chrom, final_score, final_conflicts, final_logs = population.run_genetic_algorithm(max_generations=200, mutation_rate=0.1)

        formatted_schedule = []
        map_mk = {m.id: m for m in matkul_objs}
        map_ru = {r.id: r for r in ruangan_objs}
        map_ds = {d.id: d for d in dosen_objs}

        for gene in best_chrom.genes:
            mk = map_mk[gene.matkul_id]
            ru = map_ru[gene.ruangan_id]
            ds = map_ds[gene.dosen_id]
            hari, jam = get_readable_time(gene.time_slot)

            formatted_schedule.append({
                'Hari': hari, 'Jam': jam, 'Nama_Ruangan': ru.nama,
                'Kapasitas_Ruangan': ru.kapasitas, 'Nama_MK': mk.nama,
                'Kode_MK': mk.kode, 'Dosen': ds.nama, 'Fakultas': mk.fakultas,
                'SKS': mk.sks, 'Jumlah_Mhs': mk.jumlah_mhs, 'Jenis_MK': mk.jenis,
                'assigned_time': gene.time_slot
            })

        global LAST_RESULT
        LAST_RESULT = {'schedule': formatted_schedule, 'fitness': final_score, 'conflicts': final_conflicts, 'logs': final_logs}

        create_pdf_report(formatted_schedule)
        return render_template('result.html', schedule=formatted_schedule, fitness=final_score, conflicts=final_conflicts, logs=final_logs)
    
    except Exception as e:
        flash(f"Error Algoritma: {str(e)}", 'error')
        import traceback; traceback.print_exc()
        return redirect('/')

@app.route('/hasil')
def hasil_jadwal():
    if LAST_RESULT['schedule'] is None: 
        flash("Belum ada jadwal.", 'error')
        return redirect('/')
    return render_template('result.html', schedule=LAST_RESULT['schedule'], fitness=LAST_RESULT['fitness'], conflicts=LAST_RESULT['conflicts'], logs=LAST_RESULT['logs'])

@app.route('/dosen')
def data_dosen():
    lecturers = {}
    for mk in MataKuliah.query.all():
        if mk.dosen not in lecturers: 
            lecturers[mk.dosen] = {'nama': mk.dosen, 'total_sks': 0, 'total_kelas': 0, 'daftar_matkul': []}
        lecturers[mk.dosen]['total_sks'] += mk.sks
        lecturers[mk.dosen]['total_kelas'] += 1
        lecturers[mk.dosen]['daftar_matkul'].append(f"{mk.nama_mk} ({mk.sks} SKS)")
    
    final_list = sorted(list(lecturers.values()), key=lambda x: x['total_sks'], reverse=True)
    return render_template('dosen.html', lecturers=final_list)

# --- FITUR BARU: DOWNLOAD TEMPLATE ---
@app.route('/download_template/<file_type>')
def download_template(file_type):
    # Header Standar
    headers_matkul = {
        'Kode_MK': ['CS101'], 'Nama_MK': ['Algoritma'], 'SKS': [3], 'Fakultas': ['Ilkom'], 
        'Dosen': ['Dr. Budi'], 'Waktu_Tersedia': ['1;2;3;4;5'], 
        'Jumlah_Mhs': [40], 'Jenis_MK': ['Teori'], 'Semester': [1]
    }
    headers_ruangan = {
        'Nama_Ruangan': ['R.101'], 'Kapasitas': [40], 'Jenis': ['Teori']
    }

    buffer = io.BytesIO()
    try:
        if file_type == 'excel':
            with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                pd.DataFrame(headers_matkul).to_excel(writer, sheet_name='Matkul', index=False)
                pd.DataFrame(headers_ruangan).to_excel(writer, sheet_name='Ruangan', index=False)
            filename, mimetype = 'Template_Lengkap.xlsx', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        
        elif file_type == 'csv_matkul':
            pd.DataFrame(headers_matkul).to_csv(buffer, index=False, sep=',')
            filename, mimetype = 'Template_Matkul.csv', 'text/csv'
            
        elif file_type == 'csv_ruangan':
            pd.DataFrame(headers_ruangan).to_csv(buffer, index=False, sep=',')
            filename, mimetype = 'Template_Ruangan.csv', 'text/csv'
            
        buffer.seek(0)
        return send_file(buffer, as_attachment=True, download_name=filename, mimetype=mimetype)
    except Exception as e:
        return str(e), 500

@app.route('/download_pdf')
def download_pdf(): return send_file('static/schedule_report.pdf', as_attachment=True)

@app.route('/reset_db')
def reset_db():
    MataKuliah.query.delete(); Ruangan.query.delete(); db.session.commit()
    return redirect('/')

@app.route('/delete_room/<int:id>')
def delete_room(id):
    Ruangan.query.filter_by(id=id).delete(); db.session.commit()
    return redirect('/')

def create_pdf_report(data):
    pdf = FPDF()
    pdf.add_page(); pdf.set_font("Arial", 'B', 14); pdf.cell(0, 10, "Laporan Jadwal Kuliah", 0, 1, 'C'); pdf.ln(10)
    pdf.set_font("Arial", size=8)
    pdf.cell(20, 10, "Hari", 1); pdf.cell(20, 10, "Jam", 1); pdf.cell(30, 10, "Ruang", 1); 
    pdf.cell(50, 10, "Matkul", 1); pdf.cell(40, 10, "Dosen", 1); pdf.cell(30, 10, "Fakultas", 1); pdf.ln()
    data.sort(key=lambda x: x['assigned_time'])
    for row in data:
        pdf.cell(20, 10, str(row['Hari']), 1); pdf.cell(20, 10, str(row['Jam']), 1)
        pdf.cell(30, 10, str(row['Nama_Ruangan'])[:18], 1); pdf.cell(50, 10, str(row['Nama_MK'])[:30], 1)
        pdf.cell(40, 10, str(row['Dosen'])[:25], 1); pdf.cell(30, 10, str(row['Fakultas'])[:18], 1); pdf.ln()
    pdf.output("static/schedule_report.pdf")

if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(debug=True)
from fpdf import FPDF

class PDFReport(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 15)
        self.cell(0, 10, 'Laporan Jadwal Kuliah & Ruangan', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Halaman {self.page_no()}', 0, 0, 'C')

def create_pdf(schedule_data, filename="static/schedule_report.pdf"):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_font("Arial", size=9)

    # Header Tabel
    pdf.set_fill_color(220, 230, 240)
    # Total lebar = 190 (A4 margin)
    pdf.cell(20, 10, "Hari", 1, 0, 'C', 1)
    pdf.cell(20, 10, "Jam", 1, 0, 'C', 1)
    pdf.cell(30, 10, "Ruangan", 1, 0, 'C', 1) # Kolom Baru
    pdf.cell(60, 10, "Mata Kuliah", 1, 0, 'C', 1)
    pdf.cell(40, 10, "Dosen", 1, 0, 'C', 1)
    pdf.cell(20, 10, "SKS/Mhs", 1, 1, 'C', 1)

    # Isi Tabel
    pdf.set_font("Arial", size=8)
    
    # Urutkan berdasarkan waktu
    sorted_data = sorted(schedule_data, key=lambda x: int(x['assigned_time']))
    
    for row in sorted_data:
        hari = str(row.get('Hari', '-'))
        # Ambil jam mulai saja agar muat (cth: "07:30 - 09:10" -> "07:30")
        jam_full = str(row.get('Jam', '-'))
        jam = jam_full.split(' - ')[0] if ' - ' in jam_full else jam_full
        
        ruang = str(row.get('Nama_Ruangan', '?'))
        matkul = str(row.get('Nama_MK', '-'))
        dosen = str(row.get('Dosen', '-'))
        info = f"{row.get('SKS')} / {row.get('Jumlah_Mhs')}"
        
        pdf.cell(20, 10, hari, 1)
        pdf.cell(20, 10, jam, 1)
        pdf.cell(30, 10, ruang[:18], 1)      # Potong jika terlalu panjang
        pdf.cell(60, 10, matkul[:35], 1)     # Potong nama matkul
        pdf.cell(40, 10, dosen[:25], 1)      # Potong nama dosen
        pdf.cell(20, 10, info, 1, 1, 'C')

    pdf.output(filename)
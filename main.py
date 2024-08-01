from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, initialize_app
import uvicorn
from jinja2 import Environment, FileSystemLoader, select_autoescape
import weasyprint
import hashlib
import os
from firestore import save_to_firestore

# Initialize Firebase Admin SDK
#cred = credentials.Certificate(r"D:\koding\kode utama\karangTaruna\backend\creditial.json")
#initialize_app(cred)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost"],  # Tambahkan asal (origin) yang diizinkan
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#untuk env generator pada endpoint surat-tugas
env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml']),
    cache_size=50  # Set ukuran cache untuk Jinja2 templates
)

@app.get("/")
async def root():
    return "server ready to use"

@app.post("/surat-tugas")
async def generate_pdf(
    namaPenugas: str = Form(...),
    penugassJabatan: str = Form(...),
    namaPetugas: str = Form(...),
    jabatanPetugas: str = Form(...),
    ktp: str = Form(...),
    job: str = Form(...),
    date: str = Form(...),
):
    # buat hast input untuk cache key
    data_hash = hashlib.md5((namaPenugas + penugassJabatan + namaPetugas + jabatanPetugas + ktp + job + date ).encode()).hexdigest()
    pdf_file = f'surat_Tugas_{data_hash}.pdf'

    if not os.path.exists(pdf_file):
        template = env.get_template("suratTugas.html")
        html_content = template.render(
            namaPenugas=namaPenugas,
            penugassJabatan=penugassJabatan,
            namaPetugas=namaPetugas,
            jabatanPetugas=jabatanPetugas,
            ID=ktp,
            job=job,
            date=date
        )
        weasyprint.HTML(string=html_content).write_pdf(pdf_file)

    # Simpan data ke Firestore
    data = {
        "namaPenugas": namaPenugas,
        "penugassJabatan": penugassJabatan,
        "namaPetugas": namaPetugas,
        "jabatanPetugas": jabatanPetugas,
        "ID": ktp,
        "job": job,
        "date": date
    }
    save_status = save_to_firestore(data)
    if not save_status:
        raise HTTPException(status_code=500, detail="Failed to save data to Firestore")

    return FileResponse(pdf_file, media_type='application/pdf', filename=pdf_file)

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)

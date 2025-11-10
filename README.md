#Penerapan Machine Learning untuk Deteksi Angka Berdasarkan Gestur Jari Tangan

##Tentang Proyek
Proyek ini merupakan hasil **Ujian Tengah Semester (UTS)** dan **Tugas 1** dari mata kuliah terkait Machine Learning dan Computer Vision di **Universitas Mikroskil**, dengan judul:

> **“Penerapan Machine Learning untuk Deteksi Angka Berdasarkan Gestur Jari Tangan”**

Aplikasi ini mampu mendeteksi jumlah jari yang terangkat secara **real-time** melalui kamera dan memberikan **umpan balik suara (Text-to-Speech)** secara otomatis.

---

##Tim UHUY
| No | Nama | NIM | Tugas |
|----|------|-----|-------|
| 1 | **Maulana Fattah** | 221113430 | Ketua, Implementasi logika `count_fingers` dan integrasi Text-to-Speech (TTS). |
| 2 | **Muhammad Ridwan** | 221112668 | Implementasi OpenCV pipeline (video capture, drawing, FPS) dan struktur utama program. |
| 3 | **Hans Christian Sianturi** | 221113102 | Dokumentasi proyek, analisis model, dan laporan akhir. |

---

##Teknologi yang Digunakan
| Kategori | Teknologi | Keterangan |
|-----------|------------|-------------|
| Bahasa Pemrograman | Python 3.x | Bahasa utama implementasi |
| Deteksi Tangan | [MediaPipe Hands](https://developers.google.com/mediapipe/solutions/vision/hand_landmarker) | Deteksi landmark tangan (21 titik) |
| Computer Vision | [OpenCV](https://opencv.org/) | Video capture, manipulasi frame, dan visualisasi |
| Audio | Pyttsx3 | Text-to-Speech |
| Library Pendukung | NumPy, Threading | Pengolahan matriks dan multithreading |
| IDE | VS Code / Jupyter Notebook | Lingkungan pengembangan |

---

##Konsep dan Model
Proyek ini memadukan dua pendekatan:
1. **Model Deep Learning (MediaPipe Hands)** untuk mendeteksi posisi 21 landmark tangan.
2. **Algoritma Heuristik (Geometri)** untuk menghitung jumlah jari yang terangkat berdasarkan posisi landmark:
   - Jempol → dibandingkan dari sumbu **x**
   - Empat jari lainnya → dibandingkan dari sumbu **y**

---

##Arsitektur Sistem
1. Input video dari webcam menggunakan OpenCV.
2. Frame dibalik (flip) agar interaksi seperti cermin.
3. MediaPipe mendeteksi landmark jari.
4. Algoritma menghitung jumlah jari terangkat.
5. Total jari ditampilkan di layar dan disuarakan melalui pyttsx3.

---

##Evaluasi Kinerja
- **FPS (Frame Rate):** ±25–35 FPS (real-time)
- **Akurasi Penghitungan:**  
  - Kondisi ideal: ~98–100%  
  - Kondisi kompleks (occlusion, sudut ekstrem): tetap tinggi  
- **Respons Audio:** Tidak menyebabkan lag (karena dijalankan di thread terpisah)

---

##Demo dan Deployment
- **Link GitHub Repository:** *(isi link repositori kamu di sini)*  
- **Video Demo:** *(isi link YouTube demo kamu di sini)*  

### Contoh Output:
| Input (Pose Tangan) | Output Visual | Output Audio |
|----------------------|---------------|---------------|
| Tangan kanan mengepal | TOTAL: 0 | “zero” |
| Tangan kanan lima jari | TOTAL: 5 | “five” |
| Dua tangan, total 8 jari | TOTAL: 8 | “eight” |

---

##Cara Menjalankan
1. Pastikan semua library terinstal:
   ```bash
   pip install opencv-python mediapipe pyttsx3 numpy
2. Jalankan Semua file utama
   ```bash
   python main.py

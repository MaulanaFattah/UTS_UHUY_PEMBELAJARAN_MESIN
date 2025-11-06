# ====== Import Library yang Diperlukan ======
import cv2                  # Untuk menangkap video dari kamera
import mediapipe as mp       # Untuk deteksi tangan dan landmark jari
import time                  # Untuk menghitung FPS
import numpy as np           # Untuk perhitungan koordinat
import pyttsx3               # Untuk text-to-speech (suara)
import threading             # Agar suara dijalankan tanpa membuat video macet

# INISIALISASI SISTEM DETEKSI DAN SUARA

# Inisialisasi modul hands dari Mediapipe
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Inisialisasi mesin suara pyttsx3
engine = pyttsx3.init()
engine.setProperty('rate', 170)   # Kecepatan bicara
engine.setProperty('volume', 1.0) # Volume maksimum

# Pilih suara (jika tersedia suara Bahasa Indonesia)
voices = engine.getProperty('voices')
for v in voices:
    if "indonesian" in v.name.lower() or "id" in v.id.lower():
        engine.setProperty('voice', v.id)
        break

# Pemetaan angka ke kata (untuk ucapan suara)
number_words = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine",
    10: "ten"
}

# FUNGSI UNTUK MENGATUR SUARA (MULTI-THREAD)

def speak(text):
    """
    Jalankan suara di thread terpisah agar tidak mengganggu FPS video.
    """
    t = threading.Thread(target=lambda: _speak_thread(text))
    t.start()

def _speak_thread(text):
    """
    Thread yang menjalankan fungsi bicara pyttsx3.
    """
    try:
        engine.say(text)
        engine.runAndWait()
    except RuntimeError:
        # Jika engine sedang bicara, lewati untuk mencegah crash
        pass  

# IDENTIFIKASI TITIK LANDMARK JARI
TIP_IDS = [4, 8, 12, 16, 20]   # Ujung jari
PIP_IDS = [2, 6, 10, 14, 18]   # Titik tengah jari

# FUNGSI UNTUK MENGHITUNG JUMLAH JARI YANG TERANGKAT

def count_fingers(hand_landmarks, handedness_str, image_w, image_h):
    """
    Menghitung jumlah jari yang terangkat berdasarkan koordinat landmark.
    """
    lm = hand_landmarks.landmark
    pts = np.array([[p.x * image_w, p.y * image_h] for p in lm], dtype=int)

    wrist_x, wrist_y = pts[0]
    draw_pos = (wrist_x, max(20, wrist_y - 30))  # Posisi untuk teks

    count = 0
    flipped_label = 'left' if handedness_str.lower() == 'right' else 'right'

    # === Deteksi jempol ===
    thumb_tip_x = lm[TIP_IDS[0]].x
    thumb_ip_x = lm[PIP_IDS[0]].x
    if flipped_label == 'right':
        if thumb_tip_x > thumb_ip_x:
            count += 1
    else:
        if thumb_tip_x < thumb_ip_x:
            count += 1

    # === Deteksi 4 jari lainnya ===
    for i in range(1, 5):
        if lm[TIP_IDS[i]].y < lm[PIP_IDS[i]].y:
            count += 1

    return count, draw_pos, flipped_label

# FUNGSI UNTUK MENGGAMBAR KOTAK DAN TEKS DI LAYAR

def draw_finger_box(frame, text, pos, color):
    """
    Menampilkan jumlah jari pada posisi tertentu di layar.
    """
    (text_w, text_h), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.3, 3)
    x, y = pos
    x1, y1 = max(0, x - text_w // 2 - 10), max(0, y - text_h - 10)
    x2, y2 = min(frame.shape[1], x + text_w // 2 + 10), min(frame.shape[0], y + 10)

    # Kotak transparan
    overlay = frame.copy()
    cv2.rectangle(overlay, (x1, y1), (x2, y2), color, -1)
    cv2.addWeighted(overlay, 0.4, frame, 0.6, 0, frame)

    # Tulisan di dalam kotak
    cv2.putText(frame, text, (x1 + 8, y2 - 6),
                cv2.FONT_HERSHEY_SIMPLEX, 1.3, (255, 255, 255), 3)

# FUNGSI UTAMA

def main():
    """
    Fungsi utama untuk menjalankan deteksi jari secara real-time.
    """
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Tidak bisa membuka kamera.")
        return

    # Warna untuk label
    COLOR_LEFT = (255, 0, 0)   # Biru
    COLOR_RIGHT = (0, 0, 255)  # Merah
    COLOR_TOTAL = (0, 255, 0)  # Hijau

    prev_total = -1  # Menyimpan total sebelumnya untuk deteksi perubahan

    # Inisialisasi deteksi tangan
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.6,
        min_tracking_confidence=0.6
    ) as hands:
        prev_time = time.time()

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.flip(frame, 1)
            h, w = frame.shape[:2]
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)

            left_count, right_count = 0, 0

            # Jika tangan terdeteksi
            if result.multi_hand_landmarks and result.multi_handedness:
                for hand_landmarks, handedness in zip(result.multi_hand_landmarks, result.multi_handedness):
                    hand_label = handedness.classification[0].label
                    cnt, pos, flipped_label = count_fingers(hand_landmarks, hand_label, w, h)

                    # Tentukan warna dan label tangan
                    if flipped_label == 'left':
                        color = COLOR_LEFT
                        left_count = cnt
                        label_text = "Left"
                    else:
                        color = COLOR_RIGHT
                        right_count = cnt
                        label_text = "Right"

                    # Gambar landmark dan teks
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    draw_finger_box(frame, str(cnt), pos, color)
                    cv2.putText(frame, label_text, (pos[0] - 25, pos[1] - 50),
                                cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2)

            # Hitung total jari
            total = left_count + right_count
            if total >= 0:
                cv2.rectangle(frame, (w // 2 - 100, h - 90), (w // 2 + 100, h - 30), (0, 0, 0), -1)
                cv2.putText(frame, f"TOTAL: {total}", (w // 2 - 90, h - 45),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.4, COLOR_TOTAL, 4)

            # Jika jumlah jari berubah, ucapkan jumlahnya
            if total != prev_total and total >= 0:
                word = number_words.get(total, str(total))
                speak(word)
                prev_total = total

            # Hitung dan tampilkan FPS
            fps = 1.0 / (time.time() - prev_time) if time.time() > prev_time else 0
            prev_time = time.time()
            cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30),
                        cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)

            # Tampilkan hasil deteksi
            cv2.imshow("Finger Counter Deluxe v8 - Tekan [Q] untuk keluar", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

# EKSEKUSI PROGRAM

if __name__ == "__main__":
    main()

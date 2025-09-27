# Pygame-Project
# ⚔️ Warrior Legacy

**Warrior Legacy** adalah game pertarungan 2D berbasis **Python** dan **Pygame**, dikembangkan sebagai proyek penulisan ilmiah.  
Game ini menghadirkan dua karakter utama, **Mystic Warrior** dan **Dark Sorcerer**, dengan animasi, serangan spesial, health bar, energy bar, serta arena pertarungan dinamis.

---

## 🎮 Fitur Utama
- **2 Karakter Playable**: Mystic Warrior & Dark Sorcerer dengan style unik.  
- **Animasi Sprite**: Idle, run, jump, attack, hit, dan death.  
- **Sistem Pertarungan**: Health bar, energy bar (dengan regen), attack cooldown.  
- **Arena Dinamis**: Background animasi menggunakan frame GIF.  
- **UI Lengkap**: Menu utama, layar kontrol, pause menu, skor, dan layar hasil.  
- **Audio**: Musik latar & efek suara serangan.  

---

## 🕹️ Kontrol

### Player 1
- **A / D** → Gerak kiri / kanan  
- **W** → Lompat  
- **C** → Attack 1  
- **V** → Attack 2  

### Player 2
- **← / →** → Gerak kiri / kanan  
- **↑** → Lompat  
- **NumPad 2** → Attack 1  
- **NumPad 3** → Attack 2  

> Catatan: Player harus punya cukup **energy** untuk melakukan serangan.

---

## 📂 Struktur Proyek

Warrior-Legacy/
│
├── asset/ # Sprite, background, musik, font, icon, button
│ ├── animation/ # Sprite sheet karakter
│ ├── background/ # Background statis & GIF arena
│ ├── music/ # Musik & efek suara
│ ├── font/ # Font untuk UI
│ ├── Button/ # Gambar tombol menu
│ └── icon/ # Icon game
│
├── frames/ # Frame hasil ekstrak dari GIF arena
│
├── main.py # File utama game
├── fighter.py # Class karakter & logika pertarungan
├── main_menu.py # Menu utama
├── credit_screen.py # Layar kontrol (how to play)
├── gif.py # Script ekstrak GIF ke frame
└── README.md # Dokumentasi proyek

---

## 🚀 Cara Menjalankan

1. Pastikan Python 3 sudah terinstall.  
2. Install dependensi:
   ```bash
   pip install pygame pillow
3. Jalankan game:
   python main.py

🧑‍💻 Pengembang

Raihan Ananda Firdaus – Universitas Gunadarma

📜 Lisensi

Proyek ini dibuat untuk tujuan pembelajaran dan penelitian.


✨ Selamat bertarung di Warrior Legacy!

---

## 📸 Cuplikan Gameplay


---



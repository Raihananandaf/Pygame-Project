from PIL import Image
import os

# Buka file GIF
gif = Image.open('asset/background/battlearena.gif')

# Buat folder untuk menyimpan frame-frame
if not os.path.exists('frames'):
    os.makedirs('frames')

# Ekstrak setiap frame dan simpan sebagai file terpisah
for frame in range(0, gif.n_frames):
    gif.seek(frame)
    gif.save(f'frames/frame_{frame}.png')

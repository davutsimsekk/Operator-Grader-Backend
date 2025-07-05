from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import socket

# Celery görevimizi ve app nesnesini import ediyoruz
from worker import transcribe_audio_from_url, app as celery_app

# --- AYARLAR ---
# Ses dosyalarının bulunduğu klasör (macOS üzerinde)
AUDIO_DIR = "/Users/davut/Desktop/Projeler/OperatorGraderBackend/assets" # Kendi ses dosyalarınızın olduğu klasör
PORT = 8000

# FastAPI uygulamasını oluştur
app = FastAPI()

# Ses dosyalarını sunmak için bir "static" endpoint oluşturuyoruz.
# Artık http://<ip>:8000/audio/dosyaadi.mp3 gibi erişilebilecek.
app.mount("/audio", StaticFiles(directory=AUDIO_DIR), name="audio")

def get_local_ip():
    """Makinenin yerel ağdaki IP adresini bulur."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Bu IP'ye bağlanmaya çalışmaz, sadece uygun arayüzü bulmak için kullanır
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    print(f"Yerel IP adresi: {IP}")
    return IP

def run_transcription_jobs():
    """Ses dosyalarını tarar ve transkript için görevleri başlatır."""
    audio_files = [f for f in os.listdir(AUDIO_DIR) if f.endswith(('.mp3', '.wav', '.m4a'))]
    if not audio_files:
        print(f"'{AUDIO_DIR}' içinde işlenecek ses dosyası bulunamadı.")
        return

    local_ip = get_local_ip()
    print(f"Ana makine IP adresi: {local_ip}")
    print("Görevler sıraya ekleniyor...")

    task_results = []
    for filename in audio_files:
        file_url = f"http://{local_ip}:{PORT}/audio/{filename}"
        task = transcribe_audio_from_url.delay(file_url)
        task_results.append((task, filename))
        print(f"- {filename} görevi URL ({file_url}) ile eklendi. ID: {task.id}")

    print("\nGörevlerin tamamlanması bekleniyor...")
    for task, filename in task_results:
        # .get() ile sonucun gelmesini bekliyoruz
        result_text = task.get(timeout=600)
        print(f"\n--- SONUÇ: {filename} ---\n{result_text}\n--------------------")
        # Burada veritabanına yazma işlemini yapabilirsiniz.

    print("\nTüm işlemler tamamlandı.")

# Bu script doğrudan çalıştırıldığında ne olacağını tanımlayalım
if __name__ == "__main__":
    print("FastAPI sunucusunu başlatmak için terminalde şu komutu çalıştırın:")
    print(f"uvicorn main:app --host 0.0.0.0 --port {PORT}")
    print("\nSunucu çalıştıktan sonra, görevleri başlatmak için YENİ BİR terminalde şunu çalıştırın:")
    print("python -c 'from main import run_transcription_jobs; run_transcription_jobs()'")

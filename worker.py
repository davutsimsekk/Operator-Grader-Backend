import celery
import worker_service
import torch
import requests


MAIN_PC_IP = "10.42.0.15"

workerService = worker_service.WorkerService()

app = celery.Celery('worker', broker=f'redis://{MAIN_PC_IP}:6379/0',
                     backend=f'redis://{MAIN_PC_IP}:6379/0')

@app.task
def transcribe_audio_from_url(audio_url):
    response = requests.get(audio_url)
    if response.status_code == 200:
        audio_data = response.content
        # Geçici bir dosya oluştur
        with open("temp_audio.wav", "wb") as f:
            f.write(audio_data)
        # Ses dosyasını transkripte et
        result = workerService.transcribe_audio_file("temp_audio.wav")
        return result
    else:
        print(f"Error fetching audio from URL: {response.status_code}")
        return None

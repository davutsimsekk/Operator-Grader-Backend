import celery
import worker_service
import torch
import requests
import os


#To run this worker, you need to have Redis running on your main PC with the IP address
# celery -A worker worker --pool=solo --loglevel=info
# prefork threads falan hata veriyor paralellik sikinti cikarabilyor

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
        print(f"Transcribing audio from {audio_url}")
        result = workerService.transcribe_audio_file("temp_audio.wav")
        print(f"Transcription result: {result}")
        # Geçici dosyayı sil
        os.remove("temp_audio.wav")
        return result
        
    else:
        print(f"Error fetching audio from URL: {response.status_code}")
        return None

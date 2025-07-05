import whisper_timestamped as whisper

import os
import json




def transcribe_audio(file_path, whisper_model):

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file {file_path} does not exist.")
    
    audio=whisper.load_audio(file_path)
    print("Ses dosyası yüklendi:", file_path)


    result = whisper_model.transcribe(audio, language="tr")

    print(json.dumps(result, indent=2, ensure_ascii=False))

    return result

def print_by_timestamp(result):
    """
    Segment bazında zaman damgalarını yazdırır
    """
    print("\n" + "-"*50)
    print("SEGMENT BAZINDA ZAMAN DAMGALARI")
    print("-"*50)
    for segment in result["segments"]:
        start = segment["start"]
        end = segment["end"]
        text = segment["text"]
        print(f"[{start:.2f} - {end:.2f}] {text}")
        
        # Eğer words varsa onları da yazdır
        if "words" in segment and segment["words"]:
            print("  Kelimeler:")
            for word in segment["words"]:
                word_start = word["start"]
                word_end = word["end"]
                word_text = word["text"]
                print(f"    [{word_start:.2f} - {word_end:.2f}] {word_text}")


import stt_service
import checkers
import whisper_timestamped as whisper
import torch
class WorkerService:

    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model= whisper.load_model("base", device=device)
        self.model = model
        self.model_size = "base"
        print(f"Model yüklendi: {self.model_size} - Cihaz: {device}")


    def analyze_audio_file(self, file_path):
        """
        Ses dosyasını transkripte eder ve konuşma analizi yapar.
        """
        try:
            result = stt_service.transcribe_audio(file_path, self.model)
            stt_service.print_by_timestamp(result)
            analysis_results = checkers.ConversationAnalysis.analyze_conversation(result)
            checkers.ConversationAnalysis.print_analysis_results(analysis_results)
            return analysis_results
        except Exception as e:
            print(f"Error processing audio file: {e}")
            return None

    def transcribe_audio_file_by_timestamp(self, file_path):
        """
        Ses dosyasını transkripte eder ve zaman damgalarıyla birlikte sonucu döndürür.
        """
        result = stt_service.transcribe_audio(file_path, self.model)
        stt_service.print_by_timestamp(result)
        return result

    def transcribe_audio_file(self, file_path):
        """
        Ses dosyasını transkripte eder ve text sonucu döndürür.
        """
        result = stt_service.transcribe_audio(file_path, self.model)
        return result


    def change_model_size(self, model_size):
        """
        Model boyutunu değiştirir
        """
        self.model = whisper.load_model(model_size, device=self.model.device)
        self.model_size = model_size

    def change_device(self, new_device):
        """
        Cihazı değiştirir
        """
        self.model = whisper.load_model(self.model_size, device=new_device)
        print(f"Model yeni cihazda yüklendi: {new_device}")
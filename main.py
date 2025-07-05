import whisper_timestamped as whisper
import stt_service
import torch
from checkers import (
    ConversationAnalysis
)


# CUDA'nın kullanılabilirliğini kontrol et
is_cuda_available = torch.cuda.is_available()



# Ana program
if __name__ == "__main__":
    # Ses dosyasını transkript et
    # result = stt_service.transcribe_audio("/Users/davut/Desktop/Projeler/OperatorGraderBackend/assets/ses2.wav", model_size="base", language="tr", device="cuda" if is_cuda_available else "cpu")
    
    # Kelime bazında zaman damgalarını yazdır
    # stt_service.print_by_timestamp(result)
    
    # Konuşma analizini yap
    # analysis_results = ConversationAnalysis.analyze_conversation(result)

    # Analiz sonuçlarını yazdır
    # ConversationAnalysis.print_analysis_results(analysis_results)

    print("Main program çalışıyor...")
    
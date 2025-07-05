import numpy as np

class OpeningSpeechChecker:
    def __init__(self):
        self.required_phrases = ["Merhabalar benim adım", "Size nasıl yardımcı olabilirim"]
    
    def check(self, text):
        count = sum(1 for phrase in self.required_phrases if phrase.lower() in text.lower())
        return count == len(self.required_phrases)

class duration_immediate_sentence_control :
    def __init__(self):
        self.opening_requests = ["Merhabalar benim adım", "Size nasıl yardımcı olabilirim"]
        self.info_requests = ["Adınızı öğrenebilir miyim", "İsminizi öğrenebilir miyim", "Adınız nedir", "TC’nizi öğrenebilir miyim", "Telefon numaranızı öğrenebilir miyim"]
        
    def check(self,initial_30_seconds_text, opening_requests_count=2, info_requests_count=3):
        
        
        
        opening_count = 0
        info_count = 0
        
        # Açılış ifadelerini kontrol et
        for phrase in self.opening_requests:
            if phrase.lower() in initial_30_seconds_text.lower():
                opening_count += 1
                if opening_count >= opening_requests_count:
                    break

        # Bilgi isteme ifadelerini kontrol et
        for phrase in self.info_requests:
            if phrase.lower() in initial_30_seconds_text.lower():
                info_count += 1
                if info_count >= info_requests_count:
                    break

        # Koşulları kontrol et
        if opening_count >= opening_requests_count and info_count >= info_requests_count:
            return True
        else:
            return False


class InformationInquiryChecker:
    def __init__(self):
        self.required_phrases = [
            "Adınızı öğrenebilir miyim", "İsminizi öğrenebilir miyim", "Adınız nedir",
            "TC’nizi öğrenebilir miyim", "Telefon numaranızı öğrenebilir miyim"
        ]
    
    def check(self, text):
        count = sum(1 for phrase in self.required_phrases if phrase.lower() in text.lower())
        return count >= 3

class IdentityInformationChecker:
    def __init__(self):
        self.required_phrases = ["Kimlik bilgisi teyit edildi", "Bilgileriniz doğru", "Bilgileriniz hatalı"]
    
    def check(self, text):
        return any(phrase.lower() in text.lower() for phrase in self.required_phrases)

class OrderModeChecker:
    def __init__(self):
        self.unwanted_phrases = ["al", "ver", "gir", "yap", "söyle", "konuş", "anlat", "sus", "kes", "boynuzlu"]
    
    def check(self, text):
        return not any(word.lower() in self.unwanted_phrases for word in text.split())

class SwearChecker:
    def __init__(self):
        self.swear_words = [
            "cibiliyetsiz", "orospunun", "sik", "sikik", "sikiş", "sokuk", "sokulmuş", "sikilmiş",
            "pezevenk", "pezevengi", "sikeyim", "orospu", "amına", "göt", "amcık", "yarak",
            "sikici", "şerefsiz", "yarak", "yavşak", "kutsal", "damacana"
        ]
        self.found_swears = []  # Bulunan küfürler ve zaman aralıkları
    
    def check(self, word, timestamp):
        """
        Verilen kelimenin küfür olup olmadığını kontrol eder ve eğer küfürse zaman bilgisiyle kaydeder.
        
        Args:
            word: Kontrol edilecek kelime
            timestamp: Kelimenin ses dosyasındaki başlangıç saniyesi
        
        Returns:
            bool: Kelime temizse True, küfürse False
        """
        clean_word = word.lower().strip()
        
        if clean_word in self.swear_words:
            # Zaman aralığını saniye cinsinden hesapla (ortalama bir kelime 0.5-1 saniye arası sürer)
            # Başlangıç zamanını kelimenin başladığı an, bitiş zamanını ise 1 saniye sonrası olarak kabul et
            start_time = max(0, timestamp)  # Negatif zaman olmasını engelle
            end_time = timestamp + 1  # Yaklaşık 1 saniye süre
            
            print(f"Küfür tespit edildi: '{clean_word}' - süre: {start_time:.2f} - {end_time:.2f} saniye.")
            
            # Bulunan küfürü kaydet
            self.found_swears.append({
                "word": clean_word,
                "start_time": start_time,
                "end_time": end_time
            })
            return False
        return True
    
    def get_found_swears(self):
        """Tespit edilen küfürlerin listesini döndürür"""
        return self.found_swears
    
    def clear_found_swears(self):
        """Tespit edilen küfürleri temizler"""
        self.found_swears = []
        return True

class Calculate_Wait_Time:
    def check(audio_data):
        wait_time = 0  # Example: replace with the real wait time calculation
        if wait_time > 10:
            message = f"Bekletme süresi çok uzun: {wait_time} saniye. Puan kırıldı."
            print(message)




class WaitTimeChecker:
    def __init__(self, max_wait_time=10):
        self.max_wait_time = max_wait_time
    
    def check(self, wait_time):
        if wait_time > self.max_wait_time:
            print(f"Bekletme süresi çok uzun: {wait_time} saniye. Puan kırıldı.")


class ConversationAnalysis:
    
    def analyze_conversation(result):
        """
        Whisper transkripti üzerinde tüm kontrolleri yapar ve sonuçları döndürür
        """
        # Checker sınıflarını oluştur
        opening_checker = OpeningSpeechChecker()
        duration_checker = duration_immediate_sentence_control()
        info_checker = InformationInquiryChecker()
        identity_checker = IdentityInformationChecker()
        order_checker = OrderModeChecker()
        swear_checker = SwearChecker()
        wait_checker = WaitTimeChecker()
        
        # Tam metni oluştur
        full_text = ""
        initial_30_seconds_text = ""
        
        # Segment bazında metin oluşturma ve küfür kontrolü
        for segment in result["segments"]:
            start = segment["start"]
            text = segment["text"]
            
            # İlk 30 saniye metnini oluştur
            if start <= 30:
                initial_30_seconds_text += text + " "
            
            # Tam metni oluştur
            full_text += text + " "
            
            # Kelime bazında küfür kontrolü (eğer words varsa)
            if "words" in segment:
                for word in segment["words"]:
                    word_start = word["start"]
                    word_text = word["text"]
                    swear_checker.check(word_text, word_start)
            else:
                # Words yoksa segment metni üzerinden basit kontrol
                words = text.split()
                for i, word in enumerate(words):
                    # Tahmini zaman hesaplama (segment başlangıcı + kelime sırası)
                    estimated_time = start + (i * 0.5)  # Her kelime için 0.5 saniye tahmini
                    swear_checker.check(word, estimated_time)
        
        # Kontrolleri yap
        results = {
            "opening_speech": opening_checker.check(full_text),
            "duration_immediate_control": duration_checker.check(initial_30_seconds_text),
            "information_inquiry": info_checker.check(full_text),
            "identity_information": identity_checker.check(full_text),
            "order_mode": order_checker.check(full_text),
            "swear_words_found": swear_checker.get_found_swears(),
            "is_clean_speech": len(swear_checker.get_found_swears()) == 0,
            "full_text": full_text.strip(),
            "initial_30_seconds_text": initial_30_seconds_text.strip()
        }
        
        return results

    def print_analysis_results(analysis_results):
        """
        Analiz sonuçlarını düzenli bir şekilde yazdırır
        """
        print("\n" + "="*50)
        print("KONUŞMA ANALİZİ SONUÇLARI")
        print("="*50)
        
        print(f"\n1. Açılış Konuşması: {'✓ BAŞARILI' if analysis_results['opening_speech'] else '✗ BAŞARISIZ'}")
        print(f"2. İlk 30 Saniye Kontrolü: {'✓ BAŞARILI' if analysis_results['duration_immediate_control'] else '✗ BAŞARISIZ'}")
        print(f"3. Bilgi Sorgulama: {'✓ BAŞARILI' if analysis_results['information_inquiry'] else '✗ BAŞARISIZ'}")
        print(f"4. Kimlik Bilgisi Teyidi: {'✓ BAŞARILI' if analysis_results['identity_information'] else '✗ BAŞARISIZ'}")
        print(f"5. Emir Kipi Kontrolü: {'✓ BAŞARILI' if analysis_results['order_mode'] else '✗ BAŞARISIZ'}")
        print(f"6. Küfür Kontrolü: {'✓ TEMİZ' if analysis_results['is_clean_speech'] else '✗ KÜFÜR TESPİT EDİLDİ'}")
        
        if analysis_results['swear_words_found']:
            print("\n   Tespit Edilen Küfürler:")
            for swear in analysis_results['swear_words_found']:
                print(f"   - '{swear['word']}' ({swear['start_time']:.2f}s - {swear['end_time']:.2f}s)")
        
        print(f"\n7. İlk 30 Saniye Metni:")
        print(f"   {analysis_results['initial_30_seconds_text']}")
        
        print(f"\n8. Tam Metin:")
        print(f"   {analysis_results['full_text']}")
        print("\n" + "="*50)


        
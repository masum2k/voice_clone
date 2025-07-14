# run.py
from dat import download_and_trim
from ca import clean_audio
from syn import synthesize
from inc import increase_volume
import os

def full_pipeline(youtube_url, text, lang):
    trimmed_file = "video_trimmed.wav"
    clean_file = "video_clean.wav"
    synth_output = "klon_ses.wav"
    mastered_output = "klon_ses_mastered.wav"

    proceed_trim = True
    proceed_clean = True

    # Trim kontrolü
    if os.path.exists(trimmed_file):
        choice = input(f"⚠️ {trimmed_file} zaten var. Yeniden indirmek ve kırpmak ister misin? (y/n): ").lower()
        if choice != "y":
            proceed_trim = False
            proceed_clean = False

    # Adım 1: Ses indir/kırp
    if proceed_trim:
        print("📥 Adım 1: Ses indiriliyor ve kırpılıyor...")
        download_and_trim(youtube_url)
        proceed_clean = True

    # Adım 2: Temizleme
    if proceed_clean:
        print("🎧 Adım 2: Ses temizleniyor...")
        clean_audio()
    elif not os.path.exists(clean_file):
        print(f"❌ {clean_file} bulunamadı. Temizleme atlandı ama dosya da yok. İşlem iptal.")
        return
    else:
        print(f"⏭️ Temizleme atlandı, mevcut dosya kullanılacak: {clean_file}")

    # Adım 3: Ses klonlama
    print("🗣️ Adım 3: Ses klonlanıyor...")
    synthesize(text=text, speaker_wav=clean_file, lang=lang)

    while True:
        db_input = input("🔊 Kaç dB volume artırmak istersin? (örn: 5) (Çıkmak için 'n' gir): ").strip().lower()
        if db_input == "n":
            print("⏭️ Ses seviyesi artırma tamamlandı.")
            break
        try:
            db_value = float(db_input)
            print(f"🎚️ Volume {db_value} dB artırılıyor...")
            increase_volume(input_path="klon_ses.wav", output_path="klon_ses.wav", db_increase=db_value)
        except ValueError:
            print("❌ Geçersiz sayı girdin. Lütfen bir sayı ya da 'n' gir.")



# Örnek çağırma
full_pipeline(
    youtube_url="https://www.youtube.com/watch?v=M1O_MjMRkPg",
    text="Hello, this is a test from a tedx talk. Thank you for listening.",
    lang="en"
)

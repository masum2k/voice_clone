import librosa
import soundfile as sf
from pydub import AudioSegment, effects
import noisereduce as nr
import os


def clean_audio(input_path="video_trimmed.wav", output_path="video_clean.wav"):
 
    y, sr = librosa.load(input_path, sr=22050)
    
    # Gürültü azaltma (ilk 0.5 saniye arka plan kabul edilir)
    reduced = nr.reduce_noise(y=y, sr=sr, y_noise=y[:int(sr * 0.5)])

    # Sessizlik kırp
    reduced, _ = librosa.effects.trim(reduced, top_db=20)

    # Normalizasyon (±1)
    reduced = reduced / max(abs(reduced))

    # Geçici dosya yaz
    sf.write("temp_clean.wav", reduced, sr)

    # Mono + 16-bit normalize edilmiş ses
    clean = AudioSegment.from_wav("temp_clean.wav")
    clean = clean.set_channels(1).set_sample_width(2)
    clean = effects.normalize(clean)
    clean.export(output_path, format="wav")

    os.remove("temp_clean.wav")
    print(f"✅ Cleaned audio saved: {output_path}")

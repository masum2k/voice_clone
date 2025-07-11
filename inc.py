from pydub import AudioSegment, effects

def increase_volume(input_path="klon_ses.wav", output_path="klon_ses_loud.wav", db_increase=0):
   audio = AudioSegment.from_file(input_path)

   # Önce normalize et (ortalama RMS seviyesine göre)
   normalized_audio = effects.normalize(audio)

   # Sonra volume artır (çok agresif artırmamalı)
   louder_audio = normalized_audio + db_increase

   louder_audio.export(output_path, format="wav")
   print(f"🔊 Volume güvenli şekilde {db_increase} dB artırıldı → {output_path}")
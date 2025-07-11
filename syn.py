def synthesize(text, speaker_wav="video_clean.wav", output_path="klon_ses.wav", lang=""):
    from TTS.api import TTS
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"
    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

    tts.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,
        language=lang,
        file_path=output_path
    )
    print(f"✅ Synthesized audio saved: {output_path}")

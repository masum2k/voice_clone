def download_and_trim(youtube_url, output_path="video_trimmed.wav", trim_sec=10):
    import yt_dlp
    import ffmpeg
    import os

    temp_file = "temp.m4a"

    # YouTube’dan ses indir (m4a formatında)
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
        'outtmpl': temp_file,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    if not os.path.exists(temp_file):
        raise FileNotFoundError("❌ temp.m4a dosyası oluşmadı, indirme başarısız.")

    # Süreyi al
    try:
        probe = ffmpeg.probe(temp_file)
        duration = float(probe['format']['duration'])
    except Exception as e:
        raise RuntimeError("❌ ffprobe başarısız. ffmpeg sistemine kurulu mu?") from e

    # Kırp
    start = trim_sec
    end = duration - trim_sec
    if end <= start:
        raise ValueError("❌ Video çok kısa, kırpılamaz.")

    ffmpeg.input(temp_file, ss=start, t=end-start).output(
        output_path, ac=1, ar=22050, format='wav', acodec='pcm_s16le', loglevel='quiet'
    ).overwrite_output().run()

    os.remove(temp_file)
    print(f"✅ Trimmed audio saved: {output_path}")

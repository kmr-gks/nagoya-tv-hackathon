import numpy as np
import pyaudio
import time

SAMPLE_RATE=44100

def play_sound(s: pyaudio.Stream, freq: float, duration: float):
   # 指定周波数のサイン波を指定秒数分生成
   samples = np.sin(np.arange(int(duration * SAMPLE_RATE)) * freq * np.pi * 2 / SAMPLE_RATE)
   # ストリームに渡して再生
   s.write(samples.astype(np.float32).tobytes())

start = time.time()
# PyAudio開始
p = pyaudio.PyAudio()
# ストリームを開く
stream = p.open(format=pyaudio.paFloat32,
               channels=1,
               rate=SAMPLE_RATE,
               frames_per_buffer=1024,
               output=True)
for j in range(100):
    for i in range(3):
        play_sound(stream,6600+i*300,0.02)
    for i in range(3):
        play_sound(stream,7500+i*300,0.02)
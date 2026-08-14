from pathlib import Path
import wave
import av

VIDEO = Path(__file__).with_name("American Dad Intro - For Speedruns.mp4")
AUDIO = Path(__file__).with_name("American Dad Intro Audio.wav")

container = av.open(str(VIDEO))
stream = container.streams.audio[0]
resampler = av.audio.resampler.AudioResampler(format="s16", layout="stereo", rate=44100)
raw = bytearray()
try:
    for frame in container.decode(stream):
        for converted in resampler.resample(frame):
            raw.extend(converted.to_ndarray().tobytes())
    for converted in resampler.resample(None):
        raw.extend(converted.to_ndarray().tobytes())
finally:
    container.close()

with wave.open(str(AUDIO), "wb") as output:
    output.setnchannels(2)
    output.setsampwidth(2)
    output.setframerate(44100)
    output.writeframes(bytes(raw))
print(f"saved {AUDIO} ({len(raw)} bytes)")

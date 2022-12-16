import silero, torch, time
import sounddevice as sd
import time, torchaudio

#silero - text to voice
language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'aidar'  # aidar, baya, kseniya, xenia, random
put_accent = True
put_yo = True
device = torch.device('cpu')

text = 'В недрах тундры выдры в г+етрах т+ырят в вёдра ядра кедров.'
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)

model.to(device)
audio = model.save_wav(text=text,
                       speaker=speaker,
                       sample_rate=sample_rate,
                       put_accent=put_accent,
                       put_yo=put_yo)
# torchaudio.save('test.wav', audio.waveform, sample_rate)
print(audio)
sd.play(audio, sample_rate)
time.sleep(len(audio)/sample_rate)
sd.stop()
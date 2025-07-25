import torch

# silero - text to voice
language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'xenia'  # aidar, baya, kseniya, xenia, random
put_accent = True
put_yo = True
device = torch.device('cpu')
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts',
                          language=language, speaker=model_id)
model.to(device)


def make_audio(text, speak=speaker, path='audio/result.wav'):
    audio = model.save_wav(text=text,
                           speaker=speak,
                           sample_rate=sample_rate,
                           put_accent=put_accent,
                           put_yo=put_yo,
                           audio_path=path)
    return audio

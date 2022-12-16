from aiogram import Bot, types
from aiogram.types import ContentType
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from random import randint
import soundfile as sf
import speech_recognition as sr
import silero, torch, json, sqlite3, librosa, wave
from vosk import Model, KaldiRecognizer


# bot consts
BOT_TOKEN = '5826331306:AAGsZGkD2dtC9s78yfg-A4A4kZbj_ekQbNY'
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# silero - text to voice
language = 'ru'
model_id = 'ru_v3'
sample_rate = 48000
speaker = 'aidar'  # aidar, baya, kseniya, xenia, random
put_accent = True
put_yo = True
device = torch.device('cpu')
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts',
                          language=language, speaker=model_id)
model.to(device)

# generate_joke
joke_cursor = sqlite3.connect("base.db").cursor()
joke_list = []


# speech to text
rate = 44100
speech_model = Model('small model')
rec = KaldiRecognizer(speech_model, rate)


def get_joke():
    if len(joke_list):
        res = joke_list[-1]
        joke_list.pop()
        return res
    else:
        for i in range(100):
            ID = randint(1, 129900)  # range id
            text = joke_cursor.execute(f"SELECT text FROM anek WHERE id='{ID}'").fetchall()[0][0]
            text = text.replace('\\n', '\n')
            joke_list.append(text)
        return get_joke()


def make_audio(text):
    audio = model.save_wav(text=text,
                           speaker=speaker,
                           sample_rate=sample_rate,
                           put_accent=put_accent,
                           put_yo=put_yo)
    return audio

@dp.message_handler(commands=['tell_joke'])
async def tell_a_joke(message: types.Message):
    audio = make_audio(get_joke())
    await message.answer_voice(open(audio, 'rb'))


@dp.message_handler(commands=['read_joke'])
async def read_a_joke(message: types.Message):
    await message.answer(get_joke())


@dp.message_handler(content_types=[ContentType.VOICE])
async def speech_to_text(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    path = file.file_path
    await bot.download_file(path, 'voice.wav')
    x, _ = librosa.load('voice.wav', sr=rate)
    sf.write('voice.wav', x, rate)
    wf = wave.open('tmp.wav', 'rb')
    result = ""
    last_n = False
    while True:
        data = wf.readframes(rate)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            res = json.loads(rec.Result())
            if res['text'] != '':
                result += f" {res['text']}"
                last_n = False
            elif not last_n:
                result += '\n'
                last_n = True
    res = json.loads(rec.FinalResult())
    result += res['text']
    if result:
        await message.answer(result)
        # await message.answer_voice(open(make_audio(result), 'rb'))

executor.start_polling(dp, skip_updates=True)
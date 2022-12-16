from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from random import randint
import silero, torch, time, torchaudio
import sqlite3


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


@dp.message_handler(commands=['tell_joke'])
async def tell_a_joke(message: types.Message):
    print(1)
    audio = model.save_wav(text=get_joke(),
                           speaker=speaker,
                           sample_rate=sample_rate,
                           put_accent=put_accent,
                           put_yo=put_yo)
    await message.answer_voice(open(audio, 'rb'))


@dp.message_handler(commands=['read_joke'])
async def read_a_joke(message: types.Message):
    print(2)
    await message.answer(get_joke())


executor.start_polling(dp, skip_updates=True)
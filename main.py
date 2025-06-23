from aiogram import Bot, types
from aiogram.types import ContentType
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import soundfile as sf
import librosa
from JokesGen import *
from TextToSpeech import *
from SpeechToText import *

# bot consts
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


async def download_file(message: types.Message):
    file_id = message.voice.file_id
    file = await bot.get_file(file_id)
    path = file.file_path
    await bot.download_file(path, 'audio/voice.wav')
    x, _ = librosa.load('audio/voice.wav', sr=rate)
    sf.write('audio/voice.wav', x, rate)


@dp.message_handler(commands=['tell_joke'])
async def tell_a_joke(message: types.Message):
    s = get_joke().split('\n')
    speakers = ['aidar', 'xenia']
    for i in range(len(s)):
        audio = make_audio(s[i], speak=speakers[i % 2], path=f'voice{i}.wav')
        await message.answer_voice(open(audio, 'rb'))


@dp.message_handler(commands=['read_joke'])
async def read_a_joke(message: types.Message):
    await message.answer(get_joke())


@dp.message_handler(content_types=[ContentType.VOICE])
async def voice_message(message: types.Message):
    await download_file(message)
    text = await speech_to_text(message)
    if text:
        await message.answer(text)


executor.start_polling(dp, skip_updates=True)

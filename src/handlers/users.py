import logging
import base64
import os

from io import BytesIO
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from mistralai import Mistral

from lexicon.lexicon import lexicon_ru
from service.service import mp4_to_mp3
from service.service import get_summary, get_transcribe

router = Router()
logger = logging.getLogger(__name__)

@router.message(Command(commands='start'))
async def process_start_command(message: Message):
    await message.answer(lexicon_ru['/start'])


@router.message(F.voice)
async def process_voice_message(message: Message, client: Mistral, model: str, voice_model: str):
    try:
        audio = await message.bot.download(file=message.voice.file_id)
    except Exception as ex:
        logger.error('Unable to download voice file')
        await message.reply(lexicon_ru['error'])
        raise ex
    
    audio_base64 = base64.b64encode(audio.read()).decode('UTF-8')
    transcribed = get_transcribe(client, voice_model, audio_base64)

    if message.chat.type == 'group' and message.voice.duration > 35:
        await message.reply(lexicon_ru['presummary'] + get_summary(client, model, transcribed))
    else:
        await message.reply(lexicon_ru['pre'] + transcribed)

@router.message(F.video_note)
async def process_video_note(message: Message, client: Mistral, model: str, voice_model: str):
    vid_filename = f'src/service/{message.from_user.id}video.mp4'
    aud_filename = f'src/service/{message.from_user.id}audio.mp3'

    try:
        await message.bot.download(file=message.video_note.file_id, destination=vid_filename)
    except Exception as ex:
        logger.error('Unable to download video note file')
        await message.reply(lexicon_ru['error'])
        raise ex 
    
    mp4_to_mp3(vid_filename, aud_filename)
    with open(aud_filename, 'rb') as file:
        audio = file.read()
    
    audio_base64 = base64.b64encode(audio).decode('UTF-8')
    transcribed = get_transcribe(client, voice_model, audio_base64)

    os.remove(vid_filename)
    os.remove(aud_filename)

    if message.chat.type == 'group' and message.video_note.duration > 35:
        await message.reply(lexicon_ru['presummary'] + get_summary(client, model, transcribed))
    else:
        await message.reply(lexicon_ru['pre'] + transcribed)



    

     











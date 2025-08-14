from moviepy import AudioFileClip
from mistralai import Mistral

def mp4_to_mp3(mp4_path: str, mp3_path: str):
    convert = AudioFileClip(mp4_path)
    convert.write_audiofile(mp3_path)
    convert.close()

def get_transcribe(client: Mistral, model: str, audio_base64: str) -> str:
    chat_response = client.chat.complete(
        model=model,
        messages=[{
            'role': 'user',
            'content': [
                {
                    'type': 'input_audio',
                    'input_audio': audio_base64,
                },
                {
                    'type': 'text',
                    'text': 'Сделай транскрипцию этого файла. '
                            'Если там ничего нет, пиши, что сообщение нераспознано'
                },
            ]
        }], 
    )
    return str(chat_response.choices[0].message.content)

def get_summary(client: Mistral, model: str, text: str):
    chat_response = client.chat.complete(
        model= model,
        messages = [
            {
                'role': 'user',
                'content': 'Ты должен дать краткое описание сообщения в 1-2 предложениях. '
                           'Ответ дай на русском языке.',
            },
            {
                'role': 'user',
                'content': text,
            }
        ]
    )
    return str(chat_response.choices[0].message.content)



from telethon import TelegramClient, events
import os, requests

bot_token = "5946485700:AAFu_SjKPnNDRfOin72o3qvxWpsazXJ0o34"
api_id = 18463233                                                      #
api_hash = '15894f2ce7830cef36913f109377da1a'  




client = TelegramClient('uploader123bot', api_id, api_hash)
client.start(bot_token=bot_token)





def convert_bytes(num_bytes):
    for unit in ['bytes', 'KB', 'MB', 'GB']:
        if num_bytes < 1024.0:
            return f"{num_bytes:.2f} {unit}"
        num_bytes /= 1024.0


async def progress_callback(current, total, chat_id, msg_id):
    progress = f'{round(current / total * 100, 1)}%'
    new_message = f'Uploading... {progress}\n{convert_bytes(current)} of {convert_bytes(total)}'
    await client.edit_message(chat_id, msg_id, new_message)


@client.on(events.NewMessage)
async def new_handler(event):
  user_id = event.sender_id
  text = event.raw_text

  if text == '/id' or text ==  'id':
    await event.respond(f'Your User ID is: {user_id}')
  elif '/upload' in text:
            msg = await event.respond('Processing')
            try:
                filename = text.split('\n')[1]
                url = text.split('\n')[2]
                r = requests.get(url)
                if not os.path.exists('iammrnewtonbot'):
                    os.mkdir('iammrnewtonbot')
                with open(f'iammrnewtonbot/{filename}', 'wb') as f:
                    f.write(r.content)
                await client.send_file(
                    user_id,
                    f'iammrnewtonbot/{filename}',
                    force_document=True,
                    progress_callback=lambda current, total: progress_callback(
                        current, total, event.chat_id, msg.id)
                )
                await client.edit_message(event.chat_id, msg.id, 'Here you go')
                if os.path.exists(f'iammrnewtonbot/{filename}'):
                    os.remove(f'iammrnewtonbot/{filename}')

            except Exception as e:
                await client.send_message(str(e), 1612078205)
                await event.respond('An error occured')
  

client.run_until_disconnected()

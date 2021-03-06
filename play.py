import os
import asyncio
from pytgcalls import GroupCallFactory
from pyrogram import filters, Client, idle
from pyrogram.types import Message
from config import API_ID, API_HASH, SESSION_NAME

app = Client(SESSION_NAME, API_ID, API_HASH)
group_call_factory = GroupCallFactory(app, GroupCallFactory.MTPROTO_CLIENT_TYPE.PYROGRAM)
VIDEO_CALL = {}



@app.on_message(filters.outgoing & filters.command('live'))
async def stream(client, m: Message):
    replied = m.reply_to_message
    if not replied:
        await m.reply("â **Bales Ke video KONTOL!!**")
    elif replied.video or replied.document:
        msg = await m.reply("đĨ **Mulai Mengunduh Video Bokep**")
        chat_id = m.chat.id
        try:
            video = await client.download_media(m.reply_to_message)
            await msg.edit("đ **Sabar Ngentod Lagi Proses**")
            os.system(f'ffmpeg -i "{video}" -vn -f s16le -ac 2 -ar 48000 -acodec pcm_s16le -filter:a "atempo=0.81" vid-{chat_id}.raw -y')
            print()
        except Exception as e:
            await msg.edit(f"**đĢ Mampus Error Pukie** - `{e}`")
        await asyncio.sleep(5)
        try:
            group_call = group_call_factory.get_file_group_call(f'vid-{chat_id}.raw')
            await group_call.start(chat_id)
            await group_call.set_video_capture(video)
            VIDEO_CALL[chat_id] = group_call
            await msg.edit("**đĨ Memulai Live Show!**")
            print()
        except Exception as e:
            await msg.edit(f"**Error** -- `{e}`")
    else:
        await m.reply("â **Balas Ke Video Bego!!**")

@app.on_message(filters.outgoing & filters.command('mati'))
async def stopvideo(client, m: Message):
    chat_id = m.chat.id
    try:
        await VIDEO_CALL[chat_id].stop()
        await m.reply("**âšī¸ Berhenti Oncam!**")
    except Exception as e:
        await m.reply(f"**đĢ Mampus Error Tolol** - `{e}`")

app.start()
print('>>> VC VIDEO USERBOT STARTED')
idle()
app.stop()
print('>>> VC VIDEO USERBOT STOPPED')

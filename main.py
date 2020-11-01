from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from re import sub
from os import getenv
from dotenv import load_dotenv

load_dotenv()

api_id = getenv("API_ID")
api_hash = getenv("API_HASH")
print(api_id, api_hash)
client = TelegramClient('Rhons', api_id, api_hash)

async def main():
    # Now you can use all client methods listed below, like for example...
    group_hash = await clean_text("https://t.me/joinchat/AAAAAEY2iZcPaaYC5ix6kg")
    print(group_hash)
    print("AAAAAEY2iZdlXuLKgtTUUA")
#    updates = await client(ImportChatInviteRequest('AAAAAEY2iZdlXuLKgtTUUA'))
    
    updates = await client(ImportChatInviteRequest(group_hash))
#    updates2 = await client(JoinChannelRequest('https://t.me/tg_bot_feader_test'))

async def clean_text(text):
    del_text = "https://t.me/joinchat/"
    new_text = sub(del_text, '', text)
    return new_text

with client:
    client.loop.run_until_complete(main())

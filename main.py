from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from re import sub, search
from os import getenv
from dotenv import load_dotenv

load_dotenv()

api_id = getenv("API_ID")
api_hash = getenv("API_HASH")

client = TelegramClient('Rhons', api_id, api_hash)
client.parse_mode = "html"
#sync def main():
#   updates2 = await client(JoinChannelRequest('https://t.me/tg_bot_feader_test'))


@client.on(events.NewMessage(pattern='\w{1,10} \w{1,10} https://t.me/joinchat/\w'))
async def start(event):
    message = event.message.message
    links = search("https://t.me/joinchat/\w{1,23}", message)
    print(links)
    link = links.group(0)
    print(link)
    group_hash = await clean_text(link)
    print("Try to add chat " + group_hash)
    try:
        updates = await client(ImportChatInviteRequest(group_hash))
        chanel_title = updates.chats[0].title
        message_text =  "Chat <a href='" + link + "'>" + chanel_title + "</a> add"
        await event.respond(message_text)
    except:
        await event.respond("Chat alredy existed")
    raise events.StopPropagation
        
async def clean_text(text):
    del_text = "https://t.me/joinchat/"
    new_text = sub(del_text, '', text)
    return new_text

with client:
    print("client start")
    client.run_until_disconnected()


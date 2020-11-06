from telethon import TelegramClient, events
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import JoinChannelRequest
from re import sub, search
from os import getenv
from dotenv import load_dotenv
import sqlite3
load_dotenv()

api_id = getenv("API_ID")
api_hash = getenv("API_HASH")

client = TelegramClient('Rhons', api_id, api_hash)
client.parse_mode = "html"

db_connect = sqlite3.connect("tg_sqlite.db")
cursor = db_connect.cursor()

@client.on(events.NewMessage(pattern='.{1,10} .{1,10} https://t.me/\w{1,30}'))
async def start(event):
    message = event.message.message
    print(message)
    try:
        end_channel_id = event.message.peer_id.channel_id
    except:
        end_channel_id = event.message.peer_id.chat_id
    links = search("https://t.me/joinchat/.{1,23}", message)
    if bool(links):
        link = links.group(0)
        group_hash = await clean_text_privat(link)
        print("Try to add chat " + group_hash)
        try:
            updates = await client(ImportChatInviteRequest(group_hash))
            chanel_title,chanel_id,message_text = await generate_link(link,updates)
            await event.respond(message_text)
        except:
            await event.respond("Chat alredy existed")
    else:
        links = search("https://t.me/.{1,40}", message)
        link = links.group(0)
        print("Try to add chat " + link)
        try:
            updates = await client(JoinChannelRequest(link))
            chanel_title,chanel_id,message_text = await generate_link(link,updates)
            await event.respond(message_text)
        except:
            await event.respond("Chat alredy existed")        
    cursor.execute("insert into tg_channel (title,id,url,end_channel_id) values (?, ?, ?, ?)",(chanel_title,chanel_id,link,end_channel_id))
    db_connect.commit()
    raise events.StopPropagation


async def generate_link(link,updates):
    print(updates.chats[0])
    chanel_title = updates.chats[0].title
    chanel_id = updates.chats[0].id
    message_text =  "Chat <a href='" + link + "'>" + chanel_title + "</a> add"
    return chanel_title,chanel_id,message_text
    
@client.on(events.NewMessage())
async def handler(event):
    channel_id = event.message.peer_id.channel_id
    print(channel_id)
    sql = "SELECT end_channel_id FROM tg_channel WHERE id=?"
    cursor.execute(sql, [(channel_id)])
    result = cursor.fetchone()
    result_int = int(result[0])
    await client.send_message(result_int, event.message )
        
async def clean_text_privat(text):
    del_text = "https://t.me/joinchat/"
    new_text = sub(del_text, '', text)
    return new_text



def main():
    cursor.execute("""CREATE TABLE IF NOT EXISTS tg_channel (title text, id text, url text, end_channel_id text)""")
    with client:
        print("client start")
        client.run_until_disconnected()

if __name__ == '__main__':
    main()

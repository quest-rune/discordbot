import discord, random, os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()


queue_for_help = []


class Fakeuser:
    def __init__(self, name) -> None:
        self.name = name
        

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


async def get_help(message):
    if message.author not in queue_for_help:
        queue_for_help.append(message.author)
    number_in_line = queue_for_help.index(message.author) + 1
    return_message = f"You are queued for help. You are number {number_in_line}"
    await message.channel.send(return_message)

async def print_queue(message):
    await message.channel.send(" - ".join(list(map(lambda r : r.name,queue_for_help))))

async def enqueue(message):
    name = str(round(random.random()*100))
    fakeuser = Fakeuser(name)
    queue_for_help.append(fakeuser)
    number_in_line = queue_for_help.index(fakeuser) + 1
    return_message = f"You are queued for help. You are number {number_in_line}"
    await message.channel.send(return_message)


message_commands = {
    "!gethelp" : lambda message: get_help(message),
    "!printqueue" : lambda message: print_queue(message),
    "enqueue" : lambda message: enqueue(message)

}


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(message.content):
        await message_commands[message.content](message)
        
        
client.run(os.getenv('TOKEN'))

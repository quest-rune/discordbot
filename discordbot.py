import discord, random, os
from dotenv import load_dotenv
from collections import deque

load_dotenv()

client = discord.Client()

queue_for_help = deque()

@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")


#fake functions
async def enqueue(message):
    name = str(round(random.random()*100))
    fakeuser = Fakeuser(name)
    queue_for_help.append(fakeuser)
    number_in_line = queue_for_help.index(fakeuser) + 1
    return_message = f"You are queued for help. You are number {number_in_line}"
    await message.channel.send(return_message)

class Fakeuser:
    def __init__(self, name) -> None:
        self.name = name
        

#User functions
async def get_help(message):
    if message.author not in queue_for_help:
        queue_for_help.append(message.author)
    number_in_line = queue_for_help.index(message.author) + 1
    return_message = f"You are queued for help. You are number {number_in_line}"
    await message.channel.send(return_message)

#"admin" role functions
async def print_queue(message):
    if len(queue_for_help) < 1:
        return await message.channel.send("Queue is empty")
    await message.channel.send(" - ".join(list(map(lambda r : str(r[0] + 1) + ": " + r[1].name, enumerate(queue_for_help)))))


async def dequeue(message):
    if len(queue_for_help) < 1:
        return await message.channel.send("Queue is empty")
    popped = queue_for_help.popleft()
    return_message = f"Player {popped.name} is getting help"
    await message.channel.send(return_message)

message_commands = {
    "!get" : lambda message: get_help(message),
    "!print" : lambda message: print_queue(message),
    "!enq" : lambda message: enqueue(message),
    "!deq" : lambda message: dequeue(message),
    "!help" : lambda message: print_commands(message)

}
async def print_commands(message):
    return_message = "Command\n"
    return_message += "\n".join(message_commands)
    await message.channel.send(return_message)







@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(message.content):
        if message_commands.get(message.content) is not None:
            await message_commands.get(message.content)(message)
        
        
client.run(os.getenv('TOKEN'))

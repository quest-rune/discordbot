import discord, queue
import os
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()


queue_for_help = []


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")

number_in_line = 0


message_commands = {
    "!gethelp" : lambda : f"You are queued for help. You are number {number_in_line}",
    "!print" : lambda : f"Size of queue {len(queue_for_help)}"
}

@client.event
async def on_message(message):
    global number_in_line
    if message.author == client.user:
        return
    if message.content.startswith(message.content):
        if message.author not in queue_for_help:
            queue_for_help.append(message.author)
        number_in_line = queue_for_help.index(message.author) + 1
        await message.channel.send(message_commands[message.content]())
        

client.run(os.getenv('TOKEN'))

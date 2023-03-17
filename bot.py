import os
import discord
import openai
import nest_asyncio
import conf

nest_asyncio.apply()

DISCORD_TOKEN = conf.DISCORD_TOKEN
OPENAI_API_KEY = conf.OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

class ChatBot(discord.Client):
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')
    
    async def on_message(self,message):
        if message.author == self.user:
            return
        
        input_content = [message.content]
        
        if message.attachments:
            for attachment in message.attachments:
                image_bytes = await attachment.read()
                input_content.append({'image': image_bytes})
                
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message.content},
    ],
    max_tokens=150,
    n=1,
    stop=None,
    temperature=0.5,
)        
        
        assistant_response = response['choices'][0]['message']['content']
        await message.channel.send(assistant_response)
        
client = ChatBot(intents=intents)
client.run(DISCORD_TOKEN)
            
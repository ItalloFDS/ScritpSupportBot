import discord
import openai
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'🤖 Bot conectado como {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if client.user.mentioned_in(message):
        question = message.content.replace(f"<@{client.user.id}>", "").strip()

        if question == "":
            await message.channel.send("Oi! Como posso ajudar?")
            return

        await message.channel.send("✍️ Pensando...")

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": question}],
                temperature=0.7,
                max_tokens=150
            )
            reply = response.choices[0].message.content
            await message.channel.send(reply)
        except Exception as e:
            print("Erro:", e)
            await message.channel.send("❌ Ocorreu um erro ao consultar o ChatGPT.")

client.run(DISCORD_TOKEN)

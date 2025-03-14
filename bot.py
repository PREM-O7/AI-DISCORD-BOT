import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API keys from environment variables
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY")
CHAT_API_URL = os.getenv("CHAT_API_URL")
IMAGE_API_URL = os.getenv("IMAGE_API_URL")

# Enable intents
intents = discord.Intents.default()
intents.message_content = True  # Important for message reading

# Create bot instance
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot Ready Event
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

# Ping Command
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong! `{round(bot.latency * 1000)}ms`")

# Chat Command
@bot.command()
async def chat(ctx, *, message: str):
    """AI Chatbot"""
    response = requests.post(CHAT_API_URL, json={"message": message})
    if response.status_code == 200:
        reply = response.json().get("reply", "Sorry, I couldn't process that.")
    else:
        reply = "⚠️ Chatbot API error."
    
    await ctx.send(reply)

# Image Generation Command
@bot.command()
async def image(ctx, *, query: str):
    """Fetch image from Pexels"""
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1}
    
    response = requests.get(IMAGE_API_URL, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            image_url = data["photos"][0]["src"]["original"]
            await ctx.send(image_url)
        else:
            await ctx.send("❌ No images found.")
    else:
        await ctx.send("⚠️ Image API error.")

# Run the bot
bot.run(DISCORD_TOKEN)

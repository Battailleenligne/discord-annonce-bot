import os
import discord
from discord.ext import commands
from discord.utils import get
from flask import Flask
from threading import Thread

# --- Serveur web pour Render + UptimeRobot ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Intents Discord ---
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True

bot = commands.Bot(command_prefix="!", intents=intents)

# --- Dictionnaire pour stocker les canaux de partie ---
game_channels = {}

# --- Quand le bot est prêt ---
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")

# --- Fonction pour créer le canal de partie ---
async def create_game_channel(message):
    guild = message.guild
    author = message.author
    # Nom du canal : Partie-username
    channel_name = f"partie-{author.name}"
    
    # Crée le canal texte privé
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        author: discord.PermissionOverwrite(read_messages=True)
    }
    
    channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
    game_channels[channel.id] = author.id
    await channel.send(f"{author.mention}, votre canal de partie est prêt ! 🎯")
    
    # Invite les joueurs via réaction
    await message.add_reaction("🎲")  # Les joueurs réagissent avec cet émoji

# --- Sur réaction ajoutée pour donner accès au canal ---
@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    message = reaction.message
    if reaction.emoji == "🎲":
        # Vérifie si le message correspond à un canal de partie
        for channel_id, owner_id in game_channels.items():
            if message.channel.id == message.channel.id:  # Le message original
                channel = bot.get_channel(channel_id)
                await channel.set_permissions(user, read_messages=True)
                await channel.send(f"{user.mention} a rejoint la partie ! 🎮")

# --- Détecte les messages avec "Fiche de Recherche de Partie" ---
@bot.event
async def on_message(message):
    if message.author.bot:
        return
    if "Fiche de Recherche de Partie" in message.content:
        await create_game_channel(message)
    await bot.process_commands(message)

# --- Commande ping pour tester ---
@bot.command()
async def ping(ctx):
    await ctx.send("Pong 🏓")

# --- Lancer serveur + bot ---
keep_alive()
bot.run(os.environ['TOKEN'])

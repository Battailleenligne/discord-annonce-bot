import discord
from discord.ext import commands
import os

# Activer les intents nécessaires
intents = discord.Intents.default()
intents.message_content = True
intents.members = True  # Pour gérer les permissions et salons privés

bot = commands.Bot(command_prefix="!", intents=intents)

# Quand le bot est prêt
@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

# Détecter les messages avec le format de recherche de partie
@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return

    # Vérifier si le message commence bien par "Fiche de Recherche de Partie"
    if message.content.startswith("Fiche de Recherche de Partie"):
        guild = message.guild

        # Créer un salon privé
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            message.author: discord.PermissionOverwrite(read_messages=True, send_messages=True)
        }

        channel_name = f"partie-de-{message.author.name}".lower()
        channel = await guild.create_text_channel(channel_name, overwrites=overwrites)

        await channel.send(f"{message.author.mention}, votre canal de partie est prêt ! 🎯\n"
                           "Les joueurs pourront le rejoindre en réagissant avec 🎲 à ce message.")

        # Ajouter une réaction pour que les autres puissent rejoindre
        sent_message = await channel.send("Réagissez avec 🎲 pour rejoindre cette partie.")
        await sent_message.add_reaction("🎲")

    await bot.process_commands(message)

# Gestion des réactions pour donner accès
@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    if payload.emoji.name != "🎲":
        return

    guild = bot.get_guild(payload.guild_id)
    channel = guild.get_channel(payload.channel_id)
    member = guild.get_member(payload.user_id)

    if member is None or member.bot:
        return

    await channel.set_permissions(member, read_messages=True, send_messages=True)
    await channel.send(f"{member.mention} a rejoint la partie 🎉")

# Lancer le bot avec le token stocké dans Render
bot.run(os.environ['TOKEN'])

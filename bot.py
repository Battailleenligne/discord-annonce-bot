import discord
from discord.ext import commands

# =========================
# CONFIGURATION
# =========================
ANNONCE_CHANNEL_ID = 1404546569667346444  # Remplace par l’ID du canal annonces
REACTION_EMOJI = "🎲"  # Emoji pour rejoindre la partie
TOKEN = "MTQwNDU3MzIzOTYwMjE4ODM5OQ.GzsRO-.C0qTxC_YnNqeSSNIH2ir-qeSKDFbNaavKP0Ku4"  # Remplace par ton nouveau token

# =========================
# INTENTS (autorisations)
# =========================
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True  # Lecture du contenu des messages
intents.guilds = True
intents.members = True  # Voir la liste des membres

bot = commands.Bot(command_prefix="!", intents=intents)


# =========================
# ÉVÉNEMENTS
# =========================
@bot.event
async def on_ready():
    print(f"✅ Connecté en tant que {bot.user}")


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    # Vérifie que le message est dans le canal d'annonces et contient la fiche
    if message.channel.id == ANNONCE_CHANNEL_ID and "Fiche de Recherche de Partie" in message.content:
        await create_game_channel(message)
        await message.add_reaction(REACTION_EMOJI)

    await bot.process_commands(message)


async def create_game_channel(message):
    guild = message.guild
    overwrites = {
        guild.default_role: discord.PermissionOverwrite(read_messages=False),
        message.author: discord.PermissionOverwrite(read_messages=True),
        guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True)  # ⬅ Le bot peut écrire
    }
    channel_name = f"partie-de-{message.author.name}".replace(" ", "-").lower()

    # Crée le canal privé
    channel = await guild.create_text_channel(channel_name, overwrites=overwrites)
    await channel.send(f"{message.author.mention}, votre canal de partie est prêt ! 🎯")


@bot.event
async def on_raw_reaction_add(payload):
    # Ignore les réactions du bot
    if payload.user_id == bot.user.id:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    # Récupère le message d'origine
    channel = guild.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)

    # Vérifie que c'est une fiche et que c'est le bon emoji
    if "Fiche de Recherche de Partie" in message.content and str(payload.emoji) == REACTION_EMOJI:
        channel_name = f"partie-de-{message.author.name}".replace(" ", "-").lower()
        private_channel = discord.utils.get(guild.channels, name=channel_name)
        if private_channel:
            await private_channel.set_permissions(member, read_messages=True)
            await private_channel.send(f"{member.mention} a rejoint la partie ! 🚀")


# =========================
# LANCEMENT DU BOT
# =========================
bot.run(TOKEN)

import discord
from discord import app_commands
from discord.ext import commands
import os
# Le token est stocké dans une variable d'environnement sur Render
TOKEN = os.environ['DISCORD_TOKEN']
GUILD_ID = 1404025528280682516  # Remplace par l'ID de ton serveur pour test

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Liste des choix
JEUX_CHOICES = [
    "Blood Bowl", "Bolt Action", "Game of Thrones", "Middle Earth",
    "One Page Rules", "Ronin", "Saga", "Star Wars Legion",
    "Star Wars Armada", "Trench Crusade", "Warhammer 40k",
    "Warhammer TOW", "Warhammer AOS", "Horus Heresy"
]

TYPE_JEU_CHOICES = ["Compétitif", "Casual", "Scénario maison", "Scénario Officiel", 
                    "Scénario Historique", "Campagne", "Initiation", "Découverte"]

TYPE_ARMEE_CHOICES = ["Près faite", "Apporté", "A construire"]

NIVEAU_CHOICES = ["Novice", "Découvreur", "Débutant", "Confirmé", "Expert", "Ouvert à tous"]

VTT_CHOICES = ["Tabletop Simulator", "Vassal", "Autre"]

# Création du modal (formulaire)
class AnnonceModal(discord.ui.Modal, title="Création d'annonce de partie"):
    jeux = discord.ui.Select(
        placeholder="Choisir le jeu",
        options=[discord.SelectOption(label=j) for j in JEUX_CHOICES]
    )
    type_jeu = discord.ui.Select(
        placeholder="Type de jeu",
        options=[discord.SelectOption(label=t) for t in TYPE_JEU_CHOICES]
    )
    taille = discord.ui.TextInput(label="Taille de la partie", placeholder="Ex: 500 pts")
    type_armées = discord.ui.Select(
        placeholder="Type d'armées",
        options=[discord.SelectOption(label=t) for t in TYPE_ARMEE_CHOICES]
    )
    nb_joueurs = discord.ui.TextInput(label="Nombre de joueurs", placeholder="Ex: 2")
    niveau = discord.ui.Select(
        placeholder="Niveau des joueurs",
        options=[discord.SelectOption(label=n) for n in NIVEAU_CHOICES]
    )
    date = discord.ui.TextInput(label="Date", placeholder="Ex: 13/08/2025")
    horaire = discord.ui.TextInput(label="Horaire", placeholder="Ex: 20h")
    nb_sessions = discord.ui.TextInput(label="Nombre de sessions", placeholder="Ex: 1")
    vtt = discord.ui.Select(
        placeholder="VTT utilisé",
        options=[discord.SelectOption(label=v) for v in VTT_CHOICES]
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Nouvelle annonce de partie", color=discord.Color.blue())
        embed.add_field(name="Jeu", value=self.jeux.values[0], inline=True)
        embed.add_field(name="Type de jeu", value=self.type_jeu.values[0], inline=True)
        embed.add_field(name="Taille de la partie", value=self.taille.value, inline=True)
        embed.add_field(name="Type d'armées", value=self.type_armées.values[0], inline=True)
        embed.add_field(name="Nombre de joueurs", value=self.nb_joueurs.value, inline=True)
        embed.add_field(name="Niveau", value=self.niveau.values[0], inline=True)
        embed.add_field(name="Date", value=self.date.value, inline=True)
        embed.add_field(name="Horaire", value=self.horaire.value, inline=True)
        embed.add_field(name="Nombre de sessions", value=self.nb_sessions.value, inline=True)
        embed.add_field(name="VTT utilisé", value=self.vtt.values[0], inline=True)
        await interaction.response.send_message(embed=embed)

# Commande slash
@bot.tree.command(name="annonce", description="Créer une annonce de partie", guild=discord.Object(id=GUILD_ID))
async def annonce(interaction: discord.Interaction):
    await interaction.response.send_modal(AnnonceModal())

# Synchronisation des commandes
@bot.event
async def on_ready():
    await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
    print(f"Connecté en tant que {bot.user}")

bot.run(TOKEN)



import asyncio
import discord #import du module
from discord.ext import commands
import requests # Pour les appels API
import random

# Token pour l'API

# La liste des mots bannis dans l'application
BLACK_LIST = [
    "insulte",
    "méchant",
]

# Le nombre maximun d'avertissement avant explusition de l'utilisateur
MAX_WARN = 3

# Map pour stocker les avertissements des utilisateurs
WARN = {}

last_member_join = None

#Intents
intents = discord.Intents().all()
bot = commands.Bot(command_prefix="!", intents=intents)
intents.message_content = True
# guilds = serveurs discords
intents.guilds = True
intents.members = True

async def warn_user(message) : 
    '''
    Fonction qui nous permets de warn et d'explusé un utilisateur en fonction de ses avertissements.
    '''
    # On vérifie que l'utilisateur est dans notre map et on incrémente son nombre de warn
    if message.author not in WARN :
        WARN[message.author] = 1
    else :   
        WARN[message.author] = WARN[message.author]+1
    
    # Dernier message avant l'expulsion 
    if WARN[message.author] == MAX_WARN-1 : 
        await message.author.send(f"Vous serez expulsé du serveur au prochain warn !")

    # Explusion de l'utilisateur s'il atteint le nombre maximum de warn
    if WARN[message.author] >= MAX_WARN:
         await message.author.kick(reason="Avertissements multiples")

    # Message générique pour dire que le message de l'utilisateur à été supprimer
    await message.author.send(f"Votre message a été supprimé car il contient du contenu interdit. ({WARN[message.author]} warn)")


# fonction "on_ready" pour confirmer la bonne connexion du bot sur votre serveur
@bot.event
async def on_ready():
    print (f"{bot.user.name} s'est bien connecté !")

# Annotation pour dire que l'on ecrit une fonction commande
@bot.command()
async def ping(ctx):
    '''
    !ping : qui renvoie pong avec un emoji
    '''
    await ctx.send('pong 🏓')

@bot.command()
async def touché(ctx):
    '''
    !touché : qui renvoie coulé ! avec un emoji
    '''
    await ctx.send('coulé! 🛥️')
   

@bot.command()
async def members(ctx : commands):
    '''
    !members : renvoie les informations sur les membres du serveur avec leurs rôles (bot exclue)
    '''
    members_info = ""
    for member in ctx.guild.members:
        # check de si l'utilisateur est un bot 
        if not member.bot :
            # Récupération du pseudo et des rôles du membre
            member_roles = ", ".join([role.name for role in member.roles])
            members_info += f"{member.mention} - Roles: {member_roles}\n"
    # Envoie des informations
    await ctx.send(f"Liste des membres sur le serveur:\n{members_info}")

@bot.command()
async def joke(ctx : commands):
    '''
    !joke : renvoie un blague récupéré sur l'API : https://v2.jokeapi.dev/joke/Any?lang=fr
    '''
    # Récupération de la blague via API GET
    response = requests.get('https://v2.jokeapi.dev/joke/Any?lang=fr').json()
    # Envoie de la question
    await ctx.send(f"{response["setup"]}")
    # Envoie des roulements de tambours
    tambour = await ctx.send(f"🥁🥁🥁")
    # On attends un seconde avant de supprimer les tambours
    await asyncio.sleep(1)
    # Supprimer le message envoyé par le bot
    await tambour.delete()
    # Envoie de la blague
    await ctx.send(f"{response["delivery"]}")

@bot.event
async def on_message(message):
    '''
    Listener sur les messages
    '''
    # Si le message est bonjour alors on renvoie une reaction
    if "bonjour" in message.content.lower():
        await message.add_reaction('👋')

    # Si le message est dans la black list alors on supprime le message et on éxecute la fonction warn_user
    if message.content.lower() in BLACK_LIST:
        await message.delete()
        await warn_user(message)

    # Cette fonction s'assure que le message est analysé correctement pour détecter les commandes et exécute la fonction appropriée si une commande est trouvée. 
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    '''
    Listener pour quand un utilisateur rejoins le serveur
    '''
    # On récupére l'id du channel général
    channel = bot.get_channel(1234839285811777539)
    if channel is not None:
        global last_member_join
        # On assigne la variable last_member_join avec la dernière personne qui à join
        last_member_join = member.mention
        # Envoie du message de bienvenue
        await channel.send(f'Bienvenue {member.mention} sur le serveur!')

@bot.command()
async def welcome(ctx):
    '''
    !welcome : Renvoie un message sur le serveur pour souhaiter la bienvenue au nouvel arrivant
    '''
    # Check de si la variable last_member_join est défini
    if last_member_join is not None :
        await ctx.send(f"Bienvenue sur notre serveur {last_member_join} !")

#connexion du bot au serveur avec au token
bot.run("TOKEN")
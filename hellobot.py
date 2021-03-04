import discord
from discord.ext import commands
from discord.utils import get
import mysql.connector
import os

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password=os.environ['DB_PASS'],
  database="helloBotDB"
)

mycursor = mydb.cursor(buffered=True)

intents = discord.Intents.all()
intents.reactions = True


TOKEN = os.environ['BOT_TOKEN']
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(816281196996067328)
    await channel.send(f"Hi {member.name}, welcome to {member.guild.name}!")
    await member.send(
        f'Hi {member.name}, welcome to {member.guild.name}!'
    )

@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(816281227253645342)
    msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    author = msg.author
    await channel.send(f"{payload.member} added reaction to {author}")

@bot.event
async def on_ready():
    print('My bot is ready')

@bot.command()
async def role(ctx, arg):
    print('Start')
    roles = await ctx.guild.fetch_roles()
    if arg not in roles:
        await ctx.guild.create_role(name=arg)
    member = ctx.message.author
    role = get(member.guild.roles, name=arg)
    await member.add_roles(role)
    print('Done')

@bot.command()
async def register(ctx, arg):
    mycursor.execute(
        "SELECT users, COUNT(*) FROM users WHERE users = %s GROUP BY users",
        (arg,)
    )
    if mycursor.rowcount == 0:
        sql = "INSERT INTO users VALUES (%s)"
        val = (arg,)
        mycursor.execute(sql, val)
        mydb.commit()
        await ctx.send(f"{arg} is Registered.")
        print(mycursor.rowcount, "record inserted.")
    else:
        await ctx.send(f"You're already registered.")


@bot.command()
@commands.has_role('Admin')
async def names(ctx):
    async for member in ctx.guild.fetch_members():
        await ctx.send(member)


bot.run(TOKEN)
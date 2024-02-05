import disnake
from disnake.ext import commands
import os

bot  = commands.Bot(command_prefix="ais.", help_command=None, intents=disnake.Intents.all())

@bot.event
async def on_ready():
    print(f'Бот {bot.user} работает!')
    await bot.change_presence(
        activity=disnake.Game(name="Visual Studio Code💙", type=disnake.ActivityType.streaming, url="https://discord.gg/RQh357FV4M"))

@bot.event
async def on_member_join(member):
    role = disnake.utils.get(member.guild.roles, id=1070345403020607568)
    channel = bot.get_channel(1069688784721022978)
    
    embed = disnake.Embed(
        title="Новый участник",
        description=f"{member.name}#{member.discriminator}",
        color=0xffffff
    )
    await member.add_roles(role)
    await channel.send(embed=embed)

# for file in os.listdir("./cogs"):
#     if file.endswith(".py"):
#         bot.load_extension(f"cogs.{file[:-3]}")

bot.load_extensions('cogs')

bot.run("MTIwMjYwNTA2MTA4ODQ3NzIwNQ.GJ_V0V.xAq2nkDTLdeiOCXmNKu_zLOv73cf26sbL97leQ")
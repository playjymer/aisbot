import os
import sqlite3
import disnake
from disnake.ext import commands, tasks
from datetime import datetime, timedelta
import time

CENSORE_WORDS = ['бля', 'хуй', 'бл', 'блять', 'нищий', 'тварь', 'чмо', 'ебобо', 'ебнулся', 'дура', 'пидор',
                  "сука"]

class ModeratorCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.conn = sqlite3.connect('mute_data.db')  # Подключение к базе данных SQLite
        self.cursor = self.conn.cursor()
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mute_data
                             (user_id INTEGER PRIMARY KEY, mute_time TEXT)''')
        self.cursor.execute('''ALTER TABLE mute_data
                              ADD COLUMN warns INTEGER DEFAULT 0''')
        self.conn.commit()
        self.check_mutes.start()
        
    def cog_unload(self):
        self.conn.close()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content:
            for content in message.content.split():
                for censored_word in CENSORE_WORDS:
                    if content == censored_word:
                        await message.delete()
                        await message.channel.send(f"{message.author.mention}, это слово запрещено на AIS")

    @commands.command()
    @commands.has_permissions(kick_members=True, administrator=True)
    async def kick(self, ctx, member: disnake.Member, *, reason="Нарушение правил"):
        await ctx.send(f'{member.mention} был исключён!💔 \n Причина: {reason}' )
        await member.kick(reason=reason)
        await ctx.message.delete()

    @commands.command()
    @commands.has_permissions(ban_members=True, administrator=True)
    async def ban(self, ctx, member: disnake.Member, *, reason="Нарушение правил"):
        role = disnake.utils.get(ctx.guild.roles, id=1202638444354871306)
        if role in member.roles:
            await ctx.send(f'{member.name} уже забанен😴' )
        else:
            embed = disnake.Embed(
                title=f"{member.name}, был забанен💔",
                description=f"{member.name}, был забанен администратором {ctx.author.mention}🧡 \nПричина: {reason}",
                color=0xff0000
            )

            await member.add_roles(role)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True, administrator=True)        
    async def unban(self, ctx, member: disnake.Member, *, reason="Причина не указана"):
        role = disnake.utils.get(member.guild.roles, id=1202638444354871306)

        if role in member.roles:
            embed = disnake.Embed(
                title=f"{member.name}, был разбанен❤️‍🩹",
                description=f"{member.name}, был разбанен администратором {ctx.author.mention}🧡 \nПричина: {reason}",
                color=0x00FF00

            )
            await member.remove_roles(role)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'{member.name} не забанен🤨' )

    @commands.command()
    @commands.has_permissions(ban_members=True, administrator=True)
    async def mute(self, ctx, member: disnake.Member, duration: int = None, *, reason="Нарушение правил"):
        role = disnake.utils.get(ctx.guild.roles, id=1070326897633923162)
        embed = disnake.Embed(
                title=f"{member.name}, был замьючен💔",
                description=f"{member.name}, был замьючен администратором {ctx.author.mention} на {duration} минут \nПричина: {reason}",
                color=0xff0000)
        embed2 = disnake.Embed(
                title=f"{member.name}, был замьючен💔",
                description=f"{member.name}, был замьючен администратором {ctx.author.mention} на навсегда \nПричина: {reason}",
                color=0xff0000)
        if role in member.roles:
            await ctx.send(f'{member.name} уже замьючен😴' )
        else:
            if duration:
                mute_time = datetime.now() + timedelta(minutes=duration)
                self.cursor.execute("INSERT OR REPLACE INTO mute_data (user_id, mute_time) VALUES (?, ?)",
                                    (member.id, mute_time.isoformat()))
                self.conn.commit()
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed2=embed2)
            await member.add_roles(role)

    

    def cog_unload(self):
        self.conn.close()
        self.check_mutes.cancel()

    @tasks.loop(minutes=1)  # Периодическая задача выполняется каждую минуту
    async def check_mutes(self):
        current_time = datetime.now().isoformat()
        self.cursor.execute("SELECT user_id FROM mute_data WHERE mute_time <= ?", (current_time,))
        expired_mutes = self.cursor.fetchall()
        guild = self.bot.get_guild(1069688784054141020)
        for user_id in expired_mutes:
            if guild:
                member = guild.get_member(user_id[0])
                if member:
                    role = disnake.utils.get(member.guild.roles, id=1070326897633923162)
                    await member.remove_roles(role)
                    await member.send("Вы были размьючены. Не нарушайте больше правила!")
        self.cursor.execute("DELETE FROM mute_data WHERE mute_time <= ?", (current_time,))
        self.conn.commit()
        
            

    @commands.command()
    @commands.has_permissions(ban_members=True, administrator=True)        
    async def unmute(self, ctx, member: disnake.Member, *, reason="Причина не указана"):
        role = disnake.utils.get(member.guild.roles, id=1070326897633923162)

        if role in member.roles:
            embed = disnake.Embed(
                title=f"{member.name}, был размьючен❤️‍🩹",
                description=f"{member.name}, был размьючен администратором {ctx.author.mention}🧡 \nПричина: {reason}",
                color=0x00FF00

            )
            await member.remove_roles(role)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f'{member.name} не замьючен🤨' )


    @commands.command()
    @commands.has_permissions(ban_members=True, administrator=True)  
    async def warn(self, ctx, member: disnake.Member, *, reason="Нарушение правил"):

        embed2 = disnake.Embed(
            title=f"Участнику {member.name}, был был забанен❤️‍🩹",
            description=f"Учасник {member.name}, был \nПричина: {reason}",
            color=0xff0000
        )
        role = disnake.utils.get(ctx.guild.roles, id=1202638444354871306)
        self.cursor.execute("SELECT warns FROM mute_data WHERE user_id=?", (member.id,))

        if warns:
            warns = warns[0] + 1
            self.cursor.execute("UPDATE mute_data SET warns=? WHERE user_id=?", (warns, member.id))
        else:
            warns = 1
            self.cursor.execute("INSERT INTO mute_data (user_id, warns) VALUES (?, ?)", (member.id, warns))
        self.conn.commit()

        if warns >= 3:
            await ctx.send(embed2=embed2)
            await member.add_roles(role)
        else:
            embed = disnake.Embed(
            title=f"Участнику {member.name}, был выдан варн❤️‍🩹",
            description=f"Учаснику {member.name}, был выдан варн, администратором {ctx.author.mention}🧡\nПричина: {reason} \n Количество полученных варнов: {warns}",
            color=0xff0000
        )
            await ctx.send(embed=embed)



    

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        print(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f"{ctx.author.mention}, у вас нет прав на использование этой команды!")
        elif isinstance(error, commands.UserInputError):
            await ctx.send(embed=disnake.Embed(
                description=f"Правильное использование команды: '{ctx.prefix}{ctx.command.name}' ({ctx.command.brief})\nПример {ctx.prefix}{ctx.command.usage}"
            ))
    
        
def setup(bot: commands.Bot):
    bot.add_cog(ModeratorCommands(bot))

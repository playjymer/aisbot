import os, sqlite3

import disnake
from disnake import File, AuditLogAction
from disnake.ext import commands

import datetime

colur = 0xffffff
LOG_AUDIT = 1202603818131652638


async def get_guild_update_user(guild):
    async for entry in guild.audit_logs(action = AuditLogAction.guild_update):
        return entry.user
    return None


async def get_channel_creator(guild, created_channel):
    async for entry in guild.audit_logs(action = AuditLogAction.channel_create):
        if entry.target == created_channel:
            return entry.user
    return None

async def get_channel_updater(guild, updated_channel):
    async for entry in guild.audit_logs(action = AuditLogAction.channel_update):
        if entry.target == updated_channel:
            return entry.user
    return None

async def get_channel_deleter(guild, deleted_channel):
    async for entry in guild.audit_logs(action = AuditLogAction.channel_delete):
        if entry.target.id == deleted_channel.id:
            return entry.user
    return None



async def get_role_creator(guild, created_role):
    async for entry in guild.audit_logs(action = AuditLogAction.role_create):
        if entry.target == created_role:
            return entry.user
    return None

async def get_role_updater(guild, updated_role):
    async for entry in guild.audit_logs(action = AuditLogAction.role_update):
        if entry.target == updated_role:
            return entry.user
    return None

async def get_role_deleter(guild, deleted_role):
    async for entry in guild.audit_logs(action = AuditLogAction.role_delete):
        if entry.target.id == deleted_role.id:
            return entry.user
    return None



async def get_thread_updater(guild, updated_thread):
    async for entry in guild.audit_logs(action = AuditLogAction.thread_update):
        if entry.target == updated_thread:
            return entry.user
    return None

async def get_thread_deleter(guild, deleted_thread):
    async for entry in guild.audit_logs(action = AuditLogAction.thread_delete):
        if entry.target.id == deleted_thread.id:
            return entry.user
    return None



async def get_message_deleter(guild, deleted_message):
    async for entry in guild.audit_logs(action = AuditLogAction.message_delete):
        if entry.target.id == deleted_message.author.id and entry.extra.channel.id == deleted_message.channel.id:
            return entry.user
    return None



async def get_invite_deleter(guild, deleted_invite):
	async for entry in guild.audit_logs(action = AuditLogAction.invite_delete):
		if entry.target == deleted_invite.inviter and entry.extra.code == deleted_invite.code:
			return entry.user
	return None


async def get_unban_admin(guild, unbanned_user):
	async for entry in guild.audit_logs(action = AuditLogAction.unban):
		if entry.target == unbanned_user:
			return entry.user
	return None

async def get_ban_admin(guild, banned_user):
	async for entry in guild.audit_logs(action = AuditLogAction.ban):
		if entry.target == banned_user:
			return entry.user
	return None



async def get_member_kicker(guild, removed_member):
    async for entry in guild.audit_logs(action = AuditLogAction.kick):
        if entry.target.id == removed_member.id:
            return entry.user
    return None



async def get_user_who_pinned_message(channel, message):
	reactions = message.reactions
	for reaction in reactions:
		users = await reaction.users().flatten()
		for user in users:
			if not user.bot:
				return user
	return None


class AUDIT(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_connect(self):
		with open(r'logs_bot.txt', 'a', encoding = 'utf-8') as file:
			file.write(f'LOG BOT Discord API < CONNECT > - {datetime.datetime.now()}\n\n')

	@commands.Cog.listener()
	async def on_resumed(self):
		with open(r'logs_bot.txt', 'a', encoding = 'utf-8') as file:
			file.write(f'LOG BOT Discord API < RESUMED > - {datetime.datetime.now()}\n\n')

	@commands.Cog.listener()
	async def on_disconnect(self):
		with open(r'logs_bot.txt', 'a', encoding = 'utf-8') as file:
			file.write(f'LOG BOT Discord API < DISCONNECT > - {datetime.datetime.now()}\n\n')


	@commands.Cog.listener()
	async def on_typing(self, channel, user, when):
		t_user = f"{user} ~ {user.id}"
		t_channel = f"{channel} ~ {channel.id}"
		t_data = f"{datetime.datetime.now()}"

		with open(r'logs_user_typing.txt', 'a', encoding = 'utf-8') as file:
			file.write(f'LOG SERVER USER TYPING - {datetime.datetime.now()}\nUSER: {user} ~ {user.id}  |  CHANNEL: {channel} ~ {channel.id}\n\n')


	@commands.Cog.listener()
	async def on_guild_update(self, before, after):

		user = await get_guild_update_user(before)

		if before.name != after.name:
			embed=disnake.Embed(title = f"Обновление сервера < Название >.", description = f"", color = colur)
			embed.add_field(name = f"Название до", value = f"{before.name}", inline = True)
			embed.add_field(name = f"Название после", value = f"{after.name}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.afk_channel != after.afk_channel:
			embed=disnake.Embed(title = f"Обновление сервера < АФК канал >.", description = f"", color = colur)
			embed.add_field(name = f"АФК канал до", value = f"{before.afk_channel}", inline = True)
			embed.add_field(name = f"АФК канал после", value = f"{after.afk_channel}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.afk_timeout != after.afk_timeout:
			embed=disnake.Embed(title = f"Обновление сервера < AFK Timeout >.", description = f"", color = colur)
			embed.add_field(name = f"AFK Timeout до", value = f"{before.afk_timeout}", inline = True)
			embed.add_field(name = f"AFK Timeout после", value = f"{after.afk_timeout}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.icon != after.icon:
			embed=disnake.Embed(title = f"Обновление сервера < Иконка >.", description = f"", color = colur)
			embed.add_field(name = f"Иконка до", value = f"{before.icon}", inline = True)
			embed.add_field(name = f"Иконка после", value = f"{after.icon}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.owner != after.owner:
			embed=disnake.Embed(title = f"Обновление сервера < Создатель >.", description = f"", color = colur)
			embed.add_field(name = f"Создатель до", value = f"{before.owner}", inline = True)
			embed.add_field(name = f"Создатель после", value = f"{after.owner}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.system_channel != after.system_channel:
			embed=disnake.Embed(title = f"Обновление сервера < Системный канал >.", description = f"", color = colur)
			embed.add_field(name = f"Системный канал до", value = f"{before.system_channel}", inline = True)
			embed.add_field(name = f"Системный канал после", value = f"{after.system_channel}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.rules_channel != after.rules_channel:
			embed=disnake.Embed(title = f"Обновление сервера < Канал правил >.", description = f"", color = colur)
			embed.add_field(name = f"Канал правил до", value = f"{before.rules_channel}", inline = True)
			embed.add_field(name = f"Канал правил после", value = f"{after.rules_channel}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.public_updates_channel != after.public_updates_channel:
			embed=disnake.Embed(title = f"Обновление сервера < Канал объявлений >.", description = f"", color = colur)
			embed.add_field(name = f"Канал объявлений до", value = f"{before.public_updates_channel}", inline = True)
			embed.add_field(name = f"Канал объявлений после", value = f"{after.public_updates_channel}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.preferred_locale != after.preferred_locale:
			embed=disnake.Embed(title = f"Обновление сервера < Язык >.", description = f"", color = colur)
			embed.add_field(name = f"Язык до", value = f"{before.preferred_locale}", inline = True)
			embed.add_field(name = f"Язык после", value = f"{after.preferred_locale}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.explicit_content_filter != after.explicit_content_filter:
			embed=disnake.Embed(title = f"Обновление сервера < Фильтр контента >.", description = f"", color = colur)
			embed.add_field(name = f"Фильтр контента до", value = f"{before.explicit_content_filter}", inline = True)
			embed.add_field(name = f"Фильтр контента после", value = f"{after.explicit_content_filter}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.verification_level != after.verification_level:
			embed=disnake.Embed(title = f"Обновление сервера < Уровень верефикации >.", description = f"", color = colur)
			embed.add_field(name = f"Уровень верефикации до", value = f"{before.verification_level}", inline = True)
			embed.add_field(name = f"Уровень верефикации после", value = f"{after.verification_level}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.default_notifications != after.default_notifications:
			embed=disnake.Embed(title = f"Обновление сервера < Уведомления >.", description = f"", color = colur)
			embed.add_field(name = f"Уведомления до", value = f"{before.default_notifications}", inline = True)
			embed.add_field(name = f"Уведомления после", value = f"{after.default_notifications}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.description != after.description:
			embed=disnake.Embed(title = f"Обновление сервера < Описание сервера >.", description = f"", color = colur)
			embed.add_field(name = f"Описание сервера до", value = f"{before.description}", inline = True)
			embed.add_field(name = f"Описание сервера после", value = f"{after.description}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)

		if before.splash != after.splash:
			embed=disnake.Embed(title = f"Обновление сервера < Заставка сервера >.", description = f"", color = colur)
			embed.add_field(name = f"Заставка сервера до", value = f"{before.splash_url}", inline = True)
			embed.add_field(name = f"Заставка сервера после", value = f"{after.splash_url}", inline = True)
			embed.add_field(name = f"Изменил", value = f"{user}", inline = True)
			embed.timestamp = datetime.datetime.now()
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = embed)


	@commands.Cog.listener()
	async def on_application_command_create(self, command):
		with open(r'logs_commands_register.txt', 'a', encoding = 'utf-8') as file:
			file.write(f'LOG SERVER COMMAND < CREAT > - {datetime.datetime.now()}\nCOMMAND: {command}  |  NAME: {command.name}  |  ID: {command.id}\n\n')

	@commands.Cog.listener()
	async def on_application_command_update(self, before, after):
		if before.name != after.name:
			with open(r'logs_commands_register.txt', 'a', encoding = 'utf-8') as file:
				file.write(f'LOG SERVER COMMAND < UPDATE > - {datetime.datetime.now()}\nCOMMAND: {after}  |  NAME: {before.name} => {after.name}  |  ID: {after.id}\n\n')

		if before.description != after.description:
			with open(r'logs_commands_register.txt', 'a', encoding = 'utf-8') as file:
				file.write(f'LOG SERVER COMMAND < UPDATE > - {datetime.datetime.now()}\nCOMMAND: {after}  |  NAME: {after.name}  |  DESCRIPTION: {before.description} => {after.description}  |  ID: {after.id}\n\n')

		if before.options != after.options:
			with open(r'logs_commands_register.txt', 'a', encoding = 'utf-8') as file:
				file.write(f'LOG SERVER COMMAND < UPDATE > - {datetime.datetime.now()}\nCOMMAND: {after}  |  NAME: {after.name}  |  OPTOIN: {before.options} => {after.options}  |  ID: {after.id}\n\n')

	@commands.Cog.listener()
	async def on_application_command_delete(self, command):
		with open(r'logs_commands_register.txt', 'a', encoding = 'utf-8') as file:
			file.write(f'LOG SERVER COMMAND < DELETE > - {datetime.datetime.now()}\nCOMMAND: {command}  |  NAME: {command.name}  |  ID:{command.id}\n\n')



	@commands.Cog.listener()
	async def on_guild_channel_create(self, channel):
		creator = await get_channel_creator(channel.guild, channel)
		embed=disnake.Embed(title = f"Канал создан.", description = f"", color = colur)
		embed.add_field(name = f"Канал", value = f"{channel.mention}", inline = True)
		embed.add_field(name = f"Имя канала", value = f"{channel.name}", inline = True)
		embed.add_field(name = f"ID Канала", value = f"{channel.id}", inline = True)
		embed.add_field(name = f"Создал", value = f"{creator}", inline = True)
		embed.add_field(name = f"ID создателя", value = f"{creator.id}", inline = True)
		embed.add_field(name = f"Время создания", value = f"{channel.created_at}", inline = True)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_guild_channel_update(self, before, after):
		updater = await get_channel_updater(after.guild, after)
		embed=disnake.Embed(title = f"Канал изменён.", description = f"", color = colur)
		embed.add_field(name = f"Канал", value = f"{after.mention}", inline = True)
		embed.add_field(name = f"Прошлое имя", value = f"{before.name}", inline = True)
		embed.add_field(name = f"Новое имя", value = f"{after.name}", inline = True)
		embed.add_field(name = f"ID Канала", value = f"{after.id}", inline = True)
		embed.add_field(name = f"Обновил", value = f"{updater}", inline = True)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_guild_channel_delete(self, channel):
		deleter = await get_channel_deleter(channel.guild, channel)
		embed=disnake.Embed(title = f"Канал удалён.", description = f"", color = colur)
		embed.add_field(name = f"Канал", value = f"{channel.mention}", inline = True)
		embed.add_field(name = f"Имя канала", value = f"{channel.name}", inline = True)
		embed.add_field(name = f"ID Канала", value = f"{channel.id}", inline = True)
		embed.add_field(name = f"Удалил", value = f"{deleter}", inline = True)
		embed.add_field(name = f"ID удалителя", value = f"{deleter.id}", inline = True)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)


	@commands.Cog.listener()
	async def on_guild_channel_pins_update(self, channel, last_pin):
		if not isinstance(channel, disnake.TextChannel):
			return
		pinned_messages = await channel.pins()
		if not pinned_messages:
			return
		last_pinned_message = pinned_messages[0]
		user_who_pinned = await get_user_who_pinned_message(channel, last_pinned_message)

		embed=disnake.Embed(title = f"Закреплённые сообщения обновлены.", description = f"", color = colur)
		embed.add_field(name = f"Канал", value = f"{channel.mention}", inline = True)
		embed.add_field(name = f"Имя канала", value = f"{channel.name}", inline = True)
		embed.add_field(name = f"ID Канала", value = f"{channel.id}", inline = True)
		if user_who_pinned:
			embed.add_field(name = f"Обновил", value = f"{user_who_pinned}", inline = True)
		else:
			embed.add_field(name = f"Обновил", value = f"*не определён*", inline = True)
		embed.add_field(name = f"Сообщение от", value = f"{last_pinned_message.author}", inline = True)
		embed.add_field(name = f"Сообщение", value = f"```{last_pinned_message.content}```", inline = False)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)


	@commands.Cog.listener()
	async def on_guild_role_create(self, role):
		creator = await get_role_creator(role.guild, role)
		embed=disnake.Embed(title = f"Роль создана.", description = f"", color = colur)
		embed.add_field(name = f"Роль", value = f"<@&{role.id}>", inline = True)
		embed.add_field(name = f"Имя роли", value = f"{role.name}", inline = True)
		embed.add_field(name = f"ID роли", value = f"{role.id}", inline = True)
		embed.add_field(name = f"Цвет роли", value = f"{role.color}", inline = True)
		embed.add_field(name = f"Разрешения роли", value = f"{role.permissions}", inline = True)
		embed.add_field(name = f"Время создания", value = f"{role.created_at}", inline = True)
		embed.add_field(name = f"Создал", value = f"{creator}", inline = True)
		embed.add_field(name = f"ID Создателя", value = f"{creator.id}", inline = True)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_guild_role_update(self, before, after):
		updater = await get_role_updater(after.guild, after)
		embed=disnake.Embed(title = f"Роль изменена.", description = f"", color = colur)
		embed.add_field(name = f"Роль", value = f"<@&{after.id}>", inline = True)
		embed.add_field(name = f"Прошлое имя", value = f"{before.name}", inline = True)
		embed.add_field(name = f"Новое имя", value = f"{after.name}", inline = True)
		embed.add_field(name = f"Прошлый цвет роли", value = f"{before.color}", inline = True)
		embed.add_field(name = f"Новый цвет роли", value = f"{after.color}", inline = True)
		embed.add_field(name = f"ID роли", value = f"{after.id}", inline = False)
		embed.add_field(name = f"Разрешения роли", value = f"{after.permissions}", inline = False)
		embed.add_field(name = f"Обновил", value = f"{updater}", inline = True)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_guild_role_delete(self, role):
		deleter = await get_role_deleter(role.guild, role)
		embed=disnake.Embed(title = f"Роль удалена.", description = f"", color = colur)
		embed.add_field(name = f"Имя роли", value = f"{role.name}", inline = True)
		embed.add_field(name = f"Цвет роли", value = f"{role.color}", inline = True)
		embed.add_field(name = f"ID роли", value = f"{role.id}", inline = True)
		embed.add_field(name = f"Удалил", value = f"{deleter}", inline = True)
		embed.add_field(name = f"ID удалителя", value = f"{deleter.id}", inline = True)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)


	@commands.Cog.listener()
	async def on_thread_create(self, thread):
		embed=disnake.Embed(title = f"Ветка создана.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Ветка", value = f'<#{thread.id}>', inline = True)
		embed.add_field(name = f"ID", value = f'{thread.id}', inline = True)
		embed.add_field(name = f"Type", value = f'{thread.type}', inline = True)
		embed.add_field(name = f"Создатель", value = f'<@{thread.owner_id}>', inline = True)
		embed.add_field(name = f"ID", value = f'{thread.owner_id}', inline = True)
		embed.timestamp = datetime.datetime.now()
		audit = self.bot.get_channel(LOG_AUDIT)
		await audit.send(embed = embed)

	@commands.Cog.listener()
	async def on_thread_update(self, before, after):
		updater = await get_thread_updater(after.guild, after)
		embed=disnake.Embed(title = f"Ветка изменена.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Ветка", value = f'<#{after.id}>', inline = True)
		embed.add_field(name = f"Старое название", value = f'{before}', inline = True)
		embed.add_field(name = f"Новое название", value = f'{after}', inline = True)
		embed.add_field(name = f"Обновил", value = f"{updater}", inline = True)
		embed.timestamp = datetime.datetime.now()
		audit = self.bot.get_channel(LOG_AUDIT)
		await audit.send(embed = embed)

	@commands.Cog.listener()
	async def on_thread_delete(self, thread):
		deleter = await get_thread_deleter(thread.guild, thread)
		embed=disnake.Embed(title = f"Ветка удалена.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Ветка", value = f'{thread}', inline = True)
		embed.add_field(name = f"ID", value = f'{thread.id}', inline = True)
		embed.add_field(name = f"Удалил", value = f"{deleter}", inline = True)
		embed.add_field(name = f"ID удалителя", value = f"{deleter.id}", inline = True)
		embed.timestamp = datetime.datetime.now()
		audit = self.bot.get_channel(LOG_AUDIT)
		await audit.send(embed = embed)


	@commands.Cog.listener()
	async def on_guild_emojis_update(self, guild, before, after):
		audit = self.bot.get_channel(LOG_AUDIT)
		added_emojis = [emoji for emoji in after if emoji not in before]
		removed_emojis = [emoji for emoji in before if emoji not in after]
		if added_emojis:
			for emoji in added_emojis:
				embed=disnake.Embed(title = f"Эмодзи добавлено.", url = f"", description = f"", color = colur)
				embed.add_field(name = f"Эмодзи", value = f'<:{emoji.name}:{emoji.id}>', inline = True)
				embed.add_field(name = f"Имя", value = f'{emoji.name}', inline = True)
				embed.add_field(name = f"ID", value = f'{emoji.id}', inline = True)
				embed.add_field(name = f"RES", value = f'```<:{emoji.name}:{emoji.id}>```', inline = True)
				embed.timestamp = datetime.datetime.now()
				await audit.send(embed = embed)

		for old_emoji in before:
			for new_emoji in after:
				if old_emoji.id == new_emoji.id and old_emoji.name != new_emoji.name:
					embed=disnake.Embed(title = f"Эмодзи изменено.", url = f"", description = f"", color = colur)
					embed.add_field(name = f"Эмодзи", value = f'<:{new_emoji.name}:{new_emoji.id}>', inline = True)
					embed.add_field(name = f"Прошлое имя", value = f'{old_emoji.name}', inline = True)
					embed.add_field(name = f"Новое имя", value = f'{new_emoji.name}', inline = True)
					embed.add_field(name = f"ID", value = f'{new_emoji.id}', inline = True)
					embed.add_field(name = f"RES", value = f'```<:{new_emoji.name}:{new_emoji.id}>```', inline = True)
					embed.timestamp = datetime.datetime.now()
					await audit.send(embed = embed)

		if removed_emojis:
			for emoji in removed_emojis:
				embed=disnake.Embed(title = f"Эмодзи удалено.", url = f"", description = f"", color = colur)
				embed.add_field(name = f"Эмодзи", value = f'<:{emoji.name}:{emoji.id}>', inline = True)
				embed.add_field(name = f"Имя", value = f'{emoji.name}', inline = True)
				embed.add_field(name = f"ID", value = f'{emoji.id}', inline = True)
				embed.timestamp = datetime.datetime.now()
				await audit.send(embed = embed)



	@commands.Cog.listener()
	async def on_member_ban(self, guild, user):
		audit = self.bot.get_channel(LOG_AUDIT)
		admin = await get_ban_admin(guild, user)
		embed=disnake.Embed(title = f"Участник забанен.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Участник", value = f'{user}', inline = True)
		embed.add_field(name = f"Ник", value = f'{user.name}', inline = True)
		embed.add_field(name = f"ID", value = f'{user.id}', inline = True)
		embed.add_field(name = f"Админ", value = f'{admin}', inline = True)
		embed.add_field(name = f"Ник", value = f'{admin.name}', inline = True)
		embed.add_field(name = f"ID", value = f'{admin.id}', inline = True)
		embed.timestamp = datetime.datetime.now()
		await audit.send(embed = embed)

	@commands.Cog.listener()
	async def on_member_unban(self, guild, user):
		audit = self.bot.get_channel(LOG_AUDIT)
		admin = await get_unban_admin(guild, user)
		embed=disnake.Embed(title = f"Участник разбанен.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Участник", value = f'{user}', inline = True)
		embed.add_field(name = f"Ник", value = f'{user.name}', inline = True)
		embed.add_field(name = f"ID", value = f'{user.id}', inline = True)
		embed.add_field(name = f"Админ", value = f'{admin}', inline = True)
		embed.add_field(name = f"Ник", value = f'{admin.name}', inline = True)
		embed.add_field(name = f"ID", value = f'{admin.id}', inline = True)
		embed.timestamp = datetime.datetime.now()
		await audit.send(embed = embed)


	@commands.Cog.listener()
	async def on_invite_create(self, invite):
		audit = self.bot.get_channel(LOG_AUDIT)
		embed=disnake.Embed(title = f"Приглашение создано.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Создал", value = f'{invite.inviter}', inline = True)
		embed.add_field(name = f"Приглашение", value = f'[Перейти]({invite})', inline = True)
		embed.add_field(name = f"Код", value = f'{invite.code}', inline = True)
		embed.timestamp = datetime.datetime.now()
		await audit.send(embed = embed)

	@commands.Cog.listener()
	async def on_invite_delete(self, invite):
		audit = self.bot.get_channel(LOG_AUDIT)
		deleter = await get_invite_deleter(invite.guild, invite)
		embed=disnake.Embed(title = f"Приглашение Удалено.", url = f"", description = f"", color = colur)
		if deleter:
			embed.add_field(name = f"Удалил", value = f'{deleter}', inline = True)
		else:
			embed.add_field(name = f"Удалил", value = f'*не найден*', inline = True)
		embed.add_field(name = f"Приглашение", value = f'*Удалено*', inline = True)
		embed.add_field(name = f"Код", value = f'{invite.code}', inline = True)
		embed.timestamp = datetime.datetime.now()
		await audit.send(embed = embed)


	@commands.Cog.listener()
	async def on_reaction_add(self, reaction, user):
		audit = self.bot.get_channel(LOG_AUDIT)
		embed=disnake.Embed(title = f"Реакция добавлена.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Участник", value = f'{user}', inline = True)
		embed.add_field(name = f"Реакция", value = f'{reaction.emoji}', inline = True)
		embed.add_field(name = f"ID сообщения", value = f'{reaction.message.id}', inline = True)
		embed.timestamp = datetime.datetime.now()
		await audit.send(embed = embed)

	@commands.Cog.listener()
	async def on_reaction_remove(self, reaction, user):
		audit = self.bot.get_channel(LOG_AUDIT)
		embed=disnake.Embed(title = f"Реакция удалена.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Участник", value = f'{user}', inline = True)
		embed.add_field(name = f"Реакция", value = f'{reaction.emoji}', inline = True)
		embed.add_field(name = f"ID сообщения", value = f'{reaction.message.id}', inline = True)
		embed.timestamp = datetime.datetime.now()
		await audit.send(embed = embed)


	@commands.Cog.listener()
	async def on_webhooks_update(self, channel):
		guild = channel.guild
		webhook_create, webhook_update, webhook_delete = None, None, None

		async for entry in guild.audit_logs():
			if entry.action == disnake.AuditLogAction.webhook_create and not webhook_create:
				webhook_create = entry
			elif entry.action == disnake.AuditLogAction.webhook_update and not webhook_update:
				webhook_update = entry
			elif entry.action == disnake.AuditLogAction.webhook_delete and not webhook_delete:
				webhook_delete = entry
			break

			if webhook_create and webhook_update and webhook_delete:
				break


		if webhook_create:
			usere = webhook_create.user
			audit = self.bot.get_channel(LOG_AUDIT)
			embed=disnake.Embed(title = f"Вебхук создан.", url = f"", description = f"", color = colur)
			embed.add_field(name = f"Вебхук", value = f'{webhook_create.target}', inline = True)
			embed.add_field(name = f"Канал", value = f'{channel.mention}', inline = True)
			embed.add_field(name = f"Создал", value = f'{webhook_create.user}', inline = True)
			embed.timestamp = datetime.datetime.now()
			await audit.send(embed = embed)

		elif webhook_update:
			audit = self.bot.get_channel(LOG_AUDIT)
			embed=disnake.Embed(title = f"Вебхук изменён.", url = f"", description = f"", color = colur)
			embed.add_field(name = f"Вебхук", value = f'{webhook_update.target}', inline = True)
			embed.add_field(name = f"Канал", value = f'{channel.mention}', inline = True)
			embed.add_field(name = f"Изменил", value = f'{webhook_update.user}', inline = True)
			embed.timestamp = datetime.datetime.now()
			await audit.send(embed = embed)

		elif webhook_delete:
			audit = self.bot.get_channel(LOG_AUDIT)
			embed=disnake.Embed(title = f"Вебхук удалён.", url = f"", description = f"", color = colur)
			embed.add_field(name = f"Вебхук", value = f'{webhook_delete.target}', inline = True)
			embed.add_field(name = f"Канал", value = f'{channel.mention}', inline = True)
			embed.add_field(name = f"Удалил", value = f'{webhook_delete.user}', inline = True)
			embed.timestamp = datetime.datetime.now()
			await audit.send(embed = embed)


	@commands.Cog.listener()
	async def on_message_delete(self, message):
		if message.author.id == self.bot.user.id:
			return

		deleter = await get_message_deleter(message.guild, message)
		embed=disnake.Embed(title = f"Сообщение участника было удалено.", description = f"", color = colur)
		embed.add_field(name = f"Автор", value = f"{message.author.mention}", inline = True)
		embed.add_field(name = f"ID автора", value = f"{message.author.id}", inline = True)
		embed.add_field(name = f"Канал", value = f"{message.channel}({message.channel.mention})", inline = True)
		embed.add_field(name = f"ID канала", value = f"{message.channel.id}", inline = True)
		if deleter:
			embed.add_field(name = f"Удалил", value = f"{deleter}", inline = True)
			embed.add_field(name = f"ID удалителя", value = f"{deleter.id}", inline = True)
		else:
			embed.add_field(name = f"Удалил", value = f"*не найден*", inline = True)
		embed.add_field(name = f"Сообщение", value = f"```{message.content}```", inline = False)
		embed.add_field(name = f"ID сообщения", value = f"{message.id}", inline = True)
		embed.add_field(name = f"Время", value = f"{message.created_at}", inline = True)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_message_edit(self, message_before, message_after):
		if message_before.author.id == self.bot.user.id:
			return
		if message_after.author.id == self.bot.user.id:
			return

		embed=disnake.Embed(title = f"Сообщение участника было отредактировано.", description = f"", color = colur)
		embed.add_field(name = f"Автор", value = f"{message_before.author.mention}", inline = True)
		embed.add_field(name = f"ID автора", value = f"{message_before.author.id}", inline = True)
		embed.add_field(name = f"Канал", value = f"{message_before.channel}", inline = True)
		embed.add_field(name = f"ID канала", value = f"{message_before.channel.id}", inline = True)
		embed.add_field(name = f"Старое сообщение", value = f"```{message_before.content}```", inline = False)
		embed.add_field(name = f"Новое сообщение", value = f"```{message_after.content}```", inline = False)
		embed.add_field(name = f"ID сообщения", value = f"{message_before.id}", inline = True)
		embed.add_field(name = f"Время", value = f"{message_before.created_at}", inline = True)
		embed.timestamp = datetime.datetime.now()
		channel = self.bot.get_channel(LOG_AUDIT)
		await channel.send(embed = embed)

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.roles != after.roles:
			emb = disnake.Embed(title = f'Обновление ролей участника.', colour = colur)
			async for event in before.guild.audit_logs(limit = 1, action = disnake.AuditLogAction.member_role_update):
				if getattr(event.target, "id", None) != before.id:
					continue
				emb.add_field(name = "Участник:", value = f"{before.mention}", inline = True)
				emb.add_field(name = "Админ:", value = event.user, inline = True)
				emb.add_field(name = "Изменённые роли:", value = ", ".join([getattr(r, "mention", r.id) for r in event.before.roles or event.after.roles]), inline = False)
				emb.add_field(name = "Роли до:", value = ", ".join([r.mention for r in before.roles[1:]]), inline = True)
				emb.add_field(name = "Роли после:", value = ", ".join([r.mention for r in after.roles[1:]]), inline = True)
				emb.timestamp = datetime.datetime.now()
				break
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = emb)

		if before.status != after.status:
			emb = disnake.Embed(title = f'Обновление статуса участника на сервере.', colour = colur)
			emb.add_field(name = 'Юзер:', value = f"{after.mention}", inline = True)
			emb.add_field(name = 'Статус до:', value = f"{before.status}", inline = True)
			emb.add_field(name = 'Статус после:', value = f"{after.status}", inline = True)
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = emb)

		if before.activities != after.activities:
			emb = disnake.Embed(title = f'Обновление активности участника на сервере.', colour = colur)
			emb.add_field(name = 'Юзер:', value = f"{after.mention}", inline = True)
			emb.add_field(name = 'Активность до:', value = f"{before.activities}", inline = True)
			emb.add_field(name = 'Активность после:', value = f"{after.activities}", inline = True)
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = emb)



	@commands.Cog.listener()
	async def on_user_update(self, before, after):
		if before.name != after.name:
			emb = disnake.Embed(title = f'Обновление ника юзера.', colour = colur)
			emb.add_field(name = 'Юзер:', value = f"{after.mention}", inline = True)
			emb.add_field(name = 'Ник до:', value = f"{before}", inline = True)
			emb.add_field(name = 'Ник после:', value = f"{after}", inline = True)
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = emb)

		if before.discriminator != after.discriminator:
			emb = disnake.Embed(title = f'Обновление дискриминатора юзера.', colour = colur)
			emb.add_field(name = 'Юзер:', value = f"{after.mention}", inline = True)
			emb.add_field(name = 'Дискриминатор до:', value = f"{before.discriminator}", inline = True)
			emb.add_field(name = 'Дискриминатор после:', value = f"{after.discriminator}", inline = True)
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = emb)

		if before.avatar != after.avatar:
			emb = disnake.Embed(title = f'Обновление аватарки юзера.', colour = colur)
			emb.add_field(name = 'Юзер:', value = f"{after.mention}", inline = True)
			emb.add_field(name = 'Аватар до:', value = f"{before.avatar}", inline = True)
			emb.add_field(name = 'Аватар после:', value = f"{after.avatar}", inline = True)
			channel = self.bot.get_channel(LOG_AUDIT)
			await channel.send(embed = emb)


	@commands.Cog.listener()
	async def on_thread_member_join(self, member:disnake.Member = None):
		audit = self.bot.get_channel(LOG_AUDIT)
		embed=disnake.Embed(title = f"Участник зашел в ветку.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Участник", value = f'<@{member.id}>', inline = True)
		embed.add_field(name = f"ID участника", value = f'{member.id}', inline = True)
		embed.add_field(name = f"Ветка", value = f'<#{member.thread_id}>', inline = True)
		embed.timestamp = datetime.datetime.now()
		await audit.send(embed = embed)

	@commands.Cog.listener()
	async def on_thread_member_remove(self, member:disnake.Member = None):
		audit = self.bot.get_channel(LOG_AUDIT)
		embed=disnake.Embed(title = f"Участник вышел из ветки.", url = f"", description = f"", color = colur)
		embed.add_field(name = f"Участник", value = f'<@{member.id}>', inline = True)
		embed.add_field(name = f"ID участника", value = f'{member.id}', inline = True)
		embed.add_field(name = f"Ветка", value = f'<#{member.thread_id}>', inline = True)
		embed.timestamp = datetime.datetime.now()
		await audit.send(embed = embed)



	@commands.Cog.listener()
	async def on_member_join(self, member:disnake.Member = None, guild: disnake.Guild = None):
		embed=disnake.Embed(title = f"Участник присоеденился к серверу.", url = f"", description = f"", color = colur)
		embed.set_thumbnail(url=member.avatar.url if member.avatar is not None else member.default_avatar)
		embed.add_field(name = f"Участник", value = f'{member.mention}', inline = True)
		embed.add_field(name = f"Ник", value = f'{member}', inline = True)
		embed.add_field(name = f"ID участника", value = f'{member.id}', inline = True)
		embed.add_field(name = f"Дата регистрации:", value = f'{disnake.utils.format_dt(member.created_at, "f")} ({disnake.utils.format_dt(member.created_at, "R")})', inline = True)
		embed.add_field(name = f"Присоеденился:", value = f'{disnake.utils.format_dt(member.joined_at, "f")} ({disnake.utils.format_dt(member.joined_at, "R")})', inline = True)
		embed.timestamp = datetime.datetime.now()
		audit = self.bot.get_channel(LOG_AUDIT)
		await audit.send(embed = embed)



	@commands.Cog.listener()
	async def on_member_remove(self, member:disnake.Member = None, guild: disnake.Guild = None):
		embed=disnake.Embed(title = f"Участник вышел с сервера.", url = f"", description = f"", color = colur)
		embed.set_thumbnail(url=member.avatar.url if member.avatar is not None else member.default_avatar)
		embed.add_field(name = f"Участник", value = f'{member.mention}', inline = True)
		embed.add_field(name = f"Ник", value = f'{member}', inline = True)
		embed.add_field(name = f"ID участника", value = f'{member.id}', inline = True)
		embed.add_field(name = f"Дата регистрации:", value = f'{disnake.utils.format_dt(member.created_at, "f")} ({disnake.utils.format_dt(member.created_at, "R")})', inline = True)
		embed.add_field(name = f"Присоеденился:", value = f'{disnake.utils.format_dt(member.joined_at, "f")} ({disnake.utils.format_dt(member.joined_at, "R")})', inline = True)
		embed.timestamp = datetime.datetime.now()
		audit = self.bot.get_channel(LOG_AUDIT)
		await audit.send(embed = embed)


	@commands.Cog.listener()
	async def on_voice_state_update(self, member : disnake.Member, before : disnake.VoiceState, after: disnake.VoiceState):

		logs = self.bot.get_channel(LOG_AUDIT)
		if before.channel is None:
			embed=disnake.Embed(title = f"Участник зашёл в войс.", description = f"", timestamp = datetime.datetime.now(), color = colur)
			embed.add_field(name = f"Участник", value = f"{member}({member.mention})", inline = True)
			embed.add_field(name = f"ID участника", value = f"{member.id}", inline = True)
			embed.add_field(name = f"Канал", value = f"{after.channel}({after.channel.mention})", inline = False)
			embed.add_field(name = f"ID канала", value = f"{after.channel.id}", inline = True)
			await logs.send(embed = embed)

		elif after.channel is None:
			embed=disnake.Embed(title = f"Участник вышел из войса.", description = f"", timestamp = datetime.datetime.now(), color = colur)
			embed.add_field(name = f"Участник", value = f"{member}({member.mention})", inline = True)
			embed.add_field(name = f"ID участника", value = f"{member.id}", inline = True)
			embed.add_field(name = f"Канал", value = f"{before.channel}({before.channel.mention})", inline = False)
			embed.add_field(name = f"ID канала", value = f"{before.channel.id}", inline = True)
			await logs.send(embed = embed)

		elif before.channel != after.channel:
			embed=disnake.Embed(title = f"Участник перешёл.", description = f"", timestamp = datetime.datetime.now(), color = colur)
			embed.add_field(name = f"Участник", value = f"{member}({member.mention})", inline = True)
			embed.add_field(name = f"ID участника", value = f"{member.id}", inline = True)
			embed.add_field(name = f"Перешёл из:", value = f"{before.channel.mention}", inline = False)
			embed.add_field(name = f"В канал:", value = f"{after.channel.mention}", inline = False)
			embed.add_field(name = f"ID канала", value = f"{after.channel.id}", inline = True)
			await logs.send(embed = embed)


	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if before.display_name != after.display_name:
			channel = self.bot.get_channel(LOG_AUDIT)

			embed = disnake.Embed(description=f'Имя пользователя **{after.name}** ({after.mention}) было изменено',
								  color=0x2B2D31).set_thumbnail(url=after.display_avatar)
			embed.add_field(name='Исходный ник:', value=f'`{before.display_name}`', inline=True)
			embed.add_field(name='Измененный ник:', value=f'`{after.display_name}`', inline=True)
			embed.set_footer(text=f'ID Пользователя: {after.id}', icon_url=after.display_avatar)

			await channel.send(embed=embed)

def setup(bot):
	bot.add_cog(AUDIT(bot))
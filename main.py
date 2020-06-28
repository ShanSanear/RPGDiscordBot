import os
import time

import discord
import random
import asyncio

from discord import Message, Status, TextChannel, VoiceState, VoiceChannel, Member

TOKEN = os.getenv("TOKEN")
text_channel_id = 596736875549556748
voice_channel_id = 596736875549556752
shan_id = 440059101284663296
mg_id = 366836191854723072


class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')


client = MyClient()


async def remind_mg_about_recording(after, member):
    text_channel: TextChannel = client.get_channel(text_channel_id)
    voice_channel: VoiceChannel = client.get_channel(voice_channel_id)
    if voice_channel == after.channel:
        await text_channel.send(f'Nie zapomnij o nagrywaniu, {member.mention}!')


def remind_about_short_term_tasks(after, member):
    text_channel: TextChannel = client.get_channel(text_channel_id)
    voice_channel: VoiceChannel = client.get_channel(voice_channel_id)
    if voice_channel == after.channel:
        await text_channel.send(f"Nie zapomnij o celu krótkoterminowym, {member.mention}!")


@client.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    mg = client.get_user(mg_id)
    if mg == member:
        await remind_mg_about_recording(after, member)
    else:
        await remind_about_short_term_tasks(after, member)


client.run(TOKEN)

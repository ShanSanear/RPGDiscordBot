import fandom
from discord.ext import commands
from discord.ext.commands import Context
from fandom.error import PageError

from cogs.dnd5_api import DnD5Api
from loggers import general_logger
from rpg_discord_bot import RPGDiscordBot


class Finder(commands.Cog):
    __MAX_SIZE = 1950

    def __init__(self, bot: RPGDiscordBot):
        """
        Constructor
        :param bot: RPGDiscordBot instance
        """
        self.bot = bot

    @commands.group(pass_context=True)
    async def search(self, ctx: Context):
        """
        General search function placeholder
        """
        pass

    @search.command(name='wiki', pass_context=True)
    async def wiki(self, ctx: Context, name: str, wiki_name='forgottenrealms'):
        """
        Search for given page in specified wiki (optional, Forgotten Realms wiki as default)
        :param ctx:  Context
        :param name: Wiki page which is being searched for
        :param wiki_name: Wiki which is being searched for
        """
        async with ctx.typing():
            page = fandom.page(name, wiki=wiki_name)
            summary = page.summary
            wiki_link_markup = page.url
            await ctx.send(
                content=f"\n{summary} {wiki_link_markup}"[:self.__MAX_SIZE]
            )

    @search.command(name='wiki_full', pass_context=True)
    async def wiki_full(self, ctx: Context, name: str, wiki_name='forgottenrealms'):
        """
        Search for given page in specified wiki (optional, Forgotten Realms wiki as default)
        Provides all possible information based on sections.
        :param ctx:  Context
        :param name: Wiki page which is being searched for
        :param wiki_name: Wiki which is being searched for
        """
        async with ctx.typing():
            general_logger.debug("Searching wiki '%s' for '%s'", wiki_name, name)
            try:
                page = fandom.page(name, wiki=wiki_name)
            except PageError:
                await ctx.send(f"Couldn't find '{name}' in wiki '{wiki_name}")
                return

            await ctx.send(
                content=f"\n**Summary**\n{page.content['content'][:self.__MAX_SIZE]}"

            )
            general_logger.debug("Sections in page %s: '%s'",
                                 name,
                                 ','.join(c['title'] for c in page.content['sections'])
                                 )
            for section in page.content['sections']:
                section_content = section['content']
                if len(section_content) > self.__MAX_SIZE:
                    await ctx.send(content=f'Following section will be trunctuated: {section["title"]}')
                await ctx.send(
                    content=f"\n**{section['title']}**\n{section['content']}"[:self.__MAX_SIZE]
                )

    @search.command(name='spell', pass_context=True)
    async def spell(self, ctx: Context, name: str):
        """
        Searches for DnD5e spells
        :param name: Spell which is being searched
        """
        async with ctx.typing():
            content = await DnD5Api().dnd_search("spell", name)
            await ctx.send(content)[:self.__MAX_SIZE]

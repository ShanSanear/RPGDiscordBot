import asyncio

import discord
import youtube_dl
from discord import AudioSource

youtube_dl.utils.bug_reports_message = lambda: ''


class YTDLSource(discord.PCMVolumeTransformer):
    """
    Class handling downloading music from YT.
    """
    _ytdl_format_options = {
        'format': 'bestaudio/best',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }
    ffmpeg_options = {
        'options': '-vn'
    }
    yt_downloader = youtube_dl.YoutubeDL(_ytdl_format_options)

    def __init__(self, source: AudioSource, *, data: dict, volume: float = 0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url: str, *, loop=None, stream=False):
        """
        Downloading from YT.
        :param url: Url to stream/download from
        :param loop: What kind of loop interface should be used
        :param stream: if this is stream or download
        :return: Player object
        """
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: cls.yt_downloader.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else cls.yt_downloader.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **cls.ffmpeg_options),
                   data=data)

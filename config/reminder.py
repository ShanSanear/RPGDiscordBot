from dataclasses import dataclass


@dataclass
class REMINDER:
    GM_ID: int
    BLACKLISTED_IDS: list[int]
    TEXT_CHANNEL_ID: int
    VOICE_CHANNEL_ID: int
    GM_MESSAGE: str
    OTHERS_MESSAGE: str

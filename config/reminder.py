from dataclasses import dataclass
from typing import List


@dataclass
class REMINDER:
    GM_ID: int
    BLACKLISTED_IDS: List[int]
    TEXT_CHANNEL_ID: int
    VOICE_CHANNEL_ID: int
    GM_MESSAGE: str
    OTHERS_MESSAGE: str

from __future__ import annotations

import traceback
from typing import TYPE_CHECKING

from redbot.core import Config
from redbot.core.bot import Red
from redbot.core.utils.menus import menu

if TYPE_CHECKING:
    from .evolution import Evolution


class EvolutionUtils:
    def __init__(self, cog):
        self.bot: Red = cog.bot
        self.conf: Config = cog.conf
        self.cog: Evolution = cog

    @staticmethod
    def get_total_price(level, bought, amount, bt=True):
        total = 0
        for x in range(amount):
            normal = level * 800
            level_tax = ((2 ** level) * 10) - 200
            if bt:
                tax = bought * 300
                extra = x * 300
            else:
                tax = 0
                extra = 0
            total += normal + level_tax + tax + extra
        return total

    @property
    def levels(self):
        return {
            1: {100: 5},
            2: {90: 5, 100: 50},
            3: {80: 5, 100: 50},
            4: {70: 5, 100: 50},
            5: {60: 5, 100: 50},
            6: {50: 5, 90: 50, 100: 500},
            7: {40: 5, 80: 50, 100: 500},
            8: {30: 5, 70: 50, 100: 500},
            9: {20: 5, 60: 50, 100: 500},
            10: {10: 5, 50: 50, 100: 500},
            11: {40: 50, 90: 500, 100: 750},
            12: {30: 50, 80: 500, 100: 750},
            13: {20: 50, 70: 500, 100: 750},
            14: {10: 50, 60: 500, 100: 750},
            15: {50: 500, 100: 750},
            16: {40: 500, 100: 750},
            17: {30: 500, 100: 750},
            18: {20: 500, 100: 750},
            19: {10: 500, 100: 750},
            20: {90: 750, 100: 1000},
            21: {80: 750, 100: 1000},
            22: {70: 750, 100: 1000},
            23: {60: 750, 100: 1000},
            24: {50: 750, 100: 1000},
            25: {100: 1000},
        }

    @property
    def delays(self):
        return {
            1: 86400,  # 24 hours
            2: 64800,  # 18 hours
            3: 43200,  # 12 hours
            4: 39600,  # 11 hours
            5: 36000,  # 10 hours
            6: 32400,  #  9 hours
            7: 28800,  #  8 hours
            8: 25200,  #  7 hours
            9: 21600,  #  6 hours
            10: 18000,  #  5 hours
            11: 14400,  #  4 hours
            12: 10800,  #  3 hours
            13: 7200,  #  2 hours
            14: 3600,  #  1 hour
            15: 3000,  # 50 minutes
            16: 2400,  # 40 minutes
            17: 1800,  # 30 minutes
            18: 1200,  # 20 minutes
            19: 600,  # 10 minutes
            20: 420,  #  7 minutes
            21: 300,  #  5 minutes
            22: 240,  #  4 minutes
            23: 180,  #  3 minutes
            24: 120,  #  2 minutes
            25: 60,  #  1 minute
            26: 60,  #  1 minute (Just in case)
        }

    @property
    def randlvl_chances(self):
        return [
            1,
            2,
            3,
            4,
            4,
            5,
            5,
            5,
            6,
            6,
            6,
            6,
            7,
            7,
            7,
            7,
            8,
            8,
            8,
            8,
            9,
            9,
            9,
            9,
            10,
            10,
            10,
            10,
            10,
            10,
            11,
            11,
            11,
            11,
            11,
            12,
            12,
            12,
            12,
            12,
            12,
            13,
            13,
            13,
            13,
            13,
            14,
            14,
            14,
            14,
            14,
            15,
            15,
            15,
            15,
            16,
            16,
            16,
            17,
            17,
            18,
            19,
            20,
        ]

    @property
    def randamt_chances(self):
        return [1, 1, 2, 2, 2, 3, 3, 3, 4, 5]

    async def shop_control_callback(self, ctx, pages, controls, message, page, timeout, emoji):
        description = message.embeds[0].description
        level = int(description.split(" ")[1])
        self.bot.loop.create_task(ctx.invoke(self.cog.store, level=level))
        return await menu(ctx, pages, controls, message=message, page=page, timeout=timeout)

    def format_task(self, task):
        state = task["state"].lower()
        if task["exc"]:
            e = task["exc"]
            exc = traceback.format_exception(type(e), e, e.__traceback__)
            exc_output = (
                f"Please report the following error to Neuro Assassin: ```py\n{''.join(exc)}```"
            )
        else:
            exc_output = "No error has been encountered."
        return f"Task is currently {state}.  {exc_output}"

    def init_config(self):
        default_user = {
            "animal": "",
            "animals": {},
            "multiplier": 1.0,
            "bought": {},
            "stash": {"animals": {}, "perks": {}},
        }
        default_guild = {"cartchannel": 0, "last": 0}
        default_global = {
            "travelercooldown": "2h",
            "lastcredited": {},
            "lastdailyupdate": 0,
            "daily": {},
        }
        for x in range(1, 27):
            default_global["lastcredited"][str(x)] = 0

        self.conf.register_user(**default_user)
        self.conf.register_guild(**default_guild)
        self.conf.register_global(**default_global)

    async def initialize(self):
        config = await self.cog.conf.all_users()
        for k, v in config.items():
            self.cog.cache[k] = v

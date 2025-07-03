import discord
from discord.ext import commands
from discord import app_commands

from pokemon_formats import PokePaste

import json
import os
import logging
import time
import random

flavor_text = [
    "Samsara Labyrinth <3",
    
    "Is neko drawing yaoi?",
    "Made up of 1000 of Wristohsley's golden showers.",
    "Waterboarding sure is fun",
    "the rumi x koharu allegations are not being beaten\ni am one step away from getting on AO3/j",
    "I mean what kind of 13-year-old wouldn't want to fight monster in a thong?",
    "Fucking dysphoria magic",
    "I'm coming from the back",
    "so you're being intentionally sexual?",
    "Pokemon is the only type of game where I willingly touch grass",
    "Mum dad why did you make me autistic",
]

weight = [
    90,
    
    1,
    1,
    1,
    1,
    1,
    1,
    1, 
    1, 
    1, 
    1
]

logger = logging.getLogger(__name__)
logging.basicConfig(format=f"%(asctime)s - [%(levelname)-7s] : %(message)s", filename=f"logs/game_{int(time.time())}.txt", encoding="utf-8", level=logging.DEBUG)

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = []
        with open("./data/boxdata.txt", "r") as f:
            logger.info("Begin reading information from PokePaste.")
            for url in f.readlines():
                if url[-1] == "\n":
                    url = url[:-1]
                logger.info(f"Reading from {url}.")
                try:
                    current_data = list(PokePaste.retrieve_pokepaste(url))
                except ...:
                    logger.error("Read failure.")
                else:
                    logger.info("Read success.")
                self.data = self.data + current_data
        logger.info("Pokemon data read.")
    
    def embed_obj(self, pokemon : dict, color : int = 0xffffff) -> discord.Embed:
        stat_string = ["HP", "Atk", "Def", "SpA", "SpD", "Spe"]
        ev_str = ""
        iv_str = ""
        move_list = ""
        for move in pokemon["moves"]:
            if len(move_list) > 0:
                move_list = move_list + "\n"
            move_list = move_list + move
        
        embed = discord.Embed(title = pokemon["nickname"], description = f"{pokemon["nature"]} Nature", color=color)
        embed.add_field(name = "Species", value = f"{"Shiny " if pokemon["Shiny"] else ""}" + pokemon["species"], inline = True)
        embed.add_field(name = "Level", value = pokemon["Level"], inline = True)
        embed.add_field(name = "Gender", value = pokemon["gender"], inline = True)
        embed.add_field(name = "Held item", value = pokemon["item"], inline = True)
        embed.add_field(name = "Ability", value = pokemon["ability"], inline = True)
        for stat in stat_string:
            if pokemon["evs"][stat] > 0:
                if len(ev_str) > 0:
                    ev_str = ev_str + " / "
                ev_str = ev_str + f"{pokemon["evs"][stat]} {stat}"
            if pokemon["ivs"][stat] < 31:
                if len(iv_str) > 0:
                    iv_str = iv_str + " / "
                iv_str = iv_str + f"{pokemon["ivs"][stat]} {stat}"
        if len(ev_str) > 0:
            embed.add_field(name = "EVs", value = ev_str, inline = False)
        if len(iv_str) > 0:
            embed.add_field(name = "IVs", value = iv_str, inline = False)
        embed.add_field(name = "Moves", value = move_list, inline = False)
        
        embed.set_footer(text = random.choices(flavor_text, weight, k = 1)[0])
        return embed
    
    def search_by_nickname(self, nickname : str) -> list:
        output = []
        for pokemon in self.data:
            if pokemon["nickname"] == nickname:
                output.append(pokemon)
        return output

    @app_commands.command(name = "nickname_search", description = "Search Pokemon by nicknames")
    async def nickname_search(self, interaction, nickname : str):
        logger.debug(f"Retrieve data for {nickname}")
        pokemons = self.search_by_nickname(nickname)
        embed_list = []
        logger.debug(f"Found {len(pokemons)} sets")
        if len(pokemons) <= 0:
            await interaction.response.send_message("No pokemon exists with this specific nickname.")
            return
        for pokemon in pokemons:
            embed_list.append(self.embed_obj(pokemon))
        await interaction.response.send_message(embedss = embed_list)
    
    @app_commands.command(name = "generate", description = "Get random teams")
    @app_commands.choices(choices = [
        app_commands.Choice(name = "Singular", value = "single"),
        app_commands.Choice(name = "Two-Players", value = "two")
    ])
    async def generate(self, interaction, choices : app_commands.Choice[str]):
        if (choices.value == "single"):
            logger.info("Generate a single team.")
            pokemons = random.choices(self.data, k = 6)
            embed_list = []
            for pokemon in pokemons:
                embed_list.append(self.embed_obj(pokemon))
            await interaction.response.send_message(embeds = embed_list)
            return
        if (choices.value == "two"):
            logger.info("Generate two teams.")
            choice_pool = random.choices(self.data, k = 12)
            random.shuffle(choice_pool)
            team_1 = choice_pool[:6]
            team_2 = choice_pool[6:]
            
            embed_list = []
            for pokemon in team_1:
                embed_list.append(self.embed_obj(pokemon, 0x5BCEFA))
            await interaction.response.send_message(embeds = embed_list)
            
            embed_list = []
            for pokemon in team_2:
                embed_list.append(self.embed_obj(pokemon, 0xF5A9B8))
            await interaction.followup.send(embeds = embed_list)
            return
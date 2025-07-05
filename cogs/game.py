import discord
from discord.ext import commands
from discord import app_commands

from pokemon_formats import PokePaste, Showdown

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
    
    def team_generate(self, member_per_team : int, team_count : int, repeats : bool = False) -> list:
        output = []
        pokemons = []
        if (repeats):
            for i in range(team_count):
                output.append(list(random.choice(self.data, k = member_per_team)))
        else:
            if (member_per_team * team_count > len(self.data)):
                raise ValueError("There are not enough unique mons to make this configuration work!")
            
            pokemons = list(random.choices(self.data, k = team_count * member_per_team))
            for i in range(team_count):
                output.append(pokemons[(i * member_per_team):((i + 1) * member_per_team)])
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
        await interaction.response.send_message(embeds = embed_list)
    
    @app_commands.command(name = "basic_generate", description = "Get random teams")
    @app_commands.choices(choices = [
        app_commands.Choice(name = "Singular", value = "single"),
        app_commands.Choice(name = "Two-Players", value = "two")
    ])
    @app_commands.choices(formats = [
        app_commands.Choice(name = "Embeds", value = "embeds"),
        app_commands.Choice(name = "Pokepaste-ready", value = "pokepaste"),
    ])
    async def basic_generate(self, interaction, choices : app_commands.Choice[str], formats : app_commands.Choice[str]):
        try:
            if (choices.value == "single"):
                logger.info("Generate a single team.")
                teams = self.team_generate(6, 1)
                pokemons = teams[0]
                
                if (formats.value == "embeds"):
                    embed_list = []
                    for pokemon in pokemons:
                        embed_list.append(self.embed_obj(pokemon))
                    await interaction.response.send_message(embeds = embed_list)
                elif (formats.value == "pokepaste"):
                    showdown_format = Showdown.jsonToShowdown(pokemons)
                    await interaction.response.send_message(f"```\nP{showdown_format}\n```")
                else:
                    await interaction.response.send_message("Invalid format.")
                
                return
            elif (choices.value == "two"):
                logger.info("Generate two teams.")
                teams = self.team_generate(6, 2)
                team_1 = teams[0]
                team_2 = teams[1]
                
                if (formats.value == "embeds"):
                    embed_list = []
                    for pokemon in team_1:
                        embed_list.append(self.embed_obj(pokemon, 0x5BCEFA))
                    await interaction.response.send_message(embeds = embed_list)
                    embed_list = []
                    for pokemon in team_2:
                        embed_list.append(self.embed_obj(pokemon, 0xF5A9B8))
                    await interaction.followup.send(embeds = embed_list)
                elif (formats.value == "pokepaste"):
                    showdown_format_1 = Showdown.jsonToShowdown(team_1)
                    showdown_format_2 = Showdown.jsonToShowdown(team_2)
                    await interaction.response.send_message(f"Team 1:\n```\n{showdown_format_1}\n```")
                    await interaction.followup.send(        f"Team 2:\n```\n{showdown_format_2}\n```")
                else:
                    await interaction.response.send_message("Invalid format.")                
                
                return
            else:
                await interaction.response.send_message("Invalid choice.")
        except Exception as e:
            logger.error(repr(e))
            await interaction.response.send_message(f"Error: {repr(e)}")
        
    @app_commands.command(name = "advanced_generate", description = "Get random teams with more precise options.")
    @app_commands.describe(team_count = "Number of teams")
    @app_commands.describe(member_per_team = "Number of pokemons per team")
    @app_commands.describe(allow_repeats = "Are repeats allowed?")
    @app_commands.describe(formats = "What format the output should be in?")
    @app_commands.choices(allow_repeats = [
        app_commands.Choice(name = "Yes", value = 1),
        app_commands.Choice(name = "No", value = 0),
    ])
    @app_commands.choices(formats = [
        app_commands.Choice(name = "Embeds", value = "embeds"),
        app_commands.Choice(name = "Pokepaste-ready", value = "pokepaste"),
    ])
    async def advanced_generate(self, interaction, team_count : int, member_per_team : int, allow_repeats : app_commands.Choice[int], formats : app_commands.Choice[str]):
        allow_repeats = False if allow_repeats.value == 0 else True
        teams = self.team_generate(member_per_team, team_count, allow_repeats)
        await interaction.response.send_message("Generating teams...")
        if (formats.value == "embeds"):
            for team in teams:
                team_color = random.randint(0x000000, 0xffffff)
                embed_list = []
                for pokemon in team:
                    embed_list.append(self.embed_obj(pokemon, team_color))
                await interaction.followup.send(embeds = embed_list)
        elif (formats.value == "pokepaste"):
            for idx, team in enumerate(teams):
                showdown_text = Showdown.jsonToShowdown(team)
                await interaction.followup.send(f"Team {idx + 1}:\n```\n{showdown_text}\n```")
        else:
            logger.error("Invalid values in 'formats' variable.")
            await interaction.response.send_message("Invalid format.")
            
        
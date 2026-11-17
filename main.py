import asyncio
import os
from dotenv import load_dotenv
from poke_env.data import GenData
from poke_env.player import SimpleHeuristicsPlayer
from poke_env.player import MaxBasePowerPlayer
from battle_agent import BattleAgent
from poke_env.player import RandomPlayer
from poke_env import AccountConfiguration, ShowdownServerConfiguration

async def main():
    load_dotenv()
    SHOWDOWN_USERNAME, SHOWDOWN_PASSWORD =os.getenv("SHOWDOWN_USERNAME"), os.getenv("SHOWDOWN_PASSWORD")
    player = BattleAgent(
    account_configuration=AccountConfiguration(SHOWDOWN_USERNAME, SHOWDOWN_PASSWORD),
    server_configuration=ShowdownServerConfiguration)
    print("Awaiting players...")
    await player.accept_challenges(None, 10 )



if __name__ == "__main__":
    asyncio.run(main())


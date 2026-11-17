from poke_env import LocalhostServerConfiguration
from poke_env.data import GenData
from poke_env.player import Player
from poke_env.calc import damage_calc_gen9 as calc_gen9
from poke_env.stats import compute_raw_stats
from poke_env.battle import pokemon_type, Move
import random
import json


"""
This bot is a very limited and rudementry bot which odes not try predict any switches
It is optimised for gen 9 randoms.
"""
class BattleAgent(Player):

	def __init__(self, account_configuration=None, server_configuration=LocalhostServerConfiguration):
		super().__init__(max_concurrent_battles=20,
						 account_configuration=account_configuration,
						 server_configuration=server_configuration,
						 battle_format="gen9randombattle")
		self.gen_data = GenData.from_gen(9)
		self.opponent_team = {}
		with open("data/sets.json", "r") as f:
			self.all_sets = json.load(f)

	def choose_move(self, battle):
		try:
			if battle.battle_tag not in self.opponent_team:
				self.opponent_team[battle.battle_tag] = {}

			# Unused rn
			# user_pokemon_id = battle.active_pokemon.identifier(battle.player_role)
			# opponent_pokemon_id = battle.opponent_active_pokemon.base_species

			# Getting ids and init
			selected_attack = None
			selected_switch = None
			self.add_opponent_pokemon(battle)
			self.apply_opponent_stats(battle)

			if battle.available_moves:
				selected_attack = self.best_attack(battle)
			elif battle.available_switches:
				selected_switch = self.best_switch(battle)

			if selected_attack:
				return self.create_order(selected_attack)
			elif selected_switch:
				return self.create_order(selected_switch)
		except Exception as e:
			print(e)
		return self.choose_random_move(battle)

	def best_attack(self, battle):
		# Initalising vars
		max_dmg = 0
		selected_move = None
		user_pokemon_id = battle.active_pokemon.identifier(battle.player_role)
		opponent_pokemon_id = battle.opponent_active_pokemon.identifier(battle.opponent_role)
		# Checking if we have any avaliable moves
		if battle.available_moves:
			# Only 1 avaliable option lmao
			if len(battle.available_moves) == 1:
				return battle.available_moves[0]

			# Calcing dmg for each avaliable move
			for battle_move in battle.available_moves:
				# Assuming mid roll
				tested_dmg = calc_gen9.calculate_damage(user_pokemon_id, opponent_pokemon_id, battle_move, battle)[1]*0.9
				if tested_dmg > max_dmg:
					max_dmg = tested_dmg
					selected_move = battle_move
			if max_dmg == 0:
				print("no valid damaging move therefore switching")
				return self.best_switch(battle)
			if selected_move == None:
				# No valid move found
				# Should not trigger unless I am a dofus
				return random.choice(battle.available_moves)
			else:
				return selected_move

	def best_switch(self, battle):
		try:
			active_opponent_hidden_details = self.opponent_team[battle.battle_tag][self.get_set_key(battle.opponent_active_pokemon)]
			user_pokemon_id = battle.active_pokemon.identifier(battle.player_role)
			opponent_pokemon_id = battle.opponent_active_pokemon.identifier(battle.opponent_role)
			defense_ranking = {}
			attack_ranking = {}
			speed_ranking = {}
			overall_ranking = {}

			for pokemon in battle.available_switches:
				potential_pokemon_id = pokemon.identifier(battle.player_role)
				defense_ranking[pokemon] = 0.0
				attack_ranking[pokemon] = 0.0
				speed_ranking[pokemon] = pokemon.stats["spe"]
				overall_ranking[pokemon] = 0
				# Defense testing
				for details in active_opponent_hidden_details["sets"]:
					moveset = details["movepool"]
					# Calcing dmg for each avaliable move
					for battle_move in moveset:
						# Assuming mid roll
						# damage taken stores as a flot between 0 and 1.
						battle_move = battle_move.lower().replace(" ", "").replace("-", "")
						move_obj = Move(battle_move, 9)
						tested_dmg = (calc_gen9.calculate_damage(opponent_pokemon_id, potential_pokemon_id, move_obj, battle)[1]*0.9)/pokemon.max_hp
						if defense_ranking[pokemon] < tested_dmg:
							defense_ranking[pokemon] = tested_dmg

				# Attack ranking
				for battle_move in pokemon.moves:
					# Assuming mid roll
					# damage taken stores as a float between 0 and 1.
					tested_dmg = (calc_gen9.calculate_damage(potential_pokemon_id, opponent_pokemon_id,
															 Move(battle_move, 9), battle)[1] * 0.9) / battle.opponent_active_pokemon.max_hp
					if attack_ranking[pokemon] < tested_dmg:
						attack_ranking[pokemon] = tested_dmg


			attack_ranking = sorted(attack_ranking.items(), key=lambda item: item[1], reverse=True)
			defense_ranking = sorted(defense_ranking.items(), key=lambda item: item[1], reverse=True)
			speed_ranking = sorted(speed_ranking.items(), key=lambda item: item[1], reverse=True)
			categories = [attack_ranking, defense_ranking, speed_ranking]

			for area in categories:
				for i, pokemon in enumerate(area):
					overall_ranking[pokemon[0]] += 6-i

			return sorted(overall_ranking.items(), key=lambda item: item[1], reverse=True)[0][0]
		except Exception as err:
			print(err)
			return random.choice(battle.available_switches)

	def apply_opponent_stats(self, battle):
		opponent_pokemon_out = battle.opponent_active_pokemon
		opponent_stats = compute_raw_stats(opponent_pokemon_out.species,
										   [85, 85, 85, 85, 85, 85],
										   [31, 31, 31, 31, 31, 31],
										   level=opponent_pokemon_out.level,
										   nature="quirky",
										   data=self.gen_data)
		opponent_pokemon_out.stats = {
			'atk': opponent_stats[1],
			'def': opponent_stats[2],
			'hp': opponent_stats[0],
			'spa': opponent_stats[3],
			'spd': opponent_stats[4],
			'spe': opponent_stats[5]
		}

	def add_opponent_pokemon(self, battle):
		battle_tag = battle.battle_tag
		opposing_pokemon_out = battle.opponent_active_pokemon
		opponent_name = self.get_set_key(opposing_pokemon_out)
		if opponent_name not in self.opponent_team[battle_tag]:
			self.opponent_team[battle_tag][opponent_name] = self.all_sets[opponent_name]

	def get_set_key(self, pokemon) -> str:
		species = pokemon.species
		if species in self.all_sets:
			return species

		overrides = {
			"keldeo": "keldeoresolute",
			"palafinhero": "palafin",
			"eiscuenoice": "eiscue",
			"miniormeteor": "minior",
			"mimikyubusted": "mimikyu",
			"morpekohangry": "morpeko",
			"cramorantgulping": "cramorant",
			"cramorantgorging": "cramorant",
			"terapagosterastal": "terapagos",
			"terapagosstellar": "terapagos",
		}
		if species in overrides and overrides[species] in self.all_sets:
			return overrides[species]

		if pokemon.base_species in self.all_sets:
			return pokemon.base_species

		return species

	def _battle_finished_callback(self, battle):
		super()._battle_finished_callback(battle)

		self.opponent_team.pop(battle.battle_tag, None)
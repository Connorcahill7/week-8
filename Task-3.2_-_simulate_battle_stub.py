"""
Exercise 3.2: Simulate a Turn-Based Battle (Class-Based)

In this exercise, you will create a Pokemon class and use it to simulate battles.
This demonstrates object-oriented programming principles: encapsulation, methods, and clear responsibilities.
"""

import httpx


class Pokemon:
    """
    Represents a Pokemon with stats fetched from the PokeAPI.
    """

    def __init__(self, name):
        """
        Initialise a Pokemon by fetching its data from the API and calculating its stats.

        Args:
            name (str): The name of the Pokemon (e.g., "pikachu")
        """
        #storeing the name. original for print. lower for api)
        self.name = name
        pokemon_name = name.lower()

        #fetch pokemon data from the api
        url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name}"
        response = httpx.get(url)

        if response.status_code != 200:
            raise ValueError(f"could not load data for pokemon {name}")

        data = response.json()

        #get base stats from the api  
        base_stats = {}
        for stat_info in data["stats"]:
            stat_name = stat_info["stat"]["name"]   
            base_value = stat_info["base_stat"]
            if stat_name in ("hp", "attack", "defense", "speed"):
                base_stats[stat_name] = base_value

        #calculate stats at lvl 50
        max_hp = self._calculate_hp(base_stats["hp"])
        attack = self._calculate_stat(base_stats["attack"])
        defense = self._calculate_stat(base_stats["defense"])
        speed = self._calculate_stat(base_stats["speed"])

        #store stats in a dict
        self.stats = {
            "attack": attack,
            "defense": defense,
            "speed": speed
        }

        #   hp stored separately
        self.max_hp = max_hp
        self.current_hp = max_hp

    def _calculate_stat(self, base_stat, level=50, iv=15, ev=85):
        """
        Calculate a Pokemon's stat at a given level.
        Helper method (note the underscore prefix).

        Args:
            base_stat (int): The base stat value from the API
            level (int): Pokemon level (default 50)
            iv (int): Individual value (default 15)
            ev (int): Effort value (default 85)

        Returns:
            int: The calculated stat
        """
        stat = int(((2 * base_stat + iv + (ev / 4)) * level / 100) + 5)
        return stat

    def _calculate_hp(self, base_stat, level=50, iv=15, ev=85):
        """
        Calculate a Pokemon's HP at a given level.
        HP uses a different formula than other stats.

        Args:
            base_stat (int): The base HP value from the API
            level (int): Pokemon level (default 50)
            iv (int): Individual value (default 15)
            ev (int): Effort value (default 85)

        Returns:
            int: The calculated HP
        """
        hp = int(((2 * base_stat + iv + (ev / 4)) * level / 100) + level + 10)
        return hp

    def attack(self, defender):
        """
        Attack another Pokemon, dealing damage based on stats.

        Args:
            defender (Pokemon): The Pokemon being attacked

        Returns:
            int: The amount of damage dealt
        """
        level = 50
        base_power = 60

        #formula
        damage = int(
            (((2 * level * 0.4 + 2) * self.stats["attack"] * base_power)
             / (defender.stats["defense"] * 50)) + 2
        )

        if damage < 1:
            damage = 1

        #  damage to the defender
        defender.take_damage(damage)

        return damage

    def take_damage(self, amount):
        """
        Reduce this Pokemon's HP by the damage amount.

        Args:
            amount (int): The damage to take
        
        """

        self.current_hp -= amount
        if self.current_hp < 0:
            self.current_hp = 0

    def is_fainted(self):
        """
        Check if this Pokemon has fainted (HP <= 0).

        Returns:
            bool: True if fainted, False otherwise
        """
        if self.current_hp <= 0:
            return True
        else:
            return False

         

    def __str__(self):
        """
        String representation of the Pokemon for printing.

        Returns:
            str: A nice display of the Pokemon's name and HP
        """
        return f"{self.name} HP: {self.current_hp}/{self.max_hp}"


def simulate_battle(pokemon1_name, pokemon2_name):
    """
    Simulate a turn-based battle between two Pokemon.

    Args:
        pokemon1_name (str): Name of the first Pokemon
        pokemon2_name (str): Name of the second Pokemon
    """
    #poke objectects
    pokemon1 = Pokemon(pokemon1_name)
    pokemon2 = Pokemon(pokemon2_name)

    #display battle start
    print(". Pokemon Battle ")
    print(pokemon1)
    print(pokemon2)
    print()

    #  who attacks first 
    if pokemon1.stats["speed"] > pokemon2.stats["speed"]:
        attacker = pokemon1
        defender = pokemon2
    elif pokemon2.stats["speed"] > pokemon1.stats["speed"]:
        attacker = pokemon2
        defender = pokemon1
    else:
        # if same speed  pokemon1 go first
        attacker = pokemon1
        defender = pokemon2

    print(f"{attacker.name}  attacks first (speed: {attacker.stats['speed']}).\n")

    #  loop
    round_number = 1

    while not attacker.is_fainted() and not defender.is_fainted():
        print(f"....Round {round_number} ...")

        damage = attacker.attack(defender)
        print(f"{attacker.name} delt {damage} damage to {defender.name}.")
        print(defender)
        print()

        if defender.is_fainted():
            print(f"{defender.name} has fainted")
            break

        #swaps atck and def
        attacker, defender = defender, attacker
        round_number += 1

    #print battle
    if attacker.is_fainted() and defender.is_fainted():
        print("The battle ended in a draw.")
    elif attacker.is_fainted():
        print(f"{defender.name} has won the battle with {defender.current_hp} HP")
    else:
        print(f"{attacker.name} has won the batle with {attacker.current_hp} HP ")

    print("... Battle ends ....")


if __name__ == "__main__":
    # Test your battle simulator
    simulate_battle("eevee", "jigglypuff")

    # Uncomment to test other battles:
    # simulate_battle("charmander", "squirtle")
    # simulate_battle("eevee", "jigglypuff")

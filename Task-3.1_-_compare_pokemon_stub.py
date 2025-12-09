"""
Exercise 3.1: Fetch and Compare Pokémon Stats (Stub)
- Fetch data for two Pokémon from the PokéAPI.
- Calculate their stats at level 50.
- Compare their base stats (e.g., attack, defense, speed).
"""

import httpx

def calculate_stat(base_stat, level=50, iv=15, ev=85):
    """Calculate Pokémon's stat at given level."""
    return int(((2 * base_stat + iv + (ev / 4)) * level / 100) + 5)

def calculate_hp(base_stat, level=50, iv=15, ev=85):
    """Calculate Pokémon's HP at given level."""
    return int(((2 * base_stat + iv + (ev / 4)) * level / 100) + level + 10)


def get_base_stats(pokemon_name):
    # fetch base stats from poke api
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_name.lower()}"
    response = httpx.get(url)
    data = response.json()

    base_stats = {}

    for stat_info in data["stats"]:
        stat_name = stat_info["stat"]["name"]
        base_value = stat_info["base_stat"]

        if stat_name in ("hp", "attack", "defense", "speed"):
            base_stats[stat_name] = base_value

    return base_stats

def compare_pokemon(pokemon1, pokemon2):
    """Compare the calculated stats of two Pokémon."""
    
    base1 = get_base_stats(pokemon1)
    base2 = get_base_stats(pokemon2)

    #calc 50 lvls
    stats1 = {
        "hp": calculate_hp(base1["hp"]),
        "attack": calculate_stat(base1["attack"]),
        "defense": calculate_stat(base1["defense"]),
        "speed": calculate_stat(base1["speed"])
    }

    stats2 = {
        "hp": calculate_hp(base2["hp"]),
        "attack": calculate_stat(base2["attack"]),
        "defense": calculate_stat(base2["defense"]),
        "speed": calculate_stat(base2["speed"])
    }

    #print results
    print(f"\ncomparing {pokemon1} and {pokemon2} at level 50:\n")

    for stat in ["hp", "attack", "defense", "speed"]:
        p1_value = stats1[stat]
        p2_value = stats2[stat]

        print(f"{stat}: {pokemon1} = {p1_value}, {pokemon2} = {p2_value}")

        if p1_value > p2_value:
            print(f"  {pokemon1} has higher {stat}.\n")
        elif p2_value > p1_value:
            print(f" {pokemon2} has higher {stat}.\n")
        else:
            print(f" Both have the same {stat}.\n")


# Example usage
if __name__ == "__main__":
    compare_pokemon("charmander", "squirtle")

"""
Hints:
- Use httpx.get(url) to fetch data for each Pokémon.
- Access base stats using data['stats'] and extract base_stat values.
- Use calculate_stat and calculate_hp to compute level 50 stats.
"""

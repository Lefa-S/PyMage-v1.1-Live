import time
import random

#Stat management
default_mana = 100
default_health = 150
computer_mana_shield_active = False
user_mana_shield_active = False
computer_poison_active = False
user_poison_active = False
user_poison_turns_remaining = 3
computer_poison_turns_remaining = 3
computer_current_health = default_health
computer_current_mana = default_mana
user_current_health = default_health
user_current_mana = default_mana

#Abilities
basic_attacks = ["Fireball", "Arcane Blast", "Lightning Strike"]
elemental_attacks = ["Ice Shards", "Earthquake", "Poison Cloud"]
defensive_abilities = ["Mana Shield", "Counter Strike", "Healing"]
highrisk_highreward = ["Dark Pulse", "Inferno", "Soul Flare"]

#Computer abilities random choice
computer_basic_attacks = random.choice(basic_attacks)
computer_elemental_attacks = random.choice(elemental_attacks)
computer_defensive_attacks = random.choice(defensive_abilities)
computer_highrisk_attacks = random.choice(highrisk_highreward)

# Player abilities random choice
user_basic_attacks = random.choice(basic_attacks)
user_elemental_attacks = random.choice(elemental_attacks)
user_defensive_attacks = random.choice(defensive_abilities)
user_highrisk_attacks = random.choice(highrisk_highreward)

def game_initiation():
    global play_option
    while True:
        if play_option == "e":
            pve_battle_logic()
            break
        elif play_option == "i":
            ability_descriptions()
            break
        elif play_option == "q":
            break
        else:
            print("Please enter a valid option.")
            play_option = input(
                "PyMage, are you ready? Enter E to conjure your destiny, I to see ability descriptions or Q to quit. ").lower()
            continue

def game_end():
    global user_current_health
    global computer_current_health
    global computer_current_mana
    global user_current_mana
    while True:
        print("GAME OVER!")
        game_end_input = input("Press ENTER to exit or R to restart: ").lower()
        if game_end_input == "r":
            user_current_health = 150
            user_current_mana = 100
            computer_current_health = 150
            computer_current_mana = 100
            game_initiation()
        elif game_end_input == "":
            exit()
        else:
            print("Please enter a valid option.")
            continue

def ability_descriptions():
    global play_option
    print("Basic Ability Descriptions:")
    print("-" * 100)
    print("Fireball: 30 dmg, 15 mana, Straightforward attack.")
    print("Arcane Blast: 25 dmg, 10 mana, Reliable magic attack, no special effects.")
    print("Lightning Strike: 45 dmg, 25 mana, 70% chance to hit (30% chance to miss).")
    print("-" * 100)
    print("Elemental Ability Descriptions:")
    print("-" * 100)
    print("Ice Shard: 18 dmg, 12 mana, 50% chance to freeze the enemy, causing them to skip their next turn.")
    print("Earthquake: 28 dmg, 18 mana, 30% chance to stun (disable enemy for 1 turn).")
    print("Poison Mist: 12 dmg (per turn over 3 turns), 15 mana, Reduces healing received by 50% for the duration.")
    print("-" * 100)
    print("Defensive Ability Descriptions:")
    print("-" * 100)
    print("Mana Shield: 0 dmg, 18 mana, Absorbs 50% of incoming damage for the next 2 turns.")
    print("Counterstrike: 30 dmg, 15 mana, Blocks the next incoming attack and delivers 30 damage.")
    print("Healing Light: 0 dmg, 20 mana, Heals 30 health.")
    print("-" * 100)
    print("High Risk High Reward Descriptions:")
    print("-" * 100)
    print("Dark Pulse: 40 dmg, 30 mana, Ignores defense.")
    print("Inferno: 50 dmg, 40 mana, Deals 5 health damage per turn for 3 turns.")
    print("Soul Flare: 60 dmg, 40 mana, If it lands, it deals massive damage. If it misses, you take 15 damage. Hit Chance: 60%")
    print("-" * 100)
    play_option = input("Begin game with e or quit with q? ")
    game_initiation()



#Poison functions
def user_apply_poison():
    global computer_current_health
    global user_poison_turns_remaining

    if user_poison_turns_remaining > 0:
        computer_current_health -= 12  # Poison damage per turn
        user_poison_turns_remaining -= 1
        print("Poison damage dealt!")

def computer_apply_poison():
    global user_current_health
    global computer_poison_turns_remaining

    if computer_poison_turns_remaining > 0:
        user_current_health -= 12  # Poison damage per turn
        computer_poison_turns_remaining -= 1
        print("Poison damage dealt!")

#Checking if poison is active
while computer_poison_active:
    computer_apply_poison()

while user_poison_active:
    user_apply_poison()

#Attack input
def user_focus():
    global user_current_mana
    user_current_mana += 30
    current_stats()
    computer_functions()

def automatic_user_focus():
    global user_current_mana
    print("Player mana depleted focusing...")
    user_current_mana += 30
    current_stats()
    computer_functions()

def user_basic():
    global computer_current_health
    global user_current_mana
    if user_basic_attacks == "Fireball":
        if user_current_mana < 15:
            print("Not enough mana!")
            player_functions()
        else:
            computer_current_health -= 30  # Damage
            user_current_mana -= 15  # Mana cost
            current_stats()
            computer_functions()

    elif user_basic_attacks == "Arcane Blast":
        if user_current_mana < 10:
            print("Not enough mana!")
            player_functions()
        else:
            computer_current_health -= 25  # Damage1
            user_current_mana -= 10  # Mana cost
            current_stats()
            computer_functions()

    elif user_basic_attacks == "Lightning Strike":
        if user_current_mana < 25:
            print("Not enough mana!")
            player_functions()
        else:
            computer_current_health -= 45  # Damage
            user_current_mana -= 25  # Mana cost
            current_stats()
            computer_functions()

def user_elemental():
    global computer_current_health
    global user_current_mana
    global user_poison_active
    if user_elemental_attacks == "Ice Shards":
        if user_current_mana < 12:
            print("Not enough mana!")
            player_functions()
        else:
            computer_current_health -= 18  # Damage
            user_current_mana -= 12  # Mana cost
            current_stats()
            computer_functions()

    elif user_elemental_attacks == "Earthquake":
        if user_current_mana < 18:
            print("Not enough mana!")
            player_functions()
        else:
            computer_current_health -= 28  # Damage
            user_current_mana -= 18  # Mana cost
            current_stats()
            computer_functions()

    elif user_elemental_attacks == "Poison Cloud":
        if user_current_mana < 15:
            print("Not enough mana!")
            player_functions()
        else:
            user_poison_active = True
            computer_current_health -= 12  # Damage per turn over 3 turns
            user_current_mana -= 15  # Mana cost
            current_stats()
            user_apply_poison()
            computer_functions()

def user_defensive():
    global user_current_mana
    global user_current_health
    global user_mana_shield_active

    if user_defensive_attacks == "Mana Shield":
        if user_current_mana < 50:
            print("Not enough mana!")
            player_functions()
        else:
            user_mana_shield_active = True  # Turn on the shield
            user_current_mana -= 50
            current_stats()
            computer_functions()


    elif user_defensive_attacks == "Counter Strike":
        if user_current_mana < 15:
            print("Not enough mana!")
            player_functions()
        else:
            user_current_mana -= 15  # Mana cost
            current_stats()
            computer_functions()

    elif user_defensive_attacks == "Healing":
        if user_current_mana < 20:
            print("Not enough mana!")
            player_functions()
        else:
            user_current_health += 30  # Healing amount
            user_current_mana -= 20  # Mana cost
            current_stats()
            computer_functions()

def user_highrisk():
    global computer_current_health
    global user_current_health
    global user_current_mana
    if user_highrisk_attacks == "Dark Pulse":
        if user_current_mana < 30:
            print("Not enough mana!")
            player_functions()
        else:
            computer_current_health -= 40  # Damage
            user_current_mana -= 30  # Mana cost
            current_stats()
            computer_functions()

    elif user_highrisk_attacks == "Inferno":
        if user_current_mana < 40:
            print("Not enough mana!")
            player_functions()
        else:
            computer_current_health -= 50  # Damage
            user_current_health -= 20 # User burning themselves
            user_current_mana -= 40  # Mana cost
            current_stats()
            computer_functions()

    elif user_highrisk_attacks == "Soul Flare":
        if user_current_mana < 40:
            print("Not enough mana!")
            player_functions()
        else:
            hit_chance = random.randint(1, 100)
            if hit_chance <= 60:  # 60% chance to land the attack
                computer_current_health -= 60
                user_current_mana -= 40# Damage
                computer_functions()
            else:
                user_current_health -= 40  # Miss penalty damage
                user_current_mana -= 40  # Mana cost
                current_stats()
                print("Soul Flare Missed!")
                computer_functions()

def user_death():
    current_stats()
    print("Player has been slain!")
    game_end()

def computer_focus():
    global computer_current_mana
    computer_current_mana += 30
    current_stats()
    player_functions()

def automatic_computer_focus():
    global computer_current_mana
    print("Computer mana depleted focusing...")
    computer_current_mana += 30
    current_stats()
    player_functions()

def computer_basic():
    global user_current_health
    global computer_current_mana
    global player_move
    global computer_poison_active
    if computer_basic_attacks == "Fireball":
        if computer_current_mana < 15:
            print("Not enough mana!")
            computer_functions()
        else:
            user_current_health -= 30
            computer_current_mana -= 15
            current_stats()
            player_functions()

    elif computer_basic_attacks == "Arcane Blast":
        if computer_current_mana < 10:
            print("Not enough mana!")
            computer_functions()
        else:
            user_current_health -= 25
            computer_current_mana -= 10
            current_stats()
            player_functions()

    elif computer_basic_attacks == "Lightning Strike":
        if computer_current_mana < 25:
            print("Not enough mana!")
            computer_functions()
        else:
            user_current_health -= 45
            computer_current_mana -= 25
            current_stats()
            player_functions()

def computer_elemental():
    global user_current_health
    global computer_current_mana
    global player_move
    global computer_poison_active
    if computer_elemental_attacks == "Ice Shards":
        user_current_health -= 30
        computer_current_mana -= 15
        current_stats()
        player_functions()

    elif computer_elemental_attacks == "Earthquake":
        if computer_current_mana < 40:
            print("Not enough mana!")
            computer_functions()
        else:
            user_current_health -= 28
            computer_current_mana -= 18
            current_stats()
            player_functions()

    elif computer_elemental_attacks == "Poison Cloud":
        if computer_current_mana < 14:
            print("Not enough mana!")
            computer_functions()
        else:
            computer_poison_active = True
            user_current_health -= 18
            computer_current_mana -= 14
            current_stats()
            computer_apply_poison()
            player_functions()

def computer_defensive():
    global computer_current_mana
    global user_current_health
    global computer_mana_shield_active
    global computer_current_health
    if computer_defensive_attacks == "Mana Shield":
        if computer_current_mana < 50:
            print("Not enough mana!")
            computer_functions()
        else:
            computer_mana_shield_active = True  # Turn on the shield
            computer_current_mana -= 50
            current_stats()
            player_functions()

    elif computer_defensive_attacks == "Counter Strike":
        if computer_current_mana < 15:
            print("Not enough mana!")
            computer_functions()
        else:
            computer_current_mana -= 15  # Mana cost
            current_stats()
            player_functions()

    elif computer_defensive_attacks == "Healing":
        if computer_current_mana < 20:
            print("Not enough mana!")
            computer_functions()
        else:
            computer_current_health += 30  # Healing amount
            computer_current_mana -= 20  # Mana cost
            current_stats()
            player_functions()

def computer_highrisk():
    global user_current_health
    global computer_current_mana
    global computer_current_health
    global player_move
    if computer_highrisk_attacks == "Dark Pulse":
        if computer_current_mana < 30:
            print("Not enough mana!")
            computer_functions()
        else:
            user_current_health -= 40
            computer_current_mana -= 30
            current_stats()
            player_functions()

    elif computer_highrisk_attacks == "Inferno":
        if computer_current_mana < 40:
            print("Not enough mana!")
            computer_functions()
        else:
            user_current_health -= 50
            computer_current_health -= 20  # first turn of burn
            computer_current_mana -= 40
            current_stats()
            player_functions()

    elif computer_highrisk_attacks == "Soul Flare":
        if computer_current_mana < 40:
            print("Not enough mana!")
            computer_functions()
        else:
            hit_chance = random.randint(1, 100)
            if hit_chance <= 60:
                user_current_health -= 60
                computer_current_mana -= 40
                player_functions()
            else:
                computer_current_health -= 40
                computer_current_mana -= 40
                current_stats()
                print("Soul Flare Missed!")
                player_functions()

def computer_death():
    current_stats()
    print("Computer has been slaughtered!")
    game_end()


#Update and Display player stats
def current_stats():
    print(f"""
    +-------------------------------+-------------------------------+
    |         🧠 COMPUTER           |           🧙 PLAYER           |
    +-------------------------------+-------------------------------+
    | Health:  {computer_current_health:<3} / 150            | Health: {user_current_health:<3} / 150             |
    | Mana:  {computer_current_mana:<3}/ 100               | Mana: {user_current_mana:<3} / 100               |
    |                               |                               |
    | Basic Attacks:                | Basic Attacks:                |
    | {computer_basic_attacks:<30} | {user_basic_attacks:<30} |
    | Elemental Attacks:            | Elemental Attacks:            |
    | {computer_elemental_attacks:<30} | {user_elemental_attacks:<30} |
    | Defensive Abilities:          | Defensive Abilities:          |
    | {computer_defensive_attacks:<30} | {user_defensive_attacks:<30} |
    | High-Risk, High-Reward:       | High-Risk, High-Reward:       |
    | {computer_highrisk_attacks:<30} | {user_highrisk_attacks:<30} |
    +-------------------------------+-------------------------------+
    | What Happened:                | What Happened:                |
    | - [Event description here]    | - [Event description here]    |
    +-------------------------------+-------------------------------+
    """)

def player_functions():  # Accept player_move

    while True:
        if user_current_health <= 0:
            user_death()
            break
        elif user_current_mana <= 0:
            automatic_user_focus()
            break
        player_move = input("Player, what is your choice? [type basic, elemental, defensive, HRHR or focus]: ").lower()
        if player_move == "basic":
            user_basic()
            break
        elif player_move == "elemental":
            user_elemental()
            break
        elif player_move == "defensive":
            user_defensive()
            break
        elif player_move == "hrhr":
            user_highrisk()
            break
        elif player_move == "focus":
            user_focus()
        else:
            print("Please enter a valid option.")
            continue

#computer_functions to handle its logic
def computer_functions():
    computer_move_choices = ["basic", "elemental", "defensive", "highrisk", "focus"]
    computer_move = random.choice(computer_move_choices)
    print(f"Computer move: {computer_move}")
    if computer_current_health <= 0:
        computer_death()
    elif computer_current_mana <= 0:
        automatic_computer_focus()
    elif computer_move == "basic":
        computer_basic()
    elif computer_move == "elemental":
        computer_elemental()
    elif computer_move == "defensive":
        computer_defensive()
    elif computer_move == "highrisk":
        computer_highrisk()
    elif computer_move == "focus":
        computer_focus()


# Game logic to start battle
def pve_battle_logic():
    print("Battle Begins in...")
    for i in range(5, 0, -1):
        print(i)
        time.sleep(1)

    print(" ")
    print("-" * 100)
    print(" ")
    current_stats()
    start_first = ["Player", "Computer"]
    start_first_choice = random.choice(start_first)
    print(f"{start_first_choice} starts first!")

    global player_move
    if start_first_choice == "Player":
        player_functions()
    else:
        computer_functions()

# Game title and intro
print("""
╔═══════════════════════════╗
║       🧙 PyMage 🐍        ║
╚═══════════════════════════╝

Welcome to the Arcane Arena!

You are a PyMage — a master of spells and strategy.
Face off against enemy wizards controlled by dark code,
or challenge a real opponent in magical combat.

Outsmart. Outcast. Outspell.

Will you rise... or be deleted?

Created by Mojalefa Sekgobela (May 2025)
""")

play_option = input("PyMage, are you ready? Enter E to conjure your destiny, I to see ability descriptions or Q to quit. ").lower()
game_initiation()

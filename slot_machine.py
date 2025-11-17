# =========================
# Person 1 Code
# =========================
import random
import json
import os
import datetime
import time

symbols = ['🍒', '🍋', '🔔', '💎', '7️⃣', '🍀', '♠']
symbol_multipliers = {
    '🍒': 8,
    '🍋': 6,
    '🔔': 10,
    '💎': 12,
    '7️⃣': 15,
    '🍀': 9,
    '♠': 7
}
results = []

def get_float(prompt):
    try:
        value = float(input(prompt))
        return value if value > 0 else None
    except ValueError:
        return None

def get_int(prompt):
    try:
        value = int(input(prompt))
        return value if value > 0 else None
    except ValueError:
        return None

def spin_reels():
    return [random.choice(symbols) for _ in range(3)]

def count_symbols(spin_result):
    counts = {}
    for s in spin_result:
        counts[s] = counts.get(s, 0) + 1
    return counts

def calculate_winnings(counts, bet, spin_result):
    winnings = 0

    if 3 in counts.values():  
        # FIXED: correctly detect the matched symbol
        symbol = [s for s, c in counts.items() if c == 3][0]
        multiplier = symbol_multipliers.get(symbol, 10)
        winnings = bet * multiplier
        print(f"\033[92mJACKPOT! {' | '.join(spin_result)} — You win ${winnings:.2f}!\033[0m")

    elif 2 in counts.values():
        winnings = bet * 2
        print(f"\033[94mNice! {' | '.join(spin_result)} — You win ${winnings:.2f}!\033[0m")

    else:
        print(f"\033[91m{' | '.join(spin_result)} — No match. You lost your bet.\033[0m")

    return winnings

def session_summary(results, final_balance):
    total_bet = sum(float(r['bet']) for r in results)
    total_won = sum(float(r['winnings']) for r in results)
    win_count = sum(1 for r in results if float(r['winnings']) > 0)
    print("\n===== SESSION SUMMARY =====")
    print(f"Total Spins     : {len(results)}")
    print(f"Total Bet       : ${total_bet:.2f}")
    print(f"Total Winnings  : ${total_won:.2f}")
    print(f"Win Rate        : {(win_count / len(results)) * 100:.1f}%")
    print(f"Final Balance   : ${final_balance:.2f}")
    print("============================\n")

def display_spin_table(results):
    print("\n----- SPIN RESULTS -----")
    print(f"{'Spin':<5} {'Symbols':<20} {'Bet':<8} {'Winnings':<10} {'Balance':<10}")
    for r in results:
        print(f"{r['spin']:<5} {' '.join(r['symbols']):<20} ${r['bet']:<7} ${r['winnings']:<9} ${r['balance']:<9}")
    print("------------------------\n")


# =========================
# Person 2 Code
# =========================
player_file = "players.json"
leaderboard_file = "leaderboard.json"

def load_players():
    if os.path.exists(player_file):
        with open(player_file, "r") as f:
            return json.load(f)
    return {}

def save_players(data):
    with open(player_file, "w") as f:
        json.dump(data, f, indent=4)

def load_leaderboard():
    if os.path.exists(leaderboard_file):
        with open(leaderboard_file, "r") as f:
            return json.load(f)
    return {}

def save_leaderboard(data):
    with open(leaderboard_file, "w") as f:
        json.dump(data, f, indent=4)

def login():
    data = load_players()
    name = input("Enter your player name: ").strip()
    if not name:
        print("Invalid name.")
        return login()
    if name not in data:
        print("Creating new player profile...")
        data[name] = {
            "balance": 100.0,
            "total_won": 0.0,
            "games": 0,
            "last_bonus": "",
            "level": 1,
            "streak": 0,
            "last_win": 0
        }
        save_players(data)
    else:
        print(f"Welcome back, {name}!")
    return name

def get_balance(name):
    players = load_players()
    return players.get(name, {}).get("balance", 0)

def update_balance(name, amount):
    data = load_players()
    if name in data:
        data[name]["balance"] = amount
        save_players(data)

def add_to_leaderboard(name, winnings):
    lb = load_leaderboard()
    lb[name] = lb.get(name, 0) + winnings
    save_leaderboard(lb)

def daily_bonus(name):
    players = load_players()
    today = str(datetime.date.today())
    player = players.get(name)
    if player:
        if player.get("last_bonus") == today:
            print("You already claimed your daily bonus.")
        else:
            bonus = random.randint(20, 100)
            player["balance"] += bonus
            player["last_bonus"] = today
            save_players(players)
            print(f"🎁 Daily Bonus: You received ${bonus}! New balance: ${player['balance']:.2f}")

def show_leaderboard():
    lb = load_leaderboard()
    if not lb:
        print("No leaderboard data yet.")
        return
    sorted_lb = sorted(lb.items(), key=lambda x: x[1], reverse=True)
    print("\n===== 🏆 LEADERBOARD 🏆 =====")
    for i, (player, score) in enumerate(sorted_lb[:10], start=1):
        print(f"{i}. {player:<12} ${score:.2f}")
    print("=============================")

def check_achievements(name):
    data = load_players()
    if name not in data:
        return
    p = data[name]
    earned = []
    if p["games"] >= 5:
        earned.append("Frequent Spinner")
    if p["total_won"] >= 500:
        earned.append("Lucky Star")
    if p["balance"] >= 1000:
        earned.append("High Roller")
    if earned:
        print("\n🎖️ Achievements Unlocked:")
        for a in earned:
            print(f"- {a}")
        print()
    else:
        print("No new achievements yet.")


# =========================
# Person 3 Code
# =========================

def level_up(name):
    data = load_players()
    player = data.get(name)
    if player:
        new_level = 1 + player["total_won"] // 200
        if new_level > player["level"]:
            player["level"] = new_level
            print(f"🎉 Congrats {name}, you've leveled up to Level {player['level']}!")
            save_players(data)

def streak_bonus(name):
    data = load_players()
    player = data.get(name)
    if player:
        streak = player.get("streak", 0)
        if streak >= 2:
            bonus = streak * 5
            player["balance"] += bonus
            print(f"🔥 Streak Bonus! You gained ${bonus} for a {streak}-win streak!")
            save_players(data)

def double_or_nothing(name):
    data = load_players()
    player = data.get(name)
    if not player:
        return 0

    last_win = player.get("last_win", 0)

    if last_win <= 0:
        print("No winnings to gamble.")
        return 0

    print("\n💥 Double or Nothing! 💥")
    print("Guess heads or tails. If correct, you double your winnings!")
    
    guess = input("Enter 'heads' or 'tails': ").strip().lower()
    if guess not in ["heads", "tails"]:
        print("Invalid choice.")
        return 0

    outcome = random.choice(["heads", "tails"])
    print(f"Coin toss: {outcome}")

    if guess == outcome:
        extra = last_win
        player["balance"] += extra
        player["last_win"] += extra
        print(f"🎉 You won an extra ${extra}!")
    else:
        print("😢 You lost your winnings.")
        player["balance"] -= last_win
        player["last_win"] = 0

    save_players(data)

def show_stats(name):
    data = load_players()
    player = data.get(name)
    if not player:
        return
    print("\n===== PLAYER STATS =====")
    print(f"Player: {name}")
    print(f"Level : {player['level']}")
    print(f"Balance : ${player['balance']:.2f}")
    print(f"Total Winnings: ${player['total_won']:.2f}")
    print(f"Games Played : {player['games']}")
    print(f"Win Streak   : {player['streak']}")
    print("========================\n")


# =========================
# Integrated Main Loop
# =========================

def main():
    print("🎰 Welcome to the Ultimate Slot Machine 🎰")
    name = login()

    while True:
        print(f"\n===== MAIN MENU ({name}) =====")
        print("1. Play Slot Machine")
        print("2. Claim Daily Bonus")
        print("3. View Leaderboard")
        print("4. Check Achievements")
        print("5. Show Stats")
        print("6. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            balance = get_balance(name)
            print(f"Your balance: ${balance:.2f}")
            spins = get_int("How many spins would you like to play? ")
            if not spins:
                print("Invalid input.")
                continue

            results = []
            total_won = 0.0

            for i in range(spins):
                bet = get_float(f"Spin {i+1}: Enter your bet (Current Balance: ${balance:.2f}): ")
                if not bet or bet > balance:
                    print("Invalid bet. Spin skipped.")
                    continue

                balance -= bet
                spin_result = spin_reels()
                counts = count_symbols(spin_result)

                winnings = calculate_winnings(counts, bet, spin_result)
                balance += winnings
                total_won += winnings

                results.append({
                    'spin': i + 1,
                    'symbols': spin_result,
                    'bet': f"{bet:.2f}",
                    'winnings': f"{winnings:.2f}",
                    'balance': f"{balance:.2f}"
                })

                # Update streak BEFORE bonuses
                data = load_players()
                data[name]["last_win"] = winnings

                if winnings > 0:
                    data[name]["streak"] += 1
                else:
                    data[name]["streak"] = 0

                save_players(data)

                # OPTIONAL Double or Nothing
                play_don = input("Play Double or Nothing? (y/n): ").strip().lower()
                if play_don == "y":
                    double_or_nothing(name)

                streak_bonus(name)
                level_up(name)

            display_spin_table(results)
            session_summary(results, balance)

            players = load_players()
            if name in players:
                players[name]["balance"] = balance
                players[name]["total_won"] += total_won
                players[name]["games"] += 1
                save_players(players)

            add_to_leaderboard(name, total_won)
            print(f"New balance saved: ${balance:.2f}")

        elif choice == "2":
            daily_bonus(name)

        elif choice == "3":
            show_leaderboard()

        elif choice == "4":
            check_achievements(name)

        elif choice == "5":
            show_stats(name)

        elif choice == "6":
            print("Goodbye! Your progress has been saved.")
            break

        else:
            print("Invalid option. Try again.")

main()

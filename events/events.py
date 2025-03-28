import random

def create_event_dnipro_tax(player, game_time):
    def resolve_tax_event(choice):
        today = game_time.strftime("%d.%m.%Y")

        if choice == "Заплатити податок":
            if random.random() < 0.5:
                result = "Ви сплатили справжній податок. -5000 ₴"
                player.balance -= 5000
            else:
                result = "Це був скам. Ви втратили 5000 ₴"
                player.balance -= 5000

        elif choice == "Дати хабар":
            roll = random.random()
            if roll < 0.3:
                result = "Хабар прийняли. -3000 ₴"
                player.balance -= 3000
            elif roll < 0.7:
                result = "Скамери втекли з грошима. -3000 ₴"
                player.balance -= 3000
            else:
                result = "Податкова оштрафувала. -10 000 ₴"
                player.balance -= 10000

        elif choice == "Відмовитися":
            roll = random.random()
            if roll < 0.5:
                result = "Нічого не сталося."
            elif roll < 0.8:
                result = "Скамери пошкодили офіс. -7000 ₴"
                player.balance -= 7000
            else:
                result = "Податкова наклала штраф. -15 000 ₴"
                player.balance -= 15000

        player.log.insert(0, f"{today} — {result}")

        return {
            "type": "info",
            "title": "Наслідки зустрічі",
            "text": result,
            "options": ["Закрити"]
        }

    return {
        "type": "choice",
        "title": "Дніпровські офіси",
        "text": "До вас звертається представник 'податкової'. Пропонує вирішити питання з податками.",
        "options": ["Заплатити податок", "Дати хабар", "Відмовитися"],
        "on_choice": {
            "Заплатити податок": lambda: resolve_tax_event("Заплатити податок"),
            "Дати хабар": lambda: resolve_tax_event("Дати хабар"),
            "Відмовитися": lambda: resolve_tax_event("Відмовитися")
        }
    }

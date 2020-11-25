import emoji


def price_change_emoji(change):
    change_sign = ""
    if change >= 10:
        change_sign = emoji.emojize("🚀")
    elif change > 0:
        change_sign = emoji.emojize("⬆")
    elif change < -10:
        change_sign = emoji.emojize("💩")
    elif change < 0:
        change_sign = emoji.emojize("⬇")
    return change_sign
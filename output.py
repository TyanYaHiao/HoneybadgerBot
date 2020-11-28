import emoji


def price_change_emoji(change):
    change_sign = ""
    # if change >= 10:
    #     change_sign = emoji.emojize("🚀")
    if change > 0:
        change_sign = emoji.emojize("⬆")
    # elif change < -10:
    #     change_sign = emoji.emojize("💩")
    elif change < 0:
        change_sign = emoji.emojize("⬇")
    return change_sign


def ticker_output(stock):
    output_line = "\n*" + stock.ticker_short  + ":* " \
                  + str(round(stock.cost, 1)) + " " + stock.currency_sign + ", "\
                  + stock.change_sign + " " \
                  + str(round(stock.change, 1)) + " " + stock.currency_sign + " ("\
                  + str(round(stock.change_percent, 2)) + " %)"
    return output_line

import alpaca_trade_api as tradeapi
import datetime

# Function to get the 30 delta put option
def get_30_delta_put(api, symbol):
    options = api.get_options(symbol)
    for option in options:
        if option['delta'] == 0.3:
            return option
    return None

# Function to place a credit put spread order
def place_credit_put_spread(api, symbol, quantity):
    option = get_30_delta_put(api, symbol)
    if option:
        order = api.submit_order(
            symbol=symbol,
            qty=quantity,
            side='sell',
            type='limit',
            time_in_force='day',
            order_class='bracket',
            take_profit=dict(
                limit_price=option['ask_price'] * 1.1,
            ),
            stop_loss=dict(
                stop_price=option['bid_price'] * 0.9,
            )
        )
        return order
    return None

# Main function to execute the trading bot daily
def main():
    api = tradeapi.REST('APCA-API-KEY-ID', 'APCA-API-SECRET-KEY', base_url='https://paper-api.alpaca.markets')
    symbol = 'AAPL'
    quantity = 1

    while True:
        now = datetime.datetime.now()
        if now.hour == 9 and now.minute == 30:
            place_credit_put_spread(api, symbol, quantity)
        time.sleep(60)

if __name__ == "__main__":
    main()

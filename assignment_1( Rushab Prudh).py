import pandas as pd

def open_range_breakout_strategy(data):
    pnl = 0
    position = None
    stop_loss_percentage = 0.5 / 100  # 0.5% as stop loss
    
    for index, row in data.iterrows():
        timestamp = pd.to_datetime(row['Timestamp'])
        open_price = row['Open']
        high_price = row['High']
        low_price = row['Low']
        close_price = row['Close']
        
        # Check if it's the first 15 minutes of the trading day
        if timestamp.time() >= pd.to_datetime('09:15:00').time() and timestamp.time() <= pd.to_datetime('09:30:00').time():

            # Buy if high is crossed
            if high_price > open_price:
                if position is None:
                    position = {'type': 'buy', 'entry_price': high_price, 'stop_loss': open_price * (1 - stop_loss_percentage)}
                else:
                    if position['stop_loss']< open_price * (1 - stop_loss_percentage):
                        position = {'type': 'buy', 'entry_price': high_price, 'stop_loss': open_price * (1 - stop_loss_percentage)}

            # Sell if low is crossed
            elif low_price < open_price:
                if position is None:
                    position = {'type': 'sell', 'entry_price': low_price, 'stop_loss': open_price * (1 + stop_loss_percentage)}
                else:
                    if position['stop_loss'] < open_price * (1 + stop_loss_percentage):
                        position = {'type': 'sell', 'entry_price': low_price, 'stop_loss': open_price * (1 + stop_loss_percentage)}
            
        # Check for stop loss and square off at 3:15 pm
        elif position is not None:
            if position['type'] == 'buy' and low_price < position['stop_loss']:
                pnl += position['entry_price'] - position['stop_loss']
                position = None

            elif position['type'] == 'sell' and high_price > position['stop_loss']:
                pnl += position['entry_price'] - position['stop_loss']
                position = None

            elif timestamp.time() >= pd.to_datetime('15:15:00').time():
                # Square off at 3:15 pm
                if position['type'] == 'buy':
                    pnl += close_price - position['entry_price']
                elif position['type'] == 'sell':
                    pnl += position['entry_price'] - close_price

                position = None

    return pnl

# Read data from CSV file
file_path = 'price_data.csv'  # Replace with the actual path to your CSV file
banknifty_data = pd.read_csv(file_path)
print(banknifty_data)
# Filter data for the year 2020
banknifty_data['Timestamp'] = pd.to_datetime(banknifty_data['Date']+" "+banknifty_data['Timestamp'])
banknifty_data = banknifty_data[(banknifty_data['Timestamp'].dt.year == 2020)]

# Run the strategy for the year 2020
pnl_2020 = open_range_breakout_strategy(banknifty_data)

print("Profit and Loss for 2020:", pnl_2020)

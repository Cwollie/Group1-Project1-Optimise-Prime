
import pandas as pd
import datetime
import yfinance as yf

def get_portfolio_data():
    '''
    Requests user to key in crypto tickers, and appends to a list.
    '''
    ticker_list = []
    ticker = ""
    print("Please enter the tickers of your cryptocurrencies one by one")
    print("Type 'done' when finished.")
    while ticker.casefold() != "done":
        ticker = str.upper(input("Ticker: "))
       
                           
        if ticker.casefold() != "done":
            ticker_list.append(ticker)
        else:
            break
    
    # Adds "-USD" suffix to each crypto ticker for compatibility with yfinance
    ticker_list = pd.DataFrame(columns=ticker_list).add_suffix('-USD').columns.tolist()
    return ticker_list

def get_investment_amt():
    '''
    Requests investment amount from user. 
    '''
    investment_amount = ""
    while type(investment_amount) is not float:
        try:
            investment_amount = float(input("How much do you wish to invest in total?\n"
                                            "(Please input amount without currency symbol)\n"))
        except Exception:
            print('Error: Please input a numerical value\n'
                 'Remember not to include the currency symbol\n')    
    return investment_amount


def get_ticker_data(ticker_list, years_back = 3):
    ''''
    Iterates through each ticker in user portfolio and fetches OHLCV data from Yahoo Finance API into a pandas dataframe. 
    Also records daily returns for each cryptocurrency as separate columns within the same dataframe.
    
    Parameters:
    ticker_list (list): A list of cryptocurrency tickers for which data is to be fetched
    years_back (int): Number of years back from the current date, for which data is to be fetched
    '''
    # Initialise dict to record OHLCV data
    d ={}
    # Define start and end dates
    end = datetime.datetime.now()
    start = datetime.datetime.now() - datetime.timedelta(days= 365 * years_back)
    # create empty dataframe
    cryptos_final = pd.DataFrame()
    
    # Get timeframe 
    interval_list = ['1d', '5d', '1wk', '1mo', '3mo']
    interval = str(input(
        f"\nPlease select the interval: \n"
        f"(Valid intervals: 1d, 5d, 1wk, 1mo, 3mo)\n"
    )
                  )
                  
    while interval not in interval_list:
        print("\nError: You have selected an invalid interval")
        interval = str(input(
            f"Please select the interval: \n"
            f"(Valid intervals: 1d, 5d, 1wk, 1mo, 3mo)\n"
        )
                      )
                              
    for ticker in ticker_list:
        try:
            # download the crypto price 
            crypto = yf.Ticker(ticker)
            crypto_df = crypto.history(
                start = start, 
                end = end, 
                interval = interval
            )
            
            # append the individual crpyto prices 
            if len(crypto_df) == 0:
                None
            else:
                d[(ticker, "open")] = crypto_df['Open']
                d[(ticker, "high")] = crypto_df['High']
                d[(ticker, "low")] = crypto_df["Low"]
                d[(ticker, "close")] = crypto_df["Close"]
                d[(ticker, "volume")] = crypto_df["Volume"]
                d[(ticker, "daily_return")] = crypto_df['Close'].pct_change()
        except Exception:
            None
    d = pd.DataFrame(d)
    d.dropna(inplace = True)
    return d

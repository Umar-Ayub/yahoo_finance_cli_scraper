# yahoo_finance_cli_scraper
Command line yahoo finance scraper that returns various statistics on publicly traded companies

# Usage

Navigate to repository first using cd, then use the following command
```
python financescrapper.py <ticker1> <ticker2>
```
the output is a JSON Object such as the folloiwing:
```
{
    "Previous Close": "154.52", 
    "Return on Equity": "37.07%", 
    "Current Ratio": "1.24", 
    "Total Debt": "122.4B", 
    "ticker": "aapl", 
    "EBITDA": "74.17B", 
    "Gross Profit Margins": "38.43%", 
    "Current Price": "156.41", 
    "url": "http://finance.yahoo.com/quote/aapl?p=aapl", 
    "EPS (TTM)": 9.7, 
    "1y Target Est": 192.63, 
    "Net Profit Margin": "21.13%", 
    "Earnings Date": "2018-04-30 to 2018-05-04", 
    "Open": "157.07", 
    "Bid": "157.23 x 300", 
    "Ask": "157.29 x 500", 
    "Day's Range": "150.24 - 157.89", 
    "52 Week Range": "132.75 - 180.10", 
    "Volume": "70,672,608", 
    "Avg. Volume": "32,293,132", 
    "Market Cap": "793.626B", 
    "Beta": "1.30", 
    "PE Ratio (TTM)": "16.12", 
    "Forward Dividend & Yield": "2.52 (1.61%)", 
    "Ex-Dividend Date": "2017-11-10"
}
```


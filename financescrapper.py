from lxml import html
import requests
from time import sleep
import json
import argparse
from collections import OrderedDict
from time import sleep
from pprint import pprint as pp

def parse(ticker):
    url = "http://finance.yahoo.com/quote/%s?p=%s" %(ticker, ticker)
    response = requests.get(url, verify=False) # GET request to Yahoo Finance API
    other_details_json_link = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/{0}?formatted=true&lang=en-US&region=US&modules=summaryProfile%2CfinancialData%2CrecommendationTrend%2CupgradeDowngradeHistory%2Cearnings%2CdefaultKeyStatistics%2CcalendarEvents&corsDomain=finance.yahoo.com".format(ticker)
    summary_json = requests.get(other_details_json_link) # GET request to Yahoo Finance API to retrieve more details
    print("Parsing %s" %(url))
    sleep(2)

    tree = html.fromstring(response.text)
    summary_table = tree.xpath('//div[contains(@data-test,"summary-table")]//tr')

    data = OrderedDict()
    try:
        # loads() converts a JSON to a dictionary making it suitable for data processing
        # Here we use the keys to retrieve and store data after loading our string
        loaded_json = json.loads(summary_json.text)
        y_Target_Est = loaded_json["quoteSummary"]["result"][0]["financialData"]["targetMeanPrice"]['raw']
        earnings_list = loaded_json["quoteSummary"]["result"][0]["calendarEvents"]['earnings']
        datelist = [i['fmt'] for i in earnings_list['earningsDate']]
        earnings_date = ' to '.join(datelist)
        earnings_per_share = loaded_json["quoteSummary"]["result"][0]["defaultKeyStatistics"]["trailingEps"]['raw']
        roe = loaded_json["quoteSummary"]["result"][0]["financialData"]["returnOnEquity"]['fmt']
        ebitda = loaded_json["quoteSummary"]["result"][0]["financialData"]["ebitda"]['fmt']
        currentRatio = loaded_json["quoteSummary"]["result"][0]["financialData"]["currentRatio"]['fmt']
        totalDebt = loaded_json["quoteSummary"]["result"][0]["financialData"]["totalDebt"]['fmt']
        currentPrice = loaded_json["quoteSummary"]["result"][0]["financialData"]["currentPrice"]['fmt']
        grossMargins = loaded_json["quoteSummary"]["result"][0]["financialData"]["grossMargins"]['fmt']
        netProfitMargin = loaded_json["quoteSummary"]["result"][0]["defaultKeyStatistics"]["profitMargins"]['fmt']


        for table_data in summary_table:
            raw_table_key = table_data.xpath('.//td[contains(@class,"C(black)")]//text()')
            raw_table_value = table_data.xpath('.//td[contains(@class,"Ta(end)")]//text()')
            table_key = ''.join(raw_table_key).strip()
            table_value = ''.join(raw_table_value).strip()
            data.update({table_key:table_value})
            data.update({'Current Price': currentPrice,
                         '1y Target Est':y_Target_Est,
                         'EPS (TTM)':earnings_per_share,
                         'Earnings Date':earnings_date,
                         'Net Profit Margin': netProfitMargin,
                         'Return on Equity': roe,
                         'EBITDA': ebitda,
                         'Gross Profit Margins': grossMargins,
                         'Current Ratio': currentRatio,
                         'Total Debt': totalDebt,
                         'ticker':ticker,
                         'url':url})
        return data
    except:
        print("Failed to Parse JSON")
        return {"error":"Failed to parse json response"}

if __name__=="__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument('ticker',nargs='+', help ='Usage: ticker symbols separated by spaces')
    args = argparser.parse_args()
    ticker = args.ticker
    print("Fetching data for %s" %(ticker))
    for i in ticker:
        scraped_data = parse(i)
        # Writing data to output file
        with open('%s-summary.json'%(i),'w') as f:
             json.dump(scraped_data,f,indent = 4)

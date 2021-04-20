import bs4 as bs
import requests
import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from tkinter import *
from PIL import ImageTk,Image
from mpl_finance import candlestick_ohlc

def main():
    get_data()
    selection()
    candlestick()




# Select a company
def selection():

    root = Tk()
    root.title("Eric's stock picking program!")

    def show():
        myLabel = Label(root, text=company.get()).pack()

    company = StringVar()
    company.set(tickers[0])

    drop = OptionMenu(root, company, *tickers)
    drop.pack()

    myButton = Button(root, text="Show Selection", command=show).pack()

    root.mainloop()


# Get data from wikipedia
def get_data():

    html = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

    soup = bs.BeautifulSoup(html.text)

    tickers = []

    table = soup.find('table', {'class': 'wikitable sortable'})
    rows = table.findAll('tr')[1:]

    for row in rows:
        ticker = row.findAll('td')[0].text
        tickers.append(ticker[:-1])

    
    print(tickers)

#Define time frame

def candlestick():
    start = dt.datetime(2020,1,1)
    end = dt.datetime.now()

    #Load

    data = web.DataReader(ticker, 'yahoo', start, end)

    #print(data.columns)

    # Restructure Data

    data = data[['Open', 'High', 'Low', 'Close']]

    data.reset_index(inplace=True)
    data['Date'] = data['Date'].map(mdates.date2num)

    # Visualization

    ax = plt.subplot()
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.set_title(ticker, ', Share price', color='white')
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis_date()

    candlestick_ohlc(ax, data.values, width=0.5, colorup='g')
    plt.show()

    print(data.head())

main()












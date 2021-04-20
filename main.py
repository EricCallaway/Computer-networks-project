import bs4 as bs
import requests
import datetime as dt
import pandas_datareader as web
import matplotlib.pyplot as plt 
import matplotlib.dates as mdates
from tkinter import *
from PIL import ImageTk,Image
from mpl_finance import candlestick_ohlc

# Main function
def main():
    tickers = get_data()
    user_selection = selection(tickers)
    candlestick(user_selection)
    
# Select a company
def selection(tickers):
    root = Tk()
    root.title("Eric's stock picking program!")

    def show():
        myLabel = Label(root, text=company.get()).pack()

    company = StringVar()
    company.set(tickers[0])
    drop = OptionMenu(root, company, *tickers)
    drop.pack()


    #Wanted to include the functionality to choose the stock you want from the drop down menu, but I could not figure out how to. 
    #myButton = Button(root, text="Show Selection", command=show).pack()
    #submit_button = Button(root, text="Submit", command=submit(e.get())).pack()
    #e = Entry(root, borderwidth=5, width=50)
    #e.pack()
    #e.insert(0, 'Enter the ticker symbol of the company you want to analyze. ')
    user_selection = input('Enter the ticker symbol of the stock you want to analyze: ')
    root.mainloop()
    return user_selection
    
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
    #print(tickers)
    return tickers

#Define time frame
def candlestick(ticker):
    start = dt.datetime(2020,1,1)
    end = dt.datetime.now()
    print('Company to be analyzed: ', ticker)
    print('Analyzing...')

    #Load
    data = web.DataReader(ticker, 'yahoo', start, end)

    # Restructure Data
    data = data[['Open', 'High', 'Low', 'Close']]
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].map(mdates.date2num)

    # Visualization
    ax = plt.subplot()
    ax.grid(True)
    ax.set_axisbelow(True)
    ax.set_title('{} Share price'.format(ticker), color='white')
    ax.set_facecolor('black')
    ax.figure.set_facecolor('#121212')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis_date()
    candlestick_ohlc(ax, data.values, width=0.5, colorup='g')
    plt.show()
    print(data.head())

# Submit button
def submit(user_selection):
    candlestick(user_selection)

# Calling main function
main()












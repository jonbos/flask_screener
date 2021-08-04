"""
This file contains all sentiment analysis-related logic
"""
import pandas as pd
import requests
from bs4 import BeautifulSoup
from nltk.sentiment.vader import SentimentIntensityAnalyzer

FINVIZ_STOCK_URL = "https://finviz.com/quote.ashx?t="
vader = SentimentIntensityAnalyzer()


def scrape_ticker(ticker):
    url = FINVIZ_STOCK_URL + ticker
    response = requests.get(url=url, headers={"user-agent": "my-app"})
    html = BeautifulSoup(response.text, 'html.parser')
    ticker_news = html.find(id='news-table')
    return ticker_news


def scrape_tickers(tickers):
    tables = {}

    for ticker in tickers:
        tables[ticker] = scrape_ticker(ticker)

    return tables


def format_scraped_date(news_tables):
    formatted_data = []
    for ticker, news_table in news_tables:
        rows = news_table.find_all('tr')
        for row in rows:
            title = row.a.text
            date_data = row.td.text.split(" ")
            if len(date_data) == 1:
                time = date_data[0]
            else:
                date = date_data[0]
                time = date_data[1]

            formatted_data.append([ticker, date, time, title])

    return formatted_data


def create_dataframe(parsed_data):
    return pd.DataFrame(parsed_data, columns=["ticker", "date", "time", "headline"])


def apply_sentiment_analysis(df):
    df['compound'] = df["headline"].apply(lambda headline: vader.polarity_scores(headline)['compound'])


def format_df_date(df):
    df['date'] = pd.to_datetime(df.date).dt.date

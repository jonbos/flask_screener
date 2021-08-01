import json

import plotly as plotly
import plotly.express as px
import yfinance as yf
from flask import Blueprint, render_template, request

from screener_app.sentiment_analysis import scrape_tickers, format_scraped_date, create_dataframe, \
    apply_sentiment_analysis, format_df_date

bp = Blueprint('stocks', __name__, url_prefix="/stock")


@bp.route("/", methods=("GET",))
def stock_api():
    ticker = request.args.get('ticker', default='SPY')
    period = request.args.get('period', default='1Y')
    interval = request.args.get('interval', default='1D')
    plot_json = get_price_chart(ticker, period, interval)
    sentiment_json = get_sentiment_chart(ticker)
    return render_template('stocks/info.html', plot_json=plot_json, sentiment_json=sentiment_json, ticker=ticker,
                           period=period, interval=interval)


def get_price_chart(stock, period, interval):
    st = yf.Ticker(stock)

    # Create a line graph
    df = st.history(period=(period), interval=interval)
    df = df.reset_index()
    df.columns = ['Date-Time'] + list(df.columns[1:])
    max = (df['Open'].max())
    min = (df['Open'].min())
    range = max - min
    margin = range * 0.05
    max = max + margin
    min = min - margin
    fig = px.area(df, x='Date-Time', y="Open",
                  hover_data=("Open", "Close", "Volume"),
                  range_y=(min, max), template="seaborn")

    # Create a JSON representation of the graph
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json


def get_sentiment_chart(stock):
    news_tables = scrape_tickers([stock])
    parsed_data = format_scraped_date(news_tables.items())
    df = create_dataframe(parsed_data)
    apply_sentiment_analysis(df)
    format_df_date(df)
    fig = px.bar(df, x="date", y="compound", hover_data=("headline",))
    plot_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return plot_json

import json

import plotly as plotly
import plotly.express as px
import yfinance as yf
from flask import Blueprint, render_template, request

bp = Blueprint('stocks', __name__, url_prefix="")


@bp.route("/api/stock", methods=("GET",))
def stock_api():
    ticker = request.args.get('ticker', default='SPY')
    period = request.args.get('period', default='1Y')
    interval = request.args.get('interval', default='1D')
    return gm(stock=ticker, period=period, interval=interval)


def gm(stock, period, interval):
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
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

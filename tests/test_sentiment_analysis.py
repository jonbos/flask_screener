from screener_app.sentiment_analysis import scrape_ticker


def test_scrape_ticker_returns_stock_table():
    ticker_news = scrape_ticker("AAPL")
    print(ticker_news)
    assert '<a class="tab-link-news"' in ticker_news

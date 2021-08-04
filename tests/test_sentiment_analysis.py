from bs4 import Tag

from screener_app.sentiment_analysis import scrape_ticker, scrape_tickers, format_scraped_date, create_dataframe, \
    apply_sentiment_analysis, format_df_date


def test_scrape_ticker_returns_stock_table():
    ticker_news = scrape_ticker("AAPL")
    assert type(ticker_news) == Tag and len(ticker_news) > 0


def test_scrape_ticker_returns_ticker_dict():
    ticker_dict = scrape_tickers(['AAPL'])
    assert 'AAPL' in ticker_dict.keys()
    assert type(ticker_dict['AAPL']) == Tag


def test_data_formatter_should_format_date_col():
    ticker_dict = scrape_tickers(['AAPL'])
    formatted = format_scraped_date(ticker_dict.items())
    # ticker, date, time, headline
    assert len(formatted[0]) == 4


def test_should_apply_sentiment_analysis_with_normalized_compound():
    news_tables = scrape_tickers(["AAPL"])
    parsed_data = format_scraped_date(news_tables.items())
    df = create_dataframe(parsed_data)
    apply_sentiment_analysis(df)
    assert 'compound' in [row for row in df]
    assert all([-1 < compound < 1 for compound in df['compound']])
    format_df_date(df)

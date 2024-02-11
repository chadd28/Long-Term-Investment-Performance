import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import datetime
import plotly.express as px

import warnings
warnings.filterwarnings("ignore", message="The 'unit' keyword in TimedeltaIndex construction is deprecated and will be removed in a future version. Use pd.to_timedelta instead.", category=FutureWarning, module="yfinance.utils")

st.set_page_config(
    page_title="Long Term Stock Performance"
)

st.title('Long Term Stock Investment Performance 📈')
ticker = st.sidebar.text_input('Ticker', '^GSPC')
start_year = st.sidebar.number_input('Start Year', value=2000)
end_year = st.sidebar.number_input('End Year', value=2024)
interval = st.sidebar.number_input('Interval of Years', min_value=0, max_value=25, value=7)

st.divider()
st.header("Intended Use of This Dashboard")
st.markdown("""
            - Checks stock performance over long periods of time & compare individual stocks with index.
            - The information empowers users to make decisions on long term investments.
            - **Percent Change Graph**: displays how much the stock price changed compared to [x] years ago (set by the user).
            
            For example, if Interval of Years = 7, the stock price in 2020 displayed on the chart will be compared to the stock price in 2013.

            **If you encounter an error, you can**:
            - Retype in the ticker/year to reload the data
            - Adjust "Start Year": it must be greater than the *year the stock started* + *interval of years* 
            """)
st.divider()

df = pd.DataFrame(columns=['Year', 'Adj Close'])

# creates df that has Year and Adj Close
for year in range(start_year - interval, end_year + 1):        # start_year - interval because we have to get the values x years before to calculate the interval
    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 1, 5)
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)
    first_day_closing_price = data.iloc[0]['Adj Close']

    df.loc[len(df)] = [year, first_day_closing_price]

df['Percent Change From ' + str(interval) + ' Years Ago'] = df['Adj Close'].pct_change(periods=interval) * 100    # adds percent change column to df
df = df.drop(index=df.index[:interval]).reset_index(drop=True)         # removes the unecessary years for visualization
highPrice = round(df.iloc[:, 1].max(), 2)    # calls 2nd column
lowPrice = round(df.iloc[:, 1].min(), 2)  
avgPrice = round(df.iloc[:, 1].mean(), 2)   
highChange = round(df.iloc[:, 2].max(), 2)    # calls 3rd column
lowChange = round(df.iloc[:, 2].min(), 2) 
avgChange = round(df.iloc[:, 2].mean(), 2) 
varChange = round(df.iloc[:, 2].std(), 2) 
df['Year'] = df['Year'].astype(int)
df['Year'] = df['Year'].astype(str).str.replace(',', '')

# # graph of percent change from x years ago of closing price on first day of that year
fig1 = px.bar(df, x='Year', y =df.columns[2], title="Percent Change of Last " + str(interval) + " Years of Closing Price of " + ticker + " on First Day of Each Year")
fig1.update_traces(marker=dict(color=['red' if val < 0 else 'green' for val in df.iloc[:, 2]]))
st.plotly_chart(fig1)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label='Highest Change', value='{:.2f}%'.format(highChange))
with col2:
    st.metric(label='Lowest Change', value='{:.2f}%'.format(lowChange))
with col3:
    st.metric(label='Average Change', value='{:.2f}%'.format(avgChange))
with col4:
    st.metric(label='Variance of Change (std)', value='{:.2f}%'.format(varChange))

st.divider()

# graph/table of closing price on first day of each year
fig2 = px.line(df, x = 'Year', y = 'Adj Close', title = "Closing Price of " + ticker + " on First Day of Each Year")
st.plotly_chart(fig2)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='Highest Value', value='${:,.2f}'.format(highPrice))
with col2:
    st.metric(label='Lowest Value', value='${:,.2f}'.format(lowPrice))
with col3:
    st.metric(label='Average Value', value='${:,.2f}'.format(avgPrice))

df.iloc[:, 2] = df.iloc[:, 2].map(lambda x: '{:.2f}%'.format(x))
df['Adj Close'] = df['Adj Close'].map(lambda x: '${:,.2f}'.format(x))
st.dataframe(df, width=500)
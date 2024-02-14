import streamlit as st, pandas as pd, numpy as np, yfinance as yf
import datetime
import plotly.express as px

import warnings
warnings.filterwarnings("ignore", message="The 'unit' keyword in TimedeltaIndex construction is deprecated and will be removed in a future version. Use pd.to_timedelta instead.", category=FutureWarning, module="yfinance.utils")

st.title('Compare Long Term Stock Investment Performance')
ticker1 = st.sidebar.text_input('Ticker 1', '^GSPC')
ticker2 = st.sidebar.text_input('Ticker 2', 'WMT')
start_year = st.sidebar.number_input('Start Year', value=2000)
end_year = st.sidebar.number_input('End Year', value=2024)
interval = st.sidebar.number_input('Interval of Years', min_value=0, max_value=25, value=7)

st.divider()
st.header("Intended Use")
st.markdown("- Compare individual stocks")
st.divider()

df = pd.DataFrame(columns=['Year', 'Adj Close (' + ticker1 + ')', 'Adj Close (' + ticker2 + ')'])

# creates df that has Year and Adj Close
for year in range(start_year - interval, end_year + 1):        # start_year - interval because we have to get the values x years before to calculate the interval
    start_date = datetime.datetime(year, 1, 1)
    end_date = datetime.datetime(year, 1, 5)
    data1 = yf.download(ticker1, start=start_date, end=end_date, progress=False)
    data2 = yf.download(ticker2, start=start_date, end=end_date, progress=False)
    first_day_closing_price1 = data1.iloc[0]['Adj Close']
    first_day_closing_price2 = data2.iloc[0]['Adj Close']

    df.loc[len(df)] = [year, first_day_closing_price1, first_day_closing_price2]

df['% Change from ' + str(interval) + ' Years Earlier (' + ticker1 + ')'] = df.iloc[:, 1].pct_change(periods=interval) * 100    # adds percent change column to df
df['% Change from ' + str(interval) + ' Years Earlier (' + ticker2 + ')'] = df.iloc[:, 2].pct_change(periods=interval) * 100    
df = df.drop(index=df.index[:interval]).reset_index(drop=True)         # removes the unecessary years for visualization
highPrice1 = round(df.iloc[:, 1].max(), 2)    # calls 2nd column
lowPrice1 = round(df.iloc[:, 1].min(), 2)  
avgPrice1 = round(df.iloc[:, 1].mean(), 2)  
highChange1 = round(df.iloc[:, 3].max(), 2)    # calls 4th column
lowChange1 = round(df.iloc[:, 3].min(), 2) 
avgChange1 = round(df.iloc[:, 3].mean(), 2)
varChange1 = round(df.iloc[:, 3].std(), 2) 

highPrice2 = round(df.iloc[:, 2].max(), 2)   
lowPrice2 = round(df.iloc[:, 2].min(), 2)  
avgPrice2 = round(df.iloc[:, 2].mean(), 2)  
highChange2 = round(df.iloc[:, 4].max(), 2)    
lowChange2 = round(df.iloc[:, 4].min(), 2) 
avgChange2 = round(df.iloc[:, 4].mean(), 2)
varChange2 = round(df.iloc[:, 4].std(), 2) 

df['Year'] = df['Year'].astype(int)
df['Year'] = df['Year'].astype(str).str.replace(',', '')

# # graph of percent change from x years ago of closing price on first day of that year
fig1 = px.bar(df, x='Year', y =[df.columns[3], df.columns[4]], 
              barmode = 'group', 
              title=str(ticker1) + " v.s. " + str(ticker2),
              color_discrete_map={
                  '% Change from ' + str(interval) + ' Years Ago (' + ticker1 + ')': 'lightskyblue', 
                  '% Change from ' + str(interval) + ' Years Ago (' + ticker2 + ')': 'lightsalmon'})
fig1.update_layout(yaxis_title='% Change From ' + str(interval) + ' Years Ago')
fig1.update_layout(legend=dict(x=0.3, y=1.2),  # Set 'y' coordinate close to 1
                  legend_orientation='h',   # Horizontal orientation
                  )
st.plotly_chart(fig1)


col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label='Highest Change (' + str(ticker1) + ')', value='{:.2f}%'.format(highChange1))
    st.metric(label='Highest Change (' + str(ticker2) + ')', value='{:.2f}%'.format(highChange2))
with col2:
    st.metric(label='Lowest Change (' + str(ticker1) + ')', value='{:.2f}%'.format(lowChange1))
    st.metric(label='Lowest Change (' + str(ticker2) + ')', value='{:.2f}%'.format(lowChange2))
with col3:
    st.metric(label='Average Change (' + str(ticker1) + ')', value='{:.2f}%'.format(avgChange1))
    st.metric(label='Average Change (' + str(ticker2) + ')', value='{:.2f}%'.format(avgChange2))
with col4:
    st.metric(label='Variance (' + str(ticker1) + ')', value='{:.2f}%'.format(varChange1))
    st.metric(label='Variance (' + str(ticker2) + ')', value='{:.2f}%'.format(varChange2))

st.divider()

# graph/table of closing price on first day of each year
fig2 = px.line(df, x = 'Year', y = [df.columns[1], df.columns[2]], 
               title = "Closing Price of " + str(ticker1) + " and " + str(ticker2) + ' on First Day of Each Year',
               color_discrete_map={
                  'Adj Close (' + str(ticker1) + ')': 'lightskyblue', 
                  'Adj Close (' + str(ticker2) + ')': 'lightsalmon'})
st.plotly_chart(fig2)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric(label='Highest Value (' + str(ticker1) + ')', value='${:,.2f}'.format(highPrice1))
    st.metric(label='Highest Value (' + str(ticker2) + ')', value='${:,.2f}'.format(highPrice2))
with col2:
    st.metric(label='Lowest Value (' + str(ticker1) + ')', value='${:,.2f}'.format(lowPrice1))
    st.metric(label='Lowest Value (' + str(ticker2) + ')', value='${:,.2f}'.format(lowPrice2))
with col3:
    st.metric(label='Average Value (' + str(ticker1) + ')', value='${:,.2f}'.format(avgPrice1))
    st.metric(label='Average Value (' + str(ticker2) + ')', value='${:,.2f}'.format(avgPrice2))

df.iloc[:, 1] = df.iloc[:, 1].map(lambda x: '${:,.2f}'.format(x))
df.iloc[:, 2] = df.iloc[:, 2].map(lambda x: '${:,.2f}'.format(x))
df.iloc[:, 3] = df.iloc[:, 3].map(lambda x: '{:.2f}%'.format(x))
df.iloc[:, 4] = df.iloc[:, 4].map(lambda x: '{:.2f}%'.format(x))
st.dataframe(df)
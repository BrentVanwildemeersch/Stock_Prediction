from pandas_datareader import data
import datetime

start = datetime.datetime(2013,1,1)
end = datetime.datetime(2016,1,4)
df = data.DataReader("GOOGL","yahoo", start,end)

dates=[]
for x in range(len(df)):
    newdate= str(df.index[x])
    newdate = newdate[0:10]
    dates.append(newdate)

df['dates'] = dates

print df
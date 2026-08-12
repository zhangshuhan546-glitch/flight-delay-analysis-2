import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv("C:/Users/Peter/Desktop/Aviation-Data-Analysis/data/FixedDelayedFlights.csv")
pd.set_option('display.max_columns',20)
pd.set_option('display.max_rows',20)  #限制省略

#2.了解数据
print(df.shape) #行数和列数
print(df.columns.tolist()) #行的各个信息
print(df.head()) #前五行
print(df.tail()) #后五行
print(df.info())
print(df.describe()) #数据大概信息

print(df.isnull().sum())
print(df['Origin'].nunique())
print(df['Dest'].nunique())

print(df['UniqueCarrier'].value_counts())
print(df['Cancelled'].value_counts())
print(df['Diverted'].value_counts())
print(df['Year'].value_counts())
print(df['Month'].value_counts().sort_index())

print(df[['ArrDelay','DepDelay','CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay']].describe())
df['TotalCauseDelay']=(df['ArrDelay']+df['CarrierDelay']+df['WeatherDelay']+df['NASDelay']+df['SecurityDelay']+df['LateAircraftDelay'])
print(df[['TotalCauseDelay','ArrDelay','DepDelay']].describe())

#构造特征
df['is_delay15'] = (df['ArrDelay'] > 15).astype(int)
df['DepHour']=df['CRSDepTime']//100
def time_period(x):
    if x<12:
        return '上午'
    elif x<18:
        return '下午'
    else:
        return '晚上'
df['time_period']=df['DepHour'].apply(time_period)
# print(df['time_period'].value_counts().sort_index())

#分析对比
# # 1.  整体情况：全部航班的平均延误时长、延误率是多少？(祝：大于15分钟算延误)
print('全部航班的平均延误时长',df['ArrDelay'].mean())
print('全部航班的延误率',df['is_delay15'].mean())
# 2.  对比航空公司：哪家航空公司延误率最高？哪家最低？
carrier_delay = df.groupby('UniqueCarrier').agg(
    delay_15_rate=('is_delay15','mean'))
# 对比 YV 和 AQ 的航司自身延误占比
yv_carrier = (df[df['UniqueCarrier'] == 'YV']['CarrierDelay'] > 0).mean()
aq_carrier = (df[df['UniqueCarrier'] == 'AQ']['CarrierDelay'] > 0).mean()
print('YV 航司原因占比:', yv_carrier)
print('AQ 航司原因占比:', aq_carrier)
print('延误率最高的航司是：')
print(carrier_delay.loc[carrier_delay['delay_15_rate'].idxmax()])
print('延误率最低的航司是：')
print(carrier_delay.loc[carrier_delay['delay_15_rate'].idxmin()])
# # 3.  对比机场：哪些到达机场容易延误？
airport = df.groupby('Dest')['DepDelay'].mean()
print('五个容易延误的到达机场是')
print(airport.sort_values( ascending=False))
# 高于平均延误的机场占比
airport_avg = df.groupby('Dest')['DepDelay'].mean()
print((airport_avg > airport_avg.mean()).mean())
# 4.  对比时段：早上、中午、晚上哪个时段延误更严重？
mne_delay = df.groupby('time_period')['ArrDelay'].mean().reset_index()
print('早中晚的延误分别是：')
print(mne_delay)
# # 5.对比原因：CarrierDelay、LateAircraftDelay 哪个贡献最大？
AllDelayReason=df[['WeatherDelay','CarrierDelay','NASDelay','SecurityDelay','LateAircraftDelay']]
print('五个延误原因占比')
print((AllDelayReason>0).mean().sort_values(ascending=False))
print('五个延误原因的平均值')
print(AllDelayReason.mean().sort_values(ascending=False))
# #每个原因的延误占比
cause_sum = AllDelayReason.sum()
print('五个延误原因的总占比是：')
five_cause_delay=cause_sum/cause_sum.sum()
print(cause_sum/cause_sum.sum())
# #各航空公司延误率对比
plt.figure(figsize=(12,6))

x1 = carrier_delay.index
x2 = carrier_delay['delay_15_rate'].values
plt.bar(x1,x2,label='2008')
plt.title('各航司延误率',fontsize=45,color='steelblue')

plt.xlabel('航司',fontsize=30)
plt.ylabel('延误率',fontsize=30)
plt.xticks(fontsize=20)
plt.yticks(fontsize=20)

plt.legend(fontsize=20)
plt.ylim(0,1)
plt.tight_layout()

plt.savefig('C:/Users/Peter/Desktop/Aviation-Data-Analysis/images/airport_delay.png', dpi=150)
plt.show()
#
# #时段延误对比
plt.figure(figsize=(12,12))

x1 = mne_delay['time_period'].values
x2 = mne_delay['ArrDelay'].values
plt.bar(x1,x2)

plt.title('各时段延误对比',fontsize=45,color='steelblue')
plt.xlabel('时段',fontsize=30)
plt.xticks(fontsize=20)
plt.ylabel('延误率',fontsize=30)
plt.yticks(fontsize=20)

plt.tight_layout()
plt.savefig('C:/Users/Peter/Desktop/Aviation-Data-Analysis/images/time_delay.png', dpi=150)
plt.show()

#五个延误原因的贡献对比
explode = [0,0.1,0,0,0]
plt.figure(figsize=(12,8))
x1 = five_cause_delay.index
x2 = five_cause_delay.values
plt.pie(
    x2,
    labels=x1,
    autopct='%1.1f%%',
    textprops={'fontsize':20},
    shadow=True,
    wedgeprops={'width':0.6},
    pctdistance=0.8,
    explode=explode
        )
plt.title("五个延误原因的贡献对比",fontsize=35)
plt.tight_layout()
plt.savefig('C:/Users/Peter/Desktop/Aviation-Data-Analysis/images/delay_cause.png', dpi=150)
plt.show()





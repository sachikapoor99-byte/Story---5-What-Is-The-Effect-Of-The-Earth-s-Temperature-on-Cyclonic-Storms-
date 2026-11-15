"""Run: python story5_analysis.py PATH_TO_RAW_CSV_FOLDER PATH_TO_OUTPUT_FOLDER."""
import sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

raw, out = map(Path, sys.argv[1:3])
out.mkdir(parents=True, exist_ok=True)
years = pd.Index(range(1995, 2025), name='year')
temp = pd.read_csv(raw/'GLB.Ts+dSST.csv', skiprows=1).set_index('Year')['J-D'].reindex(years)
annual = pd.DataFrame({'temperature_anomaly_c':pd.to_numeric(temp)})
assert annual.temperature_anomaly_c.notna().all()
c = pd.read_csv(raw/'ibtracs.since1980.list.v04r01.csv', skiprows=[1], keep_default_na=False, dtype={'SEASON':str},
                usecols=['SID','SEASON','BASIN','TRACK_TYPE','USA_STATUS','USA_WIND','NATURE'])
c['SEASON'] = pd.to_numeric(c.SEASON,errors='coerce')
c = c[c.SEASON.between(1995,2024) & c.BASIN.isin(['NA','WP']) & c.TRACK_TYPE.eq('main')]
c = c[c.USA_STATUS.isin(['TD','TS','HU','HR','TY','ST','TC']) | (c.USA_STATUS.str.strip().eq('') & c.NATURE.eq('TS'))]
c['wind'] = pd.to_numeric(c.USA_WIND,errors='coerce')
named = c.USA_STATUS.isin(['HU','HR','TY','ST'])
missing = c.loc[named].groupby(['BASIN','SEASON','SID']).wind.max().isna().sum()
assert missing == 0, f'{missing} explicitly classified storms lack qualifying wind records'
peak = c.groupby(['BASIN','SEASON','SID']).wind.max()
for b, tag in [('NA','hurricane'),('WP','typhoon')]:
    p = peak.loc[b].dropna()
    qualified = p[p.ge(64)]
    grouped = qualified.groupby(level='SEASON')
    annual[tag+'_count'] = grouped.size().reindex(years)
    annual[tag+'_strong_share'] = grouped.apply(lambda s:s.ge(96).mean()).reindex(years)
t = pd.read_csv(raw/'1950-2024_actual_tornadoes.csv')
t = t[t.yr.between(1995,2024)]
key = ['yr','om','date','time','st','slat','slon']
t = t.groupby(key,dropna=False,as_index=False).mag.max()
annual['tornado_count'] = t.groupby('yr').size().reindex(years)
rated = t[t.mag.between(0,5)].groupby('yr').mag
annual['tornado_rated_count'] = rated.size().reindex(years)
annual['tornado_strong_share'] = rated.apply(lambda s:s.ge(2).mean()).reindex(years)
assert annual.shape==(30,8) and annual.notna().all().all(), annual.isna().sum().to_dict()
annual.to_csv(out/'story5_annual_metrics.csv',float_format='%.8f')
def detrend(s):
    return np.asarray(s) - np.polyval(np.polyfit(years,s,1),years)
rows = []
for kind in ('hurricane','typhoon','tornado'):
    for metric in ('count','strong_share'):
        s=annual[kind+'_'+metric]; x=annual.temperature_anomaly_c
        rows.append((kind,metric,len(s),x.corr(s),np.corrcoef(detrend(x),detrend(s))[0,1]))
results = pd.DataFrame(rows,columns=['storm','measure','years','pearson_r','detrended_r'])
results.to_csv(out/'story5_correlations.csv',index=False,float_format='%.5f')
print(results.to_string(index=False)); print('Unrated U.S. tornadoes:',len(t)-rated.size().sum())
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
for metric, title in [('count','Did warmer years have more storms?'),('strong_share','Did warmer years have a larger share of strong storms?')]:
    fig, axes = plt.subplots(1,3,figsize=(13,5.4),sharex=True)
    fig.patch.set_facecolor('#f5f8fa')
    fig.subplots_adjust(left=.09,right=.96,bottom=.23,top=.73,wspace=.33)
    fig.text(.07,.92,title,weight='bold',fontsize=22,color='#183047')
    fig.text(.07,.85,'Each dot is one year from 1995 to 2024. The line shows the overall pattern.',fontsize=12,color='#42586b')
    for ax,(tag,label,col) in zip(axes,[('hurricane','North Atlantic hurricanes','#126c80'),('typhoon','West North Pacific typhoons','#5c3c8a'),('tornado','U.S. tornadoes','#9b4d13')]):
        x=annual.temperature_anomaly_c; y=annual[tag+'_'+metric]
        ax.scatter(x,y,c=col,s=29,alpha=.8)
        xx=np.array([x.min(),x.max()]); ax.plot(xx,np.polyval(np.polyfit(x,y,1),xx),color=col,lw=1.7)
        r=results.loc[results.storm.eq(tag)&results.measure.eq(metric),'pearson_r'].iloc[0]
        ax.set_title(f'{label}\nCorrelation: {r:+.2f}',fontsize=11,loc='left',pad=8)
        ax.set_xticks([.4,.6,.8,1,1.2]); ax.grid(axis='y',alpha=.23); ax.set_axisbelow(True)
        if metric=='strong_share': ax.set_ylim(0,.85); ax.yaxis.set_major_formatter(PercentFormatter(1))
    axes[0].set_ylabel('Number of storms' if metric=='count' else 'Share rated strong')
    fig.text(.53,.135,'Global temperature above the 1951–1980 average (°C)',ha='center',fontsize=11)
    note='Strong: 96-knot peak winds or higher for hurricanes and typhoons; F/EF2 or higher among rated tornadoes.'
    if metric=='strong_share': fig.text(.07,.075,note,fontsize=9)
    fig.text(.07,.035,'Sources: NASA GISTEMP v4; NOAA IBTrACS v04r01; NOAA Storm Prediction Center.',fontsize=9,color='#42586b')
    fig.savefig(out/f'story5_{metric}.png',dpi=170)
    plt.close(fig)

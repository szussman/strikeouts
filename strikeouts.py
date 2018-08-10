import numpy as np
import pandas as pd
from bokeh.plotting import figure, output_file, show
import bokeh.models.tickers as tickers
from bokeh.models import NumeralTickFormatter

output_file("so.html")

filename = "/Users/stuartzussman/Desktop/baseballdatabank-master/core/Teams.csv"
starting_df = pd.read_csv(filename)

# look at only years after 1910
df = starting_df[(starting_df.yearID>1910)]

# for years before HBP were recorded and the field is thus empty
df['HBP']=df['HBP'].fillna(0) 

# approximation of PA, ignoring catcher interference
df['PA'] = df['AB'] + df['BB'] + df['HBP']

# create series that include year and the respective statistic
so = df.groupby('yearID')['SO'].sum()
bb = df.groupby('yearID')['BB'].sum()
pa = df.groupby('yearID')['PA'].sum()

bbs, sm, yrs = bb.values, so.values, so.index

so_pct = []
bb_pct=[]

for yr in yrs:
    so_sum = df[df["yearID"]==yr]["SO"].sum()
    pa_sum = df[df["yearID"]==yr]["PA"].sum()
    bb_sum = df[df["yearID"]==yr]["BB"].sum()
    so_pct.append(so_sum/pa_sum)
    bb_pct.append(bb_sum/pa_sum)
    
# plot the data
p = figure(plot_width=1200, plot_height=600,title="Outcomes per Plate Appearance by Year", x_axis_label='Year', y_axis_label='% of PA')
p.title.align = 'center'
p.line(x=yrs,y=so_pct,line_width=2, line_color='red')
p.line(x=yrs,y=bb_pct,line_width=2, line_color='green')

p.yaxis[0].formatter = NumeralTickFormatter(format="0%")
p.circle(x=yrs,y=so_pct, legend="K/PA", line_width=2, fill_color='red',line_color="red", size=6)
p.circle(x=yrs,y=bb_pct, legend="BB/PA", line_width=2, fill_color='green',line_color="green", size=6)
p.xgrid.ticker = tickers.FixedTicker(ticks=np.arange(1910, 2030, 10))
p.xaxis.ticker = tickers.FixedTicker(ticks=np.arange(1910, 2030, 10))

p.xaxis.major_label_text_font_size = "16pt"
p.legend.location = "bottom_center"
show(p)

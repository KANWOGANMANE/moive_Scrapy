import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
df =pd.read_csv("时长.csv")
df["时长"]
hist,bin_edges = np.histogram(df["时长"], bins=35)
bar = (
    Bar()
    .add_xaxis([str(x) for x in bin_edges[:-1]])
    .add_yaxis("时长分布",[float(x) for x in hist],category_gap=0)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="时长分布图",pos_left="center"),
        legend_opts=opts.LegendOpts(is_show=False)
    )
)
bar.render("时长.html")
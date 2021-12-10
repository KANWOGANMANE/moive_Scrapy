import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar
df =pd.read_csv("评分.csv")
df["rate"]
hist,bin_edges = np.histogram(df["rate"], bins=16)
bar = (
    Bar()
    .add_xaxis([str(x) for x in bin_edges[:-1]])
    .add_yaxis("评分分布",[float(x) for x in hist],category_gap=0)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="评分分布图",pos_left="center"),
        legend_opts=opts.LegendOpts(is_show=False)
    )
)
bar.render("评分.html")
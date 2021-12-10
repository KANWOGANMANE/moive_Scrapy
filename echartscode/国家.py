from pyecharts import options as opts
from pyecharts.charts import Pie
def create_pie(datas,title)->Pie:
    pie =Pie()
    Pie().add("国家分布图",datas)
    pie = (
        Pie()
            .add("国家和地区", datas)
            .set_global_opts(title_opts=opts.TitleOpts(title="国家分布图"))
            .set_global_opts(legend_opts=opts.LegendOpts(pos_right="right"))
            .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{d}%"))
    )
    return pie
import pandas as pd
df =pd.read_csv("bb.csv")
df_kkss=df.groupby("country").size().sort_values(ascending=False)
datas =list(zip(df_kkss.index.to_list(),df_kkss.to_list()))
pie = create_pie(datas,"国家和地区")
pie.render("国家分布图.html")

import jieba
import jieba.analyse
import pandas as pd
import pyecharts.options as opts
from pyecharts.charts import WordCloud
fin = open('类型.txt',encoding='utf-8')
txt = fin.read()
word_weight = jieba.analyse.extract_tags(txt, topK=50 ,withWeight=True)
word_cloud = (
    WordCloud()
    .add(series_name='类型',data_pair=word_weight, word_size_range=[20,100])
    .set_global_opts(
    title_opts=opts.TitleOpts(
        title="   ",
        title_textstyle_opts=opts.TextStyleOpts(font_size=30),
        pos_left='center')
    )
)
word_cloud.render("类型词云图.html")
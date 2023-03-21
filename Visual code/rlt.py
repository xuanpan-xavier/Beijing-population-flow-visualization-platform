import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import HeatMap
from pyecharts.globals import ThemeType

b=pd.read_csv('./热力图数据.csv',header=None
                    ,names=['index','day','hour'])

value=[[i-15, j, b.iloc[i*24+24-j-1,0]] for i in range(15,30) for j in range(24)]
value2=[[i+15, j, b.iloc[i*24+24-j-1,0]] for i in range(15) for j in range(24)]
value.extend(value2)
c = (
    HeatMap(init_opts=opts.InitOpts(width="720px",height="480px",theme=ThemeType.CHALK))
    .add_xaxis([[i] for i in range(30)])
    .add_yaxis(
        "人流量指数",
        [[j] for j in range(23,-1,-1)],
        value,
        #label_opts=opts.LabelOpts(is_show=True, position="inside"),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(title="北京每小时平均人口密度"),
        visualmap_opts=opts.VisualMapOpts(),
    )
    .render("heatmap_with_label_show.html")
)

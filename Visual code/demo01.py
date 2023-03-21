import pyecharts.options as opts
import pyodbc
from pyecharts.charts import Line, Timeline, Grid
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType

conn=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE='';UID=sa;PWD=123;charset=cp936')
cur = conn.cursor()


background_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}],false)"
)


area_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#93edc7'}, {offset: 1, color: '#1cd8d2'}],false)"
)


def getu()->Timeline:
    days=[]
    for i in range(20200117, 20200132):
        days.append(str(i)[4:])
    for i in range(20200201, 20200216):
        days.append(str(i)[4:])
    dayss=[]
    for i in range(20200216, 20200225):
        dayss.append(str(i)[4:])
    hours=["0"+str(i) for i in range(0,10)]+[str(i) for i in range(10,24)]
    tl =Timeline(init_opts=opts.InitOpts(width="1600px", height="400px",theme=ThemeType.CHALK,))
    tl.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="5",
        pos_top = "20",
        pos_bottom = "20",
        width="60",
    )


    for hour in hours:
        sql1="select right(date,4),sum(num) as sum from api where time='"+hour+"' group by date order by date"
        cur.execute(sql1)
        r1=cur.fetchall()
        x_data1 = days
        y_data1 = [round(b/10000,2)  for a,b in r1]
        sql2="select right(date,4),sum(num) as sum from tmp where time='"+hour+"' group by date order by date"
        cur.execute(sql2)
        r2=cur.fetchall()
        x_data2 = dayss
        y_data2 = [round(b/10000,2) for a,b in r2]
        x_data=x_data1+x_data2
        y_data=y_data1+y_data2
        for i in range(39):
            print(x_data[i],y_data[i])
        print("\n\n")


        c = (
            Line(init_opts=opts.InitOpts(width="1590px",height="400px",))
            .add_xaxis(xaxis_data=x_data)
            .add_yaxis(
                series_name="人流量指数",
                y_axis=y_data,
                is_smooth=True,
                is_symbol_show=True,
                symbol="circle",
                symbol_size=6,
                linestyle_opts=opts.LineStyleOpts(color="#fff"),
                label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),

                tooltip_opts=opts.TooltipOpts(is_show=False),
                areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
            )
            .set_global_opts(
                datazoom_opts=opts.DataZoomOpts(type_="inside"),
                legend_opts=opts.LegendOpts(is_show=False),
                title_opts=opts.TitleOpts(
                    title="各时段总人流量对比",
                    pos_top="5%",
                    pos_left="center",
                    title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
                ),
                xaxis_opts=opts.AxisOpts(
                    type_="category",
                    boundary_gap=False,
                    axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
                    axisline_opts=opts.AxisLineOpts(is_show=False),
                    axistick_opts=opts.AxisTickOpts(
                        is_show=True,
                        length=25,
                        linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                    ),
                ),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    position="right",
                    axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
                    axisline_opts=opts.AxisLineOpts(
                        linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
                    ),
                    axistick_opts=opts.AxisTickOpts(
                        is_show=True,
                        length=15,
                        linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
                    ),
                    splitline_opts=opts.SplitLineOpts(
                        is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
                    ),
                ),
            )
        )

        tl.add(c,hour)
    return tl
getu().render("zxt.html")


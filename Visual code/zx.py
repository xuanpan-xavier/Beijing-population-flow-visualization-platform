import pyecharts.options as opts
from pyecharts.charts import ThemeRiver, Tab, Line,Bar
import pyodbc
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType


background_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#c86589'}, {offset: 1, color: '#06a7ff'}], false)"
)
area_color_js = (
    "new echarts.graphic.LinearGradient(0, 0, 0, 1, "
    "[{offset: 0, color: '#eb64fb'}, {offset: 1, color: '#3fbbff0d'}], false)"
)


conn=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE='';UID=sa;PWD=123;charset=cp936')
cur = conn.cursor()
cur1=conn.cursor()
sql="select date,sum(mi) as sumi,a from (SELECT a,date,mi from qyhf,m_ip where p=p2) A group by a,date"
sql1="select date,sum(pmi) as sumi,a from (SELECT a,date,pmi from qyhf,pm_i where p=p1) A group by a,date"
cur.execute(sql)
result=cur.fetchall()
cur1.execute(sql1)
result1=cur1.fetchall()
x_data = ["东部", "中部", "西部", "东北"]
y_data = [(a,b,c) for a,b,c in result]
y1_data=[(a,b,c) for a,b,c in result1]


def cr()->Bar:
    sql3 = "select distinct date from pm_i order  by date"
    cur.execute(sql3)
    r3 = cur.fetchall()
    sql = "select round(sum(mi),2) as sumi from (SELECT a,date,mi from qyhf,m_ip where p=p2) A group by date"
    sql1 = "select round(sum(pmi),2) as sumi from (SELECT a,date,pmi from qyhf,pm_i where p=p1) A group by date"
    cur.execute(sql)
    r0 = cur.fetchall()
    cur.execute(sql1)
    r1 = cur.fetchall()
    bar=Bar(
        init_opts=opts.InitOpts(width="1600px", height="400px",theme=ThemeType.CHALK,
            animation_opts=opts.AnimationOpts(
                animation_delay=1000, animation_easing="elasticOut"
            )
        ),
    )
    print([a[0] for a in r0])
    print([a[0] for a in r1])
    print([a[0] for a in r3])
    bar.add_xaxis([a[0] for a in r3])
    bar.add_yaxis("迁入", [a[0] for a in r0])
    bar.add_yaxis("迁出", [a[0] for a in r1])
    bar.set_global_opts(title_opts=opts.TitleOpts(title="迁入迁出对比", subtitle="条形图"))

    return bar

def churiver()->ThemeRiver:
    chu=(
        ThemeRiver(init_opts=opts.InitOpts(width="1600px", height="400px",theme=ThemeType.CHALK))
        .add(
            series_name=x_data,
            data=y_data,
            singleaxis_opts=opts.SingleAxisOpts(
                pos_top="50", pos_bottom="50", type_="time"
            ),
        )
        .set_global_opts(
            tooltip_opts=opts.TooltipOpts(is_show=True,trigger="axis", axis_pointer_type="line")
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="离京人员数据统计河流图"))
    )
    return chu
def ruriver()->ThemeRiver:
    ru=(
        ThemeRiver(init_opts=opts.InitOpts(width="1600px", height="400px",theme=ThemeType.CHALK))
            .add(
                series_name=x_data,
                data=y1_data,
                singleaxis_opts=opts.SingleAxisOpts(
                    pos_top="50", pos_bottom="50", type_="time"
                ),
            )
            .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=True,trigger="axis", axis_pointer_type="line")
            )
            .set_global_opts(title_opts=opts.TitleOpts(title="入京人员数据统计河流图"))
        )
    return ru;
color=["palegreen","gold","red","lightpink"]
def ruzx()->Line:
    i = 0
    ru=Line(init_opts=opts.InitOpts(width="1600px", height="400px",bg_color=JsCode(background_color_js),theme=ThemeType.CHALK))
    for item in x_data:
        sql2="select sum(pmi) as sumi from (SELECT a, date, pmi from qyhf, pm_i where p=p1) A where a='"+item+"' group by a,date order by date"
        cur.execute(sql2)
        r2=cur.fetchall()
        sql3="select distinct date from pm_i order  by date"
        cur.execute(sql3)
        r3=cur.fetchall()

        ru.add_xaxis(xaxis_data=[a[0] for a in r3])
        ru.add_yaxis(
        series_name=item+"人流量",
        y_axis=[round(a[0],2) for a in r2],
        is_smooth=True,
        is_symbol_show=True,
        symbol="circle",
        symbol_size=6,
        linestyle_opts=opts.LineStyleOpts(color=color[i%4]),
        label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
        itemstyle_opts=opts.ItemStyleOpts(
            color="red", border_color="#fff", border_width=3
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
        )
        ru.set_global_opts(
        title_opts=opts.TitleOpts(
            title="入京人流量折线图",
            pos_bottom="5%",
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
        legend_opts=opts.LegendOpts(is_show=True),
        )
        i=i+1
    return ru
def chuzx()->Line:
    chu=Line(init_opts=opts.InitOpts(width="1600px", height="400px",bg_color=JsCode(background_color_js),theme=ThemeType.CHALK))
    i=0
    for item in x_data:
        sql2="select sum(mi) as sumi from (SELECT a,date,mi from qyhf,m_ip where p=p2) A where a='"+item+"' group by a,date order by date"
        cur.execute(sql2)
        r2=cur.fetchall()
        sql3="select distinct date from pm_i order  by date"
        cur.execute(sql3)
        r3=cur.fetchall()

        chu.add_xaxis(xaxis_data=[a[0] for a in r3])
        chu.add_yaxis(
        series_name=item+"人流量",
        y_axis=[round(a[0],2) for a in r2],
        is_smooth=True,
        is_symbol_show=True,
        symbol="circle",
        symbol_size=6,
        linestyle_opts=opts.LineStyleOpts(color=color[i%4]),
        label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
        itemstyle_opts=opts.ItemStyleOpts(
            color="red", border_color="#fff", border_width=3
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(color=JsCode(area_color_js), opacity=1),
        )
        chu.set_global_opts(
        title_opts=opts.TitleOpts(
            title="出京人流量折线图",
            pos_bottom="5%",
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
        legend_opts=opts.LegendOpts(is_show=True),
        )
        i=i+1
    return chu




tab = Tab()
tab.add(cr(),'出入总量数据图')
tab.add(ruriver(),'入京河流图')
tab.add(churiver(),'出京河流图')
tab.add(ruzx(),"入京折线图")
tab.add(chuzx(),"出京折线图")





tab.render("hhh.html")
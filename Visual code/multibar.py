import pyodbc
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline, Geo, Bar, Grid, Page, Tab, Pie, Line
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from pyecharts.globals import ChartType, SymbolType, ThemeType

conn=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE='';UID=sa;PWD=123;charset=cp936')
cur = conn.cursor()
tl = Timeline(init_opts=opts.InitOpts(width="800px", height="300px", theme=ThemeType.CHALK))
days = []
for i in range(20200117, 20200132):
    days.append(i)
for i in range(20200201, 20200216):
    days.append(i)

for day in days:
    sql1 = "select p1,pmi from [pm_i] where date='" + str(day) + "' order by pmi"
    cur.execute(sql1)
    result1 = cur.fetchall()
    sql2 = "select p2,mi from [m_ip]where date='" + str(day)+ "' order by mi"
    cur.execute(sql2)
    result2 = cur.fetchall()

    x_data = [a for a, b in result1]
    bar = (
        Bar(init_opts=opts.InitOpts( theme=ThemeType.CHALK))
        .add_xaxis(x_data)
        .add_yaxis(
            "入京迁徙指数",
            y_axis=[round(b, 2) for a, b in result1],

        )
        .add_yaxis(
            "出京迁徙指数",
            y_axis=[round(b, 2) for a, b in result2],

        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各省出入京统计"),
            datazoom_opts=opts.DataZoomOpts(type_="inside"),
        )
    )

    tl.add(bar,str(day)[4:8])
tl.render("multi-bar.html")

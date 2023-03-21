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

    c = (
        Pie(init_opts=opts.InitOpts(theme='CHALK',width='600px',height='200px'))

        .add(
            "入京人流量",
            [(a,round(b,2)) for a,b in result1],
            radius=["15%", "60%"],
            center=["25%", "50%"],
            rosetype="radius",
        )
        .add(
            "出京人流量",
            [(a,round(b,2)) for a,b in result2],
            radius=["15%", "60%"],
            center=["75%", "50%"],
            rosetype="radius",
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="各省出入京人流量饼状图",pos_left="center"),legend_opts=opts.LegendOpts(is_show=False),)
    )
    tl.add(c,str(day)[4:8])
tl.render("double_circle.html")


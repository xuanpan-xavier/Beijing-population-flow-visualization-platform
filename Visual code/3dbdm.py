import pyecharts.options as opts
import pyodbc
from pyecharts.charts import Bar3D, Tab, Page
from pyecharts.globals import ThemeType
from pyecharts.options import series_options

conn=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE='';UID=sa;PWD=123;charset=cp936')
cur = conn.cursor()
sql1="select distinct type from area_passenger_info"
cur.execute(sql1)
r1=cur.fetchall()
page = Page(layout=Page.SimplePageLayout,page_title="多场景多维人流量统计图集合",interval=20)

for tmtp in [item[0] for item in r1]:
    sql2 = "select type,date,time,avg(num) as avgnum from (SELECT [type],[date],[time],[num] FROM [datavisual_work3].[dbo].[api],dbo.area_passenger_info where api.id=area_passenger_info.id) A  where type='" + tmtp + "' group by type,date,time order by date,time"
    sql3 = "select distinct date from (select type,date,time,sum(num) as sumum from (SELECT [type],[date],[time],[num] FROM [datavisual_work3].[dbo].[api],dbo.area_passenger_info where api.id=area_passenger_info.id) A  where type='" + tmtp + "' group by type,date,time) A order by date"
    sql4 = "select distinct time from (select type,date,time,sum(num) as sumum from (SELECT [type],[date],[time],[num] FROM [datavisual_work3].[dbo].[api],dbo.area_passenger_info where api.id=area_passenger_info.id) A  where type='" + tmtp + "' group by type,date,time) A order by time"
    cur.execute(sql2)
    r2 = cur.fetchall()
    cur.execute(sql3)
    r3 = cur.fetchall()
    cur.execute(sql4)
    r4 = cur.fetchall()
    hours = [a[0] for a in r4]
    days = [a[0] for a in r3]
    data = [(i, j, k) for m, i, j, k in r2]
    data = [[d[1], d[0], d[2]] for d in data]

    page.add(
        (Bar3D(init_opts=opts.InitOpts(width="1000px", height="600px"))
            .add(
            series_name="",
            data=data,
            xaxis3d_opts=opts.Axis3DOpts(type_="category", data=hours,name='hour'),
            yaxis3d_opts=opts.Axis3DOpts(type_="category", data=days,name='day'),
            zaxis3d_opts=opts.Axis3DOpts(type_="value",name='index'),
        )
            .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(
                max_=max([k for m, i, j, k in r2]),
                range_color=[
                    "#313695",
                    "#4575b4",
                    "#74add1",
                    "#abd9e9",
                    "#e0f3f8",
                    "#ffffbf",
                    "#fee090",
                    "#fdae61",
                    "#f46d43",
                    "#d73027",
                    "#a50026",
                ],
            ),title_opts=(opts.TitleOpts(tmtp[5:]+"类型场所流量统计图"))
            )

        )
    )
page.render("各类型场所人流量图.html")

import random
import pyodbc
import substring as substring
from pyecharts import options as opts
from pyecharts.charts import Bar3D, Timeline
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType


conn=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE='';UID=sa;PWD=123;charset=cp936')
cur = conn.cursor()
sql1="select distinct type from area_passenger_info"
cur.execute(sql1)
r1=cur.fetchall()


# for tmtp in [item[0] for item in r1]:
tmtp='旅游景点;公园'
sql2 = "select type,date,time,avg(num) as avgnum from (SELECT [type],[date],[time],[num] FROM [datavisual_work3].[dbo].[api],dbo.area_passenger_info where api.id=area_passenger_info.id) A  where type='" + tmtp + "' group by type,date,time order by date,time"
sql3 = "select distinct date from (select type,date,time,sum(num) as sumum from (SELECT [type],[date],[time],[num] FROM [datavisual_work3].[dbo].[api],dbo.area_passenger_info where api.id=area_passenger_info.id) A  where type='" + tmtp + "' group by type,date,time) A order by date"
sql4 = "select distinct time from (select type,date,time,sum(num) as sumum from (SELECT [type],[date],[time],[num] FROM [datavisual_work3].[dbo].[api],dbo.area_passenger_info where api.id=area_passenger_info.id) A  where type='" + tmtp + "' group by type,date,time) A order by time"
cur.execute(sql2)
r2 = cur.fetchall()
cur.execute(sql3)
r3 = cur.fetchall()
cur.execute(sql4)
r4 = cur.fetchall()
data = [(i, j, k) for m, i, j, k in r2]
print(data)
print([a[0] for a in r4])
print([a[0] for a in r3])
print(max([k for m, i, j, k in r2]),min([k for m, i, j, k in r2]))
c = (Bar3D(init_opts=opts.InitOpts(width="1600px", height="800px"))
        .add(
            "",
            [[d[1], d[0], d[2]] for d in data],
            xaxis3d_opts=opts.Axis3DOpts([a[0] for a in r4], type_="time"),
            yaxis3d_opts=opts.Axis3DOpts([a[0] for a in r3], type_="date"),
            zaxis3d_opts=opts.Axis3DOpts(type_="flow"),
        )
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(max_=max([k for m, i, j, k in r2]), min_=min([k for m, i, j, k in r2]),range_color=[
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
                    ],),
            title_opts=opts.TitleOpts(title=tmtp + "类型区域人流量图"),
            # legend_opts=opts.LegendOpts(
            #     is_show=True,
            #     selected_mode='single',
            #     pos_top='5%', pos_right='5%',
            #     orient='vertical',
            #     legend_icon='circle'
            # )
)

     )

c.render("3db.html")
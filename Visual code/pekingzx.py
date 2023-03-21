# import pyecharts.options as opts
# import pyodbc
# from pyecharts.charts import Bar3D, Tab, Timeline, Line, Radar
# from pyecharts.globals import ThemeType
# from pyecharts.options import series_options
#
# conn=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE='';UID=sa;PWD=123;charset=cp936')
# cur = conn.cursor()
#
# tl = Timeline(init_opts=opts.InitOpts(width="540px", height="450px",theme=ThemeType.CHALK))
# tl.add_schema(
#         orient="vertical",
#         is_auto_play=True,
#         is_inverse=True,
#         play_interval=5000,
#         pos_left="null",
#         pos_right="5",
#         pos_top="20",
#         pos_bottom="20",
#         width="60",
#     )
#
# sql1="select distinct type1 from apin order by type1"
# cur.execute(sql1)
# r1=cur.fetchall()
# type=[x[0] for x in r1]
#
#
# days = []
# for i in range(20200216, 20200225):
#     days.append(str(i))
#
# hour = [i for i in range(0,24)]
#
# for day in days:
#     # c=Line(init_opts=opts.InitOpts(width="790px",height="490px",theme=ThemeType.CHALK))
#     # c.add_xaxis(hour)
#     # for tp in type:
#     #     sql2="select sum(num) from tmp A,apin B where date='"+day+"' and type1='"+tp+"' and A.id=B.id group by time order by time"
#     #
#     #     cur.execute(sql2)
#     #     r2=cur.fetchall()
#     #     print(r2)
#     #     y_a=[round((a[0]/1000),2) for a in r2]
#     #
#     #     c.add_yaxis(
#     #         series_name=tp,
#     #         stack="总人流量",
#     #         y_axis=y_a,
#     #         areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
#     #         label_opts=opts.LabelOpts(is_show=False),
#     #     )
#     # c.set_global_opts(
#     #     title_opts=opts.TitleOpts(title="不同类型区域总人流量指数(预测)",pos_top="20px"),
#     #     tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
#     #     yaxis_opts=opts.AxisOpts(
#     #         type_="value",
#     #         axistick_opts=opts.AxisTickOpts(is_show=True),
#     #         splitline_opts=opts.SplitLineOpts(is_show=True),
#     #     ),
#     #     xaxis_opts=opts.AxisOpts(type_="category", boundary_gap=False),)
#
#     d=Radar(init_opts=opts.InitOpts(width="480px",height="300px",theme=ThemeType.CHALK))
#     d.add_schema(
#         schema=[
#             opts.RadarIndicatorItem(name="交通",max_=100),
#             opts.RadarIndicatorItem(name="医疗",max_=100),
#             opts.RadarIndicatorItem(name="运动健身",max_=100),
#             opts.RadarIndicatorItem(name="旅游景点",max_=100),
#             opts.RadarIndicatorItem(name="购物",max_=100),
#             opts.RadarIndicatorItem(name="教育培训",max_=100),
#         ],
#         splitarea_opt=opts.SplitAreaOpts(
#             is_show=True, areastyle_opts=opts.AreaStyleOpts(opacity=1)
#         ),
#         textstyle_opts=opts.TextStyleOpts(color="#fff"),
#     )
#     sql2 = "select sum(num) from tmp A,apin B where date='" +day+ "' and A.id=B.id and time>=8 and time <=20 group by type1 order by type1"
#     sql3 = "select sum(num) from tmp A,apin B where date='" + day + "' and A.id=B.id and (time<8 or time >20) group by type1 order by type1"
#     cur.execute(sql2)
#     r2=cur.fetchall()
#     v2=[[round((a[0]/1000),2) for a in r2]]
#     cur.execute(sql3)
#     r3 = cur.fetchall()
#     v3= [[round((a[0] / 1000), 2) for a in r3]]
#     d.add(
#         series_name="白天总人流量指数(8:00-20:00)",
#         data=v2,
#         color="#f38181",
#     linestyle_opts = opts.LineStyleOpts(width=6),
#     )
#     d.add(
#         series_name="夜间总人流量指数(20:00-23:00,0:00-8:00)",
#         data=v3,
#         color="#95e1d3",
#         linestyle_opts = opts.LineStyleOpts(width = 6),
#     )
#
#     d.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#     d.set_global_opts(
#         title_opts=opts.TitleOpts(title="单日总人流量雷达图"), legend_opts=opts.LegendOpts(orient= "vertical",pos_left=10,pos_top=30)
#     )
#     tl.add(d,day[4:])
# tl.render("Radar.html")

# import pandas as pd
#
# # 读取文件数据
# df=pd.read_csv('shortstay_20200201_20200215.csv', sep='	',engine='python',header=[0])
#
# # 列csv文件中所有列
# df.columns = [ 'date', 'time', 'x', 'y', 'num']
#
# #  删除date列中的重复项，也就是说剩下的date都是已经分好的类别
# date_cate = df.drop_duplicates(subset=['date'])
# print(date_cate.date)
# print(range(len(date_cate)))    # date中的所有类，也就是文件数
# for name in date_cate.date:
#     print(name)
#     # 当date为某一个类时，存入一个小的csv文件中，文件名为类名
#     df[df.date == name].to_csv(u"%s" %name+".csv")
#
# code=utf-8
import pandas as pd

# 打开文件
data = pd.read_csv(r'real.csv')

# 每个excel保存3万行，那么530000+数据需要18个.csv文档保存
for i in range(0, 2):
    if i ==0:
        save_data = data.iloc[i * 353229 + 1: (i + 1) * 353229 + 1]
    if i==1:
        save_data = data.iloc[i * 353229 + 1:]
    file_name = r'rl' + str(i) + '.csv'  # 保存文件路径以及文件名称
    save_data.to_csv(file_name, index=False)  # 保存格式为.csv，如果是xlsx则修改为save_data.to_excel

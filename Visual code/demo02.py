import pyodbc
from pyecharts import options as opts
from pyecharts.charts import Map, Timeline, Geo, Bar, Grid, Page, Tab, Pie, Line
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from pyecharts.globals import ChartType, SymbolType, ThemeType

conn=pyodbc.connect('DRIVER={SQL Server};SERVER=localhost;DATABASE='';UID=sa;PWD=123;charset=cp936')
cur = conn.cursor()
def getru()->Timeline:
    tl =Timeline(init_opts=opts.InitOpts(width="1400px", height="800px", theme=ThemeType.DARK))
    tl.add_schema(
            orient="vertical",
            is_auto_play=True,
            is_inverse=True,
            play_interval=5000,
            pos_left="null",
            pos_right="5",
            pos_top="20",
            pos_bottom="20",
            width="60",
            label_opts=opts.LabelOpts(is_show=True, color="#fff"),
        )

    days=[]
    for i in range(20200117,20200132):
        days.append(i)
    for i in range(20200201,20200216):
        days.append(i)

    hours=range(1,25)

    for day in days:

        sql1 = "select p1,pmi from [pm_i] where date='" + str(day) + "' order by pmi"
        sql2 = "select p1,c2 from [pm_i] where pmi<=0.02488 and date='" + str(day) + "'"
        sql3 = "select p1,c2 from [pm_i] where pmi>0.02488 and pmi<=0.09441 and date='" + str(day) + "'"
        sql4 = "select p1,c2 from [pm_i] where pmi>0.09441 and date='" + str(day) + "'"

        cur.execute(sql1)
        result1 = cur.fetchall()
        cur.execute(sql2)
        result2 = cur.fetchall()
        cur.execute(sql3)
        result3 = cur.fetchall()
        cur.execute(sql4)
        result4 = cur.fetchall()



        b = (
            Bar()
                .add_xaxis([a for a, b in result1])
                .add_yaxis(
                series_name="",
                y_axis=[round(b,2) for a, b in result1],
                label_opts=opts.LabelOpts(
                    is_show=True, position="right", formatter="{b} : {c}"
                ),
            )
                .reversal_axis()
                .set_global_opts(
                xaxis_opts=opts.AxisOpts(
                     max_=10,axislabel_opts=opts.LabelOpts(is_show=False)
                ),
                yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(is_show=False)),
                tooltip_opts=opts.TooltipOpts(is_show=False),
                visualmap_opts=opts.VisualMapOpts(
                    is_calculable=True,
                    dimension=0,
                    pos_left="10",
                    pos_top="top",
                    range_text=["High", "Low"],
                    range_color=["lightskyblue", "yellow", "orangered"],
                    textstyle_opts=opts.TextStyleOpts(color="#ddd"),
                    min_=min([b for a, b in result1]),
                    max_=max([b for a, b in result1]),
                ),
            )
        )

        c = (
            Geo(is_ignore_nonexistent_coord=True)
                .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="#546570"))
                .add(
                "省份",
                [(a, b) for a, b in result1],
                type_=ChartType.EFFECT_SCATTER,
            )
                .add(
                "迁徙指数<0.02488",
                [(a, b) for a, b in result2],
                type_=ChartType.LINES,
                effect_opts=opts.EffectOpts(
                    symbol=SymbolType.ARROW, symbol_size=6, color="yellow"
                ),
                linestyle_opts=opts.LineStyleOpts(curve=0.2),
            ).add(
                "迁徙指数∈[0.02488,0.09441)",
                [(a, b) for a, b in result3],
                type_=ChartType.LINES,
                effect_opts=opts.EffectOpts(
                    symbol=SymbolType.ARROW, symbol_size=12, color="orange"
                ),
                linestyle_opts=opts.LineStyleOpts(curve=0.2),
            ).add(
                "迁徙指数>0.09441",
                [(a, b) for a, b in result4],
                type_=ChartType.LINES,
                effect_opts=opts.EffectOpts(
                    symbol=SymbolType.ARROW, symbol_size=18, color="red"
                ),
                linestyle_opts=opts.LineStyleOpts(curve=0.2),
            )
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title="                  "+str(day)+ "入京迁徙数据统计图"))
        )

        d=(
            Pie(init_opts=opts.InitOpts(bg_color="#2c343c"))
            .add(
                series_name="迁徙指数",
                data_pair=result1,
                rosetype="radius",
                radius=["15%", "35%"],
                center=["80%", "82%"],
                itemstyle_opts=opts.ItemStyleOpts(border_width=1, border_color="rgba(0,0,0,0.3)")
            ).set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=True, formatter="{b} {d}%"),
                legend_opts=opts.LegendOpts(is_show=False),
            )
        )

        grid = (
            Grid()
            .add(b,grid_opts=opts.GridOpts(pos_left="10", pos_right="45%", pos_top="50%", pos_bottom="5"))
            .add(c,grid_opts=opts.GridOpts())
            .add(d,grid_opts=opts.GridOpts(pos_left="45%", pos_top="60%"))
        )
        tl.add(grid,str(day)[4:8])
    return tl


def getchu() -> Timeline:
    tl = Timeline(init_opts=opts.InitOpts(width="800px", height="600px", theme=ThemeType.CHALK))
    tl.add_schema(
        orient="vertical",
        is_auto_play=True,
        is_inverse=True,
        play_interval=5000,
        pos_left="null",
        pos_right="5",
        pos_top="20",
        pos_bottom="20",
        width="60",
        label_opts=opts.LabelOpts(is_show=True, color="#fff"),
    )

    days = []
    for i in range(20200117, 20200132):
        days.append(i)
    for i in range(20200201, 20200216):
        days.append(i)

    hours = range(1, 25)

    for day in days:
        sql1 = "select top(100) c1,mi from [m_i] where date='" + str(day) + "' and c2='北京' order by mi desc"
        sql2="select top(100) c1,c2 from [m_i] where date='" + str(day) + "'and c2='北京' order by mi desc"
        sql3 = "select top(100) c1,c2 from [m_i] where date='" + str(day) + "'and c1='北京' order by mi desc"
        sql4 = "select top(100) c2,mi from [m_i] where date='" + str(day) + "'and c1='北京' order by mi desc"

        cur.execute(sql1)
        result1 = cur.fetchall()
        cur.execute(sql2)
        result2 = cur.fetchall()
        cur.execute(sql3)
        result3 = cur.fetchall()
        cur.execute(sql4)
        result4 = cur.fetchall()

        c = (
            Geo(is_ignore_nonexistent_coord=True,init_opts=opts.InitOpts(theme=ThemeType.CHALK))
            .add_schema(maptype="china", itemstyle_opts=opts.ItemStyleOpts(color="#546570"))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(title_opts=opts.TitleOpts(title=str(day) + "迁徙流向图"))
                .set_series_opts(effect_opts=opts.EffectOpts())
        )



        datat=[(a,b) for a, b in result1]
        tmp=[('a',123)]
        for i in range(len(result1)):
            tmp[0]=datat[i]
            if tmp[0][1]<0.1:
                c.add(
                    "入京市",
                    tmp,
                    type_=ChartType.EFFECT_SCATTER,
                    symbol=SymbolType.DIAMOND,
                    symbol_size=1,
                    # color='#58B3CC',
                    label_opts=opts.LabelOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True)
                )
            if tmp[0][1]<1 and tmp[0][1]>=0.1:
                c.add(
                    "入京市",
                    tmp,
                    type_=ChartType.EFFECT_SCATTER,
                    symbol=SymbolType.DIAMOND,
                    symbol_size=5,
                    # color='#58B3CC',
                    label_opts=opts.LabelOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True)
                )
            else:
                c.add(
                    "入京市",
                    tmp,
                    type_=ChartType.EFFECT_SCATTER,
                    symbol=SymbolType.DIAMOND,
                    symbol_size=9,
                    # color='#58B3CC',
                    label_opts=opts.LabelOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True)
                )
        datat=[(a, b) for a, b in result4]
        for i in range(len(result4)):
            tmp[0] = datat[i]
            if tmp[0][1] < 0.1:
                c.add(
                    "出京市",
                    tmp,
                    type_=ChartType.EFFECT_SCATTER,
                    symbol=SymbolType.DIAMOND,
                    symbol_size=1,
                    # color='#F58158',
                    label_opts=opts.LabelOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True)
                )
            if tmp[0][1] < 1 and tmp[0][1] >= 0.1:
                c.add(
                    "出京市",
                    tmp,
                    type_=ChartType.EFFECT_SCATTER,
                    symbol=SymbolType.DIAMOND,
                    symbol_size=5,
                    # color='#F58158',
                    label_opts=opts.LabelOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True)
                )
            else:
                c.add(
                    "出京市",
                    tmp,
                    type_=ChartType.EFFECT_SCATTER,
                    symbol=SymbolType.DIAMOND,
                    symbol_size=9,
                    # color='#F58158',
                    label_opts=opts.LabelOpts(is_show=False),
                    tooltip_opts=opts.TooltipOpts(is_show=True)
                )
        c.add(
                "入京流向",
                [(a, b) for a, b in result2],
                type_=ChartType.LINES,
                is_polyline=True,
                linestyle_opts=opts.LineStyleOpts(width=1,opacity=0.2,curve=0.1),

            )
        c.add(
                "出京流向",
                [(a, b) for a, b in result3],
                type_=ChartType.LINES,
                is_polyline=True,
                linestyle_opts=opts.LineStyleOpts(width=1,opacity=0.2,curve=0.1),

            )

        tl.add(c, str(day)[4:8])
    return tl

getchu().render("chu1.html")






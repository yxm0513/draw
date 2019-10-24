from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.render import make_snapshot
from snapshot_selenium import snapshot


times =  'image://data:image/png;base64,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'

def bar_base() -> Bar:
    c = (
        Bar()
        .add_xaxis(['DLC', 'HK', 'UNV', 'DLC11'])
        .add_yaxis("视频：预览", [1100, 1300, 1200, 1800], gap="0%")
        .add_yaxis("视频：推图", [500, 1200, 400, 1000],gap="0%")
        #

        .add_yaxis("纯抓拍：预览",[1000, 1400, 1100, 1000], gap = "0%")
        .add_yaxis("纯抓拍：推图",[500, 900, 1000, 900], gap = "0%")
        .add_yaxis("图片：预览", [0, 0, 0, 0], markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(name="不支持", coord=['DLC', 200], symbol=times, symbol_size=30, type_="不支持"),
                  opts.MarkPointItem(name="不支持", coord=['HK', 200], symbol=times,
                                     symbol_size=30, type_="不支持"),
                  opts.MarkPointItem(name="不支持", coord=['UNV', 200], symbol=times,
                                     symbol_size=30, type_="不支持"),
                  opts.MarkPointItem(name="不支持", coord=['DLC11', 200], symbol=times,
                                     symbol_size=30, type_="不支持")]
        ))
        .add_yaxis("图片：推图", [2000, 2100, 0, 1700], markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(name="不支持", coord=['UNV', 200], symbol=times, symbol_size=30, type_="不支持")]
        ), gap="0%")
        .set_global_opts(title_opts=opts.TitleOpts(title="相机延迟", subtitle="单位 ms (图片流不支持预览)"))
    )
    return c

bar = bar_base()

bar.render(path="/tmp/a.html")

#bar.render(path = 'bar.jpeg')

make_snapshot(snapshot, bar.render(), "bar.png")


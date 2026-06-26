import pandas as pd
import folium
from folium.plugins import MarkerCluster
import webbrowser
import os

df = pd.read_excel("云南省A级景区名录_带坐标.xlsx")
df_map = df.dropna(subset=['经度', '纬度']).copy()

# 定义等级颜色
level_colors = {'5A': 'red', '4A': 'orange', '3A': 'blue', '2A': 'green', '1A': 'purple'}

# 使用高德地图底图（中文地名显示更好）
map_center = [24.5, 101.5]

# 创建地图时使用高德图层
m = folium.Map(
    location=map_center, 
    zoom_start=7,
    tiles='http://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
    attr='高德地图'
)

# 添加一个标准图层作为备选
folium.TileLayer(
    tiles='http://webrd01.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}',
    name='高德地图',
    attr='高德地图'
).add_to(m)

# 添加图层控制
folium.LayerControl().add_to(m)

# 添加标题
title_html = f'''
<h3 align="center" style="font-size:16px"><b>云南省A级旅游景区空间分布图</b></h3>
<p align="center" style="font-size:12px;color:gray">共 {len(df_map)} 个景区（含5A/4A/3A/2A/1A）</p>
'''
m.get_root().html.add_child(folium.Element(title_html))

# 添加景区标记
marker_cluster = MarkerCluster().add_to(m)
for idx, row in df_map.iterrows():
    name = row['景区名称']
    level = row['等级']
    city = row['所在州市']
    lng = row['经度']
    lat = row['纬度']
    color = level_colors.get(level, 'gray')
    
    folium.Marker(
        location=[lat, lng],
        popup=folium.Popup(f"<b>{name}</b><br>等级：{level}<br>州市：{city}", max_width=300),
        icon=folium.Icon(color=color, icon='info-sign', prefix='fa')
    ).add_to(marker_cluster)

# 添加图例
legend_html = '''
<div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000; background: white; 
            padding: 12px 16px; border: 2px solid #ccc; border-radius: 8px; font-size: 13px;">
    <b>景区等级</b><br>
    <i class="fa fa-circle" style="color:red"></i> 5A级<br>
    <i class="fa fa-circle" style="color:orange"></i> 4A级<br>
    <i class="fa fa-circle" style="color:blue"></i> 3A级<br>
    <i class="fa fa-circle" style="color:green"></i> 2A级<br>
    <i class="fa fa-circle" style="color:purple"></i> 1A级
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

output_path = "云南省A级景区空间分布地图.html"
m.save(output_path)

print(f"✅ 地图已生成：{output_path}")
webbrowser.open('file://' + os.path.realpath(output_path))
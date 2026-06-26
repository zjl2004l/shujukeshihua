import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import folium
from streamlit_folium import st_folium

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False

st.set_page_config(page_title="云南旅游数据分析", layout="wide")
st.title("📊 云南省各州市旅游数据分析")
st.caption("2015-2022年 · 16个州市 · 128条记录")

# 缓存旅游收入数据
@st.cache_data
def load_data():
    df = pd.read_csv("旅游数据.csv")
    return df

# 缓存景区坐标数据（给地图用）
@st.cache_data
def load_scenic_map_data():
    df_scenic = pd.read_excel("云南省A级景区名录_带坐标.xlsx")
    df_scenic = df_scenic.dropna(subset=["经度", "纬度"])
    return df_scenic

df = load_data()
df_map = load_scenic_map_data()

years = sorted(df["年份"].unique())
cities = sorted(df["州市"].unique())

st.sidebar.header("🔧 筛选条件")
selected_year = st.sidebar.selectbox("选择年份", years)
selected_cities = st.sidebar.multiselect("选择州市（趋势分析）", cities, default=["昆明", "大理", "丽江"])

# ========== 数据概览 ==========
st.header("📈 数据概览")
col1, col2, col3, col4 = st.columns(4)
col1.metric("总记录数", f"{len(df)} 条")
col2.metric("年份范围", f"{min(years)} - {max(years)}")
col3.metric("州市数量", f"{len(cities)} 个")
col4.metric("2022年最高收入", "2741.56 亿元 (昆明)")

# ========== 各州市旅游总收入排名 ==========
st.header("🏆 各州市旅游总收入排名")
df_year = df[df["年份"] == selected_year].sort_values("旅游总收入(亿元)", ascending=True)

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(df_year["州市"], df_year["旅游总收入(亿元)"], color="steelblue")
ax.set_xlabel("旅游总收入（亿元）")
ax.set_title(f"{selected_year}年云南省各州市旅游总收入排名")
for bar, val in zip(bars, df_year["旅游总收入(亿元)"]):
    ax.text(val + 10, bar.get_y() + bar.get_height()/2, f"{val:.1f}", va="center", fontsize=8)
st.pyplot(fig)

# ========== 主要州市旅游收入趋势 ==========
st.header("📉 主要州市旅游收入趋势")
fig, ax = plt.subplots(figsize=(10, 5))
for city in selected_cities:
    city_data = df[df["州市"] == city]
    ax.plot(city_data["年份"], city_data["旅游总收入(亿元)"], marker="o", label=city, linewidth=2)
ax.set_xlabel("年份")
ax.set_ylabel("旅游总收入（亿元）")
ax.set_title("2015-2022年旅游总收入趋势")
ax.legend()
ax.grid(alpha=0.3)
st.pyplot(fig)

# ========== 景区空间分布地图 ==========
st.header("🗺️ 云南省A级景区空间分布地图")
st.caption(f"共 {len(df_map)} 个景区（含5A/4A/3A/2A/1A）")

level_colors = {'5A': 'red', '4A': 'orange', '3A': 'blue', '2A': 'green', '1A': 'purple'}

m = folium.Map(location=[24.5, 101.5], zoom_start=7)

# 添加图例
legend_html = '''
<div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000; background: white; 
            padding: 10px 14px; border: 2px solid #ccc; border-radius: 6px; font-size: 13px;">
    <b>景区等级</b><br>
    <i class="fa fa-circle" style="color:red"></i> 5A级<br>
    <i class="fa fa-circle" style="color:orange"></i> 4A级<br>
    <i class="fa fa-circle" style="color:blue"></i> 3A级<br>
    <i class="fa fa-circle" style="color:green"></i> 2A级<br>
    <i class="fa fa-circle" style="color:purple"></i> 1A级
</div>
'''
m.get_root().html.add_child(folium.Element(legend_html))

# 批量添加标记
for idx, row in df_map.iterrows():
    folium.Marker(
        location=[row["纬度"], row["经度"]],
        popup=folium.Popup(
            f"<b>{row['景区名称']}</b><br>等级：{row['等级']}<br>州市：{row['所在州市']}",
            max_width=300
        ),
        icon=folium.Icon(color=level_colors.get(row["等级"], 'gray'), icon='info-sign', prefix='fa')
    ).add_to(m)

st_folium(m, width=1000, height=600)

# ========== 数据查询与导出 ==========
st.header("📋 数据查询")
col_year = st.selectbox("筛选年份", ["全部"] + years)
filtered = df if col_year == "全部" else df[df["年份"] == col_year]
st.dataframe(filtered.reset_index(drop=True), use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8-sig")
st.download_button("📥 下载数据为CSV", csv, "旅游数据.csv", "text/csv")

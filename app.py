import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster

# ---------------------- 修复中文乱码（兼容Windows+Linux） ----------------------
plt.rcParams['font.sans-serif'] = ['WenQuanYi Zen Hei', 'SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['axes.unicode_minus'] = False

# 页面基础配置
st.set_page_config(page_title="云南旅游数据分析", layout="wide")
st.title("🏆 云南省各州市旅游数据分析")
st.caption("2015-2022年 · 16个州市旅游收入+A级景区空间可视化")

# ---------------------- 缓存数据 + 异常容错 ----------------------
@st.cache_data
def load_travel_data():
    try:
        df = pd.read_csv("旅游数据.csv", encoding="utf-8-sig")
        # 清洗数值空行
        df = df.dropna(subset=["年份", "州市", "旅游总收入(亿元)"])
        df["旅游总收入(亿元)"] = pd.to_numeric(df["旅游总收入(亿元)"])
        return df
    except Exception as e:
        st.error(f"旅游数据CSV读取失败：{str(e)}")
        return pd.DataFrame()

@st.cache_data
def load_scenic_data():
    try:
        df_scenic = pd.read_excel("云南省A级景区名录_带坐标.xlsx")
        df_scenic = df_scenic.dropna(subset=["经度", "纬度"])
        df_scenic["经度"] = pd.to_numeric(df_scenic["经度"])
        df_scenic["纬度"] = pd.to_numeric(df_scenic["纬度"])
        return df_scenic
    except Exception as e:
        st.error(f"景区Excel读取失败：{str(e)}")
        return pd.DataFrame()

# 加载数据
df = load_travel_data()
df_map = load_scenic_data()

# 数据为空直接终止
if df.empty:
    st.stop()

years = sorted(df["年份"].unique())
cities = sorted(df["州市"].unique())

# ---------------------- 侧边栏筛选 ----------------------
st.sidebar.header("🔧 筛选控制面板")
selected_year = st.sidebar.selectbox("选择排名年份", years)
selected_cities = st.sidebar.multiselect("趋势图选择州市", cities, default=["昆明", "大理", "丽江"])

# ---------------------- 1. 数据概览指标卡 ----------------------
st.header("📊 数据总览")
col1, col2, col3, col4 = st.columns(4)
col1.metric("总数据记录", f"{len(df)} 条")
col2.metric("统计年份区间", f"{min(years)} - {max(years)}")
col3.metric("州市总数", f"{len(cities)} 个")
max_2022 = df[df["年份"] == 2022]["旅游总收入(亿元)"].max()
col4.metric("2022最高旅游收入", f"{max_2022:.2f} 亿元(昆明)")

# ---------------------- 2. 各州市旅游收入横向条形图（修复方框乱码+标签溢出） ----------------------
st.header("🏆 各州市旅游总收入排名")
df_year = df[df["年份"] == selected_year].sort_values("旅游总收入(亿元)", ascending=True)

fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.barh(df_year["州市"], df_year["旅游总收入(亿元)"], color="steelblue")
ax.set_xlabel("旅游总收入（亿元）", fontsize=12)
ax.set_title(f"{selected_year}年云南省各州市旅游总收入排名", fontsize=14, pad=15)

# 修复数值标签：动态留白，不会超出画布
x_max = df_year["旅游总收入(亿元)"].max()
ax.set_xlim(0, x_max * 1.12)  # 右侧预留12%空白放数字
for bar, val in zip(bars, df_year["旅游总收入(亿元)"]):
    ax.text(val + x_max * 0.01, bar.get_y() + bar.get_height()/2, f"{val:.1f}", va="center", fontsize=10)

st.pyplot(fig, use_container_width=True)

# ---------------------- 3. 多州市收入趋势折线图 ----------------------
st.header("📈 州市旅游收入年度变化趋势")
fig, ax = plt.subplots(figsize=(12, 6))
for city in selected_cities:
    city_data = df[df["州市"] == city].sort_values("年份")
    ax.plot(city_data["年份"], city_data["旅游总收入(亿元)"], marker="o", linewidth=2.2, label=city)
ax.set_xlabel("年份", fontsize=12)
ax.set_ylabel("旅游总收入（亿元）", fontsize=12)
ax.set_title("2015-2022年旅游总收入变化趋势", fontsize=14)
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
st.pyplot(fig, use_container_width=True)

# ---------------------- 4. A级景区空间地图（MarkerCluster优化加载速度） ----------------------
st.header("🗺️ 云南省A级景区空间分布地图")
if df_map.empty:
    st.warning("景区坐标文件读取失败，无法展示地图")
else:
    st.caption(f"有效景区数量：{len(df_map)} 个（1A-5A全覆盖）")
    level_colors = {'5A': 'red', '4A': 'orange', '3A': 'blue', '2A': 'green', '1A': 'purple'}
    # 云南中心坐标
    m = folium.Map(location=[24.5, 101.5], zoom_start=7)
    # 聚合标记，解决大量景区卡顿
    marker_cluster = MarkerCluster().add_to(m)

    # 图例悬浮框
    legend_html = '''
    <div style="position: fixed; bottom: 30px; right: 30px; z-index: 1000; background: white; 
                padding: 10px 14px; border: 2px solid #ccc; border-radius: 6px; font-size: 13px;">
        <b>景区等级图例</b><br>
        <i class="fa fa-circle" style="color:red"></i> 5A级景区<br>
        <i class="fa fa-circle" style="color:orange"></i> 4A级景区<br>
        <i class="fa fa-circle" style="color:blue"></i> 3A级景区<br>
        <i class="fa fa-circle" style="color:green"></i> 2A级景区<br>
        <i class="fa fa-circle" style="color:purple"></i> 1A级景区
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    # 批量添加聚合标记，提升渲染速度
    for _, row in df_map.iterrows():
        icon_color = level_colors.get(row["等级"], "gray")
        popup_text = f"<b>{row['景区名称']}</b><br>等级：{row['等级']}<br>所属州市：{row['所在州市']}"
        folium.Marker(
            location=[row["纬度"], row["经度"]],
            popup=folium.Popup(popup_text, max_width=320),
            icon=folium.Icon(color=icon_color, icon="map-marker", prefix="fa")
        ).add_to(marker_cluster)

    st_folium(m, width="100%", height=620)

# ---------------------- 5. 原始数据查询与导出 ----------------------
st.header("📋 原始数据查询 & 导出")
year_choose = st.selectbox("筛选年份", ["全部年份"] + years)
if year_choose == "全部年份":
    data_show = df.copy()
else:
    data_show = df[df["年份"] == year_choose]

st.dataframe(data_show.reset_index(drop=True), use_container_width=True)
# 下载CSV（中文不乱码）
csv_data = data_show.to_csv(index=False, encoding="utf-8-sig").encode("utf-8-sig")
st.download_button(
    label="📥 导出筛选后数据为CSV文件",
    data=csv_data,
    file_name="云南旅游收入数据.csv",
    mime="text/csv"
)

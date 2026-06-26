import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
matplotlib.rcParams['axes.unicode_minus'] = False

# 读取数据
file_path = r"云南各州市旅游数据_2015-2022.xlsx"
df = pd.read_excel(file_path)

# ============ 图1: 2022年各州市旅游总收入排名（柱状图）============
df_2022 = df[df["年份"] == 2022].sort_values("旅游总收入(亿元)", ascending=True)

fig1, ax1 = plt.subplots(figsize=(12, 8))
bars = ax1.barh(df_2022["州市"], df_2022["旅游总收入(亿元)"], color='steelblue')
ax1.set_xlabel("旅游总收入（亿元）", fontsize=12)
ax1.set_ylabel("州市", fontsize=12)
ax1.set_title("2022年云南省各州市旅游总收入排名", fontsize=14, fontweight='bold')
# 在柱子上添加数值标签
for bar, val in zip(bars, df_2022["旅游总收入(亿元)"]):
    ax1.text(val + 20, bar.get_y() + bar.get_height()/2, f'{val:.2f}', 
             va='center', fontsize=9)
plt.tight_layout()
plt.savefig(r"图1_2022年旅游收入排名.png", dpi=300)
plt.show()

# ============ 图2: 昆明 vs 全省旅游总收入趋势（折线图）============
df_km = df[df["州市"] == "昆明"]
df_province = df[df["州市"] == "临沧"]  # 临沧作为代表，实际应使用全省数据
# 实际上我们需要计算全省合计，但这里用昆明对比其他主要城市
# 改用：昆明、大理、丽江、曲靖的趋势对比
top_cities = ["昆明", "大理", "丽江", "曲靖", "红河"]
df_top = df[df["州市"].isin(top_cities)]

fig2, ax2 = plt.subplots(figsize=(12, 6))
for city in top_cities:
    city_data = df[df["州市"] == city]
    ax2.plot(city_data["年份"], city_data["旅游总收入(亿元)"], marker='o', label=city, linewidth=2)

ax2.set_xlabel("年份", fontsize=12)
ax2.set_ylabel("旅游总收入（亿元）", fontsize=12)
ax2.set_title("2015-2022年云南省主要州市旅游总收入趋势", fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(r"图2_主要州市收入趋势.png", dpi=300)
plt.show()

# ============ 图3: 2022年各州市旅游收入占比（饼图）============
fig3, ax3 = plt.subplots(figsize=(10, 10))
# 只显示占比>2%的州市，其他合并为"其他"
threshold = 2  # 百分比阈值
df_2022_sorted = df_2022.sort_values("旅游总收入(亿元)", ascending=False)
total = df_2022_sorted["旅游总收入(亿元)"].sum()
df_2022_sorted["占比(%)"] = df_2022_sorted["旅游总收入(亿元)"] / total * 100

# 合并小份额
main_data = df_2022_sorted[df_2022_sorted["占比(%)"] >= threshold]
other_sum = df_2022_sorted[df_2022_sorted["占比(%)"] < threshold]["旅游总收入(亿元)"].sum()

labels = list(main_data["州市"]) + ["其他"]
sizes = list(main_data["旅游总收入(亿元)"]) + [other_sum]

colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#6c5ce7', 
          '#fd79a8', '#00b894', '#e17055', '#0984e3', '#fdcb6e', '#a29bfe']
wedges, texts, autotexts = ax3.pie(sizes, labels=labels, autopct='%1.1f%%', 
                                     colors=colors[:len(labels)], startangle=90)
ax3.set_title("2022年云南省各州市旅游总收入占比", fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(r"图3_2022年旅游收入占比.png", dpi=300)
plt.show()

print("✅ 3张图表已生成并保存到：")
print("  图1: 图1_2022年旅游收入排名.png")
print("  图2: 图2_主要州市收入趋势.png")
print("  图3:图3_2022年旅游收入占比.png")
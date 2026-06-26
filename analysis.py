import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
matplotlib.rcParams['axes.unicode_minus'] = False
matplotlib.rcParams['font.size'] = 11

# ========== 1. 读取数据 ==========
df_scenic = pd.read_excel("云南省各州市A级景区统计.xlsx")
df_scenic = df_scenic[df_scenic["所在州市"] != "思茅区"]
df_scenic["所在州市"] = df_scenic["所在州市"].str.replace("市", "").str.replace("州", "")
df_scenic_summary = df_scenic.groupby("所在州市").agg({"景区总数": "sum"}).reset_index()

df_econ = pd.read_excel(r"云南各州市旅游数据_2015-2022.xlsx")
df_econ_2022 = df_econ[df_econ["年份"] == 2022][["州市", "旅游总收入(亿元)"]]

df_merged = df_scenic_summary.merge(df_econ_2022, left_on="所在州市", right_on="州市")
df_merged = df_merged.drop(columns=["州市"])
df_merged = df_merged.rename(columns={"所在州市": "州市"})

print("📊 共 {} 个州市".format(len(df_merged)))
print(df_merged[["州市", "景区总数", "旅游总收入(亿元)"]].to_string())

# ========== 2. 创建图形 ==========
fig, ax = plt.subplots(figsize=(15, 10))

# ========== 3. 绘制散点 ==========
scatter = ax.scatter(
    df_merged["旅游总收入(亿元)"], 
    df_merged["景区总数"], 
    s=df_merged["景区总数"] * 2 + 30,
    c=df_merged["旅游总收入(亿元)"],
    cmap='Blues', 
    alpha=0.8, 
    edgecolors='darkblue',
    linewidth=1.5
)

# 添加颜色条
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('旅游总收入（亿元）', fontsize=12)

# ========== 4. 趋势线 ==========
z = np.polyfit(df_merged["旅游总收入(亿元)"], df_merged["景区总数"], 1)
p = np.poly1d(z)
x_line = np.linspace(0, 3000, 100)
ax.plot(x_line, p(x_line), "--", color="red", alpha=0.8, linewidth=2.5, label="趋势线")

# ========== 5. 添加所有州市标签 ==========
for i, row in df_merged.iterrows():
    city = row["州市"]
    x = row["旅游总收入(亿元)"]
    y = row["景区总数"]
    
    if city == "昆明":
        ax.annotate(city, (x, y), xytext=(0, 15), textcoords='offset points', 
                   fontsize=13, fontweight='bold', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.4', facecolor='#FF6B6B', alpha=0.8, edgecolor='darkred'))
    elif city == "保山":
        ax.annotate(city, (x, y), xytext=(0, 12), textcoords='offset points',
                   fontsize=12, fontweight='bold', ha='center', va='center',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='gray'))
    elif city == "红河":
        ax.annotate(city, (x, y), xytext=(15, 5), textcoords='offset points',
                   fontsize=11, fontweight='bold', ha='left', va='center')
    elif city == "大理":
        ax.annotate(city, (x, y), xytext=(12, -8), textcoords='offset points',
                   fontsize=11, fontweight='bold', ha='left', va='center')
    elif city == "丽江":
        ax.annotate(city, (x, y), xytext=(-15, 5), textcoords='offset points',
                   fontsize=11, fontweight='bold', ha='right', va='center')
    elif city == "曲靖":
        ax.annotate(city, (x, y), xytext=(0, 10), textcoords='offset points',
                   fontsize=11, fontweight='bold', ha='center', va='center')
    else:
        ax.annotate(city, (x, y), xytext=(8, 6), textcoords='offset points',
                   fontsize=10, fontweight='bold', ha='left', va='center',
                   bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.6, edgecolor='lightgray'))

# ========== 6. 坐标轴 ==========
ax.set_xlabel("旅游总收入（亿元）", fontsize=14, fontweight='bold')
ax.set_ylabel("A级景区数量（个）", fontsize=14, fontweight='bold')
ax.set_title("2022年云南省各州市A级景区数量与旅游收入关联分析", fontsize=16, fontweight='bold', pad=20)

ax.set_xticks(np.arange(0, 3200, 500))
ax.set_yticks(np.arange(0, 130, 20))
ax.set_xlim(-50, 3000)
ax.set_ylim(-5, 120)
ax.grid(True, alpha=0.2, linestyle='--')

# ========== 7. 图例（移到右下角，避免与注释框重叠） ==========
legend_elements = [
    plt.Line2D([0], [0], color='red', linestyle='--', linewidth=2.5, label='趋势线'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='steelblue', 
               markersize=10, label='各州市')
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=11, framealpha=0.9)

# ========== 8. 注释框（移到右上角） ==========
ax.text(
    0.68, 0.92, 
    "● 昆明：46个景区，收入2742亿元（最高）\n" 
    "● 保山：108个景区（最多），收入473亿元\n"
    "● 大理/红河：景区与收入较为匹配\n"
    "● 趋势线呈上升趋势，景区数量与收入正向关联",
    transform=ax.transAxes,
    fontsize=10,
    verticalalignment='top',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#FFF9E6', alpha=0.9, edgecolor='#CCCCCC')
)

plt.tight_layout()
plt.savefig("图3-5_景区数量与旅游收入散点图_优化版.png", dpi=300, bbox_inches='tight')
plt.close()

print("\n✅ 优化版散点图已保存: 图3-5_景区数量与旅游收入散点图_优化版.png")
print("图例已移至右下角，注释框移至右上角，不再重叠。")
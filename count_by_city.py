import pandas as pd

# 读取景区名录
df = pd.read_excel("云南省A级景区名录_2025.xlsx")

# 将"思茅区"修正为"普洱市"
df.loc[df["所在州市"] == "思茅区", "所在州市"] = "普洱市"

# 重新保存
df.to_excel("云南省A级景区名录_2025.xlsx", index=False)

print("✅ 已修正：思茅区 → 普洱市")

# 重新统计
city_count = df.groupby('所在州市').size().reset_index(name='景区总数')
level_city = df.groupby(['所在州市', '等级']).size().unstack(fill_value=0)
result = city_count.merge(level_city, on='所在州市')
result = result.sort_values('景区总数', ascending=False)

print("\n📊 修正后的各州市A级景区统计:")
print(result.to_string())
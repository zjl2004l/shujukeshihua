import pandas as pd

# 读取景区统计
df_scenic = pd.read_excel("云南省各州市A级景区统计.xlsx")
print("景区统计中的州市名称:")
print(df_scenic["所在州市"].tolist())

# 读取旅游经济数据
df_econ = pd.read_excel(r"云南各州市旅游数据_2015-2022.xlsx")
df_econ_2022 = df_econ[df_econ["年份"] == 2022]
print("\n旅游经济数据中的州市名称:")
print(df_econ_2022["州市"].tolist())
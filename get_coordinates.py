import pandas as pd
import requests
import time

API_KEY = "f39fe2e8759a418fc23715fcf6e9d754"  # 替换成你的Key

df = pd.read_excel("云南省A级景区名录_2025.xlsx")

def get_lng_lat(name, city):
    """查询经纬度，强制限定在云南省"""
    url = "https://restapi.amap.com/v3/geocode/geo"
    params = {
        "address": name,
        "city": city,
        "key": API_KEY,
        "output": "json",
        "citylimit": "true"  # 🔑 关键：限定只返回云南省的结果
    }
    try:
        resp = requests.get(url, params, timeout=10)
        data = resp.json()
        if data["status"] == "1" and data["geocodes"]:
            location = data["geocodes"][0]["location"]
            lng, lat = location.split(",")
            # 验证坐标是否在云南省范围内
            # 云南经度约 97.5-106.2，纬度约 21.1-29.3
            if 97 < float(lng) < 107 and 20 < float(lat) < 30:
                return float(lng), float(lat)
            else:
                # 如果坐标不在云南范围，尝试用"云南省+景区名称"重新查询
                params2 = {
                    "address": f"云南省{name}",
                    "key": API_KEY,
                    "output": "json"
                }
                resp2 = requests.get(url, params2, timeout=10)
                data2 = resp2.json()
                if data2["status"] == "1" and data2["geocodes"]:
                    location = data2["geocodes"][0]["location"]
                    lng, lat = location.split(",")
                    if 97 < float(lng) < 107 and 20 < float(lat) < 30:
                        return float(lng), float(lat)
        return None, None
    except Exception as e:
        return None, None

# 批量查询
lng_list = []
lat_list = []
fail_count = 0

print(f"开始查询 {len(df)} 个景区的坐标...")

for i, row in df.iterrows():
    name = row["景区名称"]
    city = row["所在州市"]
    lng, lat = get_lng_lat(name, city)
    lng_list.append(lng)
    lat_list.append(lat)
    
    if lng is None:
        fail_count += 1
    
    if (i + 1) % 50 == 0:
        print(f"进度: {i+1}/{len(df)}，失败: {fail_count} 个")
    
    time.sleep(0.2)

df["经度"] = lng_list
df["纬度"] = lat_list

# 保存
df.to_excel("云南省A级景区名录_带坐标.xlsx", index=False)

print(f"\n✅ 查询完成！")
print(f"成功: {df['经度'].notna().sum()} 个")
print(f"失败: {df['经度'].isna().sum()} 个")
print(f"💾 已保存到: 云南省A级景区名录_带坐标.xlsx")
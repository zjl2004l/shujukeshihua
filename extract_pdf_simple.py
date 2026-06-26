import pdfplumber
import pandas as pd
import re

pdf_path = "202527171517.pdf"

all_data = []
current_section = None

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, 1):
        print(f"正在处理第 {page_num} 页...")
        text = page.extract_text()
        if not text:
            continue
        
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # 检测等级标题（如 "5A:10个、4A:197个"）
            if re.search(r'[1-5]A[:：]\d+个', line):
                # 提取等级信息
                match = re.findall(r'([1-5]A)[:：](\d+)个', line)
                for level, count in match:
                    print(f"  发现 {level}: {count}个")
                continue
            
            # 检测表格数据行：序号 + 景区名称 + 州市 + 等级 + 时间
            # 格式示例: "1 昆明市石林风景名胜区 昆明市 5A 2007-05"
            match = re.match(
                r'^(\d+)\s+([^\d]+?)\s+([^\s]+?)\s+([1-5]A)\s+(\d{4}-\d{2})$',
                line
            )
            if match:
                seq = match.group(1)
                name = match.group(2).strip()
                city = match.group(3).strip()
                level = match.group(4).strip()
                time = match.group(5).strip()
                
                all_data.append({
                    '序号': seq,
                    '景区名称': name,
                    '所在州市': city,
                    '等级': level,
                    '评定时间': time
                })
                continue
            
            # 如果正则匹配失败，尝试用空格分割
            parts = line.split()
            if len(parts) >= 5:
                # 尝试识别：第一个是序号，最后三个是州市、等级、时间，中间是名称
                first = parts[0]
                last_three = parts[-3:]
                if first.isdigit() and re.match(r'[1-5]A', last_three[1]):
                    name = ' '.join(parts[1:-3])
                    city = last_three[0]
                    level = last_three[1]
                    time = last_three[2]
                    all_data.append({
                        '序号': first,
                        '景区名称': name,
                        '所在州市': city,
                        '等级': level,
                        '评定时间': time
                    })

print(f"\n✅ 共提取 {len(all_data)} 条记录")

if all_data:
    df = pd.DataFrame(all_data)
    
    # 去重（按景区名称和等级）
    df = df.drop_duplicates(subset=['景区名称', '等级'], keep='first')
    print(f"去重后剩余 {len(df)} 条记录")
    
    # 保存
    output_path = "云南省A级景区名录_2025.xlsx"
    df.to_excel(output_path, index=False)
    print(f"💾 已保存到: {output_path}")
    print("\n前10条预览:")
    print(df.head(10))
    
    # 统计各等级数量
    print("\n📊 各等级景区数量:")
    print(df['等级'].value_counts().sort_index())
else:
    print("❌ 没有提取到数据，PDF可能是扫描版图片")
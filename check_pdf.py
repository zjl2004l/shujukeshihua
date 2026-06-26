import tabula

pdf_path = "202527171517.pdf"

try:
    # 尝试读取前3页
    dfs = tabula.read_pdf(pdf_path, pages='1-3')
    print(f"✅ PDF可读取！前3页提取到 {len(dfs)} 个表格")
    print(f"第1个表格形状: {dfs[0].shape}")
    print("\n前5行预览:")
    print(dfs[0].head())
except Exception as e:
    print(f"❌ 读取失败: {e}")
    print("\n可能原因：PDF是扫描版（图片格式），需要先用OCR转文字")
# 数据表格填充 Demo - 二次开发指引

## 项目简介
这是一个基于Streamlit的数据处理和表格生成项目。用户可以输入两段文本，系统会对输入数据进行处理，然后填充到指定的表格模板中，最终生成完整的表格并支持下载。

## 1. 快速运行
```bash
cd data_table_demo
pip install -r requirements.txt
streamlit run app.py
```

## 2. 项目结构
```
data_table_demo/
├── app.py                 # Streamlit 主应用
├── config.py              # 配置参数管理
├── data_handler.py        # 数据处理逻辑
├── templates/
│   └── blank_table.csv    # 空白表格模板
├── output/                # 输出目录
├── requirements.txt       # 项目依赖
└── README.md             # 项目说明
```

## 3. 功能特性
- 📝 支持两段文本输入
- 📊 可上传自定义表格模板（CSV/Excel）
- ⚙️ 实时调整表格行列数和占位符
- 👀 实时预览填充结果
- 💾 一键下载生成的表格

## 4. 二次开发指南

### 修改数据处理逻辑
打开 `data_handler.py`，替换 `fill_table` 函数即可：
```python
def fill_table(df: pd.DataFrame, text1: str, text2: str) -> pd.DataFrame:
    # 在这里实现你的数据处理逻辑
    # 例如：正则匹配、API调用、数据聚合等
    pass
```

### 修改/新增参数
- **固定参数** → 修改 `config.py` 中的 `Config` 类
- **动态参数** → 在 `app.py` 的侧边栏或主界面添加新的输入控件

### 更换表格模板
1. 将你的模板文件放入 `templates/` 目录
2. 确保列名与代码中的配置一致
3. 修改 `app.py` 中的默认模板路径

### 扩展功能示例
- 支持多Sheet Excel文件
- 添加数据验证和错误处理
- 集成外部API进行数据处理
- 添加数据可视化图表
- 支持批量处理多个文件

## 5. 技术栈
- **前端框架**: Streamlit
- **数据处理**: Pandas
- **文件支持**: openpyxl (Excel), csv (CSV)
- **配置管理**: dataclasses

## 6. 开发建议
- 保持代码模块化，便于维护
- 使用类型提示提高代码可读性
- 添加适当的错误处理和用户提示
- 考虑添加单元测试确保数据处理的正确性

## 7. 常见问题
**Q: 如何处理大文件？**
A: 考虑使用分块处理或流式读取，避免内存溢出。

**Q: 如何添加更多输入字段？**
A: 在 `app.py` 中添加新的 `st.text_area` 或 `st.text_input`，并在 `data_handler.py` 中相应修改函数签名。

**Q: 如何支持更多文件格式？**
A: 在 `app.py` 的 `file_uploader` 中添加新的文件类型，并使用相应的读取函数。 
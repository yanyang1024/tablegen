# 数据表格填充 Demo

一个基于 Streamlit 的数据处理和表格生成应用，支持两步式数据处理流程：先生成中间结果，再基于中间结果和参数生成最终表格。

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Streamlit 1.37.0+
- Pandas 2.2.2+
- OpenPyXL 3.1.2+

### 安装依赖
```bash
pip install -r requirements.txt
```

### 运行应用
```bash
streamlit run app.py
```

应用将在浏览器中打开：http://localhost:8501

## 📖 使用方法

### 1. 选择或上传模板
- **使用默认模板**：在侧边栏调整行数和列数
- **上传自定义模板**：支持 CSV 和 Excel 文件
  - 第一行和第一列将作为参考信息保留
  - 其他部分会自动填充为占位符

### 2. 输入五段文本
在五个文本框中输入需要处理的文本内容：
- 文本块 1-5：支持任意长度的文本输入

### 3. 生成中间结果
点击"生成中间结果"按钮：
- 系统将五段文本按空白分词
- 生成包含 `source`、`index`、`token` 三列的中间结果表
- 表格行数根据实际分词结果自适应

### 4. 输入中间阶段参数
在"中间阶段参数"输入框中输入额外参数值

### 5. 生成最终结果
点击"生成最终结果"按钮：
- 基于中间结果表和参数值生成最终表格
- 保持模板的首行首列不变
- 其他部分按规则填充处理后的数据

### 6. 下载结果
- 中间结果：点击"下载中间结果 CSV"
- 最终结果：点击"下载最终结果 CSV"

## 🏗️ 项目结构

```
data_table_demo93/
├── app.py                 # Streamlit 主应用入口
├── config.py              # 配置参数管理
├── data_handler.py        # 数据处理核心逻辑
├── templates/             # 模板文件目录
├── output/                # 输出文件目录
├── requirements.txt       # Python 依赖
└── README.md             # 项目文档
```

## ⚙️ 配置说明

### config.py 主要参数

```python
@dataclass
class Config:
    # 文本输入默认值
    default_text1: str = "hello"
    default_text2: str = "world"
    default_text3: str = "foo"
    default_text4: str = "bar"
    default_text5: str = "baz"
    
    # 中间阶段参数默认值
    default_mid_param: str = "param"
    
    # 表格尺寸
    rows: int = 5
    cols: int = 4
    
    # 占位符
    placeholder: str = "待填充"
```

## 🔧 二次开发指南

### 1. 修改数据处理逻辑

#### 中间结果生成逻辑
编辑 `data_handler.py` 中的 `generate_intermediate_result` 函数：

```python
def generate_intermediate_result(text1: str, text2: str, text3: str, text4: str, text5: str) -> pd.DataFrame:
    """
    自定义中间结果生成逻辑
    """
    # 在这里实现你的文本处理逻辑
    # 例如：文本分析、特征提取、数据清洗等
    
    # 返回 DataFrame，列数和行数可自适应
    return your_custom_dataframe
```

#### 最终结果生成逻辑
编辑 `data_handler.py` 中的 `process_intermediate_to_final` 函数：

```python
def process_intermediate_to_final(df_mid: pd.DataFrame, mid_param: str, df_template: pd.DataFrame, rows: int, cols: int) -> pd.DataFrame:
    """
    自定义最终结果生成逻辑
    """
    # 在这里实现基于中间结果和参数的最终表格生成逻辑
    # df_mid: 中间结果表
    # mid_param: 中间阶段参数
    # df_template: 模板表格
    # rows, cols: 目标表格尺寸
    
    # 返回填充后的最终表格
    return your_final_dataframe
```

### 2. 添加新的配置参数

在 `config.py` 中添加新的配置项：

```python
@dataclass
class Config:
    # 现有配置...
    
    # 新增配置
    new_parameter: str = "default_value"
    numeric_param: int = 100
    list_param: list = None
```

在 `app.py` 中使用新配置：

```python
# 在侧边栏或其他位置添加控件
new_value = st.text_input("新参数", cfg.new_parameter)
```

### 3. 修改界面布局

#### 添加新的输入控件
```python
# 在 app.py 中添加新的输入控件
new_input = st.text_area("新输入框", height=80)
new_select = st.selectbox("选择框", ["选项1", "选项2", "选项3"])
new_slider = st.slider("数值滑块", 0, 100, 50)
```

#### 添加新的展示区域
```python
# 添加新的结果展示
if st.button("新功能按钮"):
    new_result = your_new_function()
    st.subheader("新结果")
    st.dataframe(new_result)
```

### 4. 扩展数据处理功能

#### 添加新的数据处理函数
在 `data_handler.py` 中添加新函数：

```python
def your_new_data_processing_function(input_data, **kwargs):
    """
    新的数据处理函数
    """
    # 实现你的数据处理逻辑
    processed_data = process_data(input_data)
    return processed_data
```

#### 集成外部库
在 `requirements.txt` 中添加新的依赖：

```
# 现有依赖...
numpy==1.24.0
scikit-learn==1.3.0
matplotlib==3.7.0
```

### 5. 自定义模板处理

#### 支持新的文件格式
在 `create_template_from_upload` 函数中添加新格式支持：

```python
def create_template_from_upload(uploaded_file):
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        elif uploaded_file.name.endswith(".json"):  # 新增 JSON 支持
            df = pd.read_json(uploaded_file)
        else:
            raise ValueError("不支持的文件格式")
        
        # 后续处理逻辑...
```

## 🧪 测试和调试

### 运行测试
```bash
python test_app.py
```

### 调试技巧
1. 使用 `st.write()` 输出调试信息
2. 在关键位置添加 `st.info()` 显示状态
3. 使用 `st.exception()` 捕获和显示错误

### 性能优化
1. 大数据集处理时使用分页显示
2. 复杂计算使用 `@st.cache_data` 缓存
3. 避免在每次渲染时重复计算

## 📝 常见问题

### Q: 上传的 Excel 文件无法读取
A: 确保安装了 `openpyxl` 库：`pip install openpyxl`

### Q: 表格显示异常或报错
A: 检查数据类型兼容性，确保非首列已转换为 string 类型

### Q: 中间结果表格为空
A: 检查输入文本是否包含有效内容，空文本或纯空格会导致无结果

### Q: 最终结果填充不完整
A: 检查模板尺寸设置，确保行列数足够容纳所有数据

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发送邮件
- 项目讨论区

---

**注意**: 这是一个演示项目，生产环境使用前请进行充分测试和安全审查。 
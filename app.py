import streamlit as st
import pandas as pd
from pathlib import Path
from config import Config
from data_handler import fill_table, create_template_from_upload

cfg = Config()
st.set_page_config(page_title="数据表格填充 Demo", layout="centered")

st.title("1. 数据表格填充 Demo")
st.markdown("输入两段文本 → 生成填充后的表格 → 下载结果")

# 初始化session_state
if "template_df" not in st.session_state:
    st.session_state.template_df = None
if "template_rows" not in st.session_state:
    st.session_state.template_rows = cfg.rows
if "template_cols" not in st.session_state:
    st.session_state.template_cols = cfg.cols

# 侧边栏参数
with st.sidebar:
    st.header("参数调整")
    
    # 显示当前模板的尺寸信息
    if st.session_state.template_df is not None:
        st.info(f"当前模板: {st.session_state.template_rows}行 × {st.session_state.template_cols}列")
    
    # 手动调整尺寸（仅在没有上传模板时可用）
    if st.session_state.template_df is None:
        cfg.rows = st.number_input("行数", 1, 20, cfg.rows)
        cfg.cols = st.number_input("列数", 1, 10, cfg.cols)
        st.session_state.template_rows = cfg.rows
        st.session_state.template_cols = cfg.cols
    else:
        st.write("⚠️ 上传模板后，尺寸由模板决定")
    
    cfg.placeholder = st.text_input("占位符", cfg.placeholder)

# 上传或直接使用模板
st.subheader("2. 选择或上传模板")
uploaded = st.file_uploader("上传空白模板 (csv/excel)", type=["csv", "xlsx"])
tagup = False

if uploaded is not None:
    # 处理上传的文件
    tagup = True
    template_df, rows, cols, error = create_template_from_upload(uploaded)
    
    if error:
        st.error(f"文件读取错误: {error}")
        st.stop()
    
    if template_df is not None:
        st.session_state.template_df = template_df
        st.session_state.template_rows = rows
        st.session_state.template_cols = cols
        
        st.success(f"✅ 模板上传成功！尺寸: {rows}行 × {cols}列")
        
        # 显示模板预览
        st.subheader("模板预览")
        st.dataframe(template_df)
        
        # 提供重置选项
        if st.button("重置为默认模板"):
            st.session_state.template_df = None
            st.session_state.template_rows = cfg.rows
            st.session_state.template_cols = cfg.cols
            st.rerun()

# 确定使用的模板
if st.session_state.template_df is not None:
    df_blank = st.session_state.template_df
    current_rows = st.session_state.template_rows
    current_cols = st.session_state.template_cols
else:
    # 使用默认模板
    if tagup:
        df_blank = pd.read_csv("templates/blank_table.csv")
        current_rows = st.session_state.template_rows
        current_cols = st.session_state.template_cols
    else:

        cfg.rows = st.number_input("行数", 1, 20, cfg.rows)
        cfg.cols = st.number_input("列数", 1, 10, cfg.cols)
        st.session_state.template_rows = cfg.rows
        st.session_state.template_cols = cfg.cols
        # make table 
        current_cols = cfg.cols
        current_rows = cfg.rows
        df_blank = pd.DataFrame(columns=range(current_cols), index=range(current_rows))
        

st.subheader("3. 输入两段文本")
text1 = st.text_area("文本块 1", cfg.default_text1, height=60)
text2 = st.text_area("文本块 2", cfg.default_text2, height=60)

if st.button("4. 填充并预览"):
    # 传递当前的行列数参数
    df_result = fill_table(df_blank, text1, text2, current_rows, current_cols)
    st.session_state["result"] = df_result

if "result" in st.session_state:
    st.subheader("5. 结果预览")
    st.dataframe(st.session_state["result"])

    csv = st.session_state["result"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="6. 下载 CSV",
        data=csv,
        file_name="filled_table.csv",
        mime="text/csv",
    ) 
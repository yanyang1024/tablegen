import streamlit as st
import pandas as pd
from pathlib import Path
from config import Config
from data_handler import fill_table

cfg = Config()
st.set_page_config(page_title="数据表格填充 Demo", layout="centered")

st.title("1. 数据表格填充 Demo")
st.markdown("输入两段文本 → 生成填充后的表格 → 下载结果")

# 侧边栏参数
with st.sidebar:
    st.header("参数调整")
    cfg.rows = st.number_input("行数", 1, 20, cfg.rows)
    cfg.cols = st.number_input("列数", 1, 10, cfg.cols)
    cfg.placeholder = st.text_input("占位符", cfg.placeholder)

# 上传或直接使用模板
uploaded = st.file_uploader("上传空白模板 (csv/excel)", type=["csv", "xlsx"])
if uploaded:
    if uploaded.name.endswith(".csv"):
        df_blank = pd.read_csv(uploaded)
    else:
        df_blank = pd.read_excel(uploaded, engine="openpyxl")
else:
    df_blank = pd.read_csv("templates/blank_table.csv")

st.subheader("2. 输入两段文本")
text1 = st.text_area("文本块 1", cfg.default_text1, height=60)
text2 = st.text_area("文本块 2", cfg.default_text2, height=60)

if st.button("3. 填充并预览"):
    df_result = fill_table(df_blank, text1, text2)
    st.session_state["result"] = df_result

if "result" in st.session_state:
    st.subheader("4. 结果预览")
    st.dataframe(st.session_state["result"])

    csv = st.session_state["result"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="5. 下载 CSV",
        data=csv,
        file_name="filled_table.csv",
        mime="text/csv",
    ) 
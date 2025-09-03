import streamlit as st
import pandas as pd
from pathlib import Path
from config import Config
from data_handler import fill_table, create_template_from_upload, make_blank_template, generate_intermediate_result

cfg = Config()
st.set_page_config(page_title="数据表格填充 Demo", layout="centered")

st.title("1. 数据表格填充 Demo")
st.markdown("输入文本 → 生成中间结果表格与最终填充表格 → 下载结果")

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
    st.info(f"当前模板: {st.session_state.template_rows}行 × {st.session_state.template_cols}列")
    
    # 手动调整尺寸（仅在没有上传模板时可用）
    if st.session_state.template_df is None:
        cfg.rows = st.number_input("行数", 1, 20, st.session_state.template_rows)
        cfg.cols = st.number_input("列数", 1, 10, st.session_state.template_cols)
        st.session_state.template_rows = cfg.rows
        st.session_state.template_cols = cfg.cols
    else:
        st.write("⚠️ 上传模板后，尺寸由模板决定")
        if st.button("重置为默认模板"):
            st.session_state.template_df = None
            st.session_state.template_rows = cfg.rows
            st.session_state.template_cols = cfg.cols
            st.rerun()
    
    cfg.placeholder = st.text_input("占位符", cfg.placeholder)

# 上传或直接使用模板
st.subheader("2. 选择或上传模板")
uploaded = st.file_uploader("上传空白模板 (csv/excel)", type=["csv", "xlsx"])

if uploaded is not None:
    # 处理上传的文件
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

# 确定使用的模板
if st.session_state.template_df is not None:
    df_blank = st.session_state.template_df
    current_rows = st.session_state.template_rows
    current_cols = st.session_state.template_cols
else:
    # 使用动态生成的默认模板
    current_rows = st.session_state.template_rows
    current_cols = st.session_state.template_cols
    df_blank = make_blank_template(current_rows, current_cols, cfg.placeholder)

st.subheader("3. 输入五段文本")
text1 = st.text_area("文本块 1", cfg.default_text1, height=60)
text2 = st.text_area("文本块 2", cfg.default_text2, height=60)
text3 = st.text_area("文本块 3", cfg.default_text3, height=60)
text4 = st.text_area("文本块 4", cfg.default_text4, height=60)
text5 = st.text_area("文本块 5", cfg.default_text5, height=60)

if st.button("4. 生成中间结果与最终结果"):
    # 中间结果（自适应表格维度）
    mid_df = generate_intermediate_result(text1, text2, text3, text4, text5)
    st.session_state["mid_result"] = mid_df
    
    # 最终结果（基于模板填充：示例仍使用 text1, text2）
    df_result = fill_table(df_blank, text1, text2, current_rows, current_cols)
    st.session_state["result"] = df_result

# 展示中间结果
if "mid_result" in st.session_state:
    st.subheader("5. 中间结果预览")
    st.dataframe(st.session_state["mid_result"])
    csv_mid = st.session_state["mid_result"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="下载中间结果 CSV",
        data=csv_mid,
        file_name="intermediate_result.csv",
        mime="text/csv",
    )

# 展示最终结果
if "result" in st.session_state:
    st.subheader("6. 最终结果预览")
    st.dataframe(st.session_state["result"])

    csv = st.session_state["result"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="下载最终结果 CSV",
        data=csv,
        file_name="filled_table.csv",
        mime="text/csv",
    ) 
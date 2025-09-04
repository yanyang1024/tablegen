import streamlit as st
import pandas as pd
from pathlib import Path
from config import Config
from data_handler import (
    fill_table, 
    create_template_from_upload, 
    make_blank_template, 
    generate_intermediate_result, 
    generate_adaptive_table_by_option,
    process_to_final_result
)

cfg = Config()
st.set_page_config(page_title="数据表格填充 Demo", layout="centered")

st.title("1. 数据表格填充 Demo")
st.markdown("输入文本 → 生成阶段性结果 → 选择选项 → 生成自适应表格 → 输入最终参数 → 生成最终结果")

# 初始化session_state
if "template_df" not in st.session_state:
    st.session_state.template_df = None
if "template_rows" not in st.session_state:
    st.session_state.template_rows = cfg.rows
if "template_cols" not in st.session_state:
    st.session_state.template_cols = cfg.cols
if "stage_result" not in st.session_state:
    st.session_state.stage_result = None
if "adaptive_result" not in st.session_state:
    st.session_state.adaptive_result = None
if "final_result" not in st.session_state:
    st.session_state.final_result = None

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

# 步骤一：生成阶段性结果
if st.button("4. 生成阶段性结果"):
    stage_df = generate_intermediate_result(text1, text2, text3, text4, text5)
    st.session_state["stage_result"] = stage_df
    # 清空后续结果，避免误导
    st.session_state["adaptive_result"] = None
    st.session_state["final_result"] = None

# 展示阶段性结果
if st.session_state.get("stage_result") is not None:
    st.subheader("5. 阶段性结果预览")
    st.dataframe(st.session_state["stage_result"])
    csv_stage = st.session_state["stage_result"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="下载阶段性结果 CSV",
        data=csv_stage,
        file_name="stage_result.csv",
        mime="text/csv",
    )

    # 步骤二：下拉框选择
    st.subheader("6. 选择处理选项")
    selected_option = st.selectbox(
        "请选择处理方式",
        cfg.dropdown_options,
        key="option_selector"
    )
    
    # 步骤三：生成自适应表格
    if st.button("7. 生成自适应表格"):
        adaptive_df = generate_adaptive_table_by_option(
            st.session_state["stage_result"], 
            selected_option
        )
        st.session_state["adaptive_result"] = adaptive_df
        # 清空最终结果
        st.session_state["final_result"] = None

# 同时展示阶段性结果和自适应表格（如果都存在）
if (st.session_state.get("stage_result") is not None and 
    st.session_state.get("adaptive_result") is not None):
    
    st.subheader("8. 结果对比分析")
    
    # 使用两列布局同时展示两个表格
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**阶段性结果**")
        st.dataframe(st.session_state["stage_result"])
    
    with col2:
        st.write("**自适应表格**")
        st.dataframe(st.session_state["adaptive_result"])
    
    # 下载按钮
    csv_adaptive = st.session_state["adaptive_result"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="下载自适应表格 CSV",
        data=csv_adaptive,
        file_name="adaptive_table.csv",
        mime="text/csv",
    )

    # 步骤四：最终参数输入
    st.subheader("9. 最终阶段参数输入")
    final_param = st.text_input("最终阶段参数", cfg.default_final_param, key="final_param_input")

    # 步骤五：生成最终结果
    if st.button("10. 生成最终结果"):
        final_df = process_to_final_result(
            st.session_state["stage_result"],
            st.session_state["adaptive_result"],
            final_param,
            df_blank,
            current_rows,
            current_cols,
        )
        st.session_state["final_result"] = final_df

# 展示最终结果
if st.session_state.get("final_result") is not None:
    st.subheader("11. 最终结果预览")
    st.dataframe(st.session_state["final_result"])

    csv_final = st.session_state["final_result"].to_csv(index=False).encode("utf-8")
    st.download_button(
        label="下载最终结果 CSV",
        data=csv_final,
        file_name="final_result.csv",
        mime="text/csv",
    )

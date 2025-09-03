import pandas as pd
from config import Config
from typing import Optional, Tuple

cfg = Config()


def _coerce_non_header_columns_to_string(df: pd.DataFrame) -> pd.DataFrame:
    """将除首列外的所有列转换为 pandas 的 string dtype，避免 Arrow 序列化错误。"""
    if df.shape[1] <= 1:
        return df
    df_str = df.copy()
    non_header_cols = list(df_str.columns[1:])
    # 使用 pandas 扩展字符串dtype，兼容 Arrow
    df_str[non_header_cols] = df_str[non_header_cols].astype("string")
    return df_str


def fill_table(df: pd.DataFrame, text1: str, text2: str, rows: int = None, cols: int = None) -> pd.DataFrame:
    """
    智能填充逻辑：
    1. 如果提供了rows和cols参数，使用这些参数
    2. 否则使用DataFrame的实际尺寸
    3. 第一行和第一列保持不变，其他部分进行填充
    """
    # 先确保可填充区域的列为 string dtype
    df_filled = _coerce_non_header_columns_to_string(df)
    
    # 获取实际的行数和列数
    actual_rows = rows if rows is not None else len(df_filled)
    actual_cols = cols if cols is not None else len(df_filled.columns)
    
    # 确保不超出DataFrame的实际边界
    actual_rows = min(actual_rows, len(df_filled))
    actual_cols = min(actual_cols, len(df_filled.columns))
    
    idx = 0
    # 从第二行第二列开始填充（保持第一行和第一列不变）
    for r in range(1, actual_rows):
        for c in range(1, actual_cols):
            if r < len(df_filled) and c < len(df_filled.columns):
                df_filled.iloc[r, c] = f"{text1}-{text2}-{idx}"
                idx += 1
    
    # 返回前再次确保 dtype
    df_filled = _coerce_non_header_columns_to_string(df_filled)
    return df_filled

# 新增：根据行列数生成空白模板（首行首列保留，其他用占位符）

def make_blank_template(rows: int, cols: int, placeholder: Optional[str] = None) -> pd.DataFrame:
    ph = placeholder if placeholder is not None else cfg.placeholder
    rows = max(1, rows)
    cols = max(1, cols)
    df = pd.DataFrame(columns=range(cols), index=range(rows))
    df = _coerce_non_header_columns_to_string(df)
    # 仅填充非首行首列
    for r in range(1, rows):
        for c in range(1, cols):
            df.iloc[r, c] = ph
    return df


def create_template_from_upload(uploaded_file) -> Tuple[pd.DataFrame, int, int, Optional[str]]:
    """
    从上传的文件创建模板表格
    第一行和第一列作为参考信息，其他部分用占位符填充
    
    返回: (template_df, rows, cols, error_message)
    """
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine="openpyxl")
        
        # 获取实际的行数和列数
        rows = len(df)
        cols = len(df.columns)
        
        # 创建新的模板表格（保持第一行第一列）
        template_df = _coerce_non_header_columns_to_string(df)
        
        # 除了第一行和第一列，其他部分用占位符填充
        for r in range(1, rows):
            for c in range(1, cols):
                template_df.iloc[r, c] = cfg.placeholder
        
        # 返回前确保 dtype
        template_df = _coerce_non_header_columns_to_string(template_df)
        return template_df, rows, cols, None
        
    except Exception as e:
        return None, 0, 0, str(e) 
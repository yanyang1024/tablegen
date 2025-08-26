import pandas as pd
from config import Config

cfg = Config()

def fill_table(df: pd.DataFrame, text1: str, text2: str) -> pd.DataFrame:
    """
    极简逻辑：逐格写入 text1/text2 及序号
    后续可替换为任何复杂算法
    """
    df_filled = df.copy()
    idx = 0
    for r in range(cfg.rows):
        for c in range(cfg.cols):
            df_filled.iloc[r, c] = f"{text1}-{text2}-{idx}"
            idx += 1
    return df_filled 
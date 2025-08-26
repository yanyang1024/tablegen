"""
自定义数据处理逻辑示例
这个文件展示了如何替换默认的数据处理逻辑
"""

import pandas as pd
import re
from typing import List, Dict

def advanced_fill_table(df: pd.DataFrame, text1: str, text2: str) -> pd.DataFrame:
    """
    高级数据处理逻辑示例
    
    功能：
    1. 从text1中提取关键词
    2. 从text2中提取数字
    3. 根据提取的内容智能填充表格
    """
    df_filled = df.copy()
    
    # 从text1中提取关键词（假设是逗号分隔的）
    keywords = [kw.strip() for kw in text1.split(',') if kw.strip()]
    
    # 从text2中提取数字
    numbers = re.findall(r'\d+', text2)
    
    # 智能填充逻辑
    row_idx = 0
    for keyword in keywords:
        if row_idx >= len(df_filled):
            break
            
        col_idx = 0
        for number in numbers:
            if col_idx >= len(df_filled.columns):
                break
                
            # 组合关键词和数字
            cell_value = f"{keyword}_{number}"
            df_filled.iloc[row_idx, col_idx] = cell_value
            col_idx += 1
        
        row_idx += 1
    
    return df_filled

def extract_data_from_text(text: str) -> Dict[str, List[str]]:
    """
    从文本中提取结构化数据
    """
    result = {
        'keywords': [],
        'numbers': [],
        'dates': [],
        'emails': []
    }
    
    # 提取关键词（假设是大写字母开头的单词）
    keywords = re.findall(r'\b[A-Z][a-z]+\b', text)
    result['keywords'] = keywords
    
    # 提取数字
    numbers = re.findall(r'\d+', text)
    result['numbers'] = numbers
    
    # 提取日期（简单格式）
    dates = re.findall(r'\d{4}-\d{2}-\d{2}', text)
    result['dates'] = dates
    
    # 提取邮箱
    emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    result['emails'] = emails
    
    return result

def create_summary_table(df: pd.DataFrame, text1: str, text2: str) -> pd.DataFrame:
    """
    创建汇总表格
    """
    # 提取数据
    data1 = extract_data_from_text(text1)
    data2 = extract_data_from_text(text2)
    
    # 创建汇总表格
    summary_data = {
        '数据类型': ['关键词', '数字', '日期', '邮箱'],
        '文本1数量': [
            len(data1['keywords']),
            len(data1['numbers']),
            len(data1['dates']),
            len(data1['emails'])
        ],
        '文本2数量': [
            len(data2['keywords']),
            len(data2['numbers']),
            len(data2['dates']),
            len(data2['emails'])
        ]
    }
    
    return pd.DataFrame(summary_data)

# 使用示例：
if __name__ == "__main__":
    # 测试数据
    test_text1 = "Apple, Banana, Orange, Grape"
    test_text2 = "数量：10个，价格：25元，日期：2024-01-15"
    
    # 创建测试表格
    test_df = pd.DataFrame({
        'Col0': ['待填充'] * 3,
        'Col1': ['待填充'] * 3,
        'Col2': ['待填充'] * 3
    })
    
    print("原始表格:")
    print(test_df)
    print("\n处理后的表格:")
    result = advanced_fill_table(test_df, test_text1, test_text2)
    print(result)
    
    print("\n数据提取结果:")
    data1 = extract_data_from_text(test_text1)
    data2 = extract_data_from_text(test_text2)
    print("文本1提取结果:", data1)
    print("文本2提取结果:", data2) 
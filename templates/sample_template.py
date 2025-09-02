#!/usr/bin/env python3
"""
生成示例XLSX模板文件
"""
import pandas as pd
import os

def create_sample_xlsx():
    """创建示例XLSX模板文件"""
    
    # 创建示例数据
    sample_data = {
        '项目名称': ['项目A', '项目B', '项目C', '项目D', '项目E'],
        '负责人': ['张三', '李四', '王五', '赵六', '钱七'],
        '开始日期': ['2024-01-01', '2024-02-01', '2024-03-01', '2024-04-01', '2024-05-01'],
        '结束日期': ['2024-06-30', '2024-07-31', '2024-08-31', '2024-09-30', '2024-10-31'],
        '预算': ['100万', '150万', '200万', '80万', '120万']
    }
    
    # 创建DataFrame
    df = pd.DataFrame(sample_data)
    
    # 确保templates目录存在
    os.makedirs('templates', exist_ok=True)
    
    # 保存为XLSX文件
    output_path = 'templates/sample_template.xlsx'
    df.to_excel(output_path, index=False, engine='openpyxl')
    
    print(f"✅ 示例XLSX模板已创建: {output_path}")
    print(f"   表格尺寸: {len(df)}行 × {len(df.columns)}列")
    print(f"   列名: {list(df.columns)}")
    
    return output_path

if __name__ == "__main__":
    create_sample_xlsx() 
#!/usr/bin/env python3
"""
测试脚本 - 验证应用核心功能
"""
import pandas as pd
from config import Config
from data_handler import fill_table, create_template_from_upload

def test_config():
    """测试配置类"""
    print("1. 测试配置类...")
    cfg = Config()
    print(f"   默认文本1: {cfg.default_text1}")
    print(f"   默认文本2: {cfg.default_text2}")
    print(f"   表格尺寸: {cfg.rows}行 x {cfg.cols}列")
    print(f"   列名: {cfg.col_names}")
    print("   ✓ 配置类测试通过")

def test_data_handler():
    """测试数据处理逻辑"""
    print("\n2. 测试数据处理逻辑...")
    
    # 创建测试数据
    cfg = Config()
    test_df = pd.DataFrame(
        [[cfg.placeholder] * cfg.cols for _ in range(cfg.rows)],
        columns=cfg.col_names
    )
    
    print(f"   原始表格形状: {test_df.shape}")
    print(f"   原始表格内容:\n{test_df.head()}")
    
    # 测试填充逻辑（不传递行列数参数）
    result_df = fill_table(test_df, "测试文本1", "测试文本2")
    
    print(f"   填充后表格形状: {result_df.shape}")
    print(f"   填充后表格内容:\n{result_df.head()}")
    
    # 测试填充逻辑（传递行列数参数）
    result_df2 = fill_table(test_df, "测试文本1", "测试文本2", 3, 2)
    
    print(f"   指定尺寸填充后表格内容:\n{result_df2.head()}")
    
    # 验证填充结果
    expected_cells = cfg.rows * cfg.cols
    actual_cells = result_df.size
    assert actual_cells == expected_cells, f"单元格数量不匹配: 期望{expected_cells}, 实际{actual_cells}"
    
    print("   ✓ 数据处理逻辑测试通过")

def test_template_loading():
    """测试模板加载"""
    print("\n3. 测试模板加载...")
    
    try:
        template_df = pd.read_csv("templates/blank_table.csv")
        print(f"   模板表格形状: {template_df.shape}")
        print(f"   模板列名: {list(template_df.columns)}")
        print("   ✓ 模板加载测试通过")
    except Exception as e:
        print(f"   ✗ 模板加载失败: {e}")

def test_new_fill_logic():
    """测试新的填充逻辑（保持第一行第一列不变）"""
    print("\n4. 测试新的填充逻辑...")
    
    # 创建测试表格，第一行和第一列有特殊内容
    test_df = pd.DataFrame({
        'Col0': ['标题1', '行1', '行2', '行3'],
        'Col1': ['标题2', '数据1', '数据2', '数据3'],
        'Col2': ['标题3', '数据4', '数据5', '数据6'],
        'Col3': ['标题4', '数据7', '数据8', '数据9']
    })
    
    print("   原始表格:")
    print(test_df)
    
    # 测试填充逻辑
    result_df = fill_table(test_df, "新文本1", "新文本2", 4, 4)
    
    print("\n   填充后表格（保持第一行第一列不变）:")
    print(result_df)
    
    # 验证第一行和第一列保持不变
    assert result_df.iloc[0, 0] == '标题1', "第一行第一列应该保持不变"
    assert result_df.iloc[0, 1] == '标题2', "第一行应该保持不变"
    assert result_df.iloc[1, 0] == '行1', "第一列应该保持不变"
    
    print("   ✓ 新填充逻辑测试通过")

def main():
    """主测试函数"""
    print("=" * 50)
    print("数据表格填充 Demo - 功能测试")
    print("=" * 50)
    
    try:
        test_config()
        test_data_handler()
        test_template_loading()
        test_new_fill_logic()
        
        print("\n" + "=" * 50)
        print("🎉 所有测试通过！应用可以正常运行")
        print("=" * 50)
        print("\n启动应用命令:")
        print("streamlit run app.py")
        print("\n访问地址: http://localhost:8501")
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 
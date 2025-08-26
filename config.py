from dataclasses import dataclass

@dataclass
class Config:
    # 输入框默认值
    default_text1: str = "hello"
    default_text2: str = "world"
    # 表格尺寸
    rows: int = 5
    cols: int = 4
    col_names: list = None
    # 占位符
    placeholder: str = "待填充"

    def __post_init__(self):
        if self.col_names is None:
            self.col_names = [f"Col{i}" for i in range(self.cols)] 
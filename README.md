# GTCP (Gibbs Triangle Heatmap Plotter)

GTCP 是一个将三元合金成分（Mg-Si-Al）与深度（depth）关系绘制在吉布斯三角坐标中的热图工具。通过数据插值和平滑处理，生成高质量的热图，直观地展示深度值在成分空间中的分布。

## 功能

- 从 Excel 文件中加载和处理三元合金成分数据（Mg、Si、Al）
- 自动过滤数据：仅保留 Si 和 Mg 在 [0, 0.012] 范围内，且 Si+Mg ≤ 0.012 的数据点
- 将三元坐标转换为吉布斯三角坐标（等边三角形）
- 使用深度值作为颜色映射，生成热图
- 支持等高线填充和原始数据点显示
- 自动裁剪并保存右上方的图片区域
- 同时输出 PDF 和 PNG 格式

## 安装

请确保安装以下必要的 Python 库：
```bash
pip install -r requirements.txt
```

或者手动安装：
```bash
pip install pandas numpy matplotlib scipy openpyxl
```

## 使用说明

### 数据准备

1. 准备 Excel 文件（示例：`深度.xlsx`），包含以下四列：
   - **第一列**：Mg（镁）成分
   - **第二列**：Si（硅）成分
   - **第三列**：Al（铝）成分
   - **第四列**：depth（深度值，用于颜色映射）

2. 确保数据满足以下条件：
   - Si 和 Mg 的值在 [0, 0.012] 范围内
   - Si + Mg ≤ 0.012
   - Mg + Si + Al = 1（三元成分归一化）

### 运行脚本

1. 将 Excel 数据文件（`深度.xlsx`）放置于项目目录中
2. 运行主脚本：
```bash
python gibbs_triangle_heatmap.py
```

### 输出结果

脚本会生成两个文件：
- `gibbs_triangle_heatmap.pdf` - PDF格式（矢量图）
- `gibbs_triangle_heatmap.png` - PNG格式（位图，300 DPI）

**注意**：输出的图片会自动裁剪为右上方的区域，只包含三角形热图和颜色条。

### 三角形布局

- **Al（铝）**：左下角顶点
- **Mg（镁）**：右下角顶点
- **Si（硅）**：顶部顶点

热图显示的是深度值在成分空间中的分布，颜色越深表示深度值越大。


## 其他方法
使用origin软件绘制，其具体操作步骤详见谭春林的《Origin科研绘图与学术图表绘制从入门到精通》（ISBN : 978-7-301-34049-3），其具体项目文件见本项目“origin”文件夹，其结果示意图如下：

![深度](https://github.com/user-attachments/assets/3468c2a1-0b1c-437b-bf69-03eb4bf0253e)

## 许可
本项目采用 MIT License 许可协议。

## 联系
如果你有任何问题或建议，请通过1786888479@qq.com 联系我们。

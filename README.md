# GTCP (Gibbs Triangle Cloud Plotter)

GTCP 是一个将二维合金成分与其他物化性质关系绘制在吉布斯三角坐标中的工具。通过高斯核密度估计和密度图生成，GTCP 提供了一种直观的方式来展示数据的分布及其相关性。最终的吉布斯三角云图经过 Adobe Illustrator 的后期处理，以确保图像的清晰和美观。

## 功能

- 从 Excel 文件中加载和处理数据
- 使用高斯核密度估计对数据进行平滑处理
- 生成吉布斯三角图并计算密度
- 添加颜色条以表示数据密度
- 通过 Adobe Illustrator 进行后期处理和美化

## 安装

请确保安装以下必要的 Python 库：
```bash
pip install pandas matplotlib numpy scipy ternary
```

## 使用说明
### 数据准备

将包含合金成分及其他物化性质的数据保存为 Excel 文件。
确保数据列符合要求，仅保留横坐标和纵坐标均在 [0, 0.012] 范围内的数据。
### 运行脚本

将数据文件放置于项目目录中。
运行主脚本 Gibbs_Triangle_Cloud_Plotter.py 生成吉布斯三角图。

复制代码
```bash
python Gibbs_Triangle_Cloud_Plotter.py
```
### 查看结果

输出的图像将保存在项目目录中。你可以使用图像查看器查看结果，或者使用 Adobe Illustrator 进行进一步的后期处理。

## 示例
以下是生成的吉布斯三角云图示例：

![Gibbs_Triangle_Gaussian_Fit_Surface](https://github.com/user-attachments/assets/4831ff41-f0d5-4686-8ad5-ffff6d47b852)


## 其他方法
使用origin软件绘制，其具体操作步骤详见谭春林的《Origin科研绘图与学术图表绘制从入门到精通》（ISBN : 978-7-301-34049-3），其具体项目文件见本项目“origin”文件夹，其结果示意图如下：

![深度](https://github.com/user-attachments/assets/3468c2a1-0b1c-437b-bf69-03eb4bf0253e)

## 许可
本项目采用 MIT License 许可协议。

## 联系
如果你有任何问题或建议，请通过1786888479@qq.com 联系我们。

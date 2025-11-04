import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.tri as tri

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 读取Excel文件
df = pd.read_excel('深度.xlsx')

# 提取数据
# 第一列：Mg（x轴相关）
# 第二列：Si（y轴相关）
# 第三列：Al
# 第四列：depth（z轴，用于颜色映射）
Mg = df.iloc[:, 0].values
Si = df.iloc[:, 1].values
Al = df.iloc[:, 2].values
depth = df.iloc[:, 3].values

# 过滤数据：只保留Si和Mg在0~0.012范围，且Si+Mg <= 0.012的数据
filter_mask = (Si >= 0) & (Si <= 0.012) & (Mg >= 0) & (Mg <= 0.012) & ((Si + Mg) <= 0.012)
Mg_filtered = Mg[filter_mask]
Si_filtered = Si[filter_mask]
Al_filtered = Al[filter_mask]
depth_filtered = depth[filter_mask]

print(f"\n原始数据点数量: {len(Mg)}")
print(f"过滤后数据点数量: {len(Mg_filtered)}")
print(f"\n过滤条件: Si在[0, 0.012], Mg在[0, 0.012], 且Si+Mg <= 0.012")
print("\n过滤后的数据点（前10个）:")
for i in range(min(10, len(Mg_filtered))):
    print(f"点{i}: Mg={Mg_filtered[i]:.6f}, Si={Si_filtered[i]:.6f}, Al={Al_filtered[i]:.6f}, Depth={depth_filtered[i]:.2f}")

# 使用过滤后的数据
Mg = Mg_filtered
Si = Si_filtered
Al = Al_filtered
depth = depth_filtered

# 将三元坐标转换为笛卡尔坐标用于绘图
# 吉布斯三角形：等边三角形，Al在左下角，Mg和Si互换位置
def ternary_to_cartesian(mg, si, al):
    """
    将三元坐标(Mg, Si, Al)转换为笛卡尔坐标
    三角形顶点：
    - Al顶点: (0, 0) - 左下角
    - Mg顶点: (1, 0) - 右下角
    - Si顶点: (0.5, sqrt(3)/2) - 顶部
    """
    x = mg + 0.5 * si
    y = (np.sqrt(3) / 2) * si
    return x, y

# 转换所有点到笛卡尔坐标
x_cart, y_cart = ternary_to_cartesian(Mg, Si, Al)

# 创建三角网格用于插值
triang = tri.Triangulation(x_cart, y_cart)

# 创建更精细的网格用于平滑热图
# 只显示Si和Mg在0-0.012范围内的小三角形区域
# 计算这个小区域的边界
# 当Si=0, Mg=0时，Al=1，在Al顶点(0,0)
# 当Si=0.012, Mg=0时，在Al-Si边上（Si在顶部）
# 当Si=0, Mg=0.012时，在Al-Mg边上（Mg在右下角）
# 当Si+Mg=0.012时，形成边界

# 计算边界点
boundary_si = np.linspace(0, 0.012, 100)
boundary_mg = 0.012 - boundary_si
boundary_al = 1 - boundary_si - boundary_mg
boundary_x, boundary_y = ternary_to_cartesian(boundary_mg, boundary_si, boundary_al)

# 计算显示范围（包含这个小区域）
x_min = 0  # Al顶点
x_max = boundary_x.max()
y_min = 0  # Al顶点
y_max = boundary_y.max()

# 添加一些边距
x_margin = (x_max - x_min) * 0.1
y_margin = (y_max - y_min) * 0.1
x_min -= x_margin
x_max += x_margin
y_min -= y_margin
y_max += y_margin

# 创建更精细的网格（只覆盖0-0.012范围）
n_points = 200
x_range = np.linspace(max(0, x_min), x_max, n_points)
y_range = np.linspace(max(0, y_min), y_max, n_points)
X, Y = np.meshgrid(x_range, y_range)

# 将网格点转换回三元坐标
def cartesian_to_ternary(x, y):
    """
    将笛卡尔坐标转换回三元坐标
    Al在左下角，Mg在右下角，Si在顶部
    """
    si = 2 * y / np.sqrt(3)
    mg = x - 0.5 * si
    al = 1 - si - mg
    return mg, si, al

# 创建插值网格
points = np.column_stack([x_cart, y_cart])
from scipy.interpolate import griddata

# 在网格上插值depth值
Z = griddata(points, depth, (X, Y), method='cubic', fill_value=np.nan)

# 创建图形
fig, ax = plt.subplots(figsize=(10, 10))

# 绘制小三角形区域的边框（Si+Mg=0.012的边界）
# 计算边界点
boundary_si_plot = np.linspace(0, 0.012, 100)
boundary_mg_plot = 0.012 - boundary_si_plot
boundary_al_plot = 1 - boundary_si_plot - boundary_mg_plot
boundary_x_plot, boundary_y_plot = ternary_to_cartesian(boundary_mg_plot, boundary_si_plot, boundary_al_plot)

# 绘制边界线（作为小三角形的边框）
ax.plot(boundary_x_plot, boundary_y_plot, 'k-', linewidth=2, label='Si+Mg=0.012')

# 绘制Al顶点到边界的线（形成小三角形）
# Al顶点到Si=0.012, Mg=0的点（现在Si在顶部）
x_al_si, y_al_si = ternary_to_cartesian(0, 0.012, 1-0.012)
ax.plot([0, x_al_si], [0, y_al_si], 'k-', linewidth=2)

# Al顶点到Si=0, Mg=0.012的点（现在Mg在右下角）
x_al_mg, y_al_mg = ternary_to_cartesian(0.012, 0, 1-0.012)
ax.plot([0, x_al_mg], [0, y_al_mg], 'k-', linewidth=2)

# 绘制标签（Al在左下角，Si在顶部，Mg在右下角）
ax.text(-0.05, -0.05, 'Al', fontsize=14, ha='right', va='top', weight='bold')
ax.text(x_al_si - 0.01, y_al_si + 0.01, 'Si', fontsize=14, ha='right', va='bottom', weight='bold')
ax.text(x_al_mg + 0.01, y_al_mg, 'Mg', fontsize=14, ha='left', va='center', weight='bold')

# 绘制网格线（在0-0.012范围内）
# 绘制Si的等值线（从Al顶点到边界）
for i in range(1, 6):
    si_val = i * 0.002  # 0.002, 0.004, 0.006, 0.008, 0.010
    if si_val <= 0.012:
        # 从Al顶点到边界上的点
        mg_val = 0.012 - si_val
        al_val = 1 - si_val - mg_val
        x_end, y_end = ternary_to_cartesian(mg_val, si_val, al_val)
        ax.plot([0, x_end], [0, y_end], 'k--', alpha=0.3, linewidth=0.5)
        
# 绘制Mg的等值线（从Al顶点到边界）
for i in range(1, 6):
    mg_val = i * 0.002  # 0.002, 0.004, 0.006, 0.008, 0.010
    if mg_val <= 0.012:
        # 从Al顶点到边界上的点
        si_val = 0.012 - mg_val
        al_val = 1 - si_val - mg_val
        x_end, y_end = ternary_to_cartesian(mg_val, si_val, al_val)
        ax.plot([0, x_end], [0, y_end], 'k--', alpha=0.3, linewidth=0.5)

# 绘制热图
# 创建掩码：只显示Si+Mg<=0.012的区域
mask = np.zeros_like(X, dtype=bool)
for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        # 转换回三元坐标
        mg_temp, si_temp, al_temp = cartesian_to_ternary(X[i, j], Y[i, j])
        # 检查Si+Mg是否<=0.012，且所有值都非负
        if si_temp + mg_temp > 0.012 or si_temp < 0 or mg_temp < 0 or al_temp < 0:
            mask[i, j] = True  # 掩码掉不满足条件的点

# 应用掩码
Z_masked = np.ma.masked_array(Z, mask=mask)

# 绘制等高线填充图
contour = ax.contourf(X, Y, Z_masked, levels=50, cmap='viridis', alpha=0.8)
contour_lines = ax.contour(X, Y, Z_masked, levels=20, colors='black', alpha=0.3, linewidths=0.5)

# Si+Mg=0.012的边界线已经在上面绘制了

# 绘制原始数据点
scatter = ax.scatter(x_cart, y_cart, c=depth, s=100, cmap='viridis', 
                     edgecolors='black', linewidths=1.5, zorder=5)

# 添加颜色条（竖直方向，放在图的右侧，缩短长度）
cbar = plt.colorbar(contour, ax=ax, orientation='vertical', pad=0.1, location='right', shrink=0.7)
# 设置标签在上方，增大字体
cbar.set_label('Depth ', fontsize=16, rotation=0, labelpad=-45, va='top')
# 调整标签位置到上方
cbar.ax.yaxis.label.set_position((0.5, 1.15))
# 增大图例刻度字体大小
cbar.ax.tick_params(labelsize=12)

# 设置坐标轴范围，只显示0-0.012范围的小区域
ax.set_xlim(x_min, x_max)
ax.set_ylim(y_min, y_max)
ax.set_aspect('equal')
ax.axis('off')

plt.tight_layout()
# 保存PDF格式
plt.savefig('gibbs_triangle_heatmap.pdf', bbox_inches='tight', pad_inches=0.5, 
            facecolor='white', edgecolor='none', format='pdf', dpi=300)
print("\n热图已保存为: gibbs_triangle_heatmap.pdf")

# 同时保存PNG格式
plt.savefig('gibbs_triangle_heatmap.png', bbox_inches='tight', pad_inches=0.5, 
            facecolor='white', edgecolor='none', format='png', dpi=300)
print("热图已保存为: gibbs_triangle_heatmap.png")

plt.show()


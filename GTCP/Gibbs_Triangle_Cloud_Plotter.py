import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import ternary
from matplotlib.backends.backend_pdf import PdfPages
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import rcParams

# 设置字体以支持中文字符
rcParams['font.sans-serif'] = ['SimHei']  # 可根据系统安装的中文字体进行设置
rcParams['axes.unicode_minus'] = False  # 确保负号可以正常显示

# Load the Excel file
file_path = '深度.xlsx'
df = pd.read_excel(file_path)

# Extract the relevant columns
Mg = df.iloc[:, 0]
Si = df.iloc[:, 1]
Al = df.iloc[:, 2]
depth = df.iloc[:, 3]

# Apply Gaussian smoothing to the relevant range
mask = (Si >= 0) & (Si <= 0.012) & (Mg >= 0) & (Mg <= 0.012) & ((Si + Mg) <= 0.012)
Si_filtered = Si[mask]
Mg_filtered = Mg[mask]
Al_filtered = Al[mask]
depth_filtered = depth[mask]

# Debug: Print the size of filtered data
print(f"Filtered Si data size: {Si_filtered.size}")
print(f"Filtered Mg data size: {Mg_filtered.size}")
print(f"Filtered Al data size: {Al_filtered.size}")
print(f"Filtered depth data size: {depth_filtered.size}")

# Check if the filtered data is not empty
if Si_filtered.size == 0 or Mg_filtered.size == 0 or Al_filtered.size == 0 or depth_filtered.size == 0:
    raise ValueError("Filtered data is empty. Please check the input data and filter conditions.")

# Apply Gaussian smoothing
Si_smooth = gaussian_filter(Si_filtered, sigma=1)
Mg_smooth = gaussian_filter(Mg_filtered, sigma=1)
Al_smooth = gaussian_filter(Al_filtered, sigma=1)
depth_smooth = gaussian_filter(depth_filtered, sigma=1)

# Convert to Gibbs triangle coordinates
def to_gibbs_triangle(x, y, z):
    s = x + y + z
    return x / s, y / s, z / s

gibbs_x, gibbs_y, gibbs_z = to_gibbs_triangle(Si_smooth, Mg_smooth, Al_smooth)

# Debug: Print some sample values to check the transformation
print(f"Gibbs X sample: {gibbs_x[:5]}")
print(f"Gibbs Y sample: {gibbs_y[:5]}")
print(f"Gibbs Z sample: {gibbs_z[:5]}")

# Filter the coordinates within the range 0-0.012
gibbs_mask = (gibbs_x >= 0) & (gibbs_x <= 0.012) & (gibbs_y >= 0) & (gibbs_y <= 0.012)
gibbs_x_filtered = gibbs_x[gibbs_mask]
gibbs_y_filtered = gibbs_y[gibbs_mask]
depth_filtered = depth_smooth[gibbs_mask]

# Debug: Print the size of filtered Gibbs data
print(f"Filtered Gibbs X data size: {gibbs_x_filtered.size}")
print(f"Filtered Gibbs Y data size: {gibbs_y_filtered.size}")
print(f"Filtered depth data size: {depth_filtered.size}")

# Check if the filtered data is not empty after Gibbs transformation
if gibbs_x_filtered.size == 0 or gibbs_y_filtered.size == 0 or depth_filtered.size == 0:
    raise ValueError("Filtered Gibbs data is empty. Please check the input data and filter conditions.")

# Simple scatter plot to check data distribution
plt.scatter(gibbs_x_filtered, gibbs_y_filtered, c=depth_filtered, cmap='viridis', alpha=0.6)
plt.colorbar(label='深度')
plt.xlabel('Gibbs X')
plt.ylabel('Gibbs Y')
plt.title('Filtered Data Scatter Plot')
plt.show()

# Plotting a 2D histogram to visualize data distribution
plt.hist2d(gibbs_x_filtered, gibbs_y_filtered, bins=[50, 50], cmap='viridis')
plt.colorbar(label='Count')
plt.xlabel('Gibbs X')
plt.ylabel('Gibbs Y')
plt.title('2D Histogram of Filtered Data')
plt.show()

# Simplified function to fit a Gaussian
def gaussian_2d(data, amp, x0, y0, sigma_x, sigma_y):
    x, y = data
    x0 = float(x0)
    y0 = float(y0)
    a = 1 / (2 * sigma_x**2)
    c = 1 / (2 * sigma_y**2)
    g = amp * np.exp(- (a * ((x - x0) ** 2) + c * ((y - y0) ** 2)))
    return g.ravel()

# Adjusted initial guess for the parameters
initial_guess = (np.max(depth_filtered), 0.006, 0.006, 0.001, 0.001)

# Create grid for fitting
xdata = np.vstack((gibbs_x_filtered, gibbs_y_filtered))
ydata = depth_filtered

# Fit the Gaussian model with increased maxfev
try:
    popt, pcov = curve_fit(gaussian_2d, xdata, ydata, p0=initial_guess, maxfev=100000)
except RuntimeError as e:
    print(f"Fit did not converge: {e}")
    raise

# Create a grid to evaluate the fit
x_fit = np.linspace(0, 0.012, 100)
y_fit = np.linspace(0, 0.012, 100)
x_fit, y_fit = np.meshgrid(x_fit, y_fit)
z_fit = gaussian_2d((x_fit, y_fit), *popt).reshape(x_fit.shape)

# Plotting the data and the Gaussian fit in Gibbs triangle coordinates
fig, ax = plt.subplots(figsize=(10, 8))
fig, tax = ternary.figure(ax=ax)

# Set axes labels and ticks
tax.boundary(linewidth=1.5)
tax.gridlines(multiple=0.001, color="grey")
fontsize = 12
tax.set_title("高斯拟合的吉布斯三角坐标曲面投影", fontsize=fontsize)
tax.left_axis_label("Si 含量", fontsize=fontsize)
tax.right_axis_label("Mg 含量", fontsize=fontsize)
tax.bottom_axis_label("Al 含量", fontsize=fontsize)
tax.ticks(axis='lbr', linewidth=1, multiple=0.001)

# Plot the points and the Gaussian fit
tax.scatter(np.vstack((gibbs_x_filtered, gibbs_y_filtered)).T, c=depth_filtered, cmap='viridis', alpha=0.6)

# 设置坐标轴范围
ax.set_xlim(0, 0.012)
ax.set_ylim(0, 0.012)

# 绘制等高线
contour = ax.contourf(x_fit, y_fit, z_fit, levels=100, cmap='viridis', alpha=0.6)

# Add colorbar
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1)
cbar = plt.colorbar(contour, cax=cax)
cbar.set_label('深度')

# Save the plot to a PDF
with PdfPages('Gibbs_Triangle_Gaussian_Fit_Surface.pdf') as pdf:
    pdf.savefig(fig)
    plt.show()

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
import matplotlib.patheffects as path_effects

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'SimHei', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

# 1. 模型参数与训练能耗增长曲线
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('AI Model Scale vs Energy Consumption\n模型规模与能耗增长趋势', 
             fontsize=18, fontweight='bold', y=0.98)

# 数据
models = ['BERT-Large\n(2018)', 'GPT-2\n(2019)', 'GPT-3\n(2020)', 'Gopher\n(2021)', 
          'GPT-4\n(2023)', 'Gemini Ultra\n(2024)']
params = [0.34, 1.5, 175, 280, 1800, 2000]  # 参数量（亿）
energy = [0.6, 5, 130, 430, 12000, 20000]  # 能耗（万度）

# 左图：参数量增长
ax1.set_yscale('log')
bars1 = ax1.bar(models, params, color=['#3498db', '#2980b9', '#e74c3c', '#c0392b', '#9b59b6', '#8e44ad'], 
                edgecolor='black', linewidth=1.5)
ax1.set_ylabel('Parameters (Billions)\n参数量（亿）', fontsize=12, fontweight='bold')
ax1.set_xlabel('Model / Year', fontsize=12, fontweight='bold')
ax1.set_title('Model Parameter Growth\n模型参数增长（对数尺度）', fontsize=14, fontweight='bold')
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# 在柱状图上添加数值
for i, (bar, param) in enumerate(zip(bars1, params)):
    height = bar.get_height()
    if param >= 100:
        label = f'{param:.0f}B'
    else:
        label = f'{param:.1f}B'
    ax1.text(bar.get_x() + bar.get_width()/2., height,
             label, ha='center', va='bottom', fontsize=10, fontweight='bold')

# 右图：能耗增长
ax2.set_yscale('log')
bars2 = ax2.bar(models, energy, color=['#27ae60', '#229954', '#f39c12', '#e67e22', '#e74c3c', '#c0392b'],
                edgecolor='black', linewidth=1.5)
ax2.set_ylabel('Training Energy (10k kWh)\n训练能耗（万度）', fontsize=12, fontweight='bold')
ax2.set_xlabel('Model / Year', fontsize=12, fontweight='bold')
ax2.set_title('Training Energy Consumption\n训练能耗增长（对数尺度）', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# 在柱状图上添加数值
for i, (bar, en) in enumerate(zip(bars2, energy)):
    height = bar.get_height()
    if en >= 1000:
        label = f'{en/10000:.1f}亿'
    else:
        label = f'{en:.0f}万'
    ax2.text(bar.get_x() + bar.get_width()/2., height,
             label, ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('chapter-04-fig-01-model-energy-growth.png', dpi=300, bbox_inches='tight', 
            facecolor='white', edgecolor='none')
plt.close()

# 2. AI能耗增长预测 vs 全球电力供应
fig, ax = plt.subplots(figsize=(14, 8))

# 年份
years = np.array([2020, 2022, 2024, 2026, 2028, 2030])

# AI训练能耗预测（TWh）
ai_energy = np.array([2, 8, 20, 50, 100, 200])  # 太瓦时

# 全球电力供应（TWh）- 约27,000 TWh每年，假设年增长2%
global_energy = 27000 * (1.02 ** (years - 2020))

# AI占全球电力比例
percentage = (ai_energy / global_energy) * 100

# 创建组合图
ax2 = ax.twinx()

# 柱状图 - AI能耗
bars = ax.bar(years - 0.2, ai_energy, width=0.4, color='#e74c3c', alpha=0.8,
              label='AI Training Energy (TWh)', edgecolor='black', linewidth=1.5)

# 折线图 - 占比
line = ax2.plot(years, percentage, 'bo-', linewidth=3, markersize=10,
                label='AI Energy % of Global', color='#3498db')

# 添加警戒线
ax2.axhline(y=1.0, color='orange', linestyle='--', linewidth=2, label='1% Threshold')
ax2.axhline(y=3.0, color='red', linestyle='--', linewidth=2, label='3% Threshold')

# 填充预警区域
ax2.fill_between(years, 1, 3, alpha=0.2, color='orange', label='Warning Zone')
ax2.fill_between(years, 3, 10, alpha=0.2, color='red', label='Critical Zone')

# 标注关键点
ax.annotate('Current\n(~20 TWh)', xy=(2024, 20), xytext=(2022.5, 80),
            arrowprops=dict(arrowstyle='->', color='black', lw=2),
            fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.8))

ax.annotate('Projected 2030\n(~200 TWh, 0.7%)', xy=(2030, 200), xytext=(2028.5, 150),
            arrowprops=dict(arrowstyle='->', color='black', lw=2),
            fontsize=11, fontweight='bold', ha='center',
            bbox=dict(boxstyle='round,pad=0.5', facecolor='lightcoral', alpha=0.8))

ax.set_xlabel('Year', fontsize=13, fontweight='bold')
ax.set_ylabel('AI Training Energy (TWh)\nAI训练能耗（太瓦时）', fontsize=13, fontweight='bold', color='#e74c3c')
ax2.set_ylabel('Percentage of Global Electricity (%)\n占全球电力比例（%）', fontsize=13, fontweight='bold', color='#3498db')

ax.set_title('AI Energy Consumption Projection vs Global Electricity Supply\nAI能耗增长预测 vs 全球电力供应', 
             fontsize=16, fontweight='bold', pad=20)

ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years])
ax.set_ylim(0, 250)
ax2.set_ylim(0, 5)

# 合并图例
lines1, labels1 = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=10)

ax.grid(axis='y', alpha=0.3, linestyle='--')
plt.tight_layout()
plt.savefig('chapter-04-fig-02-energy-projection.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("✅ 图2完成：AI能耗增长预测 vs 全球电力供应")

# 3. 智算中心电力架构图
fig, ax = plt.subplots(figsize=(16, 10))
ax.set_xlim(0, 16)
ax.set_ylim(0, 10)
ax.axis('off')

# 标题
title = ax.text(8, 9.5, 'AI Data Center Power Architecture\n智算中心电力架构', 
                ha='center', fontsize=20, fontweight='bold')
title.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])

# 颜色定义
color_grid = '#e74c3c'
color_ups = '#f39c12'
color_hvdc = '#9b59b6'
color_server = '#3498db'
color_gpu = '#2ecc71'
color_cooling = '#1abc9c'

# 1. 电网接入
grid_box = FancyBboxPatch((0.5, 7), 2, 1.2, boxstyle="round,pad=0.1", 
                          facecolor=color_grid, edgecolor='black', linewidth=2)
ax.add_patch(grid_box)
ax.text(1.5, 7.6, 'Power Grid\n电网接入', ha='center', va='center', 
        fontsize=11, fontweight='bold', color='white')

# 2. 变电站
sub_box = FancyBboxPatch((4, 7), 2.5, 1.2, boxstyle="round,pad=0.1",
                         facecolor='#34495e', edgecolor='black', linewidth=2)
ax.add_patch(sub_box)
ax.text(5.25, 7.6, 'Substation\n变电站\n(110kV→10kV)', ha='center', va='center',
        fontsize=10, fontweight='bold', color='white')

# 3. 传统UPS方案（左侧）
ax.text(3, 5.8, 'Traditional AC UPS', fontsize=12, fontweight='bold', style='italic')

ups_box = FancyBboxPatch((1, 4), 2.5, 1.2, boxstyle="round,pad=0.1",
                         facecolor=color_ups, edgecolor='black', linewidth=2)
ax.add_patch(ups_box)
ax.text(2.25, 4.6, 'AC UPS\n交流不间断电源\n~95%效率', ha='center', va='center',
        fontsize=9, fontweight='bold', color='white')

# 4. HVDC方案（右侧）
ax.text(9, 5.8, 'Modern HVDC (Recommended)', fontsize=12, fontweight='bold', style='italic', color=color_hvdc)

hvdc_box = FancyBboxPatch((7.5, 4), 3, 1.2, boxstyle="round,pad=0.1",
                          facecolor=color_hvdc, edgecolor='black', linewidth=2)
ax.add_patch(hvdc_box)
ax.text(9, 4.6, 'HVDC\n高压直流\n~98%效率', ha='center', va='center',
        fontsize=10, fontweight='bold', color='white')

# 5. 服务器机柜
server_box = FancyBboxPatch((6, 1.5), 4, 1.8, boxstyle="round,pad=0.1",
                            facecolor=color_server, edgecolor='black', linewidth=2)
ax.add_patch(server_box)
ax.text(8, 2.8, 'Server Racks', ha='center', fontsize=11, fontweight='bold', color='white')
ax.text(8, 2.2, 'PSU: AC→DC conversion', ha='center', fontsize=9, color='white')
ax.text(8, 1.8, 'Loss: ~5%', ha='center', fontsize=9, color='white')

# 6. GPU集群
gpu_box = FancyBboxPatch((11, 1.5), 4, 1.8, boxstyle="round,pad=0.1",
                         facecolor=color_gpu, edgecolor='black', linewidth=2)
ax.add_patch(gpu_box)
ax.text(13, 2.8, 'GPU Cluster', ha='center', fontsize=11, fontweight='bold', color='white')
ax.text(13, 2.2, 'H100 × 1024', ha='center', fontsize=10, color='white')
ax.text(13, 1.8, '~700kW', ha='center', fontsize=10, fontweight='bold', color='white')

# 7. 散热系统
cooling_box = FancyBboxPatch((1, 1.5), 3.5, 1.8, boxstyle="round,pad=0.1",
                             facecolor=color_cooling, edgecolor='black', linewidth=2)
ax.add_patch(cooling_box)
ax.text(2.75, 2.8, 'Cooling System', ha='center', fontsize=11, fontweight='bold', color='white')
ax.text(2.75, 2.2, 'Liquid Cooling + CDU', ha='center', fontsize=9, color='white')
ax.text(2.75, 1.8, '~120kW (11%)', ha='center', fontsize=9, color='white')

# 绘制连接线和箭头
arrow_props = dict(arrowstyle='->', lw=2.5, color='black')

# 电网到变电站
ax.annotate('', xy=(4, 7.6), xytext=(2.5, 7.6), arrowprops=arrow_props)

# 变电站分两支
ax.annotate('', xy=(2.25, 6.5), xytext=(5.25, 7), arrowprops=arrow_props)
ax.annotate('', xy=(9, 5.2), xytext=(5.25, 7), arrowprops=arrow_props)

# UPS和HVDC到服务器
ax.annotate('', xy=(6, 2.4), xytext=(3.5, 4), arrowprops=arrow_props)
ax.annotate('', xy=(6, 2.4), xytext=(9, 4), arrowprops=arrow_props)

# 服务器到GPU
ax.annotate('', xy=(11, 2.4), xytext=(10, 2.4), arrowprops=arrow_props)

# 效率对比标注
ax.text(2.25, 3.3, 'Total: ~90%', ha='center', fontsize=10, 
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
ax.text(9, 3.3, 'Total: ~95%', ha='center', fontsize=10, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))

# 添加图例说明
legend_text = """
Key Components:
• Grid: High-voltage power transmission
• Substation: Voltage transformation (110kV→10kV)
• UPS/HVDC: Power backup and conversion
• Servers: Computing infrastructure
• GPUs: AI training accelerators
• Cooling: Thermal management system
"""
ax.text(0.5, 0.3, legend_text, fontsize=8, verticalalignment='top',
        bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.5))

plt.tight_layout()
plt.savefig('chapter-04-fig-03-power-architecture.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("✅ 图3完成：智算中心电力架构图")

# 4. 封面图 - AI能耗可视化
fig, ax = plt.subplots(figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')

# 背景渐变效果
gradient = np.linspace(0, 1, 256).reshape(1, -1)
ax.imshow(gradient, aspect='auto', extent=[0, 16, 0, 9], 
          cmap='Blues', alpha=0.3, zorder=0)

# 主标题
main_title = ax.text(8, 7.5, 'Chapter 4', fontsize=48, fontweight='bold',
                     ha='center', color='#2c3e50')
main_title.set_path_effects([path_effects.withStroke(linewidth=4, foreground='white')])

subtitle = ax.text(8, 6.5, 'The Power Challenge', fontsize=36, fontweight='bold',
                   ha='center', color='#e74c3c', style='italic')
subtitle.set_path_effects([path_effects.withStroke(linewidth=3, foreground='white')])

chinese_title = ax.text(8, 5.5, '电力挑战：AI训练的能源困境', fontsize=28,
                        ha='center', color='#34495e', fontweight='bold')

# 核心数据展示
# 大数字展示
ax.text(4, 3.5, '1.2亿', fontsize=64, fontweight='bold', ha='center', color='#e74c3c')
ax.text(4, 2.8, '度电', fontsize=24, ha='center', color='#2c3e50')
ax.text(4, 2.2, 'GPT-4训练耗电', fontsize=14, ha='center', color='#7f8c8d')

ax.text(8, 3.5, '1.1MW', fontsize=64, fontweight='bold', ha='center', color='#f39c12')
ax.text(8, 2.8, '功率', fontsize=24, ha='center', color='#2c3e50')
ax.text(8, 2.2, '千卡集群功耗', fontsize=14, ha='center', color='#7f8c8d')

ax.text(12, 3.5, '200TWh', fontsize=64, fontweight='bold', ha='center', color='#9b59b6')
ax.text(12, 2.8, '/年', fontsize=24, ha='center', color='#2c3e50')
ax.text(12, 2.2, '2030年预测', fontsize=14, ha='center', color='#7f8c8d')

# 底部引用
quote = '"当一个智算中心的用电量相当于一座小城，\\n我们必须重新思考：AI的代价是什么？"'
ax.text(8, 1, quote, fontsize=14, ha='center', color='#7f8c8d', style='italic')

# 装饰元素 - 电力符号
# 闪电符号
bolt_x = [1.5, 2, 1.8, 2.3, 1.7, 2.2, 1.6]
bolt_y = [7, 6.5, 6.5, 5.5, 5.5, 4.5, 4.5]
ax.plot(bolt_x, bolt_y, 'y-', linewidth=4, solid_capstyle='round')
ax.plot(bolt_x, bolt_y, 'orange', linewidth=2, solid_capstyle='round')

# 右侧装饰
for i in range(5):
    circle = Circle((14, 7-i*0.8), 0.2, facecolor='#3498db', alpha=0.3+i*0.15)
    ax.add_patch(circle)

plt.tight_layout()
plt.savefig('chapter-04-cover.png', dpi=300, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("✅ 图4完成：第4章封面图")

print("\n🎉 所有配图生成完成！")
print("生成文件：")
print("  1. chapter-04-fig-01-model-energy-growth.png")
print("  2. chapter-04-fig-02-energy-projection.png")
print("  3. chapter-04-fig-03-power-architecture.png")
print("  4. chapter-04-cover.png")

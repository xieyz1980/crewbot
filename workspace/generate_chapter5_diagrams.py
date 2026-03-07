#!/usr/bin/env python3
"""
第5章 AI基础设施架构图生成脚本
Generate Chapter 5 AI Infrastructure Architecture Diagrams

包含以下图表:
1. AI基础设施整体架构图 (AI Infrastructure Overview)
2. 智算中心网络拓扑图 (AI Data Center Network Topology)  
3. GPU集群调度架构图 (GPU Cluster Scheduling Architecture)
4. AI训练流水线流程图 (AI Training Pipeline Flow)

技术栈: Python + matplotlib
输出: 300dpi 高清PNG
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, Circle, FancyArrowPatch, Polygon
import numpy as np

# ==================== 全局配置 ====================
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial Unicode MS', 'SimHei', 'WenQuanYi Zen Hei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300

# 统一配色方案 - 专业科技风格
colors = {
    'primary': '#2563EB',      # 主色 - 科技蓝
    'secondary': '#3B82F6',    # 次要色
    'accent': '#60A5FA',       # 强调色
    'dark': '#1E40AF',         # 深色
    'light': '#DBEAFE',        # 浅色
    'text': '#1F2937',         # 文字色
    'bg': '#F8FAFC',           # 背景色
    'success': '#10B981',      # 成功绿
    'warning': '#F59E0B',      # 警告橙
    'danger': '#EF4444',       # 危险红
    'purple': '#8B5CF6',       # 紫色
    'teal': '#14B8A6',         # 青色
    'pink': '#EC4899',         # 粉色
    'gray': '#6B7280',         # 灰色
}

OUTPUT_DIR = '/workspace/projects/books/智算基石/images'

def save_figure(fig, filename):
    """保存图表到指定目录"""
    filepath = f"{OUTPUT_DIR}/{filename}"
    fig.savefig(filepath, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"✅ Generated: {filename}")

# ==================== 图1: AI基础设施整体架构图 ====================
def create_ai_infrastructure_overview():
    """AI基础设施整体架构图 - 分层架构视图"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.set_facecolor(colors['bg'])
    
    # 标题
    ax.text(50, 97, 'AI Infrastructure Architecture Overview', 
            fontsize=18, fontweight='bold', ha='center', va='top', color=colors['text'])
    ax.text(50, 93, 'AI基础设施整体架构图', fontsize=13, ha='center', va='top', color=colors['gray'])
    
    # ===== 第5层：应用服务层 =====
    app_box = FancyBboxPatch((3, 82), 94, 10, boxstyle="round,pad=0.02,rounding_size=0.5",
                              facecolor='#FCE7F3', edgecolor=colors['pink'], linewidth=2)
    ax.add_patch(app_box)
    ax.text(50, 88.5, '🚀 Application Services / 应用服务层', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=colors['pink'])
    
    app_items = ['LLM Services', 'Computer Vision', 'MLOps Platform', 'AI APIs', 'Model Hub']
    for i, item in enumerate(app_items):
        x = 12 + i * 16
        box = FancyBboxPatch((x-6, 83), 12, 4, boxstyle="round,pad=0.01,rounding_size=0.2",
                             facecolor='white', edgecolor=colors['pink'], linewidth=1)
        ax.add_patch(box)
        ax.text(x, 85, item, fontsize=8, ha='center', va='center', color=colors['text'])
    
    # ===== 第4层：AI平台层 =====
    platform_box = FancyBboxPatch((3, 67), 94, 13, boxstyle="round,pad=0.02,rounding_size=0.5",
                                   facecolor='#E0E7FF', edgecolor=colors['purple'], linewidth=2)
    ax.add_patch(platform_box)
    ax.text(50, 77.5, '🤖 AI Platform / AI平台层', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=colors['purple'])
    
    platform_items = [
        ('Model Training', 15, 72), ('Model Inference', 32, 72), 
        ('AutoML', 49, 72), ('Experiment Tracking', 66, 72), ('Model Registry', 83, 72),
        ('Distributed Training', 23, 68), ('Serving Framework', 43, 68),
        ('Pipeline Orchestration', 63, 68), ('Monitoring', 80, 68)
    ]
    for name, x, y in platform_items:
        box = FancyBboxPatch((x-7, y-1.5), 14, 3, boxstyle="round,pad=0.01,rounding_size=0.2",
                             facecolor='white', edgecolor=colors['purple'], linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, name, fontsize=7, ha='center', va='center', color=colors['text'])
    
    # ===== 第3层：资源编排层 =====
    orch_box = FancyBboxPatch((3, 52), 94, 13, boxstyle="round,pad=0.02,rounding_size=0.5",
                               facecolor='#D1FAE5', edgecolor=colors['success'], linewidth=2)
    ax.add_patch(orch_box)
    ax.text(50, 62.5, '⚙️ Resource Orchestration / 资源编排层', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=colors['success'])
    
    orch_items = [
        ('Kubernetes', 15, 57), ('Slurm', 32, 57), ('YARN', 49, 57),
        ('Volcano', 66, 57), ('Ray', 83, 57),
        ('GPU Scheduler', 23, 54), ('Job Queue', 43, 54),
        ('Resource Monitor', 63, 54), ('Auto-scaling', 80, 54)
    ]
    for name, x, y in orch_items:
        box = FancyBboxPatch((x-7, y-1.2), 14, 2.4, boxstyle="round,pad=0.01,rounding_size=0.2",
                             facecolor='white', edgecolor=colors['success'], linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, name, fontsize=7, ha='center', va='center', color=colors['text'])
    
    # ===== 第2层：基础设施层 =====
    infra_box = FancyBboxPatch((3, 30), 94, 20, boxstyle="round,pad=0.02,rounding_size=0.5",
                                facecolor='#DBEAFE', edgecolor=colors['primary'], linewidth=2)
    ax.add_patch(infra_box)
    ax.text(50, 47.5, '💻 Infrastructure / 基础设施层', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=colors['primary'])
    
    # 计算资源
    compute_box = FancyBboxPatch((6, 41), 28, 5, boxstyle="round,pad=0.01,rounding_size=0.3",
                                  facecolor=colors['primary'], edgecolor='white', linewidth=1.5, alpha=0.9)
    ax.add_patch(compute_box)
    ax.text(20, 44.5, 'Compute', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    ax.text(20, 42.5, 'GPU Clusters | CPU Nodes', fontsize=7, ha='center', va='center', color='#E0F2FE')
    
    # 网络资源
    network_box = FancyBboxPatch((36, 41), 28, 5, boxstyle="round,pad=0.01,rounding_size=0.3",
                                  facecolor=colors['secondary'], edgecolor='white', linewidth=1.5, alpha=0.9)
    ax.add_patch(network_box)
    ax.text(50, 44.5, 'Network', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    ax.text(50, 42.5, 'InfiniBand | RoCE | Ethernet', fontsize=7, ha='center', va='center', color='#E0F2FE')
    
    # 存储资源
    storage_box = FancyBboxPatch((66, 41), 28, 5, boxstyle="round,pad=0.01,rounding_size=0.3",
                                  facecolor=colors['accent'], edgecolor='white', linewidth=1.5, alpha=0.9)
    ax.add_patch(storage_box)
    ax.text(80, 44.5, 'Storage', fontsize=10, fontweight='bold', ha='center', va='center', color='white')
    ax.text(80, 42.5, 'NVMe | Parallel FS | Object', fontsize=7, ha='center', va='center', color='#E0F2FE')
    
    # 详细组件
    infra_details = [
        ('GPU Nodes\nH100/H800/A100', 12, 35),
        ('CPU Nodes\nIntel/AMD/ARM', 32, 35),
        ('NVSwitch\nNVLink 4.0', 52, 35),
        ('IB Switches\nNDR 400G', 72, 35),
        ('NVMe SSD\nHot Tier', 12, 32),
        ('Parallel FS\nLustre/GPFS', 32, 32),
        ('Object Store\nCeph/S3', 52, 32),
        ('Tape/Cloud\nArchive', 72, 32),
    ]
    for name, x, y in infra_details:
        box = FancyBboxPatch((x-7, y-1.5), 14, 3, boxstyle="round,pad=0.01,rounding_size=0.2",
                             facecolor='white', edgecolor=colors['primary'], linewidth=1, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y, name, fontsize=6, ha='center', va='center', color=colors['text'])
    
    # ===== 第1层：数据中心层 =====
    dc_box = FancyBboxPatch((3, 15), 94, 13, boxstyle="round,pad=0.02,rounding_size=0.5",
                             facecolor='#FEF3C7', edgecolor=colors['warning'], linewidth=2)
    ax.add_patch(dc_box)
    ax.text(50, 25.5, '🏢 Data Center / 数据中心层', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='#D97706')
    
    dc_items = [
        ('Power\nUPS/PDU', 12, 20), ('Cooling\nLiquid/Air', 28, 20),
        ('Security\nPhysical/Access', 44, 20), ('Network\nCore/Distribution', 60, 20),
        ('Facilities\nHVAC/Fire', 76, 20), ('Monitoring\nDCIM/BMS', 88, 20)
    ]
    for name, x, y in dc_items:
        box = FancyBboxPatch((x-6, y-3), 12, 6, boxstyle="round,pad=0.01,rounding_size=0.2",
                             facecolor='white', edgecolor=colors['warning'], linewidth=1)
        ax.add_patch(box)
        ax.text(x, y, name, fontsize=7, ha='center', va='center', color=colors['text'])
    
    # ===== 底部：基础设施服务 =====
    base_box = FancyBboxPatch((3, 3), 94, 10, boxstyle="round,pad=0.02,rounding_size=0.5",
                               facecolor='#E5E7EB', edgecolor=colors['gray'], linewidth=2)
    ax.add_patch(base_box)
    ax.text(50, 10.5, '🔧 Foundation Services / 基础服务', fontsize=11, fontweight='bold', 
            ha='center', va='center', color=colors['gray'])
    
    base_items = ['Identity & Access', 'Network Security', 'Data Protection', 'Compliance', 'Cost Management']
    for i, item in enumerate(base_items):
        x = 12 + i * 16
        box = FancyBboxPatch((x-6, 4.5), 12, 4, boxstyle="round,pad=0.01,rounding_size=0.2",
                             facecolor='white', edgecolor=colors['gray'], linewidth=1)
        ax.add_patch(box)
        ax.text(x, 6.5, item, fontsize=7, ha='center', va='center', color=colors['text'])
    
    # 层间连接箭头
    layer_y_positions = [82, 67, 52, 30, 15, 3]
    for i in range(len(layer_y_positions)-1):
        ax.annotate('', xy=(50, layer_y_positions[i+1] + 1), xytext=(50, layer_y_positions[i] - 0.5),
                    arrowprops=dict(arrowstyle='<->', color=colors['gray'], lw=1.5, alpha=0.6))
    
    # 图例
    ax.text(50, -1, '⬆ Northbound: User-facing Services | ⬇ Southbound: Physical Infrastructure',
            fontsize=8, ha='center', va='center', color=colors['gray'], style='italic')
    
    save_figure(fig, 'ch05-ai-infrastructure-overview.png')

# ==================== 图2: 智算中心网络拓扑图 ====================
def create_network_topology_diagram():
    """智算中心网络拓扑图 - Spine-Leaf架构"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 11), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.set_facecolor(colors['bg'])
    
    # 标题
    ax.text(50, 98, 'AI Data Center Network Topology', 
            fontsize=18, fontweight='bold', ha='center', va='top', color=colors['text'])
    ax.text(50, 94, '智算中心网络拓扑图 (Spine-Leaf架构)', fontsize=13, ha='center', va='top', color=colors['gray'])
    
    # ===== 核心层 (Spine) =====
    spine_y = 82
    ax.text(50, spine_y + 7, '🔷 Core Layer (Spine)', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='#7C3AED')
    
    spine_switches = [
        ('Spine-1', 20), ('Spine-2', 40), ('Spine-3', 60), ('Spine-4', 80)
    ]
    spine_positions = {}
    for name, x in spine_switches:
        # Spine交换机
        box = FancyBboxPatch((x-6, spine_y-3), 12, 6, boxstyle="round,pad=0.02,rounding_size=0.5",
                             facecolor='#7C3AED', edgecolor='white', linewidth=2)
        ax.add_patch(box)
        ax.text(x, spine_y, name, fontsize=9, fontweight='bold', ha='center', va='center', color='white')
        ax.text(x, spine_y-1.8, '800G', fontsize=7, ha='center', va='center', color='#DDD6FE')
        spine_positions[name] = (x, spine_y)
    
    # ===== 汇聚层 (Leaf) =====
    leaf_y = 60
    ax.text(50, leaf_y + 8, '🔶 Aggregation Layer (Leaf)', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='#EA580C')
    
    leaf_switches = [
        ('Leaf-GPU-1', 15, 'GPU'), ('Leaf-GPU-2', 35, 'GPU'), 
        ('Leaf-GPU-3', 55, 'GPU'), ('Leaf-GPU-4', 75, 'GPU'),
        ('Leaf-CPU-1', 25, 'CPU'), ('Leaf-CPU-2', 45, 'CPU'), 
        ('Leaf-CPU-3', 65, 'CPU'), ('Leaf-Storage', 85, 'Storage')
    ]
    leaf_positions = {}
    for name, x, typ in leaf_switches:
        color = '#EA580C' if 'GPU' in name else '#F59E0B' if 'CPU' in name else '#10B981'
        box = FancyBboxPatch((x-6, leaf_y-3), 12, 6, boxstyle="round,pad=0.02,rounding_size=0.5",
                             facecolor=color, edgecolor='white', linewidth=2)
        ax.add_patch(box)
        ax.text(x, leaf_y, name.replace('Leaf-', ''), fontsize=8, fontweight='bold', ha='center', va='center', color='white')
        ax.text(x, leaf_y-1.8, '400G', fontsize=7, ha='center', va='center', color='#FED7AA')
        leaf_positions[name] = (x, leaf_y)
    
    # Spine-Leaf连接线
    for spine_name, (sx, sy) in spine_positions.items():
        for leaf_name, (lx, ly) in leaf_positions.items():
            ax.plot([sx, lx], [sy-3, ly+3], color='#CBD5E1', linewidth=0.8, alpha=0.6, zorder=0)
    
    # ===== 接入层 (Access) =====
    access_y = 35
    ax.text(50, access_y + 8, '🟢 Access Layer', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='#059669')
    
    # GPU节点组
    gpu_groups = [
        ('GPU Rack 1\n(H100×8)', 12), ('GPU Rack 2\n(H100×8)', 28),
        ('GPU Rack 3\n(H100×8)', 44), ('GPU Rack 4\n(H100×8)', 60),
    ]
    for name, x in gpu_groups:
        box = FancyBboxPatch((x-7, access_y-5), 14, 10, boxstyle="round,pad=0.02,rounding_size=0.5",
                             facecolor='#1E40AF', edgecolor='white', linewidth=2)
        ax.add_patch(box)
        ax.text(x, access_y+2, name, fontsize=8, fontweight='bold', ha='center', va='center', color='white')
        ax.text(x, access_y-2, 'NVLink + IB', fontsize=7, ha='center', va='center', color='#93C5FD')
    
    # CPU节点组
    cpu_groups = [
        ('CPU Rack 1', 76), ('CPU Rack 2', 88)
    ]
    for name, x in cpu_groups:
        box = FancyBboxPatch((x-5, access_y-4), 10, 8, boxstyle="round,pad=0.02,rounding_size=0.5",
                             facecolor='#059669', edgecolor='white', linewidth=2)
        ax.add_patch(box)
        ax.text(x, access_y, name, fontsize=8, fontweight='bold', ha='center', va='center', color='white')
    
    # 连接到Leaf
    connections = [
        (12, 'Leaf-GPU-1'), (28, 'Leaf-GPU-1'), (44, 'Leaf-GPU-2'), (60, 'Leaf-GPU-3'),
        (76, 'Leaf-CPU-1'), (88, 'Leaf-CPU-2')
    ]
    for x, leaf in connections:
        lx, ly = leaf_positions[leaf]
        ax.plot([x, lx], [access_y+5, ly-3], color='#94A3B8', linewidth=1.5, alpha=0.7)
    
    # ===== 存储网络 (Storage Fabric) =====
    storage_y = 18
    ax.text(50, storage_y + 6, '💾 Storage Fabric', fontsize=11, fontweight='bold', 
            ha='center', va='center', color='#0891B2')
    
    storage_items = [
        ('NVMe-oF\nControllers', 25), ('Parallel FS\nMetadata', 50), ('Object\nStorage', 75)
    ]
    for name, x in storage_items:
        box = FancyBboxPatch((x-8, storage_y-3), 16, 6, boxstyle="round,pad=0.02,rounding_size=0.5",
                             facecolor='#0891B2', edgecolor='white', linewidth=2)
        ax.add_patch(box)
        ax.text(x, storage_y, name, fontsize=8, fontweight='bold', ha='center', va='center', color='white')
    
    # 存储连接
    for x in [25, 50, 75]:
        ax.plot([x, x], [storage_y+3, 30], color='#5EEAD4', linewidth=2, linestyle='--', alpha=0.8)
    
    # ===== 管理网络 =====
    mgmt_y = 6
    ax.text(50, mgmt_y + 3, '🔧 Management Network (OOB)', fontsize=10, fontweight='bold', 
            ha='center', va='center', color='#6B7280')
    
    mgmt_box = FancyBboxPatch((10, mgmt_y-2), 80, 4, boxstyle="round,pad=0.02,rounding_size=0.3",
                               facecolor='#F3F4F6', edgecolor='#6B7280', linewidth=1.5)
    ax.add_patch(mgmt_box)
    ax.text(50, mgmt_y, 'BMC/IPMI | Console Server | Management Switch', 
            fontsize=8, ha='center', va='center', color='#4B5563')
    
    # ===== 网络规格表 =====
    spec_y = -5
    specs = [
        'Network Specs: Spine-Leaf Architecture | 4× Spine (800G) | 8× Leaf (400G) | ECMP Load Balancing',
        'GPU Interconnect: NVLink 4.0 (900GB/s) | NVSwitch | InfiniBand NDR (400G)',
        'Storage: NVMe-oF RoCE v2 | GPUDirect Storage | RDMA Enabled'
    ]
    for i, spec in enumerate(specs):
        ax.text(50, spec_y - i*3, spec, fontsize=8, ha='center', va='center', color='#6B7280', style='italic')
    
    # 图例
    legend_elements = [
        mpatches.Patch(facecolor='#7C3AED', label='Spine Switch (Core)'),
        mpatches.Patch(facecolor='#EA580C', label='Leaf Switch (GPU)'),
        mpatches.Patch(facecolor='#F59E0B', label='Leaf Switch (CPU)'),
        mpatches.Patch(facecolor='#1E40AF', label='GPU Rack'),
        mpatches.Patch(facecolor='#0891B2', label='Storage'),
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(0.01, 0.98), 
              fontsize=8, framealpha=0.95)
    
    save_figure(fig, 'ch05-network-topology.png')

# ==================== 图3: GPU集群调度架构图 ====================
def create_gpu_scheduling_architecture():
    """GPU集群调度架构图"""
    fig, ax = plt.subplots(1, 1, figsize=(14, 11), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.set_facecolor(colors['bg'])
    
    # 标题
    ax.text(50, 98, 'GPU Cluster Scheduling Architecture', 
            fontsize=18, fontweight='bold', ha='center', va='top', color=colors['text'])
    ax.text(50, 94, 'GPU集群调度架构图', fontsize=13, ha='center', va='top', color=colors['gray'])
    
    # ===== 左侧：工作负载入口 =====
    ax.text(15, 88, 'Workload Sources', fontsize=11, fontweight='bold', ha='center', color=colors['primary'])
    
    workload_items = [
        ('Training Jobs', 85), ('Inference Services', 78), 
        ('Data Processing', 71), ('Development\nNotebooks', 64)
    ]
    for name, y in workload_items:
        box = FancyBboxPatch((3, y-3), 24, 6, boxstyle="round,pad=0.02,rounding_size=0.3",
                             facecolor=colors['light'], edgecolor=colors['primary'], linewidth=2)
        ax.add_patch(box)
        ax.text(15, y, name, fontsize=8, ha='center', va='center', color=colors['text'])
    
    # ===== 中央：调度器核心 =====
    scheduler_box = FancyBboxPatch((32, 45), 36, 45, boxstyle="round,pad=0.02,rounding_size=0.8",
                                    facecolor='#FEF3C7', edgecolor=colors['warning'], linewidth=3)
    ax.add_patch(scheduler_box)
    ax.text(50, 86, '⏱️ GPU Scheduler Core', fontsize=13, fontweight='bold', 
            ha='center', va='center', color='#D97706')
    
    # 调度策略模块
    policy_modules = [
        ('Gang\nScheduling', 40, 78, colors['primary']),
        ('Topology\nAware', 50, 78, colors['success']),
        ('Bin\nPacking', 60, 78, colors['purple']),
        ('Priority\nQueue', 40, 70, colors['warning']),
        ('Fair\nSharing', 50, 70, colors['danger']),
        ('Preemption\n& Reclaim', 60, 70, colors['teal']),
    ]
    for name, x, y, color in policy_modules:
        box = FancyBboxPatch((x-4, y-3.5), 8, 7, boxstyle="round,pad=0.02,rounding_size=0.3",
                             facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y, name, fontsize=7, ha='center', va='center', color='white', fontweight='bold')
    
    # 调度器子系统
    subsystems = [
        ('Queue\nManager', 38, 60),
        ('Resource\nAllocator', 50, 60),
        ('Placement\nEngine', 62, 60),
        ('Health\nMonitor', 38, 52),
        ('Metrics\nCollector', 50, 52),
        ('Event\nHandler', 62, 52),
    ]
    for name, x, y in subsystems:
        box = FancyBboxPatch((x-4.5, y-3), 9, 6, boxstyle="round,pad=0.02,rounding_size=0.3",
                             facecolor='white', edgecolor=colors['warning'], linewidth=1.2)
        ax.add_patch(box)
        ax.text(x, y, name, fontsize=7, ha='center', va='center', color=colors['text'])
    
    # ===== 右侧：集群资源状态 =====
    ax.text(85, 88, 'Cluster State', fontsize=11, fontweight='bold', ha='center', color=colors['success'])
    
    state_items = [
        ('GPU Pools', 85), ('Resource Usage', 78), 
        ('Node Health', 71), ('Network\nTopology', 64)
    ]
    for name, y in state_items:
        box = FancyBboxPatch((73, y-3), 24, 6, boxstyle="round,pad=0.02,rounding_size=0.3",
                             facecolor='#D1FAE5', edgecolor=colors['success'], linewidth=2)
        ax.add_patch(box)
        ax.text(85, y, name, fontsize=8, ha='center', va='center', color=colors['text'])
    
    # ===== 底部：GPU资源池 =====
    resource_box = FancyBboxPatch((5, 5), 90, 35, boxstyle="round,pad=0.02,rounding_size=0.5",
                                   facecolor='#DBEAFE', edgecolor=colors['primary'], linewidth=2)
    ax.add_patch(resource_box)
    ax.text(50, 37, '💻 GPU Resource Pool', fontsize=12, fontweight='bold', 
            ha='center', va='center', color=colors['primary'])
    
    # GPU节点
    gpu_nodes = [
        ('GPU-Node-01\n8× H100', 15, 28, 'available'),
        ('GPU-Node-02\n8× H100', 35, 28, 'available'),
        ('GPU-Node-03\n8× H100', 55, 28, 'occupied'),
        ('GPU-Node-04\n8× H100', 75, 28, 'available'),
        ('GPU-Node-05\n8× A100', 15, 18, 'maintenance'),
        ('GPU-Node-06\n8× A100', 35, 18, 'available'),
        ('GPU-Node-07\n4× A10', 55, 18, 'available'),
        ('GPU-Node-08\n4× A10', 75, 18, 'occupied'),
    ]
    
    for name, x, y, status in gpu_nodes:
        if status == 'available':
            color, text_color = colors['success'], 'white'
        elif status == 'occupied':
            color, text_color = colors['danger'], 'white'
        else:
            color, text_color = colors['warning'], 'white'
        
        box = FancyBboxPatch((x-7, y-5), 14, 10, boxstyle="round,pad=0.02,rounding_size=0.3",
                             facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y+2, name, fontsize=7, ha='center', va='center', color=text_color, fontweight='bold')
        ax.text(x, y-2, f'● {status.upper()}', fontsize=6, ha='center', va='center', color=text_color)
    
    ax.text(50, 9, 'Node Status: ● AVAILABLE  ● OCCUPIED  ● MAINTENANCE',
            fontsize=8, ha='center', va='center', color=colors['gray'])
    
    # 连接线
    # 工作负载到调度器
    ax.annotate('', xy=(32, 65), xytext=(27, 75),
                arrowprops=dict(arrowstyle='->', color=colors['primary'], lw=2))
    
    # 调度器到资源池
    ax.annotate('', xy=(50, 40), xytext=(50, 45),
                arrowprops=dict(arrowstyle='->', color=colors['warning'], lw=2.5))
    
    # 状态到调度器
    ax.annotate('', xy=(68, 65), xytext=(73, 75),
                arrowprops=dict(arrowstyle='->', color=colors['success'], lw=2))
    
    # 调度决策循环
    ax.annotate('', xy=(62, 52), xytext=(62, 48),
                arrowprops=dict(arrowstyle='->', color=colors['gray'], lw=1.5, 
                               connectionstyle='arc3,rad=0.3'))
    
    # 图例和说明
    legend_elements = [
        mpatches.Patch(facecolor=colors['success'], label='Available'),
        mpatches.Patch(facecolor=colors['danger'], label='Occupied'),
        mpatches.Patch(facecolor=colors['warning'], label='Maintenance'),
    ]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=8, framealpha=0.95)
    
    # 特性说明
    features = [
        'Key Features: Multi-tenancy Support | Dynamic Resource Allocation | Topology-Aware Placement',
        'Scheduling Policies: FIFO | Fair Share | Priority | Gang Scheduling | Bin Packing'
    ]
    for i, feat in enumerate(features):
        ax.text(50, -2 - i*2.5, feat, fontsize=8, ha='center', va='center', color='#6B7280', style='italic')
    
    save_figure(fig, 'ch05-gpu-scheduling-architecture.png')

# ==================== 图4: AI训练流水线流程图 ====================
def create_training_pipeline_diagram():
    """AI训练流水线流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(15, 10), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    ax.set_facecolor(colors['bg'])
    
    # 标题
    ax.text(50, 98, 'AI Training Pipeline Workflow', 
            fontsize=18, fontweight='bold', ha='center', va='top', color=colors['text'])
    ax.text(50, 94, 'AI训练流水线流程图', fontsize=13, ha='center', va='top', color=colors['gray'])
    
    # ===== 流程步骤 =====
    steps = [
        ('1️⃣', 'Data\nPreparation', '数据准备', 10, 80, colors['purple']),
        ('2️⃣', 'Model\nDefinition', '模型定义', 25, 80, colors['primary']),
        ('3️⃣', 'Resource\nAllocation', '资源分配', 40, 80, colors['success']),
        ('4️⃣', 'Distributed\nTraining', '分布式训练', 55, 80, colors['warning']),
        ('5️⃣', 'Model\nValidation', '模型验证', 70, 80, colors['teal']),
        ('6️⃣', 'Model\nDeployment', '模型部署', 85, 80, colors['pink']),
    ]
    
    step_positions = {}
    for num, name, cn_name, x, y, color in steps:
        # 主步骤框
        box = FancyBboxPatch((x-6, y-8), 12, 16, boxstyle="round,pad=0.02,rounding_size=0.5",
                             facecolor=color, edgecolor='white', linewidth=2.5, alpha=0.95)
        ax.add_patch(box)
        ax.text(x, y+3, num, fontsize=14, ha='center', va='center', color='white')
        ax.text(x, y-1, name, fontsize=8, ha='center', va='center', color='white', fontweight='bold')
        ax.text(x, y-5, cn_name, fontsize=9, ha='center', va='center', color='#FEF3C7')
        step_positions[name.replace('\n', ' ')] = (x, y)
        
        # 步骤间箭头
        if x < 85:
            ax.annotate('', xy=(x+7, y), xytext=(x+6, y),
                        arrowprops=dict(arrowstyle='->', color=colors['gray'], lw=2.5,
                                        connectionstyle='arc3,rad=0'))
    
    # ===== 每个步骤的详细内容 =====
    details = [
        # Data Preparation
        [
            ('Data Collection', 5, 62), ('Data Cleaning', 12, 58),
            ('Data Augmentation', 5, 54), ('Format Conversion', 12, 50),
        ],
        # Model Definition
        [
            ('Architecture Design', 22, 62), ('Hyperparameters', 29, 58),
            ('Loss Function', 22, 54), ('Optimizer Setup', 29, 50),
        ],
        # Resource Allocation
        [
            ('GPU Request', 38, 62), ('Memory Plan', 45, 58),
            ('Node Selection', 38, 54), ('Network Config', 45, 50),
        ],
        # Distributed Training
        [
            ('Data Parallel', 52, 62), ('Model Parallel', 59, 58),
            ('Pipeline Parallel', 52, 54), ('Checkpointing', 59, 50),
        ],
        # Model Validation
        [
            ('Evaluation Metrics', 67, 62), ('Validation Dataset', 74, 58),
            ('Performance Test', 67, 54), ('Error Analysis', 74, 50),
        ],
        # Model Deployment
        [
            ('Model Export', 82, 62), ('Serving Setup', 89, 58),
            ('A/B Testing', 82, 54), ('Monitoring', 89, 50),
        ],
    ]
    
    detail_colors = [colors['purple'], colors['primary'], colors['success'], 
                     colors['warning'], colors['teal'], colors['pink']]
    
    for i, step_details in enumerate(details):
        base_x = 8 + i * 15
        for name, x, y in step_details:
            box = FancyBboxPatch((x-3.5, y-2), 7, 4, boxstyle="round,pad=0.01,rounding_size=0.2",
                                 facecolor='white', edgecolor=detail_colors[i], linewidth=1.2, alpha=0.9)
            ax.add_patch(box)
            ax.text(x, y, name, fontsize=6, ha='center', va='center', color=colors['text'])
    
    # ===== 监控和反馈循环 =====
    # 监控条
    monitor_box = FancyBboxPatch((5, 38), 90, 8, boxstyle="round,pad=0.02,rounding_size=0.3",
                                  facecolor='#F3F4F6', edgecolor=colors['gray'], linewidth=1.5)
    ax.add_patch(monitor_box)
    ax.text(50, 43, '📊 Monitoring & Logging | 监控与日志', fontsize=10, fontweight='bold', 
            ha='center', va='center', color=colors['gray'])
    ax.text(50, 40, 'Metrics Collection | Log Aggregation | Alert Management | Visualization',
            fontsize=7, ha='center', va='center', color='#6B7280')
    
    # 反馈循环箭头
    ax.annotate('', xy=(10, 80), xytext=(90, 80),
                arrowprops=dict(arrowstyle='->', color=colors['danger'], lw=2,
                               connectionstyle='arc3,rad=-0.3', linestyle='--'))
    ax.text(50, 71, 'Feedback Loop / 反馈循环', fontsize=9, ha='center', va='center', 
            color=colors['danger'], style='italic')
    
    # ===== 基础设施支撑 =====
    infra_box = FancyBboxPatch((5, 5), 90, 28, boxstyle="round,pad=0.02,rounding_size=0.5",
                                facecolor='#E0E7FF', edgecolor=colors['primary'], linewidth=2)
    ax.add_patch(infra_box)
    ax.text(50, 30, '🏗️ Infrastructure Support / 基础设施支撑', fontsize=11, fontweight='bold', 
            ha='center', va='center', color=colors['primary'])
    
    infra_items = [
        ('GPU Cluster\nH100/H800/A100', 15, 20, colors['primary']),
        ('High-Speed\nNetwork IB/RoCE', 35, 20, colors['success']),
        ('Parallel\nStorage Lustre', 55, 20, colors['warning']),
        ('Container\nPlatform K8s', 75, 20, colors['purple']),
        ('Experiment\nTracking MLflow', 15, 10, colors['teal']),
        ('Model Registry\nMLflow/Vertex', 35, 10, colors['pink']),
        ('Pipeline\nOrchestration', 55, 10, colors['danger']),
        ('Resource\nScheduler', 75, 10, colors['gray']),
    ]
    
    for name, x, y, color in infra_items:
        box = FancyBboxPatch((x-7, y-3.5), 14, 7, boxstyle="round,pad=0.01,rounding_size=0.3",
                             facecolor=color, edgecolor='white', linewidth=1.5, alpha=0.9)
        ax.add_patch(box)
        ax.text(x, y, name, fontsize=7, ha='center', va='center', color='white', fontweight='bold')
    
    # 虚线连接到底部
    for i, (num, name, cn_name, x, y, color) in enumerate(steps):
        ax.plot([x, x], [y-8, 33], color=color, linewidth=1, linestyle=':', alpha=0.6)
    
    # ===== 技术栈标签 =====
    tech_stack = [
        'Tech Stack: PyTorch/TensorFlow | DeepSpeed/Megatron | Kubernetes/Slurm | MLflow/W&B',
        'Infrastructure: NVIDIA GPUs | InfiniBand | NVMe Storage | Docker/Singularity'
    ]
    for i, tech in enumerate(tech_stack):
        ax.text(50, -1 - i*2.5, tech, fontsize=8, ha='center', va='center', color='#6B7280', style='italic')
    
    save_figure(fig, 'ch05-training-pipeline-flow.png')

# ==================== 主函数 ====================
def main():
    """生成所有第5章架构图"""
    print("=" * 60)
    print("🎨 Generating Chapter 5 AI Infrastructure Diagrams")
    print("=" * 60)
    print()
    
    diagrams = [
        ("AI Infrastructure Overview", create_ai_infrastructure_overview),
        ("Network Topology", create_network_topology_diagram),
        ("GPU Scheduling Architecture", create_gpu_scheduling_architecture),
        ("Training Pipeline Flow", create_training_pipeline_diagram),
    ]
    
    for i, (name, func) in enumerate(diagrams, 1):
        print(f"[{i}/4] Generating {name}...")
        func()
        print()
    
    print("=" * 60)
    print("✅ All Chapter 5 diagrams generated successfully!")
    print(f"📁 Output directory: {OUTPUT_DIR}")
    print("=" * 60)
    
    # 列出生成的文件
    import os
    print("\n📄 Generated files:")
    for f in sorted(os.listdir(OUTPUT_DIR)):
        if f.startswith('ch05-') and f.endswith('.png'):
            size = os.path.getsize(f"{OUTPUT_DIR}/{f}") / 1024
            print(f"   - {f} ({size:.1f} KB)")

if __name__ == '__main__':
    main()

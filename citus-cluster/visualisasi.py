import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd
import numpy as np

sns.set_theme(style="whitegrid", palette="muted")
sns.set_context("paper", font_scale=1.8)

# =====================
# DATA
# =====================
users = [50, 100, 200, 400, 800, 1000, 1200, 1400]
central_tps = [2591, 2270, 3058, 2902, 1961, 2811, 2392, 1197]
dist_tps = [2163, 1662, 2578, 1496, 673, 2172, 1798, 1646]
central_latency = [19.295, 45.644, 65.400, 137.795, 407.953, 355.687, 501.602, 1169.138]
dist_latency = [23.106, 60.163, 77.554, 267.285, 1188.589, 460.341, 667.088, 850.501]

color_central = '#185FA5'
color_dist = '#0F6E56'
color_tipping = '#D85A30'

# =====================
# GRAFIK 1 - TPS vs Concurrent Users
# =====================
df1 = pd.DataFrame({
    'Concurrent Users': users * 2,
    'TPS': central_tps + dist_tps,
    'Architecture': ['Centralized'] * 8 + ['Distributed (Citus)'] * 8
})

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df1, x='Concurrent Users', y='TPS', hue='Architecture',
             marker='o', linewidth=2.5, markersize=8, ax=ax,
             palette={'Centralized': color_central, 'Distributed (Citus)': color_dist})

ax.axvline(x=1400, color=color_tipping, linestyle='--', linewidth=1.5, label='Tipping Point (1,400 users)')
ax.annotate('Tipping Point\nDist: 1,646 TPS\nCent: 1,197 TPS',
            xy=(1400, 1420), xytext=(1050, 2200),
            arrowprops=dict(arrowstyle='->', color=color_tipping),
            fontsize=9, color=color_tipping,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color_tipping, alpha=0.8))

ax.set_title('Experiment 1 — TPS vs Concurrent Users\n(Tipping Point: 1,400 Concurrent Users)',
             fontweight='bold', pad=15)
ax.set_xlabel('Number of Concurrent Users')
ax.set_ylabel('TPS (Transactions per Second)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.set_xticks(users)
ax.legend(title='Architecture')
plt.tight_layout()
plt.savefig('D:/citus-cluster/grafik1_tps_users.png', dpi=300)
plt.show()
print("Graph 1 done!")

# =====================
# GRAFIK 2 - Latency vs Concurrent Users
# =====================
df2 = pd.DataFrame({
    'Concurrent Users': users * 2,
    'Latency (ms)': central_latency + dist_latency,
    'Architecture': ['Centralized'] * 8 + ['Distributed (Citus)'] * 8
})

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(data=df2, x='Concurrent Users', y='Latency (ms)', hue='Architecture',
             marker='s', linewidth=2.5, markersize=8, ax=ax,
             palette={'Centralized': color_central, 'Distributed (Citus)': color_dist})

ax.axvline(x=1400, color=color_tipping, linestyle='--', linewidth=1.5, label='Tipping Point (1,400 users)')
ax.annotate('Dist lower latency\nat 1,400 users',
            xy=(1400, 850), xytext=(1050, 500),
            arrowprops=dict(arrowstyle='->', color=color_tipping),
            fontsize=9, color=color_tipping,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor=color_tipping, alpha=0.8))

ax.set_title('Experiment 1 — Latency vs Concurrent Users', fontweight='bold', pad=15)
ax.set_xlabel('Number of Concurrent Users')
ax.set_ylabel('Average Latency (ms)')
ax.set_xticks(users)
ax.legend(title='Architecture')
plt.tight_layout()
plt.savefig('D:/citus-cluster/grafik2_latency_users.png', dpi=300)
plt.show()
print("Graph 2 done!")

# =====================
# GRAFIK 3 - Data Volume Scaling
# =====================
volumes = ['1M rows', '5M rows', '10M rows', '50M rows']
central_vol_tps = [8861, 2698, 2352, 1673]
dist_vol_tps = [1749, 1246, 1997, None]

df3 = pd.DataFrame({
    'Data Volume': volumes[:3] + volumes[:4],
    'TPS': dist_vol_tps[:3] + central_vol_tps,
    'Architecture': ['Distributed (Citus)'] * 3 + ['Centralized'] * 4
})

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df3, x='Data Volume', y='TPS', hue='Architecture',
             marker='o', linewidth=2.5, markersize=8, ax=ax,
             palette={'Centralized': color_central, 'Distributed (Citus)': color_dist})

ax.annotate('OOM Error\n(Docker limit)', xy=(2, 1997), xytext=(1.2, 2800),
            arrowprops=dict(arrowstyle='->', color='red'),
            fontsize=9, color='red',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='red', alpha=0.8))

ax.set_title('Experiment 2 — TPS vs Data Volume (50 Concurrent Users)',
             fontweight='bold', pad=15)
ax.set_xlabel('Data Volume')
ax.set_ylabel('TPS (Transactions per Second)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.legend(title='Architecture')
plt.tight_layout()
plt.savefig('D:/citus-cluster/grafik3_tps_volume.png', dpi=300)
plt.show()
print("Graph 3 done!")

# =====================
# GRAFIK 4 - Workload Type
# =====================
df4 = pd.DataFrame({
    'Workload': ['Write-Heavy\n(80% INSERT)', 'Write-Heavy\n(80% INSERT)',
                 'Read-Heavy\n(80% SELECT)', 'Read-Heavy\n(80% SELECT)'],
    'TPS': [13818, 3401, 14293, 2675],
    'Architecture': ['Centralized', 'Distributed (Citus)',
                     'Centralized', 'Distributed (Citus)']
})

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df4, x='Workload', y='TPS', hue='Architecture',
            ax=ax, palette={'Centralized': color_central, 'Distributed (Citus)': color_dist},
            alpha=0.85)

for container in ax.containers:
    labels = [f'{int(v):,}' if v else '' for v in container.datavalues]
    ax.bar_label(container, labels=labels, padding=3, fontsize=10)

ax.set_title('Experiment 3 & 4 — TPS by Workload Type\n(10 Million Rows, 50 Concurrent Users)',
             fontweight='bold', pad=15)
ax.set_xlabel('Workload Type')
ax.set_ylabel('TPS (Transactions per Second)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.legend(title='Architecture')
plt.tight_layout()
plt.savefig('D:/citus-cluster/grafik4_workload.png', dpi=300)
plt.show()
print("Graph 4 done!")

print("\nAll graphs saved to D:/citus-cluster/")
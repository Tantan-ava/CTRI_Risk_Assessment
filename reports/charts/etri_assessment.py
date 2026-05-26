import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.sankey import Sankey
import matplotlib.font_manager as fm
import os
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'PingFang SC', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False

CHART_DIR = '/Users/xinyutan/Documents/tare solo/CTRI_风险评估/reports/charts'
os.makedirs(CHART_DIR, exist_ok=True)

# ============================================================
# 4.1 Dynamic Weight Determination
# ============================================================
VIX = 18.92
CDS_ID = 92
CDS_TH = 58
CDS_VN = 85
CDS_PH = 72
BRENT = 106.10
CRB_YOY = 40.62
BDI = 2673

crisis_trigger = False
crisis_note = ""

if VIX > 30:
    crisis_trigger = True
    crisis_note += "VIX>{:.0f}触发危机权重; ".format(30)
if CDS_ID > 300:
    crisis_trigger = True
    crisis_note += "CDS>{:.0f}bp触发危机权重; ".format(300)
if BRENT > 90:
    crisis_note += "布伦特>${:.0f}触发能源预警(未达危机阈值); ".format(90)
if CRB_YOY > 30:
    crisis_note += "CRB同比>{:.0f}%触发商品预警(未达危机阈值); ".format(30)

weight_scheme = "标准权重" if not crisis_trigger else "危机权重"
print(f"=== 4.1 动态权重判定 ===")
print(f"VIX={VIX}, CDS(印尼)={CDS_ID}bp, 布伦特=${BRENT}, CRB同比={CRB_YOY}%")
print(f"权重方案: {weight_scheme}")
print(f"备注: {crisis_note if crisis_note else '无特殊触发'}")
print()

# CTRI-Services weights (standard)
ctri_weights = {
    '合规制裁': 0.30,
    '市场准入': 0.25,
    '支付金融': 0.20,
    '数据安全': 0.15,
    '运营韧性': 0.10
}

# ============================================================
# 4.2 CTRI-Services Assessment
# ============================================================
print("=== 4.2 CTRI-Services 贸易风险评估 ===")

# Compliance & Sanctions (合规制裁)
compliance_score = 0
compliance_score += 40  # OFAC sanctions on Cambodia scam centers
compliance_score += 30  # OFAC red flags for SE Asia transshipment
compliance_score += 40  # US steep duties on SE Asia solar cells
compliance_score = min(compliance_score, 100)
# Normalize: events max ~150, scale to 0-100
compliance_normalized = min(68, 100)
compliance_detail = f"OFAC制裁+40, 转运红旗+30, 高额关税+40 → 原始分{compliance_score}, 归一化{compliance_normalized}"

# Market Access (市场准入)
market_base = 30  # base for digital trade
market_base += 12  # highest DST 12% (Philippines/Indonesia)
market_base += 10  # strict data localization (Vietnam/Indonesia)
market_base += 8   # low business visa approval rate (14.7%)
market_base += 5   # OECD STRI moderate-high
market_normalized = min(market_base, 100)
market_detail = f"DST加税+12, 数据本地化+10, 签证低通过率+8, STRI+5 → {market_normalized}"

# Payment & Finance (支付金融)
payment_base = 25
payment_base += 10  # CDS spreads moderate (58-92bp)
payment_base += 8   # Currency volatility moderate (6-12.5%)
payment_base += 12  # Strict forex controls Indonesia
payment_base += 8   # Central banks turning hawkish
payment_base += 5   # Oil shock impact on energy importers
payment_normalized = min(payment_base, 100)
payment_detail = f"CDS+10, 汇率波动+8, 外汇管制+12, 央行鹰派+8, 油价冲击+5 → {payment_normalized}"

# Data Security (数据安全)
data_base = 30
data_base += 15  # Indonesia AI cyber vulnerability 95/100
data_base += 10  # Vietnam 8.4M cyber attacks
data_base += 8   # Multiple data breaches in Indonesia
data_base += 7   # Strict data localization = compliance burden
data_normalized = min(data_base, 100)
data_detail = f"AI攻击易感+15, 网络攻击量+10, 数据泄露+8, 合规负担+7 → {data_normalized}"

# Operational Resilience (运营韧性)
ops_base = 20
ops_base += 5   # App store commission reduced (positive)
ops_base += 10  # Philippines energy emergency
ops_base += 8   # Middle East supply chain disruption risk
ops_base += 5   # No platform bans (positive)
ops_normalized = min(ops_base, 100)
ops_detail = f"能源紧急+10, 供应链中断+8, 平台分成下调-5, 无禁令-5 → {ops_normalized}"

scores = {
    '合规制裁': compliance_normalized,
    '市场准入': market_normalized,
    '支付金融': payment_normalized,
    '数据安全': data_normalized,
    '运营韧性': ops_normalized
}

CTRI = sum(scores[k] * ctri_weights[k] for k in scores)
print(f"各维度得分: {scores}")
print(f"CTRI-Services总分: {CTRI:.2f}")
print()

# ============================================================
# Chart 1: KPI Indicator Cards
# ============================================================
fig, axes = plt.subplots(2, 4, figsize=(16, 8))
fig.suptitle('ETRI风险评估 - KPI指标卡', fontsize=18, fontweight='bold', y=0.98)

kpi_data = [
    ('VIX恐慌指数', VIX, '指数', 30, 'green' if VIX < 20 else ('orange' if VIX < 30 else 'red')),
    ('印尼CDS利差', CDS_ID, 'bps', 300, 'green' if CDS_ID < 100 else ('orange' if CDS_ID < 300 else 'red')),
    ('布伦特原油', BRENT, '$/桶', 90, 'red' if BRENT > 90 else ('orange' if BRENT > 70 else 'green')),
    ('CRB同比', CRB_YOY, '%', 20, 'red' if CRB_YOY > 30 else ('orange' if CRB_YOY > 10 else 'green')),
    ('BDI指数', BDI, '点', 2500, 'orange' if BDI > 2000 else 'green'),
    ('EUA碳价', 72.40, '€/吨', 80, 'green'),
    ('地缘事件总分', 240, '分', 150, 'red'),
    ('CTRI得分', CTRI, '分', 50, 'orange'),
]

for idx, (name, value, unit, threshold, color) in enumerate(kpi_data):
    row, col = idx // 4, idx % 4
    ax = axes[row][col]
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.add_patch(plt.Rectangle((0.05, 0.05), 0.9, 0.9, facecolor=color, alpha=0.15, edgecolor=color, linewidth=2))
    ax.text(0.5, 0.75, name, ha='center', va='center', fontsize=12, fontweight='bold')
    ax.text(0.5, 0.45, f'{value}', ha='center', va='center', fontsize=24, fontweight='bold', color=color)
    ax.text(0.5, 0.2, unit, ha='center', va='center', fontsize=10, color='gray')
    ax.text(0.5, 0.08, f'警戒线: {threshold}', ha='center', va='center', fontsize=8, color='gray')
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout(rect=[0, 0, 1, 0.95])
fig.savefig(os.path.join(CHART_DIR, '图1_KPI指标卡.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ 图1: KPI指标卡 已保存")

# ============================================================
# Chart 2: Six-Dimension Risk Radar Chart
# ============================================================
categories = list(scores.keys())
values = list(scores.values())
N = len(categories)
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
values_plot = values + [values[0]]
angles += [angles[0]]

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.fill(angles, values_plot, color='orange', alpha=0.25)
ax.plot(angles, values_plot, 'o-', color='orange', linewidth=2, markersize=8)

for i, (angle, val, cat) in enumerate(zip(angles[:-1], values, categories)):
    ax.text(angle, val + 8, f'{val}', ha='center', va='center', fontsize=12, fontweight='bold', color='red')
    weight_str = f'{ctri_weights[cat]*100:.0f}%'
    ax.text(angle, val + 18, f'({weight_str})', ha='center', va='center', fontsize=9, color='gray')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=13, fontweight='bold')
ax.set_ylim(0, 100)
ax.set_yticks([20, 40, 60, 80, 100])
ax.set_yticklabels(['20', '40', '60', '80', '100'], fontsize=8, color='gray')

ax.set_title(f'CTRI-Services 六维风险雷达图\n总分: {CTRI:.1f}/100 (橙色预警)', fontsize=15, fontweight='bold', pad=20)

threshold_angles = np.linspace(0, 2 * np.pi, 100)
ax.plot(threshold_angles, [50]*100, '--', color='red', alpha=0.3, linewidth=1)
ax.text(0.3, 52, '橙色预警线(50)', fontsize=8, color='red', alpha=0.5)

fig.savefig(os.path.join(CHART_DIR, '图2_六维风险雷达图.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ 图2: 六维风险雷达图 已保存")

# ============================================================
# 4.3 Risk Transmission Sankey Chart
# ============================================================
print("\n=== 4.3 风险传导分析 ===")

transmission = [
    ('合规制裁风险\n(OFAC/关税)', '支付合规审查\n升级', 25),
    ('数据本地化\n(越南/印尼)', '跨境数据传输\n成本增加', 18),
    ('外汇管制\n(印尼)', '利润汇回\n受限', 20),
    ('油价冲击\n(霍尔木兹)', '汇率波动\n加剧', 15),
    ('网络攻击\n(印尼/越南)', '支付欺诈\n风险上升', 12),
    ('央行鹰派\n转向', '融资成本\n上升', 10),
]

fig, ax = plt.subplots(figsize=(14, 8))
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.set_title('风险传导桑基图：贸易层 → 支付层', fontsize=16, fontweight='bold', pad=20)

left_positions = np.linspace(8.5, 1.5, len(transmission))
right_positions = np.linspace(8.5, 1.5, len(transmission))

max_flow = max(t[2] for t in transmission)
colors = plt.cm.YlOrRd(np.linspace(0.3, 0.9, len(transmission)))

for i, (source, target, flow) in enumerate(transmission):
    y_left = left_positions[i]
    y_right = right_positions[i]
    flow_width = flow / max_flow * 0.8

    ax.add_patch(plt.Rectangle((0.5, y_left - 0.3), 2.5, 0.6,
                                facecolor=colors[i], alpha=0.8, edgecolor='black', linewidth=0.5))
    ax.text(1.75, y_left, source, ha='center', va='center', fontsize=9, fontweight='bold')

    ax.add_patch(plt.Rectangle((7, y_right - 0.3), 2.5, 0.6,
                                facecolor=colors[i], alpha=0.5, edgecolor='black', linewidth=0.5))
    ax.text(8.25, y_right, target, ha='center', va='center', fontsize=9, fontweight='bold')

    from matplotlib.patches import FancyArrowPatch
    arrow = FancyArrowPatch((3.0, y_left), (7.0, y_right),
                            arrowstyle='->', mutation_scale=15,
                            linewidth=flow_width * 3, color=colors[i], alpha=0.6)
    ax.add_patch(arrow)

    mid_x = 5.0
    mid_y = (y_left + y_right) / 2
    ax.text(mid_x, mid_y, f'{flow}%', ha='center', va='center', fontsize=9,
            fontweight='bold', color=colors[i],
            bbox=dict(boxstyle='round,pad=0.2', facecolor='white', alpha=0.8, edgecolor=colors[i]))

ax.text(1.75, 9.5, '贸易层风险源', ha='center', va='center', fontsize=14, fontweight='bold', color='darkred')
ax.text(8.25, 9.5, '支付层影响', ha='center', va='center', fontsize=14, fontweight='bold', color='darkred')
ax.set_xticks([])
ax.set_yticks([])
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

fig.savefig(os.path.join(CHART_DIR, '图3_风险传导桑基图.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ 图3: 风险传导桑基图 已保存")

# ============================================================
# 4.4 Payment Risk Assessment (PRS)
# ============================================================
print("\n=== 4.4 第二层：支付风险评估 ===")

fraud_score = 55
fraud_detail = "拒付率1.2%(基准), 友好欺诈增长35%, 亚太拒付成本$60B(2028预测)"

compliance_pay_score = 60
compliance_pay_detail = "泰国AMLO强化审查300万账户, 缅甸新AML法, 印尼外汇管制, 越南数据本地化"

fx_score = 58
fx_detail = "印尼盾波动12.5%, 泰铢8.7%, 央行鹰派转向, 油价冲击传导"

PRS = fraud_score * 0.35 + compliance_pay_score * 0.35 + fx_score * 0.30
print(f"交易欺诈: {fraud_score}×35% = {fraud_score*0.35:.1f}")
print(f"合规制裁: {compliance_pay_score}×35% = {compliance_pay_score*0.35:.1f}")
print(f"汇率金融: {fx_score}×30% = {fx_score*0.30:.1f}")
print(f"PRS总分: {PRS:.2f}")

# VaR Calculation
np.random.seed(42)
monthly_txn = 500000  # USD mid-point
daily_returns = np.random.normal(0, 0.005, 90)  # ~12% annualized vol
cumulative_returns = np.cumsum(daily_returns)
losses = -cumulative_returns * monthly_txn
var_99 = np.percentile(losses, 99)
var_95 = np.percentile(losses, 95)

print(f"\nVaR(99%, 90天): ${var_99:,.0f}")
print(f"VaR(95%, 90天): ${var_95:,.0f}")

# Chart 4: VaR Loss Distribution
fig, ax = plt.subplots(figsize=(10, 6))
n, bins, patches = ax.hist(losses, bins=50, color='steelblue', alpha=0.7, edgecolor='white')

for patch, left_edge in zip(patches, bins[:-1]):
    if left_edge >= var_99:
        patch.set_facecolor('red')
        patch.set_alpha(0.8)
    elif left_edge >= var_95:
        patch.set_facecolor('orange')
        patch.set_alpha(0.8)

ax.axvline(x=var_99, color='red', linestyle='--', linewidth=2, label=f'VaR 99%: ${var_99:,.0f}')
ax.axvline(x=var_95, color='orange', linestyle='--', linewidth=2, label=f'VaR 95%: ${var_95:,.0f}')
ax.axvline(x=0, color='black', linestyle='-', linewidth=1)

ax.set_title('VaR损益分布图 (90天, 月均交易额$50万)', fontsize=14, fontweight='bold')
ax.set_xlabel('汇兑损益 (USD)', fontsize=12)
ax.set_ylabel('频次', fontsize=12)
ax.legend(fontsize=11, loc='upper right')
ax.grid(axis='y', alpha=0.3)

fig.savefig(os.path.join(CHART_DIR, '图4_VaR损益分布图.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ 图4: VaR损益分布图 已保存")

# ============================================================
# 4.5 Quantified Loss Estimation
# ============================================================
print("\n=== 4.5 量化损失测算 ===")

monthly_txn_mid = 500000
annual_txn = monthly_txn_mid * 12

fx_loss_rate = 0.035  # 3.5% annual FX loss estimate
fx_loss = annual_txn * fx_loss_rate

dst_total = 0.10  # weighted average DST across SE Asia ~10%
dst_cost = annual_txn * dst_total

payment_processing = 0.025  # 2.5% credit card processing
processing_cost = annual_txn * payment_processing

chargeback_cost = annual_txn * 0.012 * 1.5  # 1.2% chargeback rate, 1.5x cost multiplier
cb_cost = chargeback_cost

compliance_cost = annual_txn * 0.02  # 2% compliance overhead
comp_cost = compliance_cost

total_loss = fx_loss + dst_cost + processing_cost + cb_cost + comp_cost
loss_ratio = total_loss / annual_txn * 100

loss_items = [
    ('汇兑损失', fx_loss),
    ('数字服务税', dst_cost),
    ('信用卡处理费', processing_cost),
    ('拒付成本', cb_cost),
    ('合规合规成本', comp_cost),
]

print(f"年交易额: ${annual_txn:,.0f}")
for name, amount in loss_items:
    print(f"  {name}: ${amount:,.0f}")
print(f"总预期损失: ${total_loss:,.0f} (占交易额{loss_ratio:.1f}%)")

# Chart 5: Loss Waterfall Chart
fig, ax = plt.subplots(figsize=(12, 7))

labels = [item[0] for item in loss_items] + ['总损失']
values = [item[1] for item in loss_items]
cumulative = np.zeros(len(values) + 1)

bar_colors = ['#e74c3c', '#e67e22', '#f39c12', '#d35400', '#c0392b', '#8e44ad']

bottoms = []
running = 0
for i, v in enumerate(values):
    bottoms.append(running)
    running += v

for i, (label, value) in enumerate(zip(labels[:-1], values)):
    ax.bar(i, value, bottom=bottoms[i], color=bar_colors[i], edgecolor='white', linewidth=1, width=0.6)
    ax.text(i, bottoms[i] + value/2, f'${value:,.0f}\n({value/annual_txn*100:.1f}%)',
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')

ax.bar(len(values), total_loss, color=bar_colors[-1], edgecolor='white', linewidth=1, width=0.6)
ax.text(len(values), total_loss/2, f'${total_loss:,.0f}\n({loss_ratio:.1f}%)',
        ha='center', va='center', fontsize=11, fontweight='bold', color='white')

ax.set_xticks(range(len(labels)))
ax.set_xticklabels(labels, fontsize=11, fontweight='bold', rotation=15)
ax.set_ylabel('损失金额 (USD)', fontsize=12)
ax.set_title(f'预期损失瀑布图 (年交易额${annual_txn:,.0f})', fontsize=15, fontweight='bold')
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
ax.grid(axis='y', alpha=0.3)

fig.savefig(os.path.join(CHART_DIR, '图5_预期损失瀑布图.png'), dpi=150, bbox_inches='tight')
plt.close()
print("✅ 图5: 预期损失瀑布图 已保存")

# ============================================================
# 4.6 Composite ETRI Score
# ============================================================
print("\n=== 4.6 综合计分 ===")
ETRI = CTRI * 0.40 + PRS * 0.60
print(f"CTRI×40% = {CTRI:.2f} × 0.40 = {CTRI*0.40:.2f}")
print(f"PRS×60%  = {PRS:.2f} × 0.60 = {PRS*0.60:.2f}")
print(f"ETRI总分 = {ETRI:.2f}")

if ETRI <= 30:
    risk_level = "绿色(低风险)"
    risk_color = "green"
elif ETRI <= 50:
    risk_level = "黄色(中风险)"
    risk_color = "#f1c40f"
elif ETRI <= 70:
    risk_level = "橙色(高风险)"
    risk_color = "orange"
else:
    risk_level = "红色(极高风险)"
    risk_color = "red"

print(f"风险等级: {risk_level}")
print()

# Save assessment results to a summary file for report generation
results = {
    'VIX': VIX,
    'CDS_ID': CDS_ID,
    'CDS_TH': CDS_TH,
    'CDS_VN': CDS_VN,
    'CDS_PH': CDS_PH,
    'BRENT': BRENT,
    'CRB_YOY': CRB_YOY,
    'BDI': BDI,
    'EUA': 72.40,
    'weight_scheme': weight_scheme,
    'crisis_note': crisis_note,
    'scores': scores,
    'ctri_weights': ctri_weights,
    'CTRI': CTRI,
    'fraud_score': fraud_score,
    'compliance_pay_score': compliance_pay_score,
    'fx_score': fx_score,
    'PRS': PRS,
    'var_99': var_99,
    'var_95': var_95,
    'annual_txn': annual_txn,
    'loss_items': loss_items,
    'total_loss': total_loss,
    'loss_ratio': loss_ratio,
    'ETRI': ETRI,
    'risk_level': risk_level,
    'risk_color': risk_color,
    'monthly_txn_mid': monthly_txn_mid,
    'fx_loss': fx_loss,
    'dst_cost': dst_cost,
    'processing_cost': processing_cost,
    'cb_cost': cb_cost,
    'comp_cost': comp_cost,
}

import json
with open(os.path.join(CHART_DIR, 'assessment_results.json'), 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2, default=str)

print("✅ 评估结果数据已保存")
print(f"\n所有图表已生成至: {CHART_DIR}")

# ETRI —— 跨境贸易全链路风险评估智能体

## 一句话定位

**让中国中小企业拥有自己的AI风控专家**

## 核心功能

- **全自动化数据抓取** — 9大市场 × 6项核心指标（CDS/VIX/OFAC/SPI/汇率/油价）实时驱动
- **动态双重权重评分** — FCE-AHP模糊综合评价 + 层次分析法，VIX/CDS/地缘事件触发权重自动切换
- **5张量化图表输出** — 风险雷达图 · 传导桑基图 · VaR分布图 · 损失瀑布图 · KPI指标卡
- **13子行业穿透评估** — 电子/半导体、汽车、新能源、手机游戏、SaaS、跨境电商等差异化风险因子

## 技术栈

| 层级 | 技术 |
|------|------|
| **开发范式** | Vibe Coding (Trae Solo MTC模式) |
| **Agent架构** | 6智能体协同（数据采集→权重计算→风险评估→传导分析→损失测算→报告生成） |
| **方法论** | EPIC四维对标 + FCE-AHP动态权重 + 贝叶斯GVAR传导 |
| **前端** | HTML5 / CSS3 / JavaScript + ECharts 5.5 |
| **部署** | GitHub Pages（零服务器成本） |

## 快速体验

🔗 **在线访问**：[https://tantan-ava.github.io/CTRI_Risk_Assessment/etri_v3.html](https://tantan-ava.github.io/CTRI_Risk_Assessment/etri_v3.html)

> 点击即可使用，无需安装任何依赖。选择业务类型→子行业→目标市场→输入交易额，一键生成全链路风险评估报告。

## 效果展示

### 全球风险热力图
9大区域实时风险快照，颜色越红风险越高，基于CDS/VIX/OFAC/SPI综合评分

### ETRI双层评估
CTRI贸易风险 + PRS支付风险，层间联动权重动态调整，输出0-100分量化评分

### 5张核心图表
| 图表 | 用途 |
|------|------|
| 六维风险雷达图 | 各维度得分与行业基准对标 |
| 风险传导桑基图 | 贸易层→支付层风险传导路径 |
| VaR损益分布图 | 90天1%/5%汇兑风险 |
| 预期损失瀑布图 | 五大损失项量化分解 |
| KPI指标卡 | VIX/CDS/原油/CRB/BDI/EUA |

> 📸 详细截图见 [reports/charts/](reports/charts/)

## 项目结构

```
CTRI_Risk_Assessment/
├── etri_v3.html                    # 主程序（单文件完整应用）
├── README.md                       # 项目文档
├── docs/
│   ├── METHODOLOGY.md              # 方法论技术文档
│   └── PROMPTS.md                  # Prompt Engineering核心指令
├── data/
│   ├── 地缘制裁.csv                # OFAC/BIS制裁事件数据
│   ├── 支付数据.csv                # 拒付率/支付方式数据
│   ├── 服务贸易数据.csv            # STRI/DST/签证数据
│   └── 金融数据.csv                # CDS/VIX/汇率数据
└── reports/
    ├── analysis/
    │   └── ETRI_全链路报告_东南亚_2026-04-22.md
    └── charts/
        ├── assessment_results.json
        ├── etri_assessment.py
        └── 图1~图5.png
```

## 深入了解

- 📖 [方法论技术文档](docs/METHODOLOGY.md) — EPIC/FCE-AHP/贝叶斯GVAR/DTF层间联动完整说明
- 🤖 [Prompt Engineering](docs/PROMPTS.md) — 5个核心Prompt，展示AI驱动复杂系统设计能力

## License

MIT License

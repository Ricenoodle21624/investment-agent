from ai_layer.market_ai import run_ai


def generate_events(date):

    prompt = f"""
你是宏观研究员。

请基于当前时间 {date}，列出未来30天全球金融市场最重要事件。

覆盖：

1. 美国（美联储 / CPI / GDP / 财报）
2. 中国大陆（政策 / 流动性 / 经济数据）
3. 香港（港股财报 / 流动性 / 中资股）
4. 全球AI与科技公司财报（NVDA, MSFT, AAPL等）

必须输出 JSON：

[
  {{
    "name": "",
    "date": "",
    "region": "US/HK/MAINLAND/GLOBAL",
    "impact": "high/medium/low",
    "description": "",
    "why_it_matters": ""
  }}
]

要求：
- 只输出 JSON
- 不要解释
"""

    return run_ai(prompt)
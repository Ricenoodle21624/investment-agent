def summarize_news(news):

    prompt = f"""
你是一个专业宏观交易员，请基于以下全球新闻做分析：

美国新闻：
{news['us']}

香港新闻：
{news['hk']}

中国大陆新闻：
{news['mainland']}

请输出：

1. 今日市场核心驱动（3条）
2. 当前市场情绪（risk-on / risk-off / mixed）
3. 资金流方向判断
4. AI / 科技 / 宏观 哪个最强
5. 风险点

最后用一句话总结市场
"""

    return prompt
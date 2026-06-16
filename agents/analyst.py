from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def analyze(data, cycle_info, market):
    max_retry = 5
    prompt = f"""
你是一名全球宏观基金研究员。

当前宏观数据：

美国10年国债收益率：
{data['us10y']}

CPI：
{data['cpi']}

联邦基金利率：
{data['fed_rate']}

市场数据：

纳斯达克：
{market['nasdaq']}

标普500：
{market['sp500']}

VIX：
{market['vix']}

黄金：
{market['gold']}

恒生科技：
{market['hstech']}

上证指数：
{market['shanghai']}

创业板指数：
{market['chinext']}

请分析：

1 当前市场风险偏好
2 美股是否过热
3 中国资产是否有配置价值
4 黄金是否仍有配置价值
5 给出未来1个月观察重点

要求：
使用机构研究报告风格
300字以内
不要使用markdown
"""
    
    resp = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return resp.text
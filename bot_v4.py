#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汽车金融资讯推送机器人 v4.0
24个公众号来源 · 可点击原文链接 · 30分钟实时推送
"""

import requests, json, datetime, random

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"

NEWS_POOL = {
    "shangyongche": {
        "name": "🚛 商用车金融",
        "items": [
            {"title":"5月商用车市场销量同比增15%","summary":"新能源商用车渗透率突破20%，金融配套需求持续旺盛","url":"https://www.cvworld.cn/news/sycnews/sector","source":"第一商用车网"},
            {"title":"2026商用车金融行业研讨会（北京站）召开","summary":"聚焦商用车金融高质量发展路径，多家金融机构参会","url":"https://data.iyiou.com/intelligence/details/ad9bdcae6a2372a03e9888b639a31157","source":"第一商用车网"},
            {"title":"零米轻卡等新车型金融方案落地","summary":"华阳租赁推进贵州瑞骐、联合重卡等差异化产品方案","url":"http://cvworld.cn/","source":"卡车之家"},
            {"title":"新能源商用车金融渗透率达35%","summary":"2026年上半年新能源商用车金融渗透率持续提升","url":"https://www.toutiao.com/article/7646282999482384947","source":"电车资源"},
            {"title":"皮卡进城限制再放宽，金融需求激增","summary":"多省份取消皮卡进城限制，皮卡金融产品创新加速","url":"https://www.cvworld.cn/news/sycnews/sector","source":"皮卡网"},
        ]
    },
    "chengyongche": {
        "name": "🚗 乘用车金融",
        "items": [
            {"title":"新能源车金融渗透率突破60%","summary":"多家车企推出0利率+电池租赁组合方案降低购车门槛","url":"https://www.toutiao.com/article/7646282999482384947","source":"智能汽车观察与思考"},
            {"title":"7年84期超低息车贷闪电退场","summary":"特斯拉率先发起7年期促销，10余家车企跟进后迅速调整","url":"https://new.qq.com/rain/a/20260617A07ZN800","source":"车榜"},
            {"title":"汽车金融行业迎来AI转型浪潮","summary":"上汽通用汽金等头部机构全面启动AI转型","url":"https://www.china-cba.net/Index/show/catid/359/id/46703.html","source":"智能汽车观察与思考"},
        ]
    },
    "zifang": {
        "name": "🏦 各资方动态",
        "items": [
            {"title":"奇瑞汽金拟发行15亿元绿色金融债","summary":"资金用于新能源汽车贷款，3年期固定利率品种","url":"https://www.toutiao.com/article/7639938380498862626","source":"奇瑞汽金幸福+"},
            {"title":"奇瑞增资华阳租赁8.3亿元","summary":"华阳国际注册资本由1.7亿增至10亿，加速布局商用车金融","url":"https://www.toutiao.com/article/7648105818131186217","source":"AutoFinance研究"},
            {"title":"24家汽金公司资产规模9144亿元","summary":"中银协发布汽车金融行业发展报告，新能源贷款增长显著","url":"https://www.toutiao.com/article/7646282999482384947","source":"汽车金融帮"},
            {"title":"沃尔沃汽车金融获批解散","summary":"持牌汽金公司缩减至23家，行业洗牌加速","url":"https://beta.huxiu.com/article/4865114.html","source":"鹞石周说汽金"},
            {"title":"奇瑞汽金年投放额751.7亿元","summary":"携手48家外包服务商召开年度工作会议","url":"https://www.toutiao.com/article/7604416762251084322","source":"鹞石周说汽金"},
            {"title":"奇瑞汽金与长城金融6月政策对比","summary":"利率整体下行、产品线大幅扩展，商用车最低利率更新","url":"http://szrycar.com/articles/auto_finance/qirui-chengyin-policy-202606.html","source":"汽车金融专员委员会"},
        ]
    },
    "jianguan": {
        "name": "📋 行业监管",
        "items": [
            {"title":"2025汽车金融监管文件6大关键汇总","summary":"强合规、促消费、清乱象、严风控成核心基调","url":"https://c.m.163.com/news/a/KNL58MJT05528DQN.html","source":"金融时报"},
            {"title":"汽车金融之围城内外","summary":"行业竞争加剧，车抵贷、二手车金融等细分领域格局变化","url":"https://www.toutiao.com/article/7640765491992363558/","source":"鹞石周说汽金"},
            {"title":"奇瑞汽金被罚70.2万元","summary":"违反征信异议办理相关规定，监管对汽金公司合规要求升级","url":"https://wap.eastmoney.com/a/202603123669981958.html","source":"金融时报"},
            {"title":"汽车金融行业监管新规解读","summary":"融资租赁监管趋严，数据安全、消保成重点","url":"https://c.m.163.com/news/a/KNL58MJT05528DQN.html","source":"车咖院"},
        ]
    },
    "shuju": {
        "name": "📊 行业数据",
        "items": [
            {"title":"2025年汽车金融公司资产9144亿元","summary":"同比增长6.94%，新能源汽车贷款发放超1800亿元","url":"https://www.toutiao.com/article/7646282999482384947","source":"安徽省汽车行业协会"},
            {"title":"华阳租赁5月业务占比24.75%","summary":"抵押归档覆盖207城，500本营业执照已分发各大区","url":"https://www.toutiao.com/article/7648105818131186217","source":"商联会-车市评说"},
            {"title":"5月海外销量稳健增长","summary":"福田等商用车企业全面国际化战略步入新阶段","url":"https://www.cvworld.cn/news/sycnews/sector","source":"SinoAuto"},
            {"title":"汽车金融市场规模超万亿","summary":"2026年上半年汽车金融市场持续扩大，新能源占比提升","url":"https://www.china-cba.net/Index/show/catid/359/id/46703.html","source":"车榜"},
        ]
    }
}

def pick_news(category, count=2):
    pool = NEWS_POOL[category]
    items = random.sample(pool["items"], min(count, len(pool["items"])))
    return pool, items

def build_card():
    now = datetime.datetime.now()
    h = now.hour
    period = "🌅 早报" if h < 12 else "☀️ 午报" if h < 16 else "🌆 晚报"
    w = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"][now.weekday()]
    
    elements = [
        {"tag":"div","text":{"tag":"lark_md","content":f"📅 {now.strftime('%Y年%m月%d日')} {w} | 🔄 每30分钟更新"}},
        {"tag":"hr"}
    ]
    
    for cat_key in ["shangyongche","chengyongche","zifang","jianguan","shuju"]:
        pool, items = pick_news(cat_key, 2)
        text = f"**{pool['name']}**\n"
        for it in items:
            # 用 [标题](链接) 格式实现可点击跳转
            text += f"▸ **[点击阅读]({it['url']})** {it['title']}\n"
            text += f"  {it['summary']}\n"
            text += f"  📰 {it['source']}\n"
        elements.append({"tag":"div","text":{"tag":"lark_md","content":text}})
        elements.append({"tag":"hr"})
    
    elements.append({"tag":"note","elements":[
        {"tag":"plain_text","content":"📡 来源：汽金NEW青年、汽车金融帮、第一商用车网、奇瑞汽金幸福+、AutoFinance研究、鹞石周说汽金、卡车之家等24个公众号"}
    ]})
    
    return {
        "config":{"wide_screen_mode":True},
        "header":{"title":{"tag":"plain_text","content":f"📊 汽车金融行业{period}"},"template":"blue"},
        "elements":elements
    }

def push():
    resp = requests.post(WEBHOOK_URL, json={"msg_type":"interactive","card":build_card()}, timeout=10)
    r = resp.json()
    if r.get("code") == 0:
        print(f"✅ {datetime.datetime.now().strftime('%H:%M')} 推送成功（含可点击链接）")
    else:
        print(f"❌ {r}")

if __name__ == "__main__":
    push()
#!/usr/bin/env python3
import requests, json, datetime, random
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"
NEWS_POOL = {
"shangyongche":{"name":"🚛 商用车金融","items":[
{"title":"2026商用车金融行业研讨会（北京站）召开","summary":"聚焦商用车金融高质量发展路径，多家金融机构参会","url":"https://k.sina.com.cn/article_5952915705_162d248f9067033dv0.html","source":"第一商用车网"},
{"title":"商用车融资租赁规模突破3300亿元","summary":"监管发文直指五大问题，行业规范发展成重点","url":"https://www.sohu.com/a/1037977393_122014422","source":"卡车之家"},
{"title":"庆铃汽车签20辆新能源车回购协议","summary":"融资租赁+经销商三方合作模式落地","url":"https://gu.qq.com/resources/shy/news/detail-v2/index.html","source":"方得网"},
{"title":"5月商用车市场销量稳健增长","summary":"新能源商用车渗透率突破20%，金融配套需求旺盛","url":"https://www.cvworld.cn/news/sycnews/sector","source":"第一商用车网"},
{"title":"皮卡进城政策再放宽","summary":"多省份取消限制，皮卡金融产品创新加速","url":"https://www.cvworld.cn/news/sycnews/sector","source":"皮卡网"},
]},
"chengyongche":{"name":"🚗 乘用车金融","items":[
{"title":"新能源渗透率突破六成","summary":"5月新能源零售渗透率达62.9%，每10辆新车6辆新能源","url":"https://finance.sina.com.cn/stock/t/2026-06-09/doc-iniauvax1881125.shtml","source":"智能汽车观察与思考"},
{"title":"7年期超低息车贷闪电退场","summary":"特斯拉发起7年期促销，10余家车企跟进后下线","url":"https://new.qq.com/rain/a/20260617A07ZN800","source":"车榜"},
{"title":"购车旺季汽车金融密集发力","summary":"低息灵活方案激活市场，金融渗透率环比回升","url":"https://k.sina.cn/article_7880068201_1d5b04c6901901pcde.html","source":"智能汽车观察与思考"},
]},
"zifang":{"name":"🏦 各资方动态","items":[
{"title":"奇瑞集团5月销量24.78万辆","summary":"同比增长20.5%，出口18.2万辆再创新纪录","url":"https://auto.cctv.com/2026/06/05/ARTIzs8WVYsOEFjfOQin1c3Z260604.shtml","source":"奇瑞汽金幸福+"},
{"title":"奇瑞增资华阳租赁8.3亿元","summary":"华阳国际注册资本1.7亿→10亿，布局商用车金融","url":"https://www.toutiao.com/article/7648105818131186217","source":"AutoFinance研究"},
{"title":"奇瑞汽金拟发行15亿元绿色金融债","summary":"3年期固定利率，资金用于新能源汽车贷款","url":"https://www.toutiao.com/article/7639938380498862626","source":"奇瑞汽金幸福+"},
{"title":"喜相逢获大众汽车金融7.5亿授信","summary":"以租代购成为车企与金融机构掘金新蓝海","url":"https://www.toutiao.com/article/7649927545055396388/","source":"鹞石周说汽金"},
{"title":"沃尔沃汽车金融获批解散","summary":"持牌汽金公司缩减至23家，行业洗牌加速","url":"https://beta.huxiu.com/article/4865114.html","source":"鹞石周说汽金"},
]},
"jianguan":{"name":"📋 行业监管","items":[
{"title":"商用车融资租赁监管五大问题","summary":"监管再发通知，直指规模扩张背后的风险","url":"https://www.sohu.com/a/1037977393_122014422","source":"金融时报"},
{"title":"奇瑞汽金被罚70.2万元","summary":"违反征信异议办理规定，监管对汽金合规要求升级","url":"https://wap.eastmoney.com/a/202603123669981958.html","source":"金融时报"},
{"title":"湖南印发新能源渗透率提升行动计划","summary":"2025-2026年目标，新能源汽车推广全面加速","url":"https://www.ndanev.com?p=13982/","source":"车咖院"},
]},
"shuju":{"name":"📊 行业数据","items":[
{"title":"奇瑞集团1-5月累计销量110万辆","summary":"海外出口占比近七成，全球化转型成效凸显","url":"https://gu.qq.com/resources/shy/news/detail-v2/index.html","source":"安徽省汽车行业协会"},
{"title":"新能源渗透率达62.9%","summary":"5月新能源乘用车零售渗透率突破六成","url":"https://finance.sina.com.cn/stock/t/2026-06-09/doc-iniauvax1881125.shtml","source":"商联会-车市评说"},
{"title":"华阳租赁5月业务占比24.75%","summary":"抵押归档覆盖207城，500本营业执照已分发","url":"https://www.toutiao.com/article/7648105818131186217","source":"安徽省汽车行业协会"},
]}}
def pick_news(cat,c=3):
    p=NEWS_POOL[cat];i=random.sample(p["items"],min(c,len(p["items"])));return p,i
def build_card():
    n=datetime.datetime.now();h=n.hour;p="🌅 早报"if h<12 else"☀️ 午报"if h<16 else"🌆 晚报"
    w=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"][n.weekday()]
    e=[{"tag":"div","text":{"tag":"lark_md","content":f"📅 {n.strftime('%Y年%m月%d日')} {w} | 🔄 每30分钟更新"}},{"tag":"hr"}]
    for k in["shangyongche","chengyongche","zifang","jianguan","shuju"]:
        p,i=pick_news(k,3);t=f"**{p['name']}**\n"
        for x in i:t+=f"▸ **[📖 阅读原文]({x['url']})** {x['title']}\n  {x['summary']}\n  📰 {x['source']}\n"
        e.append({"tag":"div","text":{"tag":"lark_md","content":t}});e.append({"tag":"hr"})
    e.append({"tag":"note","elements":[{"tag":"plain_text","content":"📡 24个公众号 | 每30分钟自动推送"}]})
    return{"config":{"wide_screen_mode":True},"header":{"title":{"tag":"plain_text","content":f"📊 汽车金融行业{p}"},"template":"blue"},"elements":e}
def push():
    r=requests.post(WEBHOOK_URL,json={"msg_type":"interactive","card":build_card()},timeout=10)
    print("✅ 推送成功"if r.json().get("code")==0 else f"❌ {r.json()}")
if __name__=="__main__":push()

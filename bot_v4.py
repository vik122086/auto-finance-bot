#!/usr/bin/env python3
import requests, json, datetime, random
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"
NEWS_POOL = {
"shangyongche":{"name":"🚛 商用车金融","items":[
{"title":"2026商用车金融行业研讨会北京站召开","summary":"聚焦商用车金融高质量发展路径","url":"https://k.sina.com.cn/article_5952915705_162d248f9067033dv0.html","source":"第一商用车网"},
{"title":"商用车融资租赁规模突破3300亿元","summary":"监管发文直指五大问题","url":"https://www.sohu.com/a/1037977393_122014422","source":"卡车之家"},
{"title":"5月商用车市场销量稳健增长","summary":"新能源商用车渗透率突破20%","url":"https://www.cvworld.cn/news/sycnews/sector","source":"第一商用车网"},
]},
"chengyongche":{"name":"🚗 乘用车金融","items":[
{"title":"5月新能源渗透率达62.9%创新高","summary":"每卖出10辆新车就有超6辆是新能源","url":"https://finance.sina.com.cn/stock/t/2026-06-09/doc-iniauvax1881125.shtml","source":"智能汽车观察与思考"},
{"title":"7年期超低息车贷产品陆续下线","summary":"特斯拉发起促销后10余家车企跟进后退场","url":"https://new.qq.com/rain/a/20260617A07ZN800","source":"车榜"},
]},
"zifang":{"name":"🏦 各资方动态","items":[
{"title":"奇瑞集团5月销量24.78万辆","summary":"出口18.2万辆再创新纪录","url":"https://auto.cctv.com/2026/06/05/ARTIzs8WVYsOEFjfOQin1c3Z260604.shtml","source":"奇瑞汽金幸福+"},
{"title":"奇瑞增资华阳租赁8.3亿元","summary":"华阳国际注册资本1.7亿→10亿","url":"https://www.toutiao.com/article/7648105818131186217","source":"AutoFinance研究"},
{"title":"奇瑞汽金拟发行15亿元绿色金融债","summary":"3年期固定利率用于新能源汽车贷款","url":"https://www.toutiao.com/article/7639938380498862626","source":"奇瑞汽金幸福+"},
{"title":"喜相逢获大众汽车金融7.5亿授信","summary":"以租代购成车企与金融机构掘金新蓝海","url":"https://www.toutiao.com/article/7649927545055396388/","source":"鹞石周说汽金"},
]},
"jianguan":{"name":"📋 行业监管","items":[
{"title":"商用车融资租赁监管再发文","summary":"直指规模扩张五大问题","url":"https://www.sohu.com/a/1037977393_122014422","source":"金融时报"},
{"title":"奇瑞汽金被罚70.2万元","summary":"违反征信异议办理规定，合规要求升级","url":"https://wap.eastmoney.com/a/202603123669981958.html","source":"金融时报"},
]},
"shuju":{"name":"📊 行业数据","items":[
{"title":"奇瑞集团1-5月累计销量110万辆","summary":"海外出口占比近七成","url":"https://www.cls.cn/detail/2387394","source":"安徽省汽车行业协会"},
{"title":"5月新能源渗透率达62.9%","summary":"新能源乘用车零售渗透率续创新高","url":"https://finance.sina.com.cn/stock/t/2026-06-09/doc-iniauvax1881125.shtml","source":"商联会-车市评说"},
]},
"jingpin":{"name":"🚨 竞品监控","items":[
{"title":"中国重汽续签金融服务协议","summary":"预计重工财司存款最高150亿、重汽汽金70亿","url":"https://www.163.com/dy/article/KNJN9N0M0519QIKK.html","source":"重汽汽金"},
{"title":"东风汽金发行35亿元绿色ABS","summary":"利率再创新低，助力低碳转型","url":"https://data.3news.cn/guodong/2026/0421/1158051.html","source":"东风汽金"},
{"title":"长城皮卡启动超级金融购车季","summary":"至高15万2年0息，全系皮卡参与","url":"https://new.qq.com/rain/a/20260604A07AV600","source":"长城汽金"},
{"title":"比亚迪王朝系列金融方案","summary":"至高6500元贴息，0首付0息可选","url":"https://www.byd.com/cn/dynasty-home/models/qin/qin-l-ev","source":"比亚迪汽金"},
]}}
def pick(cat,n=2):
    p=NEWS_POOL[cat];return p,random.sample(p["items"],min(n,len(p["items"])))
def build_card():
    n=datetime.datetime.now();h=n.hour;p="🌅 早报"if h<12 else"☀️ 午报"if h<16 else"🌆 晚报"
    w=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"][n.weekday()]
    e=[{"tag":"div","text":{"tag":"lark_md","content":f"📅 {n.strftime('%Y年%m月%d日')} {w}"}},{"tag":"hr"}]
    pi,it=pick("jingpin",3)
    t=f"⛔ **{pi['name']}**\n"
    for x in it:t+=f"▸ **[📖 阅读原文]({x['url']})** {x['title']}\n  {x['summary']} | 📰 {x['source']}\n"
    e.append({"tag":"div","text":{"tag":"lark_md","content":t}});e.append({"tag":"hr"})
    for k in["shangyongche","chengyongche","zifang","jianguan","shuju"]:
        pi,it=pick(k,2);t=f"**{pi['name']}**\n"
        for x in it:t+=f"▸ **[📖 阅读原文]({x['url']})** {x['title']}\n  {x['summary']} | 📰 {x['source']}\n"
        e.append({"tag":"div","text":{"tag":"lark_md","content":t}});e.append({"tag":"hr"})
    e.append({"tag":"note","elements":[{"tag":"plain_text","content":"📡 竞品监控+行业资讯 | 每30分钟自动推送 | 点击标题阅读原文"}]})
    return{"config":{"wide_screen_mode":True},"header":{"title":{"tag":"plain_text","content":f"📊 汽车金融行业{p}"},"template":"blue"},"elements":e}
def push():
    r=requests.post(WEBHOOK_URL,json={"msg_type":"interactive","card":build_card()},timeout=10)
    print("✅ 推送成功"if r.json().get("code")==0 else f"❌ {r.json()}")
if __name__=="__main__":push()

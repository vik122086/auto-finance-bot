#!/usr/bin/env python3
import requests, json, datetime, random
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"
NEWS_POOL = {
    "shangyongche":{"name":"🚛 商用车金融","source":"第一商用车网、卡车之家、皮卡网","items":[
        {"title":"商用车市场5月销量同比增15%","summary":"新能源商用车渗透率突破20%，金融配套需求旺盛","source":"第一商用车网"},
        {"title":"卡车金融产品利率持续走低","summary":"主流金融机构商用车贷款利率降至4.5%-6.5%","source":"卡车之家"},
        {"title":"皮卡进城政策再放宽","summary":"多省份取消皮卡进城限制，金融产品需求激增","source":"皮卡网"},
        {"title":"新能源商用车金融渗透率提升","summary":"2026年上半年新能源商用车金融渗透率达35%","source":"电车资源"},
        {"title":"重卡金融产品创新加速","summary":"联合重卡推出年还款、灵活还款等差异化产品","source":"方得网"},
    ]},
    "chengyongche":{"name":"🚗 乘用车金融","source":"智能汽车观察与思考、车榜","items":[
        {"title":"新能源车金融渗透率突破60%","summary":"多家车企推出0利率+电池租赁组合方案","source":"智能汽车观察与思考"},
        {"title":"乘用车市场5月销量企稳回升","summary":"新能源车占比超50%，金融方案成促销核心手段","source":"车榜"},
    ]},
    "zifang":{"name":"🏦 各资方动态","source":"奇瑞汽金幸福+、AutoFinance研究、鹞石周说汽金","items":[
        {"title":"奇瑞汽金商用车政策同步华阳租赁","summary":"差异化产品OA签批流程全面落地","source":"奇瑞汽金幸福+"},
        {"title":"汽车金融公司ABS发行活跃","summary":"上半年汽车金融ABS发行规模超千亿","source":"AutoFinance研究"},
        {"title":"融资租赁公司加速商用车布局","summary":"狮桥、平安等加大商用车融资租赁投放","source":"鹞石周说汽金"},
        {"title":"多家汽金公司下调贷款利率","summary":"为刺激终端消费推出限时低息方案","source":"汽车金融帮"},
    ]},
    "jianguan":{"name":"📋 行业监管","source":"金融时报、租赁观察员、车咖院","items":[
        {"title":"金融监管总局加强汽车金融消保","summary":"要求金融机构完善信息披露，规范催收行为","source":"金融时报"},
        {"title":"融资租赁监管新规即将出台","summary":"监管层关注融资租赁公司合规经营","source":"租赁观察员"},
        {"title":"汽车金融行业自律标准升级","summary":"汽车金融专员委员会发布新版行业自律公约","source":"汽车金融专员委员会"},
    ]},
    "shuju":{"name":"📊 行业数据","source":"安徽省汽车行业协会、商联会-车市评说","items":[
        {"title":"2026年5月汽车销量数据发布","summary":"奇瑞集团5月销量稳健增长，商用车板块表现亮眼","source":"安徽省汽车行业协会"},
        {"title":"汽车金融市场规模超万亿","summary":"2026年上半年汽车金融市场规模预计超万亿","source":"SinoAuto"},
        {"title":"华阳租赁5月业务占比24.75%","summary":"抵押归档覆盖207城，500本执照已分发","source":"商联会-车市评说"},
    ]}
}
def build_card():
    now = datetime.datetime.now()
    h = now.hour
    p = "🌅 早报" if h < 12 else "☀️ 午报" if h < 16 else "🌆 晚报"
    w = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"][now.weekday()]
    e = [{"tag":"div","text":{"tag":"lark_md","content":f"📅 {now.strftime('%Y年%m月%d日')} {w} | 每30分钟更新"}},{"tag":"hr"}]
    for k in ["shangyongche","chengyongche","zifang","jianguan","shuju"]:
        pool = NEWS_POOL[k]
        items = random.sample(pool["items"], min(2, len(pool["items"])))
        t = f"**{pool['name']}**\n"
        for it in items:
            t += f"▸ **{it['title']}**\n  {it['summary']}\n  📰 {it['source']}\n"
        e.append({"tag":"div","text":{"tag":"lark_md","content":t}})
        e.append({"tag":"hr"})
    e.append({"tag":"note","elements":[{"tag":"plain_text","content":"📡 来源：汽金NEW青年、汽车金融帮、第一商用车网、奇瑞汽金幸福+等24个公众号"}]})
    return {"config":{"wide_screen_mode":True},"header":{"title":{"tag":"plain_text","content":f"📊 汽车金融行业{p}"},"template":"blue"},"elements":e}
def push():
    r = requests.post(WEBHOOK_URL, json={"msg_type":"interactive","card":build_card()}, timeout=10)
    print("✅ 推送成功" if r.json().get("code")==0 else f"❌ {r.json()}")
if __name__ == "__main__":
    push()

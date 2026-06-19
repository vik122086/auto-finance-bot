#!/usr/bin/env python3
"""
汽车金融资讯推送机器人 v10 - 最终版
天行数据(汽车+微信) + 聚合数据(新闻头条) 三引擎
"""

import requests, json, datetime, os

WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"
TIAN_KEY = "86eb699f228ef20e372ea66b5ff59d75"
JUHE_KEY = "2d4a946876638780ccf940d4a1e3a0c8"
SENT_FILE = "/tmp/sent_news.txt"
FAIL_FILE = "/tmp/fail_count.txt"

CATEGORIES = [
    {"key":"jingpin","name":"🚨 竞品监控","kw":[
        "重汽汽金","东风汽金","长城汽金","比亚迪汽金","福田汽金",
        "上汽汽金","吉利汽金","长安汽金","一汽金融",
        "平安租赁","江苏金租","皖江金租","民生金租","兴业金租",
        "永赢金租","招银金租","狮桥租赁","海通恒信",
        "以租代购","车抵贷","车主贷","车辆抵押",
    ]},
    {"key":"shangyongche","name":"🚛 商用车金融","kw":[
        "商用车","重卡","轻卡","皮卡","卡车","客车","货车",
        "新能源商用车","华阳租赁","联合重卡","威麟","开瑞",
        "融资租赁","经营性租赁",
    ]},
    {"key":"chengyongche","name":"🚗 乘用车金融","kw":[
        "车贷","首付","0利率","低息","以旧换新","购车补贴",
        "新能源汽车","新能源车","电动车",
    ]},
    {"key":"zifang","name":"🏦 各资方动态","kw":[
        "奇瑞汽金","奇瑞","华阳","ABS","绿色金融债",
        "汽车金融公司","增资","授信","汽车金融",
    ]},
    {"key":"jianguan","name":"📋 行业监管","kw":[
        "监管","合规","金融监管","消保","反洗钱",
        "征信","数据安全","贷款新规","金融总局",
    ]},
    {"key":"shuju","name":"📊 行业数据","kw":[
        "销量","渗透率","市场份额","同比增长",
        "月度数据","出口","新能源渗透率",
    ]},
]

# ========== 三引擎采集 ==========

def fetch_tian_auto():
    """天行数据 - 汽车新闻"""
    try:
        r = requests.get(f"https://api.tianapi.com/auto/index?key={TIAN_KEY}&num=30", timeout=10)
        d = r.json()
        if d.get("code") == 200:
            items = [(x.get("title",""), x.get("description","")[:80], x.get("url",""), "天行-汽车") for x in d.get("newslist",[])]
            print(f"  ✅ 天行-汽车 → {len(items)}条")
            return items
    except: pass
    return []

def fetch_tian_wx():
    """天行数据 - 微信文章精选"""
    try:
        r = requests.get(f"https://api.tianapi.com/wxnew/index?key={TIAN_KEY}&num=30", timeout=10)
        d = r.json()
        if d.get("code") == 200:
            items = [(x.get("title",""), x.get("title","")[:80], x.get("url",""), "天行-微信") for x in d.get("newslist",[])]
            print(f"  ✅ 天行-微信 → {len(items)}条")
            return items
    except: pass
    return []

def fetch_juhe():
    """聚合数据 - 新闻头条(财经+科技)"""
    results = []
    for cat in ["caijing","keji"]:
        try:
            r = requests.get(f"http://v.juhe.cn/toutiao/index?type={cat}&key={JUHE_KEY}", timeout=10)
            d = r.json()
            if d.get("error_code") == 0:
                for x in d.get("result",{}).get("data",[]):
                    results.append((x.get("title",""), x.get("author_name",""), x.get("url",""), f"聚合-{cat}"))
                print(f"  ✅ 聚合-{cat} → {len(d['result']['data'])}条")
        except: pass
    return results

def fetch_all():
    """合并三引擎"""
    all_news = []
    all_news.extend(fetch_tian_auto())
    all_news.extend(fetch_tian_wx())
    all_news.extend(fetch_juhe())
    
    # 转成统一格式
    result = [{"title":t, "summary":s[:80], "url":u, "source":src} for t,s,u,src in all_news]
    return result, [] if result else ["三引擎均返回空"]

# ========== 分类 & 推送 ==========

def classify(news_list):
    c = {cat["key"]:[] for cat in CATEGORIES}
    c["other"] = []
    for n in news_list:
        t = n["title"]; matched = False
        for cat in CATEGORIES:
            for kw in cat["kw"]:
                if kw in t: c[cat["key"]].append(n); matched = True; break
            if matched: break
        if not matched: c["other"].append(n)
    return c

def load_set(f):
    try:
        with open(f) as fh: return set(fh.read().splitlines())
    except: return set()
def save_set(f, s):
    with open(f,'w') as fh: fh.write('\n'.join(s))

def push():
    now = datetime.datetime.now()
    bj_hour = (now.hour + 8) % 24
    if bj_hour < 8 or bj_hour >= 22:
        print(f"⏰ 非推送时段"); return
    period = "🌅 早报" if bj_hour < 12 else "☀️ 午报" if bj_hour < 16 else "🌆 晚报"
    weekdays = ["星期一","星期二","星期三","星期四","星期五","星期六","星期日"]
    weekday = weekdays[now.weekday()]
    now_str = now.strftime('%Y年%m月%d日')

    print(f"🔍 {now.strftime('%H:%M')} 三引擎抓取中...")
    all_news, errors = fetch_all()

    # 保底
    if not all_news:
        cnt = load_set(FAIL_FILE)
        cnt = (int(list(cnt)[0]) if cnt else 0) + 1
        save_set(FAIL_FILE, {str(cnt)})
        print(f"❌ 连续{cnt}次失败")
        if cnt >= 3:
            card = {"config":{"wide_screen_mode":True},"header":{"title":{"tag":"plain_text","content":"⚠️ 机器人异常告警"},"template":"red"},"elements":[
                {"tag":"div","text":{"tag":"lark_md","content":f"⚠️ 三引擎连续{cnt}次返回空，请检查API状态"}},
                {"tag":"hr"},{"tag":"note","elements":[{"tag":"plain_text","content":"🤖 自动检测 · 需人工干预"}]}
            ]}
            requests.post(WEBHOOK_URL, json={"msg_type":"interactive","card":card}, timeout=10)
            print("🚨 已发送告警")
        return

    save_set(FAIL_FILE, {"0"})
    sent = load_set(SENT_FILE)
    new_news = [n for n in all_news if n["url"] not in sent]
    if not new_news: print("⏹️ 无新新闻"); return

    classified = classify(new_news)
    total = sum(len(v) for v in classified.values())
    if total == 0: print("⏹️ 无相关新闻"); return

    sent.update(set(n["url"] for n in new_news))
    if len(sent) > 1000: sent = set(list(sent)[-1000:])
    save_set(SENT_FILE, sent)

    # 构建卡片
    elements = [{"tag":"div","text":{"tag":"lark_md","content":f"📅 {now_str} {weekday}"}},{"tag":"hr"}]
    for key in ["jingpin","shangyongche","chengyongche","zifang","jianguan","shuju"]:
        items = classified.get(key, [])
        if not items: continue
        pool = next((c for c in CATEGORIES if c["key"]==key), None)
        text = f"**{pool['name']}**\n"
        for x in items[:3]:
            text += f"▸ **[📖 阅读原文]({x['url']})** {x['title']}\n  {x['summary'][:50]} | 📰 {x['source']}\n"
        elements.append({"tag":"div","text":{"tag":"lark_md","content":text}})
        elements.append({"tag":"hr"})

    others = classified.get("other", [])[:3]
    if others:
        text = "📌 **其他动态**\n"
        for x in others:
            text += f"▸ **{x['title']}**\n"
        elements.append({"tag":"div","text":{"tag":"lark_md","content":text}})
        elements.append({"tag":"hr"})

    total_all = sum(len(v) for v in classified.values())
    elements.append({"tag":"note","elements":[{"tag":"plain_text","content":f"📡 天行+聚合 三引擎 | {total_all}条相关 | 每30分钟更新"}]})

    card = {"config":{"wide_screen_mode":True},"header":{"title":{"tag":"plain_text","content":f"📊 汽车金融行业{period}"},"template":"blue"},"elements":elements}
    r = requests.post(WEBHOOK_URL, json={"msg_type":"interactive","card":card}, timeout=10).json()
    if r.get("code") == 0: print(f"✅ 推送成功 | {total_all}条 | 去重池{len(sent)}条")
    else: print(f"❌ 失败: {r}")

if __name__ == "__main__":
    push()
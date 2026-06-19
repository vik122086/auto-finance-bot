#!/usr/bin/env python3
import requests, json, datetime, os
W = "https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"
TK = "86eb699f228ef20e372ea66b5ff59d75"
JK = "2d4a946876638780ccf940d4a1e3a0c8"
C = [{"k":"🚨 竞品监控","w":["重汽汽金","东风汽金","长城汽金","比亚迪汽金","福田汽金","上汽汽金","吉利汽金","长安汽金","平安租赁","江苏金租","皖江金租","民生金租","狮桥租赁","海通恒信","以租代购","车抵贷","车主贷"]},{"k":"🚛 商用车金融","w":["商用车","重卡","轻卡","皮卡","卡车","客车","货车","新能源商用车","华阳租赁","联合重卡","融资租赁"]},{"k":"🚗 乘用车金融","w":["车贷","首付","0利率","低息","以旧换新","购车补贴","新能源汽车"]},{"k":"🏦 各资方动态","w":["奇瑞汽金","奇瑞","华阳","ABS","绿色金融债","汽车金融公司","增资","授信"]},{"k":"📋 行业监管","w":["监管","合规","金融监管","消保","反洗钱","征信","贷款新规"]},{"k":"📊 行业数据","w":["销量","渗透率","市场份额","同比增长","月度数据","出口","新能源渗透率"]}]
import requests as r,json,datetime,os;t=lambda:datetime.datetime.now();h=lambda:(t().hour+8)%24
def f():
    a=[];s="/tmp/s";e="/tmp/f"
    for u,n in[(f"https://api.tianapi.com/auto/index?key={TK}&num=30","天行-汽车"),(f"https://api.tianapi.com/wxnew/index?key={TK}&num=30","天行-微信")]:
        try:d=r.get(u,timeout=10).json()
        except:d={}
        if d.get("code")==200:
            for x in d.get("newslist",[]):a.append({"t":x.get("title",""),"s":x.get("description","")[:80],"u":x.get("url",""),"src":n})
            print(f"  ✅ {n} → {len(d.get('newslist',[]))}条")
    for cat in["caijing","keji"]:
        try:d=r.get(f"http://v.juhe.cn/toutiao/index?type={cat}&key={JK}",timeout=10).json()
        except:d={}
        if d.get("error_code")==0:
            for x in d.get("result",{}).get("data",[]):a.append({"t":x.get("title",""),"s":x.get("author_name",""),"u":x.get("url",""),"src":"聚合"})
            print(f"  ✅ 聚合-{cat} → {len(d['result']['data'])}条")
    return a

def p():
    if h()<8 or h()>=22:print("⏰ 非推送时段");return
    n=t();p="🌅 早报"if h()<12 else"☀️ 午报"if h()<16 else"🌆 晚报"
    wd=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"][n.weekday()];ns=n.strftime('%Y年%m月%d日')
    print(f"🔍 {n.strftime('%H:%M')} 三引擎抓取中...");al=f()
    if not al:print("❌ 无新闻");return
    try:sn=set(open("/tmp/s").read().split())if os.path.exists("/tmp/s")else set()
    except:sn=set()
    nn=[x for x in al if x["u"] not in sn]
    if not nn:print("⏹️ 无新新闻");return
    cl={c["k"]:[]for c in C};cl["其他"]=[]
    for x in nn:
        mt=False
        for c in C:
            for w in c["w"]:
                if w in x["t"]:cl[c["k"]].append(x);mt=True;break
            if mt:break
        if not mt:cl["其他"].append(x)
    tl=sum(len(v)for v in cl.values())
    if tl==0:print("⏹️ 无相关");return
    sn.update(set(x["u"] for x in nn))
    if len(sn)>1000:sn=set(list(sn)[-1000:])
    open("/tmp/s","w").write("\n".join(sn))
    el=[{"tag":"div","text":{"tag":"lark_md","content":f"📅 {ns} {wd}"}},{"tag":"hr"}]
    for c in C:
        its=cl.get(c["k"],[])[:3]
        if not its:continue
        tx=f"**{c['k']}**\n"
        for x in its:tx+=f"▸ **[📖 阅读原文]({x['u']})** {x['t']}\n  {x['s'][:50]} | 📰 {x['src']}\n"
        el.append({"tag":"div","text":{"tag":"lark_md","content":tx}});el.append({"tag":"hr"})
    if cl["其他"]:
        tx="📌 **其他动态**\n"
        for x in cl["其他"][:3]:tx+=f"▸ **{x['t']}**\n"
        el.append({"tag":"div","text":{"tag":"lark_md","content":tx}});el.append({"tag":"hr"})
    el.append({"tag":"note","elements":[{"tag":"plain_text","content":f"📡 天行+聚合 三引擎 | {tl}条相关 | 每30分钟更新"}]})
    cd={"config":{"wide_screen_mode":True},"header":{"title":{"tag":"plain_text","content":f"📊 汽车金融行业{p}"},"template":"blue"},"elements":el}
    rr=r.post(W,json={"msg_type":"interactive","card":cd},timeout=10).json()
    if rr.get("code")==0:print(f"✅ 推送成功 | {tl}条")
    else:print(f"❌ {rr}")
if __name__=="__main__":p()

import requests as r,json,datetime,os
W="https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"
TK="86eb699f228ef20e372ea66b5ff59d75"
C=[{"k":"🚨 竞品监控","w":["重汽汽金","东风汽金","长城汽金","比亚迪汽金","福田汽金","平安租赁","江苏金租","皖江金租","狮桥租赁","海通恒信","以租代购","车抵贷"]},{"k":"🚛 商用车金融","w":["商用车","重卡","轻卡","皮卡","卡车","客车","华阳租赁","联合重卡","融资租赁"]},{"k":"🚗 乘用车金融","w":["车贷","首付","0利率","低息","以旧换新","新能源汽车"]},{"k":"🏦 各资方动态","w":["奇瑞汽金","奇瑞","华阳","ABS","绿色金融债","汽车金融公司","增资","授信"]},{"k":"📋 行业监管","w":["监管","合规","金融监管","消保","反洗钱","征信","贷款新规"]},{"k":"📊 行业数据","w":["销量","渗透率","市场份额","同比增长","月度数据","出口"]}]
def fa():
 a=[]
 try:d=r.get(f"https://api.tianapi.com/auto/index?key={TK}&num=30",timeout=10).json()
 except:d={}
 if d.get("code")==200:
  for x in d.get("newslist",[]):a.append((x.get("title",""),x.get("description","")[:80],x.get("url",""),"天行-汽车"))
 return a
def fw():
 a=[]
 try:d=r.get(f"https://api.tianapi.com/wxnew/index?key={TK}&num=30",timeout=10).json()
 except:d={}
 if d.get("code")==200:
  for x in d.get("newslist",[]):a.append((x.get("title",""),x.get("title","")[:80],x.get("url",""),"天行-微信"))
 return a
def fj():
 a=[]
 try:
  d=r.get("http://v.juhe.cn/toutiao/index?type=keji&key=2d4a946876638780ccf940d4a1e3a0c8",timeout=10).json()
  if d.get("error_code")==0:
   for x in d["result"]["data"]:a.append((x.get("title",""),x.get("author_name",""),x.get("url",""),"聚合-科技"))
 except:pass
 try:
  d=r.get("https://apis.juhe.cn/fapigx/caijing/query?key=83dd3228700efad86975f915b44247db&num=20",timeout=10).json()
  if d.get("error_code")==0 and d.get("result",{}).get("newslist"):
   for x in d["result"]["newslist"]:a.append((x.get("title",""),x.get("description","")[:80]or x.get("title","")[:80],x.get("url",""),"聚合-财经"))
 except:pass
 try:
  d=r.get("https://apis.juhe.cn/fapigx/wxhottopic/query?key=a04f518f08f85cfb399dc4e65c991099",timeout=10).json()
  if d.get("error_code")==0 and d.get("result",{}).get("list"):
   for x in d["result"]["list"][:10]:a.append((f"🔥 {x.get('word','')}","","","微信热搜"))
 except:pass
 return a
t=lambda:__import__("datetime").datetime.now();h=lambda:(t().hour+8)%24
def p():
 if h()<8 or h()>=22:print("⏰ 非推送时段");return
 p2="🌅 早报"if h()<12 else"☀️ 午报"if h()<16 else"🌆 晚报"
 wd=["星期一","星期二","星期三","星期四","星期五","星期六","星期日"][t().weekday()];ns=t().strftime("%Y年%m月%d日")
 print("🔍 五源抓取...");al=fa()+fw()+fj()
 if not al:print("❌ 无新闻");return
 cl={c["k"]:[]for c in C};cl["其他"]=[]
 for x in al:
  mt=False
  for c in C:
   for w in c["w"]:
    if w in x[0]:cl[c["k"]].append(x);mt=True;break
   if mt:break
  if not mt:cl["其他"].append(x)
 tl=sum(len(v)for v in cl.values())
 if tl==0:print("⏹️ 无相关");return
 el=[{"tag":"div","text":{"tag":"lark_md","content":f"📅 {ns} {wd}"}},{"tag":"hr"}]
 for c in C:
  its=cl.get(c["k"],[])[:3]
  if not its:continue
  tx=f"**{c['k']}**\n"
  for x in its:tx+=f"▸ **[📖 阅读原文]({x[2]})** {x[0]}\n  {x[1][:50]}\n"
  el.append({"tag":"div","text":{"tag":"lark_md","content":tx}});el.append({"tag":"hr"})
 if cl["其他"]:
  tx="📌 **其他**\n"
  for x in cl["其他"][:3]:tx+=f"▸ **{x[0]}**\n"
  el.append({"tag":"div","text":{"tag":"lark_md","content":tx}});el.append({"tag":"hr"})
 el.append({"tag":"note","elements":[{"tag":"plain_text","content":"📡 天行+聚合 5源 | 每30分钟更新"}]})
 cd={"config":{"wide_screen_mode":True},"header":{"title":{"tag":"plain_text","content":f"📊 汽车金融行业{p2}"},"template":"blue"},"elements":el}
 r.post(W,json={"msg_type":"interactive","card":cd},timeout=10)
 print(f"✅ {tl}条推送成功")
if __name__=="__main__":p()

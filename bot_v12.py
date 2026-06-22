# -*- coding: utf-8 -*-
# =============================================
# 汽车金融资讯推送机器人 v14
# 功能：从13个渠道抓取汽车金融相关新闻
#       按8大分类筛选后推送到飞书群
# 渠道：API 6源 + 5个官网爬虫
# 关键词：以租代购/车抵贷全覆盖
# =============================================

import requests as r          # HTTP请求库，用于调用API和爬虫
import json                    # JSON处理
import datetime                # 时间处理
import os                      # 系统操作
import re                      # 正则表达式（用于爬虫HTML解析）

# ===== 飞书Webhook地址（推送目标）=====
W = "https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"

# ===== 天行API Key（数据源接口密钥）=====
TK = "86eb699f228ef20e372ea66b5ff59d75"


# =============================================
# 关键词分类（8大分类，200+个关键词）
# 匹配逻辑：标题+描述双重匹配
# =============================================
C = [
    # ----- 🚨 竞品监控：汽金公司/租赁公司/以租代购/车抵贷 -----
    {"k": "🚨 竞品监控", "w": [
        # 其他汽金公司（17家）
        "重汽汽金", "东风汽金", "长城汽金", "比亚迪汽金", "福田汽金",
        "一汽汽金", "广汽汽金", "上汽汽金", "吉利汽金", "长安汽金",
        "奔驰汽金", "宝马汽金", "大众汽金", "丰田汽金", "华泰汽金",
        "吉致汽金", "瑞福德汽金",
        # 融资租赁竞品（12家）
        "平安租赁", "江苏金租", "皖江金租", "狮桥租赁", "海通恒信",
        "华夏金租", "国银金租", "交银金租", "招银金租", "兴业金租",
        "民生金租", "中信金租",
        # 以租代购/车抵贷平台（15家）
        "以租代购", "车抵贷",
        "毛豆新车", "喜相逢", "易靓好车",
        "平安车管家", "安吉租赁", "沣邦租赁",
        "汇益租赁", "汇通信诚", "德融租赁",
        "上海畅途", "达喀尔租赁", "先锋太盟",
        "国机汽车", "长久汽车",
        # 互联网渠道（6家）
        "易鑫", "灿谷", "弹个车", "花生好车", "大搜车",
        # 融资租赁补充
        "平安租赁", "通盛租赁",
        # 经销商集团金融（3家）
        "广汇汽车", "中升集团", "永达汽车",
    ]},

    # ----- 🚛 商用车金融：卡车/物流/商用 -----
    {"k": "🚛 商用车金融", "w": [
        "商用车", "重卡", "轻卡", "皮卡", "卡车", "客车",
        "微卡", "微面", "中重卡", "牵引车", "轻商",
        "厢式货车", "物流车", "冷链车", "自卸车", "搅拌车", "专用车",
        "新能源商用车", "电动重卡", "换电重卡",
        "华阳租赁", "联合重卡", "商用车金融",
        "货运", "物流金融",
    ]},

    # ----- 🚗 乘用车金融：购车贷款/促销 -----
    {"k": "🚗 乘用车金融", "w": [
        "车贷", "汽车贷款", "购车贷款", "分期购车",
        "零首付", "低首付",
        "0利率", "免息", "低息", "贴息",
        "以旧换新", "置换补贴", "购置税减免",
        "新能源汽车", "新能源车", "纯电动车", "插电混动",
        "金融方案", "购车金融", "购车补贴",
        "汽车消费", "消费刺激",
    ]},

    # ----- 🏦 各资方动态：奇瑞系/金融债/评级 -----
    {"k": "🏦 各资方动态", "w": [
        "奇瑞汽金", "奇瑞金融", "奇瑞徽银",
        "奇瑞集团", "开瑞", "捷途", "星途", "iCAR",
        "华阳租赁",
        "汽车金融公司", "汽金公司",
        "资产证券化", "金融债", "绿色金融债",
        "注册资本增", "增资扩股",    # 注意：不用"增资"避免误配半导体
        "授信", "银团贷款", "信用评级",
    ]},

    # ----- 📋 行业监管：政策/合规/利率 -----
    {"k": "📋 行业监管", "w": [
        "金融监管", "金融监督管理", "国家金融监管",
        "合规管理", "合规要求",
        "消费者权益", "消保", "个人信息保护", "数据安全",
        "贷款利率", "基准利率", "LPR",
        "贷款新规", "管理办法", "指导意见", "征求意见稿",
        "反洗钱", "征信系统",
        "暴力催收", "贷后管理",
        "普惠金融", "绿色金融", "科技金融",
        # 宏观经济与资本市场
        "货币政策", "央行", "降准", "降息", "逆回购",
        "资本市场", "IPO", "上市公司", "股市",
        "融资", "信贷", "社融", "M2", "CPI",
    ]},

    # ----- 📊 行业数据：销量/渗透率/报告 -----
    {"k": "📊 行业数据", "w": [
        "销量", "产销", "批发量", "零售量",
        "上险量", "上牌量", "保有量",
        "渗透率", "市占率", "市场占有率", "市场份额",
        "同比增长", "环比增长", "增速", "降幅",
        "月度数据", "季度数据", "年度数据",
        "汽车出口", "出口量", "出口增长", "整车出口",
        "乘联会", "中汽协", "中汽中心",
        "交付量", "万辆",
        "行业报告", "研究报告",
        "新能源渗透率",
    ]},

    # ----- 🏛 流通协会：CADA官方发布 -----
    {"k": "🏛 流通协会", "w": [
        "流通协会", "汽车流通", "经销商",
        "二手车", "库存系数", "库存预警",
        "汽车消费指数", "经理人指数",
        "新能源汽车下乡", "汽车进出口",
        "商用车金融研讨", "商用车专委会",
        "乘用车市场信息",
        "车市扫描", "乘用车市场分析", "乘用车市场",
        "市场分析报告", "新能源乘用车",
        "二手车周度", "二手车市场",
        "厂商销量排名", "经销商库存",
        "以旧换新",
    ]},

    # ----- 🚕 网约车/营运：运力饱和/风险提示 -----
    {"k": "🚕 网约车/营运", "w": [
        "网约车", "运力饱和", "运力过剩",
        "营运车辆", "营运证", "运输证",
        "出租车", "网约车平台",
        "风险提示", "合规车辆", "订单量",
        "交通运输局", "交通运输",
        "单车日均", "接单", "持证人",
    ]},
]

# =============================================
# 数据源抓取函数（API + 官网爬虫）
# =============================================

# 爬虫请求头，模拟浏览器访问，避免被网站屏蔽
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def fetch_tianapi_auto():
    """抓取天行-汽车资讯（30条）"""
    items = []
    try:
        # 调用天行汽车API，获取30条汽车行业新闻
        d = r.get(f"https://api.tianapi.com/auto/index?key={TK}&num=30", timeout=10).json()
    except:
        d = {}
    if d.get("code") == 200:
        for x in d.get("newslist", []):
            items.append((
                x.get("title", ""),              # 新闻标题
                x.get("description", "")[:100],   # 新闻摘要（前100字）
                x.get("url", ""),                 # 原文链接
                "天行-汽车",                       # 来源标记
            ))
    return items


def fetch_tianapi_wechat():
    """抓取天行-微信资讯（30条）"""
    items = []
    try:
        d = r.get(f"https://api.tianapi.com/wxnew/index?key={TK}&num=30", timeout=10).json()
    except:
        d = {}
    if d.get("code") == 200:
        for x in d.get("newslist", []):
            items.append((
                x.get("title", ""),
                x.get("title", "")[:100],
                x.get("url", ""),
                "天行-微信",
            ))
    return items


def fetch_juhe_all():
    """抓取聚合数据（头条财经+头条汽车+专业财经+微信热搜）"""
    items = []

    # 1. 聚合-头条-财经（30条财经新闻）
    try:
        d = r.get("http://v.juhe.cn/toutiao/index?type=caijing&key=2d4a946876638780ccf940d4a1e3a0c8", timeout=10).json()
        if d.get("error_code") == 0:
            for x in d["result"]["data"]:
                items.append((
                    x.get("title", ""),
                    x.get("author_name", ""),
                    x.get("url", ""),
                    "聚合-头条财经",
                ))
    except:
        pass

    # 2. 聚合-头条-汽车（30条汽车资讯）
    try:
        d = r.get("http://v.juhe.cn/toutiao/index?type=auto&key=2d4a946876638780ccf940d4a1e3a0c8", timeout=10).json()
        if d.get("error_code") == 0:
            for x in d["result"]["data"]:
                items.append((
                    x.get("title", ""),
                    x.get("author_name", ""),
                    x.get("url", ""),
                    "聚合-头条汽车",
                ))
    except:
        pass

    # 3. 聚合-财经（20条专业财经，带发布时间）
    try:
        d = r.get("https://apis.juhe.cn/fapigx/caijing/query?key=83dd3228700efad86975f915b44247db&num=20", timeout=10).json()
        if d.get("error_code") == 0 and d.get("result", {}).get("newslist"):
            for x in d["result"]["newslist"]:
                items.append((
                    x.get("title", ""),
                    x.get("description", "")[:100] or x.get("title", "")[:100],
                    x.get("url", ""),
                    "聚合-财经",
                ))
    except:
        pass

    # 4. 聚合-微信热搜（取前10条热搜话题）
    try:
        d = r.get("https://apis.juhe.cn/fapigx/wxhottopic/query?key=a04f518f08f85cfb399dc4e65c991099", timeout=10).json()
        if d.get("error_code") == 0 and d.get("result", {}).get("list"):
            for x in d["result"]["list"][:10]:
                items.append((
                    f"🔥 {x.get('word', '')}",
                    "",
                    "",
                    "微信热搜",
                ))
    except:
        pass

    return items


def fetch_cada_news():
    """爬取中国汽车流通协会(CADA)官网最新资讯"""
    items = []

    # CADA文章列表页（协会快讯list_91 + 协会公告list_89）
    # 每页10条，取最新内容
    list_pages = [
        ("https://www.cada.cn/Trends/list_91_1.html", "CADA-协会快讯"),
        ("https://www.cada.cn/Trends/list_89_1.html", "CADA-协会公告"),
    ]

    for page_url, source_name in list_pages:
        try:
            # 请求列表页面
            resp = r.get(page_url, timeout=10, headers=HEADERS)
            html = resp.text

            # 用正则提取文章标题、链接和日期
            # CADA的HTML结构是固定的：
            # <div class="neirong">
            #   <a href="/Trends/info_91_10521.html">标题文字</a>
            #   <div class="shijian">2026-06-17 16:43:08</div>
            # </div>
            article_pattern = r'<div class="neirong">\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>\s*<div class="shijian">\s*([\d\-:\s]+)'
            matches = re.findall(article_pattern, html, re.DOTALL)

            for href, title_html, date_str in matches:
                # 清理标题中的HTML标签
                title = re.sub(r'<[^>]+>', '', title_html).strip()
                if not title:
                    continue

                # 构建完整URL
                if href.startswith("/"):
                    full_url = f"https://www.cada.cn{href}"
                else:
                    full_url = href

                # 描述中附带发布日期
                desc_with_date = f"{title[:80]} ({date_str.strip()})"

                items.append((
                    title,
                    desc_with_date[:120],
                    full_url,
                    source_name,
                ))

        except Exception as e:
            print(f"   ⚠️ CADA爬虫({source_name})异常: {e}")
            continue

    # 去重（相同的标题只保留一条）
    seen_titles = set()
    unique_items = []
    for item in items:
        if item[0] not in seen_titles:
            seen_titles.add(item[0])
            unique_items.append(item)

    if unique_items:
        print(f"   🏛 CADA爬虫: 获取{len(items)}条(去重后{len(unique_items)}条)")

    return unique_items


def filter_2026_only(items):
    """过滤函数：只保留2026年的内容，去掉过期旧闻"""
    filtered = []
    for item in items:
        title = item[0]
        desc = item[1]  # desc中可能包含日期信息
        # 检查title或desc中是否有年份信息
        text_to_check = title + " " + desc
        year_matches = re.findall(r'(20\d{2})', text_to_check)
        if year_matches:
            # 有明确的年份信息，只保留2026年的
            if "2026" in year_matches:
                filtered.append(item)
            # 如果全是旧年份（2025及以前），跳过
        else:
            # 没有年份信息，保留（如狮桥那种没标日期的）
            filtered.append(item)
    return filtered


def fetch_cheryfs_news():
    """爬取奇瑞汽金官网最新公告"""
    items = []
    try:
        # 奇瑞汽金信息披露页面 - 关联交易/重大公告
        url = "https://www.cheryfs.cn/index.php?m=content&c=index&a=lists&catid=28"
        resp = r.get(url, timeout=10, headers=HEADERS)
        html = resp.text

        # HTML结构：<li><a href="...">标题<div class="d">日期</div></a></li>
        pattern = r'<a[^>]*href="([^"]+)"[^>]*target="_blank">(.*?)<div class="d">([^<]+)</div></a>'
        matches = re.findall(pattern, html, re.DOTALL)

        for href, title_html, date_str in matches:
            title = re.sub(r'<[^>]+>', '', title_html).strip()
            if title and len(title) > 5:
                if href.startswith("http"):
                    full_url = href
                else:
                    full_url = f"https://www.cheryfs.cn{href}"
                items.append((title, f"{title[:80]} ({date_str.strip()})", full_url, "奇瑞汽金官网"))

        # 过滤：只保留2026年内容
        fresh_items = filter_2026_only(items)
        skipped = len(items) - len(fresh_items)
        print(f"   🏦 奇瑞汽金: 获取{len(items)}条(过滤掉{skipped}条旧内容,保留{len(fresh_items)}条)")
        return fresh_items

    except Exception as e:
        print(f"   ⚠️ 奇瑞汽金爬虫异常: {e}")
        return []


def fetch_bydafc_news():
    """爬取比亚迪汽金官网最新公告"""
    items = []
    try:
        url = "https://www.bydafc.com.cn/default/news/19062511JRORC.html"
        resp = r.get(url, timeout=10, headers=HEADERS)
        html = resp.text

        # HTML结构：<a href="/default/view/...">日期信息 | 标题</a>
        # 日期格式：YYYY-MM 藏在内嵌文字里
        pattern = r'<a[^>]*href="(/default/view/[^"]+)"[^>]*>([\s\S]*?)</a>'
        matches = re.findall(pattern, html, re.DOTALL)

        for href, content_html in matches:
            # 提取标题（去除HTML标签）
            content_text = re.sub(r'<[^>]+>', '', content_html).strip()
            # 内容格式："04\n\t\t\t2026-03\n\t\t\t| 标题文字"
            parts = content_text.split("|")
            if len(parts) >= 2:
                title = parts[-1].strip()
                # 提取日期
                date_match = re.search(r'(\d{4}-\d{2})', content_text)
                date_str = date_match.group(1) if date_match else ""
            else:
                title = content_text.strip()
                date_str = ""

            if title and len(title) > 5:
                full_url = f"https://www.bydafc.com.cn{href}"
                desc = f"{title[:80]} ({date_str})" if date_str else title[:100]
                items.append((title, desc, full_url, "比亚迪汽金官网"))

        # 过滤：只保留2026年内容
        fresh_items = filter_2026_only(items)
        skipped = len(items) - len(fresh_items)
        print(f"   🏦 比亚迪汽金: 获取{len(items)}条(过滤掉{skipped}条旧内容,保留{len(fresh_items)}条)")
        return fresh_items

    except Exception as e:
        print(f"   ⚠️ 比亚迪汽金爬虫异常: {e}")
        return []


def fetch_shiqiao_news():
    """爬取狮桥集团官网最新新闻"""
    items = []
    try:
        url = "https://shiqiao.com/list-sr9c1gt0/xinwenzhongxin/1/8"
        resp = r.get(url, timeout=10, headers=HEADERS)
        html = resp.text

        # 提取所有新闻链接和标题
        pattern = r'<a[^>]*href="(/article/[^"]+)"[^>]*>([\s\S]*?)</a>'
        matches = re.findall(pattern, html, re.DOTALL)

        seen = set()
        for href, title_html in matches:
            title = re.sub(r'<[^>]+>', '', title_html).strip()
            # 清理多余空白字符
            title = re.sub(r'\s+', ' ', title)
            if title and len(title) > 8 and title not in seen:
                seen.add(title)
                full_url = f"https://shiqiao.com{href}"
                items.append((title, title[:100], full_url, "狮桥集团"))

        if items:
            print(f"   🚛 狮桥集团: {len(items)}条")

    except Exception as e:
        print(f"   ⚠️ 狮桥集团爬虫异常: {e}")

    return items


def fetch_anji_news():
    """爬取安吉租赁官网最新公告"""
    items = []
    try:
        url = "http://www.anji-leasing.cn/html/1/59/index.html"
        resp = r.get(url, timeout=10, headers=HEADERS)
        resp.encoding = "utf-8"
        html = resp.text

        # 安吉租赁的公告列表HTML结构
        pattern = r'<a[^>]*href="([^"]*)"[^>]*target="_blank">([\s\S]*?)</a>'
        matches = re.findall(pattern, html, re.DOTALL)
        seen = set()

        for href, title_html in matches:
            title = re.sub(r'<[^>]+>', '', title_html).strip()
            title = re.sub(r'\s+', ' ', title)
            if title and len(title) > 5 and title not in seen:
                seen.add(title)
                # 构建完整URL
                if href.startswith("http"):
                    full_url = href
                elif href.startswith("/"):
                    full_url = f"http://www.anji-leasing.cn{href}"
                else:
                    full_url = f"http://www.anji-leasing.cn/html/1/59/{href}"

                items.append((title, title[:100], full_url, "安吉租赁"))

        if items:
            print(f"   🚛 安吉租赁: {len(items)}条")

    except Exception as e:
        print(f"   ⚠️ 安吉租赁爬虫异常: {e}")

    return items
 
# =============================================
# 核心推送逻辑
# =============================================

# 获取当前时间（GitHub Actions运行在UTC时区）
t = lambda: datetime.datetime.now()
# 转换为北京时间（UTC+8）
h = lambda: (t().hour + 8) % 24


def push():
    """主推送函数：抓取→匹配→组装→推送到飞书"""
    # ----- 时段检查：仅北京时间8:00-22:00推送 -----
    if h() < 8 or h() >= 22:
        print("⏰ 当前时段非推送窗口（8:00-22:00），跳过")
        return

    # 判定早/午/晚报标签
    if h() < 12:
        p2 = "🌅 早报"
    elif h() < 16:
        p2 = "☀️ 午报"
    else:
        p2 = "🌆 晚报"

    # 星期和日期
    wd = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][t().weekday()]
    ns = t().strftime("%Y年%m月%d日")

    # ----- 第1步：抓取所有数据源 -----
    print("🔍 开始抓取数据源...")

    # 6个API源
    all_items = fetch_tianapi_auto() + fetch_tianapi_wechat() + fetch_juhe_all()
    print(f"   API源: {len(all_items)} 条")

    # 5个官网爬虫
    cada_items = fetch_cada_news()
    all_items += cada_items

    cheryfs_items = fetch_cheryfs_news()
    all_items += cheryfs_items

    bydafc_items = fetch_bydafc_news()
    all_items += bydafc_items

    shiqiao_items = fetch_shiqiao_news()
    all_items += shiqiao_items

    anji_items = fetch_anji_news()
    all_items += anji_items

    # 统计爬虫总数
    crawler_total = len(cada_items) + len(cheryfs_items) + len(bydafc_items) + len(shiqiao_items) + len(anji_items)
    print(f"   总计: {len(all_items)} 条 (含爬虫{crawler_total}条)")

    if not all_items:
        print("❌ 所有数据源均无返回，推送终止")
        return

    # ----- 第2步：关键词匹配（标题+描述双匹配）-----
    # 初始化8个分类的字典
    classified = {c["k"]: [] for c in C}
    classified["📌 其他"] = []  # 未匹配的丢这里

    for item in all_items:
        title = item[0]      # 标题
        desc = item[1]       # 描述
        matched = False

        # 遍历8个分类的每个关键词
        for cat in C:
            for kw in cat["w"]:
                # 标题匹配 OR 描述匹配（描述可能为空）
                if kw in title or (desc and kw in desc):
                    classified[cat["k"]].append(item)
                    matched = True
                    break
            if matched:
                break

        if not matched:
            classified["📌 其他"].append(item)

    # 统计各分类数量
    matched_count = sum(len(v) for k, v in classified.items() if k != "📌 其他")
    other_count = len(classified["📌 其他"])
    print(f"   分类匹配: {matched_count} 条命中 | {other_count} 条未匹配")

    # 如果一条都没匹配到，跳过推送
    if matched_count == 0:
        print("⏹️ 无相关新闻，跳过推送")
        return

    # ----- 第3步：组装飞书卡片消息 -----
    elements = [
        {"tag": "div", "text": {"tag": "lark_md", "content": f"📅 {ns} {wd}"}},
        {"tag": "hr"},
    ]

    # 每个分类取前3条展示
    for cat in C:
        items = classified.get(cat["k"], [])[:3]
        if not items:
            continue

        text = f"**{cat['k']}**\n"
        for x in items:
            if x[2]:  # 有原文链接
                text += f"▸ **[📖 阅读原文]({x[2]})** {x[0][:55]}\n"
            else:  # 无链接（如微信热搜）
                text += f"▸ **{x[0]}**\n"

        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": text}})
        elements.append({"tag": "hr"})

    # 📌 其他分类（展示前3条热点）
    if classified["📌 其他"]:
        text = "📌 **其他热点**\n"
        for x in classified["📌 其他"][:3]:
            text += f"▸ **{x[0][:40]}**\n"
        elements.append({"tag": "div", "text": {"tag": "lark_md", "content": text}})
        elements.append({"tag": "hr"})

    # 底部脚注
    elements.append({
        "tag": "note",
        "elements": [{"tag": "plain_text", "content": f"📡 API 6源+5爬虫 | 匹配{matched_count}条 | {ns} {p2}"}]
    })

    # ----- 第4步：构建飞书消息卡片并发送 -----
    card = {
        "config": {"wide_screen_mode": True},
        "header": {
            "title": {"tag": "plain_text", "content": f"📊 汽车金融行业{p2}"},
            "template": "blue",
        },
        "elements": elements,
    }

    try:
        # 发送POST请求到飞书Webhook
        resp = r.post(W, json={"msg_type": "interactive", "card": card}, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            print(f"✅ 推送成功！共展示 {matched_count} 条相关新闻 + {min(other_count, 3)} 条热点")
        else:
            print(f"⚠️ 推送返回异常: {result}")
    except Exception as e:
        print(f"❌ 推送失败: {e}")


# ===== 入口：直接运行就执行推送 =====
if __name__ == "__main__":
    push()

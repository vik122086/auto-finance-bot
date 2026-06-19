#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
汽车金融资讯推送机器人 v2.0
飞书互动卡片格式 · 带分类标签 + 阅读原文跳链
"""

import requests
import json
import datetime
import random
import hashlib

# ==================== 飞书Webhook ====================
WEBHOOK_URL = "https://open.feishu.cn/open-apis/bot/v2/hook/59535d63-0c5c-49ae-9f45-5dbc22cf8138"

# ==================== 资讯库（标题+简介+链接） ====================

NEWS_POOL = {
    "shangyongche": {
        "name": "🚛 商用车金融",
        "color": "blue",
        "emoji": "🚛",
        "items": [
            {
                "title": "华阳租赁三季度商用车商务政策发布",
                "summary": "三季度商务政策指导意见已邮件发送各大区，差异化产品同步机制落地执行",
                "url": "https://mp.weixin.qq.com/s/example1"
            },
            {
                "title": "联合重卡担保业务法人贷即将放款",
                "summary": "首笔法人贷进件推进中，四方挂靠协议方案替代原协议约束条款",
                "url": "https://mp.weixin.qq.com/s/example2"
            },
            {
                "title": "奇瑞商用车业务切换进展",
                "summary": "中南区已完成切换，华东区6月24日切换，华南/华中等后续跟进",
                "url": "https://mp.weixin.qq.com/s/example3"
            },
            {
                "title": "开瑞新能源5月渗透率达49%",
                "summary": "不含大客户渗透率49.0%，累计放款6,970台，较1月提升21个百分点",
                "url": "https://mp.weixin.qq.com/s/example4"
            },
            {
                "title": "贵州瑞骐融资比例调整上线",
                "summary": "AB类客户融资比例95%→100%，车价按客户评级调整功能已上线",
                "url": "https://mp.weixin.qq.com/s/example5"
            },
            {
                "title": "威麟皮卡年还款产品西南试点",
                "summary": "贴息5000元/台，利率9.99%，云南普洱/版纳/文山/昆明经销商已对接",
                "url": "https://mp.weixin.qq.com/s/example6"
            },
        ]
    },
    "chengyongche": {
        "name": "🚗 乘用车金融",
        "color": "green",
        "emoji": "🚗",
        "items": [
            {
                "title": "多家车企推新能源0利率金融方案",
                "summary": "新能源车金融渗透率持续提升，电池租赁（BaaS）模式加速普及",
                "url": "https://mp.weixin.qq.com/s/example7"
            },
            {
                "title": "汽车以旧换新政策金融配套跟进",
                "summary": "多地出台补贴政策，金融机构配套贴息方案同步落地",
                "url": "https://mp.weixin.qq.com/s/example8"
            },
            {
                "title": "乘用车金融渗透率突破65%",
                "summary": "新能源金融成增长主力，线上化审批率持续提升",
                "url": "https://mp.weixin.qq.com/s/example9"
            },
        ]
    },
    "zifang": {
        "name": "🏦 各资方动态",
        "color": "purple",
        "emoji": "🏦",
        "items": [
            {
                "title": "奇瑞汽金产品政策同步机制落地",
                "summary": "华阳租赁OA审批流程打通，差异化政策按渠道/产品分类签批",
                "url": "https://mp.weixin.qq.com/s/example10"
            },
            {
                "title": "多家汽车金融公司发行ABS",
                "summary": "融资成本维持低位，东风汽金ABS利率创年内新低",
                "url": "https://mp.weixin.qq.com/s/example11"
            },
            {
                "title": "狮桥租赁深化商用车金融布局",
                "summary": "持续推进商用车融资租赁，渠道下沉至县域市场",
                "url": "https://mp.weixin.qq.com/s/example12"
            },
            {
                "title": "重汽汽金差异化产品迭代",
                "summary": "商用车金融产品持续迭代，与华阳形成差异化竞争格局",
                "url": "https://mp.weixin.qq.com/s/example13"
            },
        ]
    },
    "jianguan": {
        "name": "📋 行业监管",
        "color": "red",
        "emoji": "📋",
        "items": [
            {
                "title": "金融监管总局关注汽车金融消保",
                "summary": "消费者权益保护成监管重点，合规经营要求持续升级",
                "url": "https://mp.weixin.qq.com/s/example14"
            },
            {
                "title": "汽车融资租赁监管趋严",
                "summary": "合规经营成行业共识，数据安全合规要求升级",
                "url": "https://mp.weixin.qq.com/s/example15"
            },
            {
                "title": "LPR连续持平融资成本稳定",
                "summary": "汽车金融市场融资成本保持稳定，利于业务扩张",
                "url": "https://mp.weixin.qq.com/s/example16"
            },
        ]
    },
    "shuju": {
        "name": "📊 主机厂数据",
        "color": "orange",
        "emoji": "📊",
        "items": [
            {
                "title": "华阳租赁5月业务占比24.75%",
                "summary": "抵押归档覆盖207城，500本执照已分发各大区",
                "url": "https://mp.weixin.qq.com/s/example17"
            },
            {
                "title": "开瑞新能源1-5月渗透率提升",
                "summary": "从28%提升至49%，增长21个百分点，放量明显",
                "url": "https://mp.weixin.qq.com/s/example18"
            },
            {
                "title": "奇瑞集团5月销量稳健增长",
                "summary": "商用车板块表现亮眼，联合重卡销量环比改善",
                "url": "https://mp.weixin.qq.com/s/example19"
            },
        ]
    }
}


def pick_and_build(category, count=2):
    """从分类中随机选取几条并构建卡片模块"""
    pool = NEWS_POOL[category]
    items = random.sample(pool["items"], min(count, len(pool["items"])))
    
    # 构建分类标签行
    lines = [f"**{pool['emoji']} {pool['name']}**"]
    
    for item in items:
        lines.append(f"▸ **[{item['title']}]({item['url']})**")
        lines.append(f"  {item['summary']}")
    
    return "\n".join(lines)


def build_interactive_card():
    """构建飞书互动卡片"""
    now = datetime.datetime.now()
    hour = now.hour
    
    if hour < 12:
        period = "🌅 早报"
    elif hour < 16:
        period = "☀️ 午报"
    else:
        period = "🌆 晚报"
    
    weekday_map = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday = weekday_map[now.weekday()]
    
    # 卡片元素
    elements = []
    
    # 日期行
    elements.append({
        "tag": "div",
        "text": {
            "tag": "lark_md",
            "content": f"📅 {now.strftime('%Y年%m月%d日')} {weekday}"
        }
    })
    
    elements.append({"tag": "hr"})
    
    # 各分类内容
    categories = ["shangyongche", "chengyongche", "zifang", "jianguan", "shuju"]
    for i, cat in enumerate(categories):
        content = pick_and_build(cat, 2)
        elements.append({
            "tag": "div",
            "text": {
                "tag": "lark_md",
                "content": content
            }
        })
        if i < len(categories) - 1:
            elements.append({"tag": "hr"})
    
    # 底部信息
    elements.append({
        "tag": "note",
        "elements": [
            {
                "tag": "plain_text",
                "content": "🤖 每天自动推送 · 点击标题阅读原文"
            }
        ]
    })
    
    card = {
        "config": {
            "wide_screen_mode": True
        },
        "header": {
            "title": {
                "tag": "plain_text",
                "content": f"📊 汽车金融行业{period}"
            },
            "template": "blue"
        },
        "elements": elements
    }
    
    return card


def push():
    """推送到飞书"""
    card = build_interactive_card()
    
    # 先用文本消息测试（卡片格式复杂，先确保推送通路）
    payload = {
        "msg_type": "interactive",
        "card": card
    }
    
    try:
        resp = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        result = resp.json()
        if result.get("code") == 0:
            print(f"✅ {datetime.datetime.now().strftime('%H:%M')} 互动卡片推送成功")
        else:
            print(f"❌ 推送失败: {json.dumps(result, ensure_ascii=False)}")
            # 如果卡片失败，降级为文本推送
            print("⚠️ 降级为文本推送...")
            text_content = f"📊 汽车金融行业{period}\n📅 {now.strftime('%Y年%m月%d日')} {weekday}\n\n"
            for cat in ["shangyongche", "chengyongche", "zifang", "jianguan", "shuju"]:
                items = random.sample(NEWS_POOL[cat]["items"], 2)
                text_content += f"{NEWS_POOL[cat]['emoji']} {NEWS_POOL[cat]['name']}\n"
                for item in items:
                    text_content += f"   ▸ {item['title']} - {item['summary']}\n"
                text_content += "\n"
            text_content += "---\n🤖 每天自动推送"
            payload2 = {"msg_type": "text", "content": {"text": text_content}}
            resp2 = requests.post(WEBHOOK_URL, json=payload2, timeout=10)
            print(f"✅ 文本降级推送: {resp2.json()}")
    except Exception as e:
        print(f"❌ 推送异常: {e}")


if __name__ == "__main__":
    push()
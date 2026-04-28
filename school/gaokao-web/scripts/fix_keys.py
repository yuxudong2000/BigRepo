#!/usr/bin/env python3
"""Fix/expand keys to match admissions.json exactly"""
import json, copy

with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/admissions.json') as f:
    admissions = json.load(f)

with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/school_details.json') as f:
    details = json.load(f)

# Get all combos from admissions
combos = set()
for row in admissions:
    combos.add((row['school_name'], row['major_name']))

# Map: old_key -> list of new_keys (real admissions keys)
remap = {
    # 中科大 - map to all 5 actual majors
    "中国科学技术大学|计算机类(含双学士学位)": [
        "中国科学技术大学|工科试验班(信息智能方向)",
        "中国科学技术大学|理科试验班类(数学及大数据技术)",
        "中国科学技术大学|理科试验班类(物理及应用物理)",
    ],
    # 北航 - map to AI+计算机
    "北京航空航天大学|工科试验班(AI先进技术拔尖班)": [
        "北京航空航天大学|人工智能(卓越人才培养试验班)",
        "北京航空航天大学|工科试验班类(计算与智能科学类)",
        "北京航空航天大学|计算机科学与技术(拔尖学生培养计划)",
        "北京航空航天大学|工科试验班类(信息科学与技术类)",
    ],
    # 北邮 - map to all relevant
    "北京邮电大学|计算机类(网络安全)": [
        "北京邮电大学|计算机类",
        "北京邮电大学|计算机类(元班)",
        "北京邮电大学|网络空间安全（大类招生）",
        "北京邮电大学|人工智能（大类招生）",
        "北京邮电大学|电子信息类",
        "北京邮电大学|电子信息类(元班)",
        "北京邮电大学|通信工程（大类招生）",
        "北京邮电大学|软件工程",
    ],
    # 华科 - map to CS and electronic
    "华中科技大学|工科试验班(AI先进技术拔尖班)": [
        "华中科技大学|计算机类(计算机学院)",
        "华中科技大学|计算机类(网安学院)",
        "华中科技大学|电子信息类(未来技术实验班)",
        "华中科技大学|电子信息工程(智能通信启明实验班)",
        "华中科技大学|自动化类",
        "华中科技大学|电子信息类(电信学院)",
        "华中科技大学|电子信息类(集成电路启明实验班)",
    ],
    # 华工 - map to AI/CS majors
    "华南理工大学|工科试验班(计算机与电子信息)": [
        "华南理工大学|工科试验班(AI先进技术拔尖班)",
        "华南理工大学|工科试验班(AI与低空技术)",
        "华南理工大学|计算机类",
        "华南理工大学|电子科学与技术",
        "华南理工大学|软件工程",
        "华南理工大学|工科试验班(卓越人才班)",
        "华南理工大学|工科试验班(院士特色班)",
    ],
    # 南大
    "南京大学|理科试验班(理科各专业)": [
        "南京大学|理科试验班(匡亚明学院大理科班)",
        "南京大学|理科试验班类(数理科学类)",
        "南京大学|理科试验班类(化学与生命科学类)",
        "南京大学|计算机科学与技术",
        "南京大学|计算机科学与技术(至诚班)",
        "南京大学|人工智能",
    ],
    # 南开
    "南开大学|数学类": [
        "南开大学|理科试验班(数学与大数据)",
        "南开大学|理科试验班(数学与智能省身班)",
        "南开大学|理科试验班(物理与光电信息技术工程)",
        "南开大学|工科试验班(信息科学与技术)",
    ],
    # 哈工大
    "哈尔滨工业大学|计算机类(计算机)": [
        "哈尔滨工业大学|工科试验班(AI院士特色班)",
        "哈尔滨工业大学|工科试验班(AI加先进技术领军班深圳拔尖班)",
        "哈尔滨工业大学|工科试验班(未来技术拔尖班)",
        "哈尔滨工业大学|工科试验班(自主智能系统院士特色班)",
        "哈尔滨工业大学|工科试验班(院士特色班)",
    ],
    # 天大
    "天津大学|理科试验班(弘毅学堂)": [
        "天津大学|工科试验班(智慧化工与绿色低碳类)",
        "天津大学|工科试验班(智能与计算类)",
        "天津大学|工科试验班(智能制造与建造)",
        "天津大学|工科试验班(未来技术学院)",
        "天津大学|工科试验班(电气信息类)",
        "天津大学|工科试验班(精仪与光电信息类)",
    ],
    # 西交
    "西安交通大学|工科试验班(钱学森班)": [
        "西安交通大学|工科试验班(智能制造类)",
        "西安交通大学|工科试验班(电气类)",
        "西安交通大学|工科试验班(计算机科学技术类)",
        "西安交通大学|人工智能(新工科卓越计划)",
        "西安交通大学|计算机科学与技术(国家拔尖计划)",
        "西安交通大学|自动化(钱学森班)",
        "西安交通大学|能源与动力工程(钱学森班)",
        "西安交通大学|工科试验班(智慧能源类)",
        "西安交通大学|工科试验班(航天航空类)",
        "西安交通大学|理科试验班(数学类)",
        "西安交通大学|理科试验班(物理类)",
    ],
}

new_details = {}

for key, data in details.items():
    if key in remap:
        # Copy to multiple new keys
        for new_key in remap[key]:
            new_school, new_major = new_key.split('|', 1)
            if (new_school, new_major) in combos:
                updated = copy.deepcopy(data)
                new_details[new_key] = updated
                print(f"  EXPAND: '{key}' -> '{new_key}'")
    else:
        # Keep as-is
        new_details[key] = data

# Write
with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/school_details.json', 'w', encoding='utf-8') as f:
    json.dump(new_details, f, ensure_ascii=False, indent=2)

print(f"\nTotal details after fix: {len(new_details)}")

# Coverage check
matched = sum(1 for key in new_details if tuple(key.split('|', 1)) in combos)
print(f"Matched with admissions: {matched}/{len(combos)} ({matched/len(combos)*100:.1f}%)")

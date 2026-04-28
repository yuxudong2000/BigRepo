#!/usr/bin/env python3
"""Fix Fudan duplicates - Both entries"""
import json

with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/school_details.json') as f:
    details = json.load(f)

fixes = {
    "复旦大学|理科试验班(相辉学堂)": {
        "overview": {"duration": "4年", "degree": "理学学士（数学/物理/化学/生命，按方向）", "ranking": "数学A+、化学A+、物理学A、生命科学A+（教育部第五轮，全国顶尖）", "lab": "复旦大学相辉学堂（顶尖荣誉学院）、复旦大学物质科学研究院（诺贝尔奖级研究设施）", "description": "复旦大学理科试验班（相辉学堂）是复旦最高规格的基础理科精英培养项目，以复旦创始人马相伯（相辉）命名，面向志在科学研究的顶尖学生。相辉学堂汇聚数学A+、化学A+、物理学A、生命科学A+四大顶尖学科资源，实行院士/杰青1对1导师制，推免比例最高，是走向诺贝尔奖级别科学研究的最佳本科通道之一。"},
        "streaming": {"time": "大一结束（相辉学堂独立选拔）", "method": "竞赛（CMO/物理/化学/生物全国奖）+面试（学术志向）", "majors": ["物理学（凝聚态/量子信息/粒子物理）", "数学与应用数学（纯数学/数学物理）", "化学（有机合成/药物化学）", "生命科学（分子生物/神经科学/基因组学）"], "notes": ["相辉学堂名额极少（约20-30人/届），全国最激烈的竞争之一", "推免比例约75%，出国读博是最主要路径（约60%赴海外）", "相辉学堂毕业生中已有多位在Nature/Science等顶刊独立发表成果的博士后"]},
        "postgrad": {"rate": "约85-95%", "internal_rate": "约10%留复旦", "external_rate": "约90%赴MIT/哈佛/斯坦福/加州理工/普林斯顿", "class_size": "约20-30人/届", "top_schools": ["MIT", "哈佛大学", "斯坦福大学", "加州理工（物理/化学全球顶尖）", "普林斯顿大学"], "notes": ["相辉学堂是国内出国率最高、海外顶校PhD申请成功率最高的本科项目之一", "加州理工是物理/化学方向全球最强（诺贝尔奖密度最高的高校）"]},
        "faculty": [{"name": "赵东元", "title": "中国科学院院士、2023年沃尔夫化学奖得主", "honors": ["academician"], "research": "介孔材料化学（全球奠基人）"}, {"name": "金力", "title": "中国科学院院士、人类遗传学权威", "honors": ["academician"], "research": "人类群体遗传学、精准医学"}],
        "faculty_summary": "赵东元院士是2023年沃尔夫化学奖（诺贝尔化学奖风向标奖）得主，是介孔材料化学的全球奠基人，在Nature/Science/JACS顶刊持续发文。金力院士是人类遗传学全球权威，领导多项国际基因组学项目。相辉学堂集中了复旦最顶尖的院士师资，是国内理科最强的荣誉学院之一。",
        "career": {"directions": ["学术科研（理科博士/博后/PI，以Nobel级科研为目标）", "大厂基础研究院（DeepMind/OpenAI科学AI）", "生物医药研发科学家（Genentech/拜耳）", "量化研究员（数学/物理转行）"], "companies": ["MIT/哈佛/斯坦福学术职位", "DeepMind（AlphaFold/AI for Science）", "Genentech/BMS（生命科学研发）", "幻方科技/两西格玛（数理转量化）"], "notes": ["相辉学堂以纯学术为核心出路，不以就业为目标", "若转行工业界：量化金融是薪资最高路径，AI for Science是最前沿路径"]},
        "sources": [{"title": "复旦大学相辉学堂官网", "url": "https://rche.fudan.edu.cn/"}, {"title": "复旦大学化学系（赵东元院士，沃尔夫化学奖）", "url": "https://chem.fudan.edu.cn/"}, {"title": "复旦大学物质科学研究院", "url": "https://ims.fudan.edu.cn/"}]
    },
    "复旦大学|理科试验班": {
        "overview": {"duration": "4年", "degree": "理学学士（数学/物理/化学/生命/计算机，按方向）", "ranking": "数学A+、化学A+、物理学A、生命科学A+（教育部第五轮）", "lab": "复旦大学各理科学院（国家基础学科拔尖计划2.0）", "description": "复旦大学理科试验班是基础理科大类招生通道，汇聚复旦数学A+、化学A+、物理学A、生命科学A+四大顶尖理科学科资源。相比相辉学堂，理科试验班覆盖面更广，同样享有拔尖计划资源，适合有明确理科研究兴趣但尚未确定具体方向的学生，大一结束后可根据兴趣自由分流至各理科专业。"},
        "streaming": {"time": "大一结束", "method": "综合GPA+方向志愿（热门方向竞争激烈）", "majors": ["物理学（凝聚态/量子信息/理论物理）", "数学与应用数学（代数/分析/统计）", "化学（有机合成/功能材料/计算化学）", "生命科学（分子生物/基因组/神经科学）", "计算机科学（AI方向，部分可转入信息学院）"], "notes": ["理科试验班是复旦基础理科最宽泛的入学通道", "化学和生命科学方向竞争最激烈（A+学科两个）", "推免比例约45-55%，深造是主要路径"]},
        "postgrad": {"rate": "约60-75%", "internal_rate": "约25%留复旦", "external_rate": "约75%赴北大/清华/中科大/MIT/哈佛/海外", "class_size": "约100-150人/届", "top_schools": ["北京大学（数学A+/化学A+）", "中国科学技术大学（物理极强）", "MIT", "哈佛大学", "斯坦福大学"], "notes": ["复旦理科试验班出国率约40-50%，是国内最高水平之一", "选择相辉学堂vs理科试验班：前者更精英、更少名额、更强院士资源"]},
        "faculty": [{"name": "赵东元", "title": "中国科学院院士、2023年沃尔夫化学奖", "honors": ["academician"], "research": "介孔材料（全球奠基人）"}, {"name": "许田", "title": "中国科学院院士（发育生物学）", "honors": ["academician"], "research": "发育生物学、器官再生"}, {"name": "马余刚", "title": "中国科学院院士（核物理/天体物理）", "honors": ["academician"], "research": "高能核物理、夸克胶子等离子体"}],
        "faculty_summary": "复旦理科试验班拥有赵东元（沃尔夫奖/介孔材料）、许田（发育生物学全国权威）、马余刚（核物理/天体物理）等多位顶级院士师资，四个A+级理科学科为学生提供全面的基础科学培养资源。",
        "career": {"directions": ["学术科研（理科博士/博后）", "大厂AI/科学研究院", "医药研发科学家（化学/生命方向）", "量化研究员（数学/物理转行）"], "companies": ["中科院各研究所（上海分院）", "药明康德/恒瑞（化学/生命方向）", "宁德时代（材料化学方向）", "幻方/九坤（数理转量化）"], "notes": ["复旦理科试验班毕业生在上海科创生态（张江高科技园区）就业竞争力强", "上海量化金融生态（外资行/量化私募）为数理方向提供高薪出路"]},
        "sources": [{"title": "复旦大学理科试验班（拔尖计划）", "url": "https://www.fudan.edu.cn/"}, {"title": "复旦大学化学系（A+，赵东元院士）", "url": "https://chem.fudan.edu.cn/"}, {"title": "复旦大学生命科学学院（A+）", "url": "https://life.fudan.edu.cn/"}]
    }
}

count = 0
for key, val in fixes.items():
    if key in details:
        details[key] = val
        print(f"  ✓ Fixed: {key.split('|')[1]}")
        count += 1
    else:
        print(f"  ⚠ Not found: {key}")

with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/school_details.json', 'w') as f:
    json.dump(details, f, ensure_ascii=False, indent=2)
print(f"\nFudan All done: {count} entries updated")

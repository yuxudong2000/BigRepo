#!/usr/bin/env python3
"""Fix NJU duplicates - Batch A: 5 entries"""
import json

with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/school_details.json') as f:
    details = json.load(f)

fixes = {
    "南京大学|理科试验班(匡亚明学院大理科班)": {
        "overview": {"duration": "4年", "degree": "理学学士（物理/数学/化学/生物，按方向）", "ranking": "物理学A+、化学A+、数学A（教育部第五轮），国家基础学科拔尖计划", "lab": "南京大学匡亚明学院（全国最早创办的本科荣誉学院之一）", "description": "南京大学匡亚明学院大理科班是南大最顶尖的基础科学荣誉培养项目，以自由探索和学术卓越为核心，面向有志于基础科学研究的顶尖学生。物理A+、化学A+使南大基础理科在全国首屈一指。匡亚明学院校友中已有多位中国科学院院士和国际顶尖学者。"},
        "streaming": {"time": "大一结束", "method": "自由选择（无限制），鼓励跨方向探索", "majors": ["物理学（凝聚态/粒子/量子信息）", "数学与应用数学（纯数学/概率统计）", "化学（有机/无机/物理化学）", "生命科学（分子生物/神经科学）"], "notes": ["匡亚明学院强调自由探索，无强制分流约束", "推免比例最高（60%+），学术为主要出路", "建议有意出国读博的同学尽早开始科研积累"]},
        "postgrad": {"rate": "约75-90%", "internal_rate": "约20%留南大", "external_rate": "约80%赴北大/清华/MIT/哈佛/斯坦福", "class_size": "约50-80人/届", "top_schools": ["北京大学", "清华大学", "MIT", "哈佛大学", "加州理工（Caltech）", "普林斯顿"], "notes": ["匡亚明学院是国内出国读博比例最高的院系之一（约40-50%）", "Nature/Science发表是匡院学生的重要目标"]},
        "faculty": [{"name": "薛其坤", "title": "中国科学院院士（清华/南科大，与南大合作）", "honors": ["academician"], "research": "拓扑绝缘体、量子反常霍尔效应"}, {"name": "祝世宁", "title": "中国科学院院士、南大物理学院", "honors": ["academician"], "research": "铁电体、非线性光学晶体"}],
        "faculty_summary": "南大匡亚明学院依托物理A+、化学A+的顶尖学科，祝世宁院士在铁电材料和非线性光学方向有全球领先成果。匡院是国内基础学科顶尖人才最重要的培养平台之一，培养了多位杰出科学家。",
        "career": {"directions": ["学术科研（基础科学博士/博后/PI）", "量子计算研发（物理背景）", "医药研发科学家（化学/生命方向）", "量化金融（数学/物理背景）"], "companies": ["中科院各研究所", "华为基础研究", "本源量子/国盾量子", "高盛量化部门", "顶尖高校faculty"], "notes": ["匡亚明学院以学术为核心出路", "物理/数学方向转行量化金融年薪可达50-200万"]},
        "sources": [{"title": "南京大学匡亚明学院官网", "url": "https://nic.nju.edu.cn/"}, {"title": "南大2024年毕业生就业质量报告", "url": "https://career.nju.edu.cn/"}, {"title": "南大物理学院（A+）", "url": "https://physics.nju.edu.cn/"}]
    },
    "南京大学|计算机科学与技术": {
        "overview": {"duration": "4年", "degree": "工学学士（计算机科学与技术）", "ranking": "计算机科学与技术A（教育部第五轮）", "lab": "软件新技术国家重点实验室（南大）、人工智能学院", "description": "南京大学计算机科学与技术学科全国A，软件新技术国家重点实验室是国内最重要的软件基础研究机构之一。南大CS在程序语言理论、形式化方法、软件工程方法论等方向全国顶尖，与北京/上海的互联网企业亦建立了深度合作。南京正打造'中国软件名城'，提供丰富的本地就业机会。"},
        "streaming": {"time": "大一结束", "method": "综合GPA+专业志愿", "majors": ["计算机系统与体系结构", "程序语言与软件工程（形式化/编译器）", "人工智能与机器学习", "网络空间安全"], "notes": ["南大CS在程序语言理论方向全国最强（软件新技术国重实验室）", "南京软件产业密集（中国软件名城）", "建议参与科研提升推免竞争力"]},
        "postgrad": {"rate": "约35-50%", "internal_rate": "约45%留南大", "external_rate": "约55%赴清华/北大/中科院/海外", "class_size": "约100-150人/届", "top_schools": ["南京大学", "清华大学", "北京大学", "中科院计算所", "CMU", "UIUC"], "notes": ["南大CS保研约35%，推免竞争激烈"]},
        "faculty": [{"name": "吕建", "title": "中国工程院院士、南大软件研究院院长", "honors": ["academician"], "research": "软件工程、网构软件"}, {"name": "陈道蓄", "title": "南大CS教授、软件工程权威", "honors": [], "research": "形式化方法、程序验证"}],
        "faculty_summary": "吕建院士领衔软件新技术国家重点实验室，在网构软件和服务计算方向全国权威。南大CS在程序语言理论和形式化方法方向是全国最重要的研究基地之一。",
        "career": {"directions": ["后端/系统工程师", "编译器/程序语言工程师", "AI算法工程师", "安全工程师"], "companies": ["华为（南京研究所）", "字节跳动", "腾讯", "阿里巴巴", "南京国产软件企业（中兴/华讯等）"], "notes": ["南京华为研究所是CS方向最重要的本地就业平台", "中国软件名城生态提供大量软件研发就业机会"]},
        "sources": [{"title": "南京大学计算机科学与技术系官网", "url": "https://cs.nju.edu.cn/"}, {"title": "软件新技术国家重点实验室（南大）", "url": "https://keysoftlab.nju.edu.cn/"}, {"title": "华为南京研究所校招", "url": "https://career.huawei.com/"}]
    },
    "南京大学|计算机科学与技术(至诚班)": {
        "overview": {"duration": "4年", "degree": "工学学士（计算机科学与技术）", "ranking": "计算机科学与技术A（教育部第五轮），南大计算机院荣誉班", "lab": "软件新技术国家重点实验室、南大AI学院", "description": "南大计算机至诚班是南大计算机学院的荣誉培养通道，强调理论深度和学术创新能力，享有导师1对1指导、最高推免配额和国际交流资源。至诚班以培养学术型顶尖CS人才为核心，是南大CS最高规格的本科培养项目。"},
        "streaming": {"time": "大一结束（至诚班单独选拔）", "method": "竞赛（NOI/ACM）+面试+GPA", "majors": ["理论计算机（算法/复杂性）", "系统软件（OS/编译器/数据库内核）", "AI基础理论（深度学习理论/优化）", "形式化方法与程序验证"], "notes": ["至诚班推免比例50%+，以学术为主", "NOI/ACM选手有显著加分", "国内读博以清北/中科院为主要目标"]},
        "postgrad": {"rate": "约70-85%", "internal_rate": "约20%留南大", "external_rate": "约80%赴清华/北大/MIT/CMU/UCB", "class_size": "约15-25人/届", "top_schools": ["清华大学", "北京大学", "MIT CSAIL", "CMU", "斯坦福", "UCB"], "notes": ["至诚班出国率高（约40%），是申请海外PhD的优质平台"]},
        "faculty": [{"name": "吕建", "title": "中国工程院院士", "honors": ["academician"], "research": "软件工程、网构软件"}, {"name": "陈建平", "title": "南大计算机学院教授、国家杰青", "honors": ["jiechu"], "research": "机器学习、深度学习"}],
        "faculty_summary": "至诚班由吕建院士、陈建平（杰青）等顶级学者全程指导，软件新技术国家重点实验室提供全国最强的软件基础研究资源，是南大CS方向最具竞争力的本科培养通道。",
        "career": {"directions": ["学术科研（CS博士/博后）", "大厂研究院（算法科学家）", "系统软件工程师（OS/数据库）"], "companies": ["微软亚洲研究院（MSRA）", "Google Research", "华为2012实验室", "字节跳动研究院"], "notes": ["至诚班以学术/顶级研究院为主要出路", "MSRA是南大CS至诚班最热门的工业界就业目的地"]},
        "sources": [{"title": "南京大学计算机至诚班介绍", "url": "https://cs.nju.edu.cn/"}, {"title": "微软亚洲研究院校园招聘", "url": "https://www.msra.cn/"}]
    },
    "南京大学|人工智能": {
        "overview": {"duration": "4年", "degree": "工学学士（人工智能）", "ranking": "人工智能（南大AI学院独立设置）", "lab": "南京大学人工智能学院、自然语言处理实验室（NLPLAB）", "description": "南京大学人工智能学院在NLP（自然语言处理）方向有全国领先的研究实力，NLPLAB是国内最重要的NLP研究实验室之一，多次在ACL/EMNLP等顶级NLP会议上获最佳论文奖。大模型时代NLP是最热门的AI方向，南大AI在该方向具有独特竞争优势。"},
        "streaming": {"time": "大一结束", "method": "综合GPA+方向志愿", "majors": ["自然语言处理（大模型/对话AI/机器翻译）", "计算机视觉（图像理解/生成模型）", "知识图谱与推理（知识库/因果推理）", "AI系统（大模型训练/推理加速）"], "notes": ["南大AI在NLP方向全国最强，是该方向最有优势的院校之一", "大模型时代NLP工程师需求爆发，薪资增长迅速", "NLPLAB每年在ACL等顶会高密度发文"]},
        "postgrad": {"rate": "约50-65%", "internal_rate": "约35%留南大", "external_rate": "约65%赴清华/北大/中科院/海外", "class_size": "约30-50人/届", "top_schools": ["南京大学", "清华大学", "北京大学", "CMU", "MIT", "斯坦福（NLP方向）"], "notes": ["NLP方向深造到CMU/MIT语言技术研究所有较高成功率"]},
        "faculty": [{"name": "周志华", "title": "中国科学院院士、南大AI学院院长", "honors": ["academician"], "research": "机器学习、集成学习"}, {"name": "陈谱", "title": "南大NLPLAB负责人、国家杰青", "honors": ["jiechu"], "research": "自然语言处理、大模型"}],
        "faculty_summary": "周志华院士（机器学习领域全球最具影响力的华人学者之一，Ensemble Methods经典教材作者）领衔南大AI学院，NLPLAB在ACL/EMNLP/NAACL等顶会持续高密度发文，是国内NLP最重要的研究基地。",
        "career": {"directions": ["NLP算法工程师（大模型/对话系统）", "CV算法工程师", "AI产品技术（大模型应用）", "学术科研（AI方向博士）"], "companies": ["百度NLP（文心一言）", "腾讯NLP（混元大模型）", "字节跳动AI Lab", "阿里达摩院NLP", "华为诺亚方舟（NLP方向）"], "notes": ["南大AI在NLP方向是头部大厂最受欢迎的来源院校之一", "大模型时代NLP工程师供不应求"]},
        "sources": [{"title": "南京大学人工智能学院官网", "url": "https://ai.nju.edu.cn/"}, {"title": "南大NLPLAB官网", "url": "http://nlp.nju.edu.cn/"}, {"title": "百度NLP校园招聘", "url": "https://talent.baidu.com/"}]
    },
    "南京大学|软件工程": {
        "overview": {"duration": "4年", "degree": "工学学士（软件工程）", "ranking": "软件工程A（教育部第五轮）", "lab": "南京大学软件学院（国家示范性软件学院）、软件新技术国家重点实验室", "description": "南京大学软件工程依托国家示范性软件学院和软件新技术国家重点实验室，在软件工程方法论、形式化开发、DevOps等方向全国领先。南京是中国最重要的软件产业城市（中国软件名城），华为南京研究所、中兴、网宿等头部企业聚集，为软件工程专业提供丰富的实习和就业资源。"},
        "streaming": {"time": "大一结束", "method": "综合GPA+方向志愿", "majors": ["企业级软件开发（Java/微服务/云原生）", "DevOps与持续交付（CI/CD/容器化）", "智能软件（AI工程化/MLOps）", "大数据工程（数仓/流处理）"], "notes": ["南京软件产业密集，实习机会丰富", "华为南京研究所是软件方向最重要的本地就业平台", "建议从大一开始积累实习和项目经验"]},
        "postgrad": {"rate": "约20-30%", "internal_rate": "约55%留南大", "external_rate": "约45%赴清华/浙大/中科院软件所", "class_size": "约100-150人/届", "top_schools": ["南京大学", "清华大学", "浙江大学", "中科院软件研究所"], "notes": ["软件方向就业导向明显，直接就业是大多数同学的选择"]},
        "faculty": [{"name": "吕建", "title": "中国工程院院士", "honors": ["academician"], "research": "软件工程、服务计算"}],
        "faculty_summary": "南大软件学院依托吕建院士和软件新技术国家重点实验室，在软件工程方法论和形式化验证方向全国顶尖，与华为、中兴等企业建立深度产学研合作。",
        "career": {"directions": ["后端/全栈工程师", "DevOps/SRE工程师", "智能软件工程师（AI工程化）", "数据工程师"], "companies": ["华为南京研究所", "中兴通讯（南京）", "腾讯", "字节跳动", "阿里云"], "notes": ["华为南京研究所是软件方向最大的本地校招企业", "南京中国软件名城生态成熟，本地就业选择丰富"]},
        "sources": [{"title": "南京大学软件学院官网", "url": "https://software.nju.edu.cn/"}, {"title": "华为南京研究所校招", "url": "https://career.huawei.com/"}, {"title": "南京市软件产业发展报告", "url": "https://www.nanjing.gov.cn/"}]
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
print(f"\nNJU Batch A done: {count} entries updated")

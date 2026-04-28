#!/usr/bin/env python3
"""Fix BUPT duplicates - Batch A: 5 entries"""
import json

with open('/Users/yuxudong/Downloads/高考/gaokao-web/data/school_details.json') as f:
    details = json.load(f)

fixes = {
    "北京邮电大学|计算机类": {
        "overview": {"duration": "4年", "degree": "工学学士（计算机科学与技术/数据科学/智能科学，按方向）", "ranking": "计算机科学与技术A-（教育部第五轮）", "lab": "北邮网络与交换技术国家重点实验室（计算机+通信交叉方向）", "description": "北京邮电大学计算机类大类招生依托网络与交换技术国家重点实验室，在网络计算、分布式系统、云计算等领域有鲜明的通信行业背景特色。北邮是全国通信和信息类毕业生就业最好的院校之一，依托北京科技生态（中关村）和通信行业（华为/中兴/爱立信）形成双重就业优势。"},
        "streaming": {"time": "大一结束", "method": "综合GPA+方向志愿", "majors": ["计算机科学与技术（系统/算法）", "数据科学与大数据技术", "人工智能", "网络工程（云计算/SDN）"], "notes": ["北邮CS与通信背景结合，在网络计算方向独具特色", "华为/中兴/爱立信等通信巨头是北邮CS最重要的就业平台", "北京中关村科技园提供丰富的互联网大厂就业机会"]},
        "postgrad": {"rate": "约30-40%", "internal_rate": "约50%留北邮", "external_rate": "约50%赴清华/北大/中科院计算所", "class_size": "约100-150人/届", "top_schools": ["北京邮电大学", "清华大学", "北京大学", "中科院计算技术研究所"], "notes": ["北邮CS保研约25-30%，竞争较激烈"]},
        "faculty": [{"name": "吕廷杰", "title": "北邮计算机学院教授、通信网络权威", "honors": [], "research": "通信网络、互联网经济"}, {"name": "张平", "title": "中国工程院院士、北邮无线通信权威", "honors": ["academician"], "research": "移动通信、6G技术"}],
        "faculty_summary": "张平院士在6G通信技术方向全国权威，网络与交换技术国家重点实验室是国内通信网络最重要的研究机构。北邮CS与通信系统深度交叉，在网络协议、分布式系统方向有独特积累。",
        "career": {"directions": ["后端/系统工程师", "网络工程师（云网络/SDN）", "AI算法工程师", "数据科学家"], "companies": ["华为（北京/深圳研究所）", "中兴通讯", "字节跳动", "腾讯", "阿里云"], "notes": ["华为是北邮CS最大的校招雇主", "北京互联网大厂（字节/百度/京东）是重要就业平台"]},
        "sources": [{"title": "北京邮电大学计算机学院官网", "url": "https://scs.bupt.edu.cn/"}, {"title": "华为校园招聘", "url": "https://career.huawei.com/"}, {"title": "北邮2024就业质量报告", "url": "https://career.bupt.edu.cn/"}]
    },
    "北京邮电大学|计算机类(元班)": {
        "overview": {"duration": "4年", "degree": "工学学士（计算机科学与技术）", "ranking": "计算机科学与技术A-（教育部第五轮），北邮计算机荣誉班", "lab": "网络与交换技术国家重点实验室、北邮AI创新研究院", "description": "北邮计算机元班是北邮计算机学院的荣誉精英培养通道，强调研究能力和创新思维，享有1对1导师指导和最高推免配额。元班名额极少（每届约20-30人），是北邮CS最高规格的本科培养项目，以培养学术和工业界双高端人才为目标。"},
        "streaming": {"time": "大一结束（元班单独选拔）", "method": "竞赛（NOI/ACM优先）+面试+GPA", "majors": ["理论计算机与算法", "AI基础研究（深度学习理论）", "系统软件（OS/编译器/数据库）", "网络安全与密码学"], "notes": ["元班推免比例约50%，学术路径为主", "NOI/ACM竞赛生有显著优势", "与普通班相比享有更好的科研资源和导师配置"]},
        "postgrad": {"rate": "约65-80%", "internal_rate": "约20%留北邮", "external_rate": "约80%赴清华/北大/CMU/MIT", "class_size": "约20-30人/届", "top_schools": ["清华大学", "北京大学", "CMU", "MIT CSAIL", "UCB"], "notes": ["元班是北邮出国申请PhD成功率最高的培养通道"]},
        "faculty": [{"name": "张平", "title": "中国工程院院士", "honors": ["academician"], "research": "移动通信、AI通信交叉"}, {"name": "孙松林", "title": "北邮计算机学院教授、国家级人才", "honors": [], "research": "机器学习、通信AI交叉"}],
        "faculty_summary": "北邮计算机元班由张平院士等顶级学者指导，享有网络与交换技术国家重点实验室的全部科研资源，是北邮CS最具学术竞争力的本科培养路径。",
        "career": {"directions": ["学术科研（CS博士）", "大厂研究院（算法科学家）", "系统软件核心工程师"], "companies": ["微软亚洲研究院", "百度研究院", "华为2012实验室", "Google Research"], "notes": ["元班以顶级研究院和海外PhD为主要出路"]},
        "sources": [{"title": "北邮计算机学院元班介绍", "url": "https://scs.bupt.edu.cn/"}, {"title": "微软亚洲研究院校园招聘", "url": "https://www.msra.cn/"}]
    },
    "北京邮电大学|人工智能（大类招生）": {
        "overview": {"duration": "4年", "degree": "工学学士（人工智能）", "ranking": "人工智能（北邮AI创新研究院），通信+AI交叉特色", "lab": "北邮人工智能学院、北邮-华为智能通信联合实验室", "description": "北邮人工智能大类招生依托北邮在通信领域的独特背景，在AI与通信融合方向（网络智能化、智能无线通信、AI for Network）具有全国独特的学科特色。北京-华为联合AI实验室提供丰富的产学研合作机会，是AI+通信方向最有特色的本科培养院校之一。"},
        "streaming": {"time": "大一结束", "method": "综合GPA+方向志愿", "majors": ["AI for通信网络（网络智能化/自动驾驶网络）", "计算机视觉（图像/视频AI）", "自然语言处理（大模型应用）", "联邦学习与隐私计算（通信安全AI）"], "notes": ["AI+通信融合是北邮最有特色的AI方向，全国唯一性强", "华为联合实验室提供通信AI最前沿的研究资源", "北京中关村AI生态提供丰富的就业机会"]},
        "postgrad": {"rate": "约35-50%", "internal_rate": "约45%留北邮", "external_rate": "约55%赴清华/北大/中科院自动化所", "class_size": "约50-80人/届", "top_schools": ["北京邮电大学", "清华大学", "北京大学", "中科院自动化研究所"], "notes": ["中科院自动化所是AI方向最重要的深造机构之一"]},
        "faculty": [{"name": "张平", "title": "中国工程院院士", "honors": ["academician"], "research": "AI驱动的无线通信（6G AI）"}, {"name": "林宝军", "title": "北邮AI学院院长、国家级人才", "honors": [], "research": "深度学习、通信AI交叉"}],
        "faculty_summary": "北邮AI学院依托张平院士在AI通信交叉领域的深厚积累，北邮-华为智能通信联合实验室在网络智能化（AI for 6G）方向是国内最重要的研究平台之一，培养AI与通信双背景的复合型人才。",
        "career": {"directions": ["AI算法工程师（通信/网络方向）", "网络智能化工程师（运营商/设备商）", "CV/NLP算法工程师", "联邦学习/隐私计算工程师"], "companies": ["华为（无线通信AI研究）", "中国移动/联通/电信（网络AI）", "字节跳动AI Lab", "百度", "中兴通讯"], "notes": ["AI+通信方向在华为/运营商有独特竞争优势", "通用AI方向在北京互联网大厂有良好就业机会"]},
        "sources": [{"title": "北邮人工智能学院官网", "url": "https://ai.bupt.edu.cn/"}, {"title": "华为校园招聘（AI岗位）", "url": "https://career.huawei.com/"}, {"title": "中国移动校园招聘", "url": "https://campus.10086.cn/"}]
    },
    "北京邮电大学|网络空间安全（大类招生）": {
        "overview": {"duration": "4年", "degree": "工学学士（网络空间安全）", "ranking": "网络空间安全A（教育部第五轮）", "lab": "北邮网络空间安全学院、可信分布式计算与服务教育部重点实验室", "description": "北京邮电大学网络空间安全是全国网安A级学科，结合北邮在通信网络安全的独特背景，在5G通信安全、密码协议、工控安全等方向具有全国领先地位。网安方向国家战略需求持续旺盛，北邮网安毕业生在运营商/设备商/政府机构就业竞争力极强。"},
        "streaming": {"time": "大一结束", "method": "综合GPA+面试（含政治背景审查）", "majors": ["通信网络安全（5G安全/NB-IoT安全）", "密码学与安全协议（国密标准）", "网络攻防与渗透测试（CTF）", "数据安全与隐私保护（GDPR合规）"], "notes": ["5G通信安全是北邮网安最有特色的方向（全国唯一性强）", "CTF竞赛是进入顶尖安全企业的敲门砖", "部分方向涉密，有政治背景审查"]},
        "postgrad": {"rate": "约35-50%", "internal_rate": "约50%留北邮", "external_rate": "约50%赴清华/北大/中科院信安所", "class_size": "约50-80人/届", "top_schools": ["北京邮电大学", "清华大学", "中科院信息工程研究所（网安权威）"], "notes": ["中科院信息工程所是网络安全学术研究最权威机构"]},
        "faculty": [{"name": "杨义先", "title": "中国工程院院士、北邮网安权威", "honors": ["academician"], "research": "密码学、网络安全"}, {"name": "钮心忻", "title": "北邮网安学院教授、通信安全专家", "honors": [], "research": "信息隐藏、数字水印"}],
        "faculty_summary": "杨义先院士在密码学和网络安全方向全国权威，北邮网安在通信安全和密码协议方向与华为等设备商深度合作，是国内通信行业网络安全人才最重要的培养基地。",
        "career": {"directions": ["通信安全工程师（5G/IoT安全）", "渗透测试/漏洞研究员", "密码工程师", "数据安全工程师", "国家网安机构"], "companies": ["华为（安全研究）", "中国移动（网络安全部）", "奇安信", "绿盟科技", "国家密码局相关单位"], "notes": ["北邮网安在运营商（移动/联通/电信）和设备商（华为/中兴）有独特就业竞争力", "通信安全薪资高于普通网安岗位"]},
        "sources": [{"title": "北邮网络空间安全学院官网", "url": "https://scss.bupt.edu.cn/"}, {"title": "杨义先院士团队（密码学）", "url": "https://scss.bupt.edu.cn/"}, {"title": "奇安信校园招聘", "url": "https://www.qianxin.com/"}]
    },
    "北京邮电大学|通信工程（大类招生）": {
        "overview": {"duration": "4年", "degree": "工学学士（通信工程）", "ranking": "信息与通信工程A+（教育部第五轮，全国最强）", "lab": "网络与交换技术国家重点实验室、泛网无线通信教育部重点实验室", "description": "北京邮电大学通信工程是北邮最核心的传统强势专业，信息与通信工程A+全国最强。北邮是中国通信行业最重要的人才摇篮，华为/中兴/中国移动等行业巨头长期将北邮列为一类顶尖校招来源。5G/6G浪潮下，通信工程人才需求持续旺盛。"},
        "streaming": {"time": "大一结束", "method": "综合GPA+方向志愿", "majors": ["移动通信系统（5G/6G协议栈/基站设计）", "光纤通信（光传输/光网络）", "卫星通信（低轨卫星/星间链路）", "无线传感网与物联网"], "notes": ["北邮通信工程A+全国最强，就业竞争力极强", "华为/中兴是通信方向最重要的就业平台（薪资高）", "卫星通信（低轨卫星互联网）是近年新兴高薪方向"]},
        "postgrad": {"rate": "约30-40%", "internal_rate": "约55%留北邮", "external_rate": "约45%赴清华/东南/中科院电子所", "class_size": "约150-200人/届", "top_schools": ["北京邮电大学", "清华大学（EE/通信）", "东南大学（通信A+）", "中科院电子学研究所"], "notes": ["东南大学通信A+是除北邮外最强的通信学科"]},
        "faculty": [{"name": "张平", "title": "中国工程院院士", "honors": ["academician"], "research": "6G移动通信、语义通信"}, {"name": "彭木根", "title": "北邮信息学院教授、国家杰青", "honors": ["jiechu"], "research": "异构网络、D2D通信"}],
        "faculty_summary": "张平院士是中国6G通信研究的领军人物，彭木根（杰青）在异构网络和D2D通信方向有国际领先成果。网络与交换技术国家重点实验室是国内通信网络最重要的研究机构，直接支撑华为等企业的6G研发。",
        "career": {"directions": ["通信系统工程师（5G/6G基站研发）", "射频工程师", "卫星通信工程师", "通信网络规划优化工程师（运营商）"], "companies": ["华为无线网络BG（全球最大通信设备商）", "中兴通讯（5G）", "中国移动/联通/电信（运营商）", "大唐移动（5G国标参与方）", "中国卫星（低轨卫星互联网）"], "notes": ["华为无线是北邮通信方向最重要的就业平台，起薪25-40万/年", "卫星互联网（华为/中国卫星/中国电科）是近年薪资增长最快的通信子方向"]},
        "sources": [{"title": "北邮信息与通信工程学院官网（A+）", "url": "https://sce.bupt.edu.cn/"}, {"title": "华为无线校园招聘", "url": "https://career.huawei.com/"}, {"title": "中国移动校园招聘", "url": "https://campus.10086.cn/"}]
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
print(f"\nBUPT Batch A done: {count} entries updated")

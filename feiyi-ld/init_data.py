"""
初始化非遗数据
"""
from app import app, db, FeiyiItem, FeiyiKnowledge
import json

def init_sample_data():
    """初始化示例数据"""
    
    # 创建数据库表
    with app.app_context():
        db.create_all()
        
        # 检查是否已有数据
        if FeiyiItem.query.first():
            print("数据库已有数据，跳过初始化")
            return
        
        # 示例非遗项目数据
        sample_items = [
            {
                'name': '昆曲',
                'category_id': 4,
                'description': '昆曲是中国最古老的剧种之一，被誉为"百戏之祖"',
                'origin_place': '江苏昆山',
                'history': '昆曲起源于14世纪中国的昆山，至今已有600多年历史。明代魏良辅对昆山腔进行改革，奠定了昆曲的基础。',
                'characteristics': '昆曲以工尺谱记谱，曲调优美，表演细腻，被称为"水磨调"。其表演融合了唱、念、做、打等多种艺术形式。',
                'inheritance_status': '活跃传承',
                'protection_level': '世界非物质文化遗产',
                'representative_inheritor': '汪世瑜、蔡正仁、梁谷音等',
                'images': json.dumps(['kunqu1.jpg', 'kunqu2.jpg']),
                'videos': json.dumps(['kunqu_performance.mp4'])
            },
            {
                'name': '京剧',
                'category_id': 4,
                'description': '京剧是中国五大戏曲剧种之一，被誉为中国国粹',
                'origin_place': '北京',
                'history': '京剧形成于19世纪中期，由徽剧、汉剧、昆曲、秦腔等剧种融合发展而成。',
                'characteristics': '京剧以西皮、二黄为主要声腔，表演程式化，脸谱艺术独特，有生、旦、净、丑四大行当。',
                'inheritance_status': '活跃传承',
                'protection_level': '世界非物质文化遗产',
                'representative_inheritor': '梅兰芳、程砚秋、尚小云、荀慧生等',
                'images': json.dumps(['jingju1.jpg', 'jingju2.jpg']),
                'videos': json.dumps(['jingju_performance.mp4'])
            },
            {
                'name': '中医针灸',
                'category_id': 9,
                'description': '中医针灸是中国传统医学的重要组成部分',
                'origin_place': '中国',
                'history': '针灸疗法起源于新石器时代，距今已有数千年历史。《黄帝内经》奠定了针灸理论基础。',
                'characteristics': '通过针刺和艾灸刺激人体穴位，调节气血，治疗疾病。具有简便易行、疗效显著的特点。',
                'inheritance_status': '活跃传承',
                'protection_level': '世界非物质文化遗产',
                'representative_inheritor': '石学敏、王雪苔、贺普仁等',
                'images': json.dumps(['zhenjiu1.jpg', 'zhenjiu2.jpg']),
                'videos': json.dumps(['zhenjiu_technique.mp4'])
            },
            {
                'name': '蜀锦织造技艺',
                'category_id': 8,
                'description': '蜀锦是中国四大名锦之一，有"寸锦寸金"之誉',
                'origin_place': '四川成都',
                'history': '蜀锦起源于春秋战国时期，至今已有2000多年历史。汉代时蜀锦已远销海外。',
                'characteristics': '蜀锦色彩绚丽，图案精美，质地坚韧。传统工艺复杂，需要高超的技艺。',
                'inheritance_status': '濒危',
                'protection_level': '国家级非物质文化遗产',
                'representative_inheritor': '钟秉章、贺斌等',
                'images': json.dumps(['shujin1.jpg', 'shujin2.jpg']),
                'videos': json.dumps(['shujin_weaving.mp4'])
            },
            {
                'name': '太极拳',
                'category_id': 6,
                'description': '太极拳是中国传统武术的代表，融合了哲学、医学、美学',
                'origin_place': '河南温县陈家沟',
                'history': '太极拳起源于明末清初，由陈王廷创编。后发展出陈、杨、武、吴、孙五大流派。',
                'characteristics': '动作缓慢柔和，刚柔相济，以意导气，以气运身，具有健身养生和技击功能。',
                'inheritance_status': '活跃传承',
                'protection_level': '世界非物质文化遗产',
                'representative_inheritor': '陈小旺、杨振铎、吴阿敏等',
                'images': json.dumps(['taijiquan1.jpg', 'taijiquan2.jpg']),
                'videos': json.dumps(['taijiquan_demo.mp4'])
            },
            {
                'name': '二十四节气',
                'category_id': 10,
                'description': '二十四节气是中国古代农业文明的智慧结晶',
                'origin_place': '中国',
                'history': '二十四节气形成于春秋战国时期，完善于汉代，是中国古代用来指导农事的补充历法。',
                'characteristics': '根据太阳在黄道上的位置变化，将一年分为24个节气，反映了季节、气候、物候的变化规律。',
                'inheritance_status': '活跃传承',
                'protection_level': '世界非物质文化遗产',
                'representative_inheritor': '刘晓峰、萧放等民俗学者',
                'images': json.dumps(['24jieqi1.jpg', '24jieqi2.jpg']),
                'videos': json.dumps(['24jieqi_intro.mp4'])
            }
        ]
        
        # 添加项目数据
        for item_data in sample_items:
            item = FeiyiItem(**item_data)
            db.session.add(item)
        
        # 示例知识库数据
        sample_knowledge = [
            {
                'title': '什么是非物质文化遗产',
                'content': '非物质文化遗产是指各种以非物质形态存在的与群众生活密切相关、世代相承的传统文化表现形式，包括口头传统、传统表演艺术、民俗活动和节庆、有关自然界和宇宙的民间传统知识和实践、传统手工艺技能等以及与上述传统文化表现形式相关的文化空间。',
                'category_id': None,
                'keywords': '非遗,定义,文化遗产,传统文化',
                'source': '联合国教科文组织'
            },
            {
                'title': '中国非遗保护的重要意义',
                'content': '保护非物质文化遗产对于维护文化多样性、促进可持续发展、增强民族认同感具有重要意义。它是人类文明的重要组成部分，承载着深厚的历史文化内涵，是连接过去、现在和未来的文化纽带。',
                'category_id': None,
                'keywords': '非遗保护,文化多样性,民族认同,可持续发展',
                'source': '中国非物质文化遗产保护中心'
            },
            {
                'title': '昆曲的艺术特色',
                'content': '昆曲被称为"百戏之祖"，其艺术特色主要体现在：1.音乐优美，被誉为"水磨调"；2.表演细腻，程式严谨；3.文学性强，多为文人创作；4.服饰华美，舞台效果精致。昆曲对后来的京剧、越剧等剧种都产生了深远影响。',
                'category_id': 4,
                'item_id': 1,
                'keywords': '昆曲,艺术特色,水磨调,百戏之祖',
                'source': '中国戏曲学院'
            }
        ]
        
        # 添加知识库数据
        for knowledge_data in sample_knowledge:
            knowledge = FeiyiKnowledge(**knowledge_data)
            db.session.add(knowledge)
        
        # 提交数据
        db.session.commit()
        print("示例数据初始化完成！")
        print(f"添加了 {len(sample_items)} 个非遗项目")
        print(f"添加了 {len(sample_knowledge)} 条知识库记录")

if __name__ == '__main__':
    init_sample_data()
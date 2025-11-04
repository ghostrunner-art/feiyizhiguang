from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from markupsafe import Markup
import os
from datetime import datetime
from dotenv import load_dotenv
import requests
import json

# 加载环境变量
load_dotenv()

app = Flask(__name__)
CORS(app)

# 数据库配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///feiyi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here'

db = SQLAlchemy(app)

# 数据库模型定义
class FeiyiItem(db.Model):
    """非遗项目模型"""
    __tablename__ = 'feiyi_items'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False, comment='项目名称')
    category_id = db.Column(db.Integer, nullable=False, comment='分类ID')
    description = db.Column(db.Text, comment='项目描述')
    origin_location = db.Column(db.String(100), comment='发源地')
    historical_background = db.Column(db.Text, comment='历史背景')
    cultural_value = db.Column(db.Text, comment='文化价值')
    inheritance_status = db.Column(db.Text, comment='传承状况')
    protection_measures = db.Column(db.Text, comment='保护措施')
    protection_level = db.Column(db.String(50), comment='保护级别')
    representative_inheritor = db.Column(db.String(200), comment='代表性传承人')
    declaration_date = db.Column(db.String(50), comment='申报时间')
    images = db.Column(db.Text, comment='相关图片URL，JSON格式')
    videos = db.Column(db.Text, comment='相关视频URL，JSON格式')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id,
            'description': self.description,
            'origin_location': self.origin_location,
            'historical_background': self.historical_background,
            'cultural_value': self.cultural_value,
            'inheritance_status': self.inheritance_status,
            'protection_measures': self.protection_measures,
            'protection_level': self.protection_level,
            'representative_inheritor': self.representative_inheritor,
            'declaration_date': self.declaration_date,
            'images': self.images,
            'videos': self.videos,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class FeiyiKnowledge(db.Model):
    """非遗知识库模型"""
    __tablename__ = 'feiyi_knowledge'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False, comment='知识标题')
    content = db.Column(db.Text, nullable=False, comment='知识内容')
    category_id = db.Column(db.Integer, comment='关联分类ID')
    item_id = db.Column(db.Integer, db.ForeignKey('feiyi_items.id'), comment='关联项目ID')
    keywords = db.Column(db.String(500), comment='关键词，逗号分隔')
    source = db.Column(db.String(200), comment='知识来源')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='更新时间')
    
    # 关联关系
    item = db.relationship('FeiyiItem', backref=db.backref('knowledge_items', lazy=True))
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'category_id': self.category_id,
            'item_id': self.item_id,
            'keywords': self.keywords,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UserInteraction(db.Model):
    """用户交互记录模型"""
    __tablename__ = 'user_interactions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), comment='会话ID')
    question = db.Column(db.Text, nullable=False, comment='用户问题')
    answer = db.Column(db.Text, comment='AI回答')
    category_id = db.Column(db.Integer, comment='相关分类ID')
    item_id = db.Column(db.Integer, comment='相关项目ID')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='创建时间')
    
    def to_dict(self):
        """转换为字典格式"""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'question': self.question,
            'answer': self.answer,
            'category_id': self.category_id,
            'item_id': self.item_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 导入华为云AI模块
from huawei_ai import get_ai_response, huawei_ai_client

# 非遗分类
FEIYI_CATEGORIES = [
    {'id': 1, 'name': '民间文学', 'description': '包括神话、传说、民间故事、民间歌谣、谚语等'},
    {'id': 2, 'name': '传统音乐', 'description': '包括民间音乐、文人音乐、宫廷音乐、宗教音乐等'},
    {'id': 3, 'name': '传统舞蹈', 'description': '包括民间舞蹈、宫廷舞蹈、宗教舞蹈等'},
    {'id': 4, 'name': '传统戏剧', 'description': '包括昆曲、京剧、豫剧、越剧等各种地方戏曲'},
    {'id': 5, 'name': '曲艺', 'description': '包括相声、评书、快板、大鼓等说唱艺术'},
    {'id': 6, 'name': '传统体育、游艺与杂技', 'description': '包括武术、龙舟、风筝、杂技等'},
    {'id': 7, 'name': '传统美术', 'description': '包括绘画、雕塑、建筑装饰、工艺美术等'},
    {'id': 8, 'name': '传统技艺', 'description': '包括纺织、冶炼、制茶、烹饪、中医药等传统工艺'},
    {'id': 9, 'name': '传统医药', 'description': '包括中医诊疗法、中药炮制技艺、针灸等'},
    {'id': 10, 'name': '民俗', 'description': '包括节庆、婚丧嫁娶、祭祀等民间习俗'}
]

@app.route('/')
def index():
    """首页"""
    return render_template('index.html', categories=FEIYI_CATEGORIES)

@app.route('/api/categories')
def get_categories():
    """获取非遗分类API"""
    return jsonify(FEIYI_CATEGORIES)

@app.route('/ai-chat')
def ai_chat_page():
    """AI聊天页面"""
    return render_template('ai_chat.html')

@app.route('/api/category/<int:category_id>')
def get_category_detail(category_id):
    """获取分类详情API"""
    category = next((cat for cat in FEIYI_CATEGORIES if cat['id'] == category_id), None)
    if not category:
        return jsonify({'error': '分类不存在'}), 404
    
    # 这里可以添加更多该分类下的具体项目
    items = FeiyiItem.query.filter_by(category_id=category_id).all()
    category_data = category.copy()
    category_data['items'] = [item.to_dict() for item in items]
    
    return jsonify(category_data)

@app.route('/api/ai/chat', methods=['POST'])
def ai_chat():
    """AI智能问答接口"""
    data = request.get_json()
    user_question = data.get('question', '')
    session_id = data.get('session_id', '')
    
    if not user_question:
        return jsonify({'error': '问题不能为空'}), 400
    
    try:
        # 调用华为云AI接口
        ai_response = get_ai_response(user_question)
        
        # 保存用户交互记录
        interaction = UserInteraction(
            session_id=session_id,
            question=user_question,
            answer=ai_response
        )
        db.session.add(interaction)
        db.session.commit()
        
        return jsonify({
            'answer': ai_response,
            'session_id': session_id,
            'timestamp': interaction.created_at.isoformat()
        })
    except Exception as e:
        return jsonify({'error': f'AI服务暂时不可用: {str(e)}'}), 500

@app.route('/api/knowledge')
def get_knowledge():
    """获取知识库API"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    category_id = request.args.get('category_id', type=int)
    keyword = request.args.get('keyword', '')
    
    query = FeiyiKnowledge.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if keyword:
        query = query.filter(FeiyiKnowledge.title.contains(keyword) | 
                           FeiyiKnowledge.content.contains(keyword) |
                           FeiyiKnowledge.keywords.contains(keyword))
    
    knowledge_items = query.order_by(FeiyiKnowledge.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'items': [item.to_dict() for item in knowledge_items.items],
        'total': knowledge_items.total,
        'pages': knowledge_items.pages,
        'current_page': page,
        'per_page': per_page
    })

@app.route('/api/items')
def get_items():
    """获取非遗项目列表API"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    category_id = request.args.get('category_id', type=int)
    keyword = request.args.get('keyword', '')
    
    query = FeiyiItem.query
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if keyword:
        query = query.filter(FeiyiItem.name.contains(keyword) | 
                           FeiyiItem.description.contains(keyword))
    
    items = query.order_by(FeiyiItem.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return jsonify({
        'items': [item.to_dict() for item in items.items],
        'total': items.total,
        'pages': items.pages,
        'current_page': page,
        'per_page': per_page
    })

@app.route('/api/item/<int:item_id>')
def get_item_detail(item_id):
    """获取非遗项目详情API"""
    item = FeiyiItem.query.get_or_404(item_id)
    
    # 获取相关知识
    related_knowledge = FeiyiKnowledge.query.filter_by(item_id=item_id).all()
    
    item_data = item.to_dict()
    item_data['related_knowledge'] = [k.to_dict() for k in related_knowledge]
    
    return jsonify(item_data)

@app.route('/api/search')
def search():
    """全局搜索API"""
    keyword = request.args.get('keyword', '')
    if not keyword:
        return jsonify({'error': '搜索关键词不能为空'}), 400
    
    # 搜索项目
    items = FeiyiItem.query.filter(
        FeiyiItem.name.contains(keyword) | 
        FeiyiItem.description.contains(keyword) |
        FeiyiItem.characteristics.contains(keyword)
    ).limit(10).all()
    
    # 搜索知识库
    knowledge = FeiyiKnowledge.query.filter(
        FeiyiKnowledge.title.contains(keyword) |
        FeiyiKnowledge.content.contains(keyword) |
        FeiyiKnowledge.keywords.contains(keyword)
    ).limit(10).all()
    
    return jsonify({
        'items': [item.to_dict() for item in items],
        'knowledge': [k.to_dict() for k in knowledge],
        'keyword': keyword
    })

@app.route('/categories')
def categories_page():
    """分类页面"""
    return render_template('categories.html', categories=FEIYI_CATEGORIES)

@app.route('/category/<int:category_id>')
def category_detail_page(category_id):
    """分类详情页面"""
    category = next((cat for cat in FEIYI_CATEGORIES if cat['id'] == category_id), None)
    if not category:
        return "分类不存在", 404
    
    # 获取该分类下的项目
    items = FeiyiItem.query.filter_by(category_id=category_id).all()
    
    return render_template('category_detail.html', category=category, items=items)

@app.route('/item/<int:item_id>')
def item_detail_page(item_id):
    """项目详情页面"""
    item = FeiyiItem.query.get_or_404(item_id)
    category = next((cat for cat in FEIYI_CATEGORIES if cat['id'] == item.category_id), None)
    
    # 获取相关知识
    related_knowledge = FeiyiKnowledge.query.filter_by(item_id=item_id).all()
    
    # 获取相关项目（同分类的其他项目）
    related_items = FeiyiItem.query.filter(
        FeiyiItem.category_id == item.category_id,
        FeiyiItem.id != item_id
    ).limit(4).all()
    
    return render_template('item_detail.html', 
                         item=item, 
                         category=category,
                         related_knowledge=related_knowledge,
                         related_items=related_items)

def get_category_description(category_id):
    """获取分类描述"""
    descriptions = {
        1: '口头传统和表现形式，包括作为非物质文化遗产媒介的语言；传统的故事、传说、史诗、神话等。',
        2: '传统音乐包括民歌、器乐、戏曲音乐、宗教音乐等多种形式，体现了中华民族深厚的音乐文化底蕴。',
        3: '传统舞蹈是中华民族文化的重要组成部分，包括民间舞蹈、宫廷舞蹈、宗教舞蹈等多种形式。',
        4: '传统戏剧是中国传统文化的瑰宝，包括京剧、昆曲、豫剧、越剧等多个剧种。',
        5: '曲艺是中华民族独有的艺术形式，包括相声、评书、快板、大鼓等多种表演形式。',
        6: '传统体育、游艺与杂技体现了中华民族的智慧和创造力，包括武术、龙舟、风筝等。',
        7: '传统美术包括绘画、雕塑、工艺美术等，体现了中华民族的审美情趣和艺术成就。',
        8: '传统技艺是中华民族智慧的结晶，包括手工技艺、制作技艺等传统工艺。',
        9: '传统医药是中华民族几千年来积累的宝贵财富，包括中医诊疗法、中药炮制技艺等。',
        10: '民俗是人民群众在长期生产生活中形成的传统习俗，包括节庆、礼仪、信仰等。'
    }
    return descriptions.get(category_id, '传统文化的重要组成部分')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)
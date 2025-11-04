"""
华为云AI接口集成模块
"""
import requests
import json
import os
from typing import Dict, Any, Optional
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class HuaweiAIClient:
    """华为云AI客户端"""
    
    def __init__(self, api_key: str = None, endpoint: str = None):
        """
        初始化华为云AI客户端
        
        Args:
            api_key: API密钥
            endpoint: API端点
        """
        # 使用您提供的API配置
        self.api_key = api_key or os.getenv('HUAWEI_AI_API_KEY') 
        self.endpoint = endpoint or os.getenv('HUAWEI_AI_ENDPOINT') 
        self.model = "deepseek-v3.2-exp"  # 使用您指定的模型
        
        if not self.api_key or not self.endpoint:
            logger.warning("华为云AI配置不完整，请检查环境变量")
        else:
            logger.info("华为云AI配置已加载")
    
    def chat_completion(self, 
                       messages: list, 
                       model: str = None,
                       max_tokens: int = 1000,
                       temperature: float = 0.7) -> Dict[str, Any]:
        """
        调用华为云AI聊天完成接口
        
        Args:
            messages: 消息列表
            model: 模型名称
            max_tokens: 最大token数
            temperature: 温度参数
            
        Returns:
            API响应结果
        """
        if not self.api_key or not self.endpoint:
            return {
                'error': 'AI服务配置不完整',
                'content': '抱歉，AI服务暂时不可用，请联系管理员配置华为云AI接口。'
            }
        
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
        
        # 使用您提供的API格式
        payload = {
            'model': model or self.model,
            'messages': messages,
            'chat_template_kwargs': {
                'thinking': True
            }
        }
        
        try:
            logger.info(f"调用华为云AI接口: {self.endpoint}")
            response = requests.post(
                self.endpoint,
                headers=headers,
                data=json.dumps(payload),
                timeout=30,
                verify=False  # 添加verify=False参数
            )
            
            logger.info(f"API响应状态码: {response.status_code}")
            response.raise_for_status()
            result = response.json()
            
            logger.info("华为云AI接口调用成功")
            return {
                'success': True,
                'content': result.get('choices', [{}])[0].get('message', {}).get('content', ''),
                'usage': result.get('usage', {}),
                'model': result.get('model', model or self.model)
            }
            
        except requests.exceptions.Timeout:
            logger.error("华为云AI接口调用超时")
            return {
                'error': 'timeout',
                'content': '抱歉，AI服务响应超时，请稍后重试。'
            }
        except requests.exceptions.HTTPError as e:
            logger.error(f"华为云AI接口HTTP错误: {e}")
            return {
                'error': 'http_error',
                'content': f'AI服务暂时不可用，HTTP错误: {e.response.status_code}'
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"华为云AI接口请求错误: {e}")
            return {
                'error': 'request_error',
                'content': '网络连接错误，请检查网络设置。'
            }
        except json.JSONDecodeError as e:
            logger.error(f"华为云AI接口响应解析错误: {e}")
            return {
                'error': 'json_error',
                'content': 'AI服务响应格式错误。'
            }
        except Exception as e:
            logger.error(f"华为云AI接口未知错误: {e}")
            return {
                'error': 'unknown_error',
                'content': f'AI服务发生未知错误: {str(e)}'
            }
    
    def ask_about_feiyi(self, question: str, session_id: str = None) -> str:
        """
        询问非遗相关问题
        
        Args:
            question: 用户问题
            session_id: 会话ID（可选）
            
        Returns:
            AI回答
        """
        # 构建非遗专业的系统提示
        system_prompt = """你是一位博学的中华非物质文化遗产文化助手，深谙传统文化之精髓。

请以古雅而不失亲切的语调回答问题，遵循以下原则：
1. 提供准确、专业的非遗知识，引经据典
2. 语言典雅，体现传统文化底蕴
3. 适当运用古典文学表达，但保持现代人易懂
4. 体现对传统文化的敬重和传承精神
5. 如遇不确定信息，坦诚相告
6. 激发用户对非遗文化的兴趣和传承意识

你的回答应如春风化雨，既有学者之严谨，又有师者之温度。"""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
        
        result = self.chat_completion(messages)
        
        if result.get('success'):
            return result['content']
        else:
            return result.get('content', '抱歉，在下暂时无法为您解答，请稍候再试。')
    
    def generate_feiyi_introduction(self, category: str, item_name: str = "") -> str:
        """
        生成非遗项目介绍
        
        Args:
            category: 非遗分类
            item_name: 具体项目名称
            
        Returns:
            生成的介绍文本
        """
        if item_name:
            prompt = f"请详细介绍非物质文化遗产项目：{item_name}（属于{category}类别）。包括其历史渊源、特色特点、传承现状等方面。"
        else:
            prompt = f"请详细介绍非物质文化遗产的{category}类别，包括其定义、主要特征、代表性项目等。"
        
        return self.ask_about_feiyi(prompt)

# 创建全局客户端实例
huawei_ai_client = HuaweiAIClient()

def get_ai_response(question: str, session_id: str = None) -> str:
    """
    获取AI回答的便捷函数
    
    Args:
        question: 用户问题
        session_id: 会话ID
        
    Returns:
        AI回答
    """
    try:
        return huawei_ai_client.ask_about_feiyi(question, session_id)
    except Exception as e:
        logger.error(f"AI响应失败: {e}")
        # 如果华为云AI不可用，使用本地知识库回退
        return get_local_knowledge_response(question)

def get_local_knowledge_response(question):
    """
    基于本地知识库的简单问答回退机制
    """
    question_lower = question.lower()
    
    # 非遗类别相关问答
    if any(keyword in question_lower for keyword in ['昆曲', 'kunqu']):
        return """昆曲是中国最古老的戏曲剧种之一，被誉为"百戏之祖"。它起源于明代，以其精美的唱腔、优雅的表演和深厚的文学底蕴而闻名。昆曲的表演特点包括：
1. 唱腔优美，注重字正腔圆
2. 表演细腻，身段优雅
3. 文学性强，多取材于古典名著
4. 音乐伴奏以笛子为主
昆曲于2001年被联合国教科文组织列为"人类口述和非物质遗产代表作"。"""
    
    elif any(keyword in question_lower for keyword in ['京剧', 'peking opera', '国粹']):
        return """京剧是中国的国粹艺术，形成于19世纪中期，具有以下特点：
1. 行当分明：生、旦、净、丑四大行当
2. 唱念做打：综合性表演艺术
3. 脸谱艺术：不同颜色代表不同性格
4. 服装华美：传统戏曲服饰精美
5. 音乐伴奏：以京胡为主要乐器
京剧融合了音乐、舞蹈、文学、美术等多种艺术形式，是中华文化的重要载体。"""
    
    elif any(keyword in question_lower for keyword in ['针灸', 'acupuncture', '中医']):
        return """中医针灸是中国传统医学的重要组成部分，有着数千年的历史：
1. 历史悠久：起源可追溯到石器时代
2. 理论基础：基于经络学说和阴阳五行理论
3. 治疗方法：通过针刺和艾灸调节人体气血
4. 适应症广：可治疗多种疾病
5. 安全有效：副作用小，疗效显著
针灸于2010年被联合国教科文组织列入人类非物质文化遗产代表作名录。"""
    
    elif any(keyword in question_lower for keyword in ['太极', 'taichi', '太极拳']):
        return """太极拳是中国传统武术的代表，具有深厚的文化价值：
1. 哲学内涵：体现了中国古代的阴阳哲学
2. 健身功效：强身健体，延年益寿
3. 文化传承：承载着中华武术文化
4. 国际影响：在世界各地广泛传播
5. 精神修养：注重内外兼修，身心并重
太极拳不仅是一种武术，更是一种生活哲学和文化符号。"""
    
    elif any(keyword in question_lower for keyword in ['蜀锦', 'shu brocade']):
        return """蜀锦是中国四大名锦之一，产于四川成都，有着悠久的历史：
1. 历史传承：始于春秋战国时期
2. 工艺精湛：采用传统手工织造技术
3. 图案精美：多以花鸟、山水为题材
4. 色彩丰富：使用天然染料，色泽持久
5. 文化价值：体现了古代丝绸文化的精髓
蜀锦制作技艺于2006年被列入国家级非物质文化遗产名录。"""
    
    elif any(keyword in question_lower for keyword in ['二十四节气', '节气', 'solar terms']):
        return """二十四节气是中国古代农业文明的智慧结晶：
1. 科学价值：准确反映季节变化和气候规律
2. 农业指导：指导农事活动的重要依据
3. 文化内涵：承载着丰富的民俗文化
4. 生活智慧：影响着人们的日常生活
5. 国际认可：2016年被列入联合国教科文组织人类非物质文化遗产代表作名录
二十四节气体现了中华民族对自然规律的深刻认识。"""
    
    # 通用非遗问答
    elif any(keyword in question_lower for keyword in ['非遗', '非物质文化遗产', 'intangible heritage']):
        return """非物质文化遗产是指各种以非物质形态存在的与群众生活密切相关、世代相承的传统文化表现形式。包括：
1. 民间文学：神话、传说、民间故事等
2. 传统音乐：民歌、器乐等
3. 传统舞蹈：民族舞蹈、宗教舞蹈等
4. 传统戏剧：各种地方戏曲
5. 曲艺：相声、评书等
6. 传统体育游艺与杂技
7. 传统美术：绘画、雕塑等
8. 传统技艺：手工艺制作技艺
9. 传统医药：中医药等
10. 民俗：节庆、礼仪等
保护非遗对于传承中华文化具有重要意义。"""
    
    else:
        return f"""感谢您对非物质文化遗产的关注！您的问题"{question}"很有意思。

我是"非遗之光"网站的AI助手，专门为您介绍中国丰富的非物质文化遗产。虽然目前AI服务配置尚未完善，但我可以为您提供以下帮助：

🎭 **戏曲艺术**：昆曲、京剧等传统戏曲
🎵 **音乐舞蹈**：各地民歌、民族舞蹈
🎨 **传统技艺**：蜀锦、景泰蓝等手工艺
⚕️ **传统医药**：中医针灸、中药炮制
🥋 **体育杂技**：太极拳、武术等
📅 **民俗文化**：二十四节气、传统节日

您可以浏览网站的分类页面了解更多详细信息，或者询问具体的非遗项目。让我们一起探索中华文化的瑰宝！"""
from flask import Flask, request, jsonify
import logging
from bot_states import BotStates
from max_api import MaxAPI
from gsheets_integration import GoogleSheetsIntegration
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация компонентов
bot_states = BotStates()
max_api = MaxAPI()
gsheets = GoogleSheetsIntegration()

class MaxBot:
    def __init__(self):
        self.confirmation_token = os.getenv("MAX_CONFIRMATION_TOKEN")
        self.secret_key = os.getenv("MAX_SECRET_KEY")
        self.access_token = os.getenv("MAX_ACCESS_TOKEN")
    
    def handle_webhook(self, data):
        """Обработка входящих вебхуков от MAX"""
        try:
            # Проверяем тип события
            event_type = data.get('type')
            
            if event_type == 'confirmation':
                # Подтверждение URL для Callback API
                return self.confirmation_token
                
            elif event_type == 'message_new':
                # Новое сообщение
                return self.handle_new_message(data)
                
            elif event_type == 'message_event':
                # Событие от кнопки
                return self.handle_button_event(data)
            
            return 'ok'
            
        except Exception as e:
            logger.error(f"Webhook error: {e}")
            return 'ok'
    
    def handle_new_message(self, data):
        """Обработка нового сообщения"""
        message_data = data['object']['message']
        user_id = message_data['from_id']
        text = message_data.get('text', '')
        
        # Если это команда /start
        if text.lower() in ['/start', 'start', 'начать']:
            return self.send_welcome_message(user_id)
        
        # Обработка текстовых сообщений
        return self.handle_user_message(user_id, text)
    
    def handle_button_event(self, data):
        """Обработка нажатия кнопки"""
        user_id = data['object']['user_id']
        payload = data['object']['payload']
        
        if isinstance(payload, dict) and 'command' in payload:
            command = payload['command']
            return self.handle_button_command(user_id, command)
        
        return 'ok'
    
    def send_welcome_message(self, user_id):
        """Отправка приветственного сообщения"""
        welcome_text = """Привет! 👋 Я Майлз — виртуальный помощник цифрового сервиса «Я студент», созданный тремя студентами.

Сейчас я помогу тебе разобраться, как работает это окно. Если появятся вопросы — просто напиши мне, я с радостью помогу.

Выбери категорию:"""
        
        keyboard = {
            "inline": True,
            "buttons": [
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Абитуриентам",
                            "payload": '{"command": "applicants"}'
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text", 
                            "label": "Студентам",
                            "payload": '{"command": "students"}'
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Сотрудникам университета", 
                            "payload": '{"command": "staff"}'
                        },
                        "color": "primary"
                    }
                ]
            ]
        }
        
        max_api.send_message(user_id, welcome_text, keyboard)
        return 'ok'
    
    def handle_button_command(self, user_id, command):
        """Обработка команд от кнопок"""
        response = bot_states.handle_command(user_id, command)
        
        if response.get('keyboard'):
            max_api.send_message(user_id, response['text'], response['keyboard'])
        else:
            max_api.send_message(user_id, response['text'])
        
        return 'ok'
    
    def handle_user_message(self, user_id, text):
        """Обработка текстовых сообщений пользователя"""
        # Здесь будет логика обработки текстовых ответов
        # (отзывы, вопросы к ИИ и т.д.)
        response = bot_states.handle_text_message(user_id, text)
        max_api.send_message(user_id, response)
        return 'ok'

# Инициализация бота
max_bot = MaxBot()

@app.route('/webhook', methods=['POST'])
def webhook():
    """Endpoint для вебхуков от MAX"""
    data = request.get_json()
    logger.info(f"Received webhook: {data}")
    
    result = max_bot.handle_webhook(data)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "max-bot"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

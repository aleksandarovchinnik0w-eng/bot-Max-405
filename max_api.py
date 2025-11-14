import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

class MaxAPI:
    def __init__(self):
        self.access_token = os.getenv("MAX_ACCESS_TOKEN")
        self.api_version = "5.199"
        self.base_url = "https://api.vk.com/method"
    
    def send_message(self, user_id, message, keyboard=None):
        """Отправка сообщения пользователю"""
        try:
            method_url = f"{self.base_url}/messages.send"
            
            payload = {
                "user_id": user_id,
                "message": message,
                "access_token": self.access_token,
                "v": self.api_version,
                "random_id": 0
            }
            
            if keyboard:
                payload["keyboard"] = json.dumps(keyboard)
            
            response = requests.post(method_url, data=payload)
            result = response.json()
            
            if 'error' in result:
                logger.error(f"API Error: {result['error']}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Send message error: {e}")
            return False
    
    def create_keyboard(self, buttons, inline=True):
        """Создание клавиатуры для MAX"""
        keyboard = {
            "inline": inline,
            "buttons": []
        }
        
        for row in buttons:
            keyboard_row = []
            for button in row:
                keyboard_row.append({
                    "action": {
                        "type": "text",
                        "label": button['label'],
                        "payload": json.dumps(button['payload'])
                    },
                    "color": button.get('color', 'primary')
                })
            keyboard["buttons"].append(keyboard_row)
        
        return keyboard

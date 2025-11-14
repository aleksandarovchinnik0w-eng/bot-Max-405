import json
import os

class BotStates:
    def __init__(self):
        self.user_states = {}
    
    def handle_command(self, user_id, command):
        """Обработка команд от кнопок"""
        # Сохраняем состояние пользователя
        self.user_states[user_id] = command
        
        if command == "applicants":
            return self.get_applicants_menu()
        elif command == "students":
            return self.get_students_menu()
        elif command == "staff":
            return self.get_staff_menu()
        elif command == "back":
            return self.handle_back_command(user_id)
        
        # Обработка других команд...
        return {"text": "Выберите действие:"}
    
    def get_applicants_menu(self):
        """Меню для абитуриентов"""
        text = """Прекрасно! ✨ Я вижу, ты абитуриент — значит, впереди самое интересное!

Выбери, с чего начнём 👇"""
        
        keyboard = {
            "inline": True,
            "buttons": [
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Направления обучения", 
                            "payload": {"command": "faculties"}
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Приемная комиссия",
                            "payload": {"command": "admission_committee"}
                        },
                        "color": "secondary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text", 
                            "label": "Выразительная кнопка",
                            "payload": {"command": "feedback"}
                        },
                        "color": "positive"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Назад",
                            "payload": {"command": "back"}
                        },
                        "color": "negative" 
                    }
                ]
            ]
        }
        
        return {"text": text, "keyboard": keyboard}
    
    def get_students_menu(self):
        """Меню для студентов"""
        text = "Привет, студент! 👋 Чем могу помочь?"
        
        keyboard = {
            "inline": True,
            "buttons": [
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Расписание",
                            "payload": {"command": "schedule"}
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Учебные сервисы", 
                            "payload": {"command": "study_services"}
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Назад",
                            "payload": {"command": "back"}
                        },
                        "color": "negative"
                    }
                ]
            ]
        }
        
        return {"text": text, "keyboard": keyboard}
    
    def handle_back_command(self, user_id):
        """Обработка кнопки Назад"""
        previous_state = self.user_states.get(user_id, "main")
        
        if previous_state == "applicants":
            return self.get_applicants_menu()
        elif previous_state == "students":
            return self.get_students_menu() 
        elif previous_state == "staff":
            return self.get_staff_menu()
        else:
            return self.get_main_menu()
    
    def get_main_menu(self):
        """Главное меню"""
        text = "Выберите категорию:"
        
        keyboard = {
            "inline": True,
            "buttons": [
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Абитуриентам",
                            "payload": {"command": "applicants"} 
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Студентам",
                            "payload": {"command": "students"}
                        },
                        "color": "primary"
                    }
                ],
                [
                    {
                        "action": {
                            "type": "text",
                            "label": "Сотрудникам университета",
                            "payload": {"command": "staff"}
                        },
                        "color": "primary"
                    }
                ]
            ]
        }
        
        return {"text": text, "keyboard": keyboard}

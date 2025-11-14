import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from bot_states import BotStates
from gsheets_integration import GoogleSheetsIntegration
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MaxBot:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.states = BotStates()
        self.gsheets = GoogleSheetsIntegration()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        welcome_text = """
Привет! 👋 Я Майлз — виртуальный помощник цифрового сервиса «Я студент», созданный тремя студентами.

Сейчас я помогу тебе разобраться, как работает это окно. Если появятся вопросы — просто напиши мне, я с радостью помогу.

Цифровой сервис «Я студент» — это удобная платформа, созданная на базе Max, чтобы упростить жизнь абитуриентов, студентов и сотрудников университета.

Здесь можно решать учебные и организационные вопросы в одном месте, экономя время на рутине.

Пока сервис работает на базе Крымского федерального университета, но мои создатели уже планируют расширение — возможно, совсем скоро твой университет тоже станет часть проекта 🚀

Если ты абитуриент, я помогу тебе:
• Разобраться с факультетами и направлениями обучения
• Узнать, сколько баллов нужно для поступления на интересующее направление
• Подобрать подходящее направление по твоим интересам и результатам
• Быстро связаться с приёмной комиссией
Добро пожаловать в «Я студент» — давай разберёмся во всём вместе! 🎓
        """

        keyboard = [
            [InlineKeyboardButton("Абитуриентам", callback_data="applicants")],
            [InlineKeyboardButton("Студентам", callback_data="students")],
            [InlineKeyboardButton("Сотрудникам университета", callback_data="staff")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(welcome_text, reply_markup=reply_markup)

    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик нажатий кнопок"""
        query = update.callback_query
        await query.answer()

        user_id = query.from_user.id
        data = query.data

        # Сохраняем состояние пользователя
        if data in ["applicants", "students", "staff"]:
            context.user_data['current_section'] = data

        # Обрабатываем кнопку в зависимости от текущего состояния
        response = await self.states.handle_state(user_id, data, context.user_data)

        if response.get('file'):
            await query.message.reply_document(document=response['file'])
        else:
            keyboard = self._create_keyboard(response.get('buttons', []))
            await query.edit_message_text(
                text=response['text'],
                reply_markup=keyboard,
                parse_mode='Markdown'
            )

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик текстовых сообщений"""
        user_message = update.message.text
        user_id = update.message.from_user.id

        # Обработка выразительной кнопки (отзывы)
        if context.user_data.get('waiting_feedback'):
            await self._save_feedback(user_id, user_message)
            await update.message.reply_text("Спасибо за отзыв! 💫")
            context.user_data['waiting_feedback'] = False
            return

        # Обработка вопросов к ИИ помощнику
        if context.user_data.get('waiting_ai_question'):
            ai_response = await self._get_ai_response(user_message)
            await update.message.reply_text(ai_response)
            return

        # Обработка предложений проектов
        if context.user_data.get('waiting_project_proposal'):
            await self._save_project_proposal(user_id, user_message)
            await update.message.reply_text("Спасибо за предложение проекта! 🚀")
            context.user_data['waiting_project_proposal'] = False
            return

        # Обработка отзывов о преподавателях
        if context.user_data.get('waiting_sop_feedback'):
            await self._save_sop_feedback(user_id, user_message)
            await update.message.reply_text("Благодарим за оценку! 📝")
            context.user_data['waiting_sop_feedback'] = False
            return

    def _create_keyboard(self, buttons):
        """Создает клавиатуру из списка кнопок"""
        keyboard = []
        for button in buttons:
            if isinstance(button, list):
                row = [InlineKeyboardButton(btn, callback_data=btn) for btn in button]
                keyboard.append(row)
            else:
                keyboard.append([InlineKeyboardButton(button, callback_data=button)])
        return InlineKeyboardMarkup(keyboard)

    async def _save_feedback(self, user_id, feedback):
        """Сохраняет отзыв в Google Sheets"""
        try:
            self.gsheets.save_feedback(user_id, feedback)
        except Exception as e:
            logger.error(f"Error saving feedback: {e}")

    async def _save_project_proposal(self, user_id, proposal):
        """Сохраняет предложение проекта"""
        try:
            self.gsheets.save_project_proposal(user_id, proposal)
        except Exception as e:
            logger.error(f"Error saving project proposal: {e}")

    async def _save_sop_feedback(self, user_id, feedback):
        """Сохраняет отзыв о преподавателе"""
        try:
            self.gsheets.save_sop_feedback(user_id, feedback)
        except Exception as e:
            logger.error(f"Error saving SOP feedback: {e}")

    async def _get_ai_response(self, question):
        """Получает ответ от ИИ помощника"""
        # Здесь будет интеграция с вашей ИИ системой
        return "Это демо-ответ от ИИ помощника. В реальной версии здесь будет интеграция с вашей базой знаний."

    def run(self):
        """Запускает бота"""
        application = Application.builder().token(self.token).build()

        # Обработчики
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CallbackQueryHandler(self.handle_button))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

        # Запуск бота
        application.run_polling()


if __name__ == "__main__":
    bot = MaxBot()
    bot.run()
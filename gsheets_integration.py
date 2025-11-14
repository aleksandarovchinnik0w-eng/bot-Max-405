import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime


class GoogleSheetsIntegration:
    def __init__(self):
        self.setup_client()

    def setup_client(self):
        """Настройка клиента Google Sheets"""
        try:
            scopes = [
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive"
            ]

            creds = Credentials.from_service_account_file(
                "credentials/service_account.json",
                scopes=scopes
            )

            self.client = gspread.authorize(creds)

        except Exception as e:
            print(f"Google Sheets setup error: {e}")

    def save_feedback(self, user_id, feedback):
        """Сохраняет отзыв в таблицу"""
        try:
            worksheet = self.client.open("MaxBot Data").worksheet("Feedback")
            worksheet.append_row([
                datetime.now().isoformat(),
                user_id,
                feedback,
                "user_feedback"
            ])
        except Exception as e:
            print(f"Error saving feedback: {e}")

    def save_project_proposal(self, user_id, proposal):
        """Сохраняет предложение проекта"""
        try:
            worksheet = self.client.open("MaxBot Data").worksheet("Projects")
            worksheet.append_row([
                datetime.now().isoformat(),
                user_id,
                proposal,
                "pending"
            ])
        except Exception as e:
            print(f"Error saving project proposal: {e}")

    def save_sop_feedback(self, user_id, feedback):
        """Сохраняет отзыв о преподавателе"""
        try:
            worksheet = self.client.open("MaxBot Data").worksheet("SOP")
            worksheet.append_row([
                datetime.now().isoformat(),
                user_id,
                feedback
            ])
        except Exception as e:
            print(f"Error saving SOP feedback: {e}")

    def get_open_days(self):
        """Получает информацию о днях открытых дверей"""
        try:
            worksheet = self.client.open_by_key("your_google_sheet_id").worksheet("OpenDays")
            records = worksheet.get_all_records()
            return records
        except Exception as e:
            print(f"Error getting open days: {e}")
            return []
from utils.google_sheets import Spreadsheets

from data.config import SPREADSHEET_ID, CREDENTIALS_FILE


spreadsheets = Spreadsheets(CREDENTIALS_FILE, SPREADSHEET_ID)

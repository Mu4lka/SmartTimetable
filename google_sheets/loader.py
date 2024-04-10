from data.config import SPREADSHEET_ID, CREDENTIALS_FILE
from utils.google_sheets import Spreadsheets

spreadsheets = Spreadsheets(CREDENTIALS_FILE, SPREADSHEET_ID)

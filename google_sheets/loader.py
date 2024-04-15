from data.config import SPREADSHEET_ID, CREDENTIALS_FILE
from utils.google import AsyncSpreadsheets

spreadsheets = AsyncSpreadsheets(CREDENTIALS_FILE, SPREADSHEET_ID)

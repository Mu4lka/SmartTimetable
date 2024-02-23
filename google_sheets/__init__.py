import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from data.config import CREDENTIALS_FILE

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
http_auth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http=http_auth)

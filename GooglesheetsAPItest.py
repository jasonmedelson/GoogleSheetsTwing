import gspread
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json',scope)
client = gspread.authorize(creds)
sheet = client.open('daybreak twinge automation').sheet1
legislators = sheet.get_all_records()
#print(legislators)
sheet.update_cell(1,2,'Stacy')
print("done")

import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

#logging.basicConfig(level=logging.DEBUG)

#define scope of permissions
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#access credential data
credentials = ServiceAccountCredentials.from_json_keyfile_name('GrizzlyAuth-9eb3e3edde26.json', scope)

#authorize using credentials
gc = gspread.authorize(credentials)

#open worksheet
wks = gc.open('GrizzlyAuth').sheet1

print ("Worksheet Authorized")

#define login method to login people
def login(idnumber):

    prevID = idnumber
    defaultRow = 1

    #START TRY: break if cell is not found
    try:
        cell = wks.find(idnumber)
        print("idnumber found")
    except gspread.exceptions.CellNotFound:

        print("idnumber not found")
        while (wks.cell(defaultRow, 1).value != ""):

            defaultRow+=1
            
        wks.update_cell(defaultRow, 1, idnumber)
        cell = wks.find(idnumber)
        wks.update_cell(cell.row, 7, datetime.now().time())
        wks.update_cell(cell.row, 11, 'FALSE')

    #END TRY

    valueOfLoggedIn = wks.cell(cell.row, 11).value

    #BEGIN IF: if logged in, log out. else
    if (valueOfLoggedIn == "TRUE"):

        #if logged in, logout
        wks.update_cell(cell.row, 11, 'FALSE')

        #update logout time
        wks.update_cell(cell.row, 8, datetime.now().time())
        print("logged out") #logged out

    elif(valueOfLoggedIn == "FALSE"):

        #if logged out, login
        wks.update_cell(cell.row, 11, 'TRUE')

        #update login time
        wks.update_cell(cell.row, 7, datetime.now().time())

        #blank out logout time
        wks.update_cell(cell.row, 8, "logged in")
        print("logged in") #logged in

        while(idnumber == idnumber):

            #if cell is not found, break out of loop
            try:
                cell = wks.find(idnumber)
            except gspread.exceptions.CellNotFound:
                break
            
            #if value changes, break out of loop
            if (idnumber != prevID):
                print("Name is not same as previous name.")
                break

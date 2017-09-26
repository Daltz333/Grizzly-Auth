import gspread
import logging
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

#logging.basicConfig(level=logging.DEBUG)

#define scope of permissions
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

#access credential data
credentials = ServiceAccountCredentials.from_json_keyfile_name('GrizzlyAuth-f7980f75f42b.json', scope)

#authorize using credentials
gc = gspread.authorize(credentials)

#open worksheet
wks = gc.open('GrizzlyAuth').worksheet('Current')
wks2 = gc.open('GrizzlyAuth').worksheet('LoggedHours')

print ("Worksheet Authorized")

#logout at midnight
def logout():
    try:
        cell_list = wks.range('11:60')
        
        for cell in cell_list:
            cell.value = 'FALSE'

        # Update in batch
        wks.update_cells(cell_list)

    except gspread.exceptions.AuthenticationError:
        gc = gspread.authorize(credentials)
        print("Sheet not authorized... Authorized.")
        logout()

#define login method to login people
def login(idnumber):
    defaultColumn = 1
    defaultRow = 1

#START TRY: except and reauthenticate
    try:
        #START TRY: break if cell is not found
        try:
            cell = wks.find(idnumber)
            print(idnumber + " found")

        except gspread.exceptions.CellNotFound:
            return

        #END TRY

        valueOfLoggedIn = wks.cell(cell.row, 11).value

        #BEGIN IF: if logged in, log out. else
        if (valueOfLoggedIn == "TRUE"):
            #if logged in, logout
            wks.update_cell(cell.row, 11, 'FALSE')

            #update logout time
            wks.update_cell(cell.row, 8, datetime.now().time())

            #grab total hours
            totalHours = wks.cell(cell.row, 10).value

            #attempt to get date variable
            try:
                currentdate = wks2.find(datetime.today().date())
            
            #if date not found, create date
            except gspread.exceptions.CellNotFound:
                while (wks2.cell(1, defaultColumn).value != ""):
                    defaultColumn +=1

                wks2.update_cell(1, defaultColumn, datetime.today().date())
                currentdate = wks2.find(datetime.today().date())

            #attempt to get id variable on wks2
            try:
                wks2_idnumber = wks2.find(idnumber)

            #if idnumber not found, create idnumber
            except gspread.exceptions.CellNotFound:
                while (wks2.cell(defaultRow, 1).value != ""):
                    defaultRow+=1

                wks2.update_cell(defaultRow, 1, idnumber)
                wks2_idnumber = wks2.find(idnumber)

            wks2.update_cell(wks2_idnumber.row, currentdate.col, totalHours)

            print(idnumber + " logged out") #logged out

        elif(valueOfLoggedIn == "FALSE"):
            #if logged out, login
            wks.update_cell(cell.row, 11, 'TRUE')

            #update login time
            wks.update_cell(cell.row, 7, datetime.now().time())

            #blank out logout time
            wks.update_cell(cell.row, 8, "logged in")
            print(idnumber + " logged in") #logged in

        else:
            pass

    except gspread.exceptions.AuthenticationError:
        gc = gspread.authorize(credentials)
        print("Sheet not authorized... Authorized.")
        return

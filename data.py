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

            #log hours and date
            try:
                #find idnumber on 2nd sheet, if found then update the date/time
                cell2 = wks2.find(idnumber)
                while (wks2.cell(defaultColumn) != ""):
                    defaultColumn+=1

                cell2_value = datetime.today().date() + " " + datetime.now().time()
                wks2.update_cell(cell2.row, defaultColumn, cell2_value)

            except gspread.exceptions.CellNotFound:
                while (wks2.cell(defaultRow) != ""):
                    defaultColumn+=1

                wks2.update_cell(defaultColumn, 1, idnumber)
                cell2 = wks2.find(idnumber)

                while (wks2.cell(defaultColumn) != ""):
                    defaultColumn+=1

                cell2_value = datetime.today().date() + " " + datetime.now().time()
                wks2.update_cell(cell2.row, defaultColumn, cell2_value)

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

login(108479)
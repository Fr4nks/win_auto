from pywinauto.application import Application

import os
import json
from datetime import datetime
from datetime import timedelta
import tkinter as tk

import warnings
warnings.filterwarnings("ignore", message="32-bit application should be automated using 32-bit Python")


# get last month
with open('settings.json') as f:
    settings = json.load(f)

genhire = settings['genhire']
name = settings['name']
password = settings['password']

print(genhire )

if os.path.isfile(genhire) is False:
    print('THIS PATH DOES NOT EXIST!!!: ', genhire)
else:
    print('THIS PATH EXISTS: ', genhire)


now = datetime.now()
pre_month_last_obj =  now.replace(day=1) - timedelta(days=1)
premonthlast = datetime.strftime(pre_month_last_obj,'%d%m%Y')

pre_month_first_obj = pre_month_last_obj.replace(day=1)
premonthfirst = datetime.strftime(pre_month_first_obj,'%d%m%Y')

#app = Application(backend="uia").start("Z:\GHFB.exe")
#app = Application(backend="win32").connect(path=r"Z:\GHFB.exe", title="Genhire")
#app.Tfmain.set_focus()

#app.Tfmain.TLMDPageControl.click(coords=(0, 0))

#test = app.Tfmain.TLMDPageControl.print_control_identifiers()
def close_windows(app):
    app.TfrmViewHire.TBitBtn18.click()
    app.ViewContractDetails.TBitBtn1.click()

#    close_window(TfrmViewHire=None, TBitBtn18=None)
#    close_window(ViewContractDetails=None, TPanel5=None)
#    close_window(ViewQuoteDetails=None, TPanel18=None)
#    close_window(NEWCONTRACT=None, TBitBtn3=None)



def task_input(task=None):
    if task != 's' and task != 'r' and task != 'a' and task != 't':
        print ('Enter s for Statement')
        print ('Enter r for Repair')
        print ('Enter a for Repair and Statement')
        print ('')
        task = input("Enter: s, r, a: ")
        if task != 's' and task != 'r' and task != 'a' and task != 't':
            return task_input()
        else:
            return task

def login(app, name, password):
    try:
        app.TfmLogin.TBtnWinControl2.click()
        app.TwwLookupDlg.wait('visible', timeout=5)
        app.TwwLookupDlg.TwwIncrementalSearch1.type_keys(name+'{ENTER}')
        app.TfrmLogin.TEdit1.type_keys(password+'{ENTER}')
    except:
        print('Genhire already open')

def connect_genhire():
    try:
        app = Application(backend="win32").connect(path=genhire, title="Genhire")
        app.Tfmain.set_focus()
        print('Genhire is running...')
        print('Are we logid in?')
        loged_in = app.Tfmain.is_visible()
        if loged_in is False:
            print('No')
            login(app, name, password)
        else:
            print('Yes')
        return app
    except:
        print('Genhire is not open, Try to start')
        pass
    try:
        app = Application(backend="win32").start(genhire)
        print('Genhire us starting...')
        login(app, name, password)
        print('Genhire is logging in...')
        return app
    except:
        print('Genhire failed to open')

def repair(app, client):
    app.Tfmain.TLMDPageControl.click_input(coords = (701, 10))
    app.Tfmain.TLMDPageControl.click_input(coords = (36, 40))
    app.TfrmCompany.TLMDPageControl1.click_input(coords = (546, 15))
    app.TfrmCompany.TBitBtn2.click() #Repair Invoice Calculation
    app.TfrmInvRepair.TBtnWinControl1.click() 
    app.TwwLookupDlg.TwwIncrementalSearch1.type_keys(client+"{ENTER}")
    app.TfrmInvRepair.TBitBtn3.click() #Invoice Repair | OK
    app.TMessageForm.TButton2.click() #POPUP | Are you sure you wish to Repair all invoices [YES].
    app.TfrmInvRepair.wait_not('visible', timeout=3600000000)
    app.TfrmCompany.TBitBtn4.click()
    
def exit_this(app):
    app.Find.Close.Click()
    #main_exist = app.Tfmain.exists()
    #if main_exist is True:
    #    app.Tfmain.TBitBtn2.click()
    #    app.TmessageForm.TButton1.click()

def last_month(app):
    app.Tfmain.TLMDPageControl.click_input(coords = (515, 10))
    app.Tfmain.TLMDPageControl.click_input(coords = (664, 91))
    #est = app.TfrmAgeState.TwwDBDateTimePicker.print_control_identifiers()
    #app.TfrmAgeState.TBtnWinControl5.click().click().type_keys('{PAUSE 0.5}7{PAUSE 0.5}')
    #.type_keys(premonthlast)1010
    app.TfrmAgeState.TBtnWinControl5.click()
    #app.TfrmAgeState.TBtnWinControl5.click_input(coords = (10, -10))
    app.TfrmAgeState.TwwwDBDateTimePicker2.click_input(coords = (10, 10), double = True,)
    #app.TfrmAgeState.TwwwDBDateTimePicker2.click().type_keys('07', with_spaces=True, set_foreground=False)

def statement(app, client):
    #app.Tfmain.TLMDPageControl.FinancialsTLMDTabSheet.click()
    # !!!!!!!!!FINANCIALS
    app.Tfmain.TLMDPageControl.click_input(coords = (515, 10))
    #530 1.5
    #815

    #1366
    #1920 1.4

    #app.Tfmain.TLMDPageControl.FinancialsTLMDTabSheet.Financials.print_control_identifiers()
    # !!!!!!!!!AGEING
    app.Tfmain.TLMDPageControl.click_input(coords = (664, 91))
    #app.Tfmain.TLMDPageControl.print_control_identifiers()
    last_month(app)
    app.TfrmAgeState.TBtnWinControl3.click()
    app.Lookup.TwwIncrementalSearch.type_keys(client)
    app.Lookup.TwwIncrementalSearch.type_keys('{PAUSE 0.5}{UP}')
    last_month(app)
    app.Lookup.TBitBtn2.click()
    app.TfrmAgeState.TBtnWinControl2.click()
    app.Lookup.TwwIncrementalSearch.type_keys(client)
    app.Lookup.TwwIncrementalSearch.type_keys('{PAUSE 0.5}{DOWN}')
    app.Lookup.TBitBtn2.click()
    app.TfrmAgeState.TBitBtn2.click()
    app.TMessageForm.TButton2.click()
    app.TfrmAgeState.TBitBtn9.click()
    app.Warning.TButton1.click()
    app.TfrmAgeState.TBtnWinControl3.click()
    app.Lookup.TwwIncrementalSearch.type_keys(client)
    app.Lookup.TBitBtn2.click()
    app.TfrmAgeState.TBtnWinControl2.click()
    app.Lookup.TwwIncrementalSearch.type_keys(client)
    app.Lookup.TBitBtn2.click()
    app.TfrmAgeState.TBitBtn8.click()
    app.TmessageForm.TButton1.click()
    app.TmessageForm.TButton1.click()
    app.TfrxPreviewForm.TToolBar1.print_control_identifiers()
    app.TfrxPreviewForm.TToolBar1.click_input(coords = (60, 16))
    app.TfrxPDFExportDialog.TButton2.click()
    #app.TfrxPDFExportDialog.wait_not('visible', timeout=360)
    app.SaveAs.type_keys('{PAUSE 0.5}{ENTER}')

client = input("Please enter Client Code: ")

task = task_input()

if task == 's':
    app = connect_genhire()
    statement(app, client)
elif task == 'r':
    app = connect_genhire()
    if " " in client:
        client = client.split()
        for i in client:
            repair(app, i)
    else:
        repair(app, client)

    app.Tfmain.TBitBtn2.click()
    app.TMessageForm.TButton1.click()
    app = connect_genhire()
elif task == 'a':
    app = connect_genhire()
    repair(app, client)
    app.Tfmain.TBitBtn2.click()
    app.TMessageForm.TButton1.click()
    app = connect_genhire()
    statement(app, client)
elif task == 't':
    app = connect_genhire()
    close_windows(app)


#app.TfrmAgeState.TBitBtn2.click()


#test = app.Tfmain.IME.print_control_identifiers()

#app.Tfmain.get_dialog_props_from_handle()

#app = Application(backend="win32").connect(handle=0x00200418)
#app.IME.Financials.click()
# L313, T313, R1132, B522)
# 'Button', 'Day \r\nEnd', 'Day \r\nEndButton', 'Button0', 'Button1', 'Button2', 'ExitButton', 'Exit', 'Pane', '', 'Pane0', 'Pane1', 'Pane2', '0', '1', '2', 'Pane3', 'Hiring', 'HiringPane', '3', 'TitleBar', 'Menu', 'SystemMenu', 'System', 'SystemMenuItem', 'MenuItem', 'System0', 'System1', 'System2', 'Button3', 'Minimize', 'MinimizeButton', 'Button4', 'Maximize', 'MaximizeButton', 'Button5', 'CloseButton', 'Close'
# 'Day \r\nEndButton', 'Button', 'Day \r\nEnd', 'Button0', 'Button1', 'Button2',
# 'Exit', 'ExitButton', '', 'Pane', '0', '1', '2', 'Pane0', 'Pane1', 'Pane2', 'Financials', 'FinancialsPane', 'Pane3', '3', 'TitleBar', 'System', 'Menu', 'SystemMenu', 'System0', 'System1', 'System2', 'MenuItem', 'SystemMenuItem', 'Button3', 'Minimize', 'MinimizeButton', 'MaximizeButton', 'Button4', 'Maximize', 'CloseButton', 'Button5', 'Close']
# ['Button', 'Day \r\nEndButton', 'Day \r\nEnd', 'Button0', 'Button1', 'Button2', 'Exit', 'ExitButton', '', 'Pane', '0', '1', '2', 'Pane0', 'Pane1', 'Pane2', 'Pane3', 'ClientsPane', 'Clients', '3', 'TitleBar', 'SystemMenu', 'Menu', 'System', 'MenuItem', 'SystemMenuItem', 'System0', 'System1', 'System2', 'Button3', 'MinimizeButton', 'Minimize', 'Button4', 'Maximize', 'MaximizeButton', 'Button5', 'Close', 'CloseButton'])'

#GenhireHiringmanagementSoftwareXe3 === MAIN WINDOW ===
#StaticWrapper
#TLMDPageControl


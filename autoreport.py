from pywinauto.application import Application
from pywinauto.keyboard import send_keys

from datetime import datetime
from datetime import timedelta
import time



# get last month
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

def login(app, name='FR', password='FRA'):
    try:
        app.TfmLogin.set_focus()
        app.TfmLogin.TBtnWinControl2.click()

        app.TwwLookupDlg.wait('visible', timeout=5)
        app.TwwLookupDlg.TwwDBGrid.set_focus()
        time.sleep(1)
        app.TwwLookupDlg.TwwIncrementalSearch1.send_keystrokes('{BACKSPACE}{BACKSPACE}{BACKSPACE}{BACKSPACE}')
        app.TwwLookupDlg.TwwIncrementalSearch1.send_keystrokes(name)
        time.sleep(1)
        app.TwwLookupDlg.TBitBtn2.click()

        app.TfrmLogin.wait('visible', timeout=5)
        app.TfrmLogin.TEdit1.type_keys(password)
        app.TfrmLogin.TBitBtn2.click()
    except:
        print('Genhire already open')

def connect_genhire():
    try:
        app = Application(backend="win32").connect(path=r"Z:\GHFB.exe", title="Genhire")
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
        app = Application(backend="win32").start(r"Z:\GHFB.exe")
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
    app.TfrmCompany.TBitBtn2.click()
    app.TfrmInvRepair.TBtnWinControl1.click()
    app.TwwLookupDlg.TwwIncrementalSearch1.type_keys(client)
    app.TwwLookupDlg.TBitBtn2.click()
    app.TfrmInvRepair.TBitBtn3.click()
    app.TMessageForm.TButton2.click()
    app.TfrmInvRepair.wait_not('visible', timeout=360)
    app.TfrmCompany.TBitBtn5.click()
    
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
    app.Tfmain.TLMDPageControl.click_input(coords = (515, 10))
    app.Tfmain.TLMDPageControl.click_input(coords = (664, 91))
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
    app.TfrxPreviewForm.TToolBar1.click_input(coords = (60, 16))
    app.TfrxPDFExportDialog.TButton2.click()
    app.TfrxPDFExportDialog.wait_not('visible', timeout=360)
    app.SaveAs.type_keys('{PAUSE 0.5}{ENTER}')

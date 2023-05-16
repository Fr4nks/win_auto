import json
from pywinauto.application import Application
import warnings

warnings.filterwarnings("ignore", message="32-bit application should be automated using 32-bit Python")

with open('settings.json') as f:
    settings = json.load(f)

genhire = settings['genhire']
name = settings['name']
password = settings['password']
app = Application(backend="win32").start(genhire)
app.TfmLogin.set_focus()
app.TfmLogin.TBtnWinControl2.click()
app.TwwLookupDlg.TwwIncrementalSearch1.set_focus()
app.TwwLookupDlg.TwwIncrementalSearch1.type_keys(name+'{ENTER}')
app.TfrmLogin.TEdit1.type_keys(password+'{ENTER}')



    

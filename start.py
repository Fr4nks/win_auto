import json
from pywinauto.application import Application
import warnings

warnings.filterwarnings("ignore", message="32-bit application should be automated using 32-bit Python")

with open('settings.json') as f:
    settings = json.load(f)

app = Application(backend="win32").start(settings['genhire'])
app.TfmLogin.TBtnWinControl2.click()
app.TwwLookupDlg.TwwIncrementalSearch1.type_keys(settings['name']+'{ENTER}')
app.TfrmLogin.TEdit1.type_keys(settings['password']+'{ENTER}')



    

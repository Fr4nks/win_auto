import os
import sys
import re
import xml.etree.ElementTree as ET
from pdf.ver_pdfminer import convert_pdf
from modules.language import PluralDict
from modules.language import translate
from modules.numbers import stringtoint
from modules.numbers import container_number
from datetime import datetime
import fdb
import calendar

# test_pdf_file = 'C:\\Users\\fr4nk\\Documents\\python64\\BOS002Invoice60773.pdf'
test_pdf_file = 'C:\\Users\\fr4nk\\Documents\\python64\\test6.pdf'
database_file = 'C:\\Users\\fr4nk\Documents\\python64\\GENDATA.FDB'


def get_pdf(test_pdf_file):
    try:
        # GET FILE FROM WINDOWS, THE FILE RIGHT CLICKED ON.
        return sys.argv[1]
    except:
        print('Error getting PDF from sys.argv[1] Switching to test mode...')
        pass
    try:
        if os.path.isfile(test_pdf_file) is True:
            print('Test PDF file found...')
            return test_pdf_file
        else:
            print('NO TEST PDF FILE FOUND!!!')
    except:
        print('Could not find anny pdf files...')


def mine_filename(save_pdf):
    try:
        pattern = re.compile(r'\\([^\\]*)\.')
        mine_file_name = re.search(pattern, save_pdf)
        client, invoice = mine_file_name[1].split('Invoice')
        print ('File name mined successfully!')
        return client, invoice
    except:
        print('Mining file name failed...')
        client = None
        invoice = None
        return client, invoice


def find_cleanstring(dirtystring):
    cleanerstring = dirtystring.replace('&', '&amp;')  # problem with xml.etree parsing &
    try:
        cleanstring = re.search(r'<data\b[^>]*>([\s\S]*?)<\/data>', cleanerstring)
        xml_data = format(cleanstring.group(0))
        tree_data = ET.fromstring(xml_data)
        print ('<data></data> tag found in dirtystring!')
        return tree_data
    except:
        print ('No <data></data> tag found')

save_pdf = get_pdf(test_pdf_file)
dirtystring = convert_pdf(save_pdf, format='text')
xml_object = find_cleanstring(dirtystring)


def get_this(
    # 1.) FILENAME STRING - from function mine filename. Only contract and client.
    # 2.) FIREBIRD DATABASE
    method='fetchone',
    table=None,
    out=None,
    row_equels=None,
    this_prop=None,
    # 3.) PDF XML
    tree=xml_object,
    xml=None,
    # 4.) PDF REGEX
    dirtystring=dirtystring,
    regex=None
):
    if os.path.isfile(database_file) is True and out is not None:
        try:
            sql_string = ("select {} from {} where {} = '{}'").format(out, table, row_equels, this_prop)
            con = fdb.connect(database=database_file, user='sysdba', password='masterkey')
            cur = con.cursor()
            cur.execute(sql_string)
            if method is 'fetchone':
                line = cur.fetchone()
                print ('Firebird fetchone database data...')
                return line[0]
            if method is 'fetchall':
                lines = cur.fetchall()
                print ('Firebird fetchall database data...')
                return [x[0] for x in lines]
        except:
            print('Try Firebird database failed, except triggered...')
            pass

    if tree is not None:
        print('Try XML string...')
        try:
            xml_return = tree.find(xml).text
            if xml_return is not None:
                print ('xml mined success!!!')
                return xml_return
        except:
            print('xml mine failed, except triggered...!!!')
            pass

    if regex is not None:
        print('Try dirty string...')
        try:
            pattern = re.compile(regex)
            search = re.findall(pattern, dirtystring)
            if search[1] is None and search[0] is not None:
                return search[0]
            if search is not None:
                return search
        except:
            print('regular expression failed, except triggered...')
            pass
    else:
        print ('No data found...')

client, invoice_numb = mine_filename(save_pdf)

if invoice_numb is None:
    invoice_numb = get_this(
        xml='invoice',
        regex=r'nv ([0-9]{5})',
        )
print('Invoice:', invoice_numb)

if client is None:
    client = get_this(
        table='GH_INV',
        out='CLIENT',
        row_equels='INVOICE',
        this_prop=invoice_numb,
        # xml='client',
        regex=r'ref: ([A-Z]{3}[0-9]{3})'
        )
    CLIENT = client.upper()
print('Client:', client)

if client is not None and invoice_numb is None:
    invoice = get_this(
        table='GH_INV',
        out='INVOICE',
        row_equels='CLIENT',
        this_prop=client
    )

finance_email = get_this(
    table='CLIENTS',
    out='FINANCEEMAIL',
    row_equels='CLIENT',
    this_prop=client,
    xml='financeemail'
    )
print('Finance email:', finance_email)

if finance_email is None:
    email_field = get_this(
        table='CLIENTS',
        out='EMAIL',
        row_equels='CLIENT',
        this_prop=client,
        xml='email'
        )
    email = email_field
    
if email_field is None:
    email_field = 'None'

        
else:
    email = finance_email


email_list = email.split(",")
email = email_list[0]

if len(email_list) >= 2:
    cc = email_list[1]
else:
    cc = ''


print ('Email:', email)

name = get_this(
    table='CLIENTS',
    out='CLIENTCOMPANY',
    row_equels='CLIENT',
    this_prop=client,
    xml='name',
    )
NAME = name.upper()

print ('Name: ', name)

contract_data_numb = get_this(
    table='GH_INV',
    out='DOCNUM',
    row_equels='INVOICE',
    this_prop=invoice_numb
)
print('contract database number:', contract_data_numb)

contract_numb = get_this(
    table='CONTRACT',
    out='CONTRACTNO',
    row_equels='CONTRACT',
    this_prop=contract_data_numb
    )

print ('çontract number:', contract_numb)

container_lines = get_this(
    method='fetchall',
    table='CONLINE',
    out='EQUIP',
    row_equels='CONTRACT',
    this_prop=contract_data_numb,
    regex=r'(CONT-[0-9]{1,3})'
    )
print('contract line:', container_lines)

regex = re.compile(r'(CONT-[0-9]{1,3})')
filtered_containers = list(filter(lambda i: regex.search(i), container_lines))
container_list = [container.replace('CONT-', '') for container in filtered_containers]
container_raw = "%2C ".join(container_list)
regex = re.compile(r'(%2C) ([0-9]{1,3})$')
container_numbers = (re.sub(regex, r' & \2', container_raw))

get_date_out = get_this(
    table='CONTRACT',
    # out='DATEOUT',
    row_equels='CONTRACT',
    this_prop=contract_data_numb,
    # xml='dateout',
    regex=r'\/([0-9]{2})\/'
    )
print('Date out', get_date_out)

def date_out(get_date_out):
    is_string = isinstance(get_date_out, str)  # xml
    is_datetime = isinstance(get_date_out, datetime)  # database
    is_list = isinstance(get_date_out, list)  # regex
    if is_string is True:
        try:
            return datetime.strptime(get_date_out, '%d/%m/%Y')
        except:
            print('date format error %d/%m/%Y')
    if is_datetime is True:
        return get_date_out.month
    if is_list is True:
        return int(get_date_out[1])

monthinteger = date_out(get_date_out)
if monthinteger is not None:
    month = calendar.month_name[monthinteger]
else:
    month = 'Default'

MONTH = month.upper()
print('Month:', month)


# OUTPUT
def lenth_conlines(conlines):
    if conlines is None:
        return 0
    else:
        return len(conlines)

numb_cont = lenth_conlines(filtered_containers)  # Not finished, will pick up locks and any other things on container invoice
print (numb_cont)
numb_inv = 1
data = PluralDict({'faktuur': numb_inv, 'invoice': numb_inv, 'container': numb_cont})

pre_word_faktuur = "faktu{faktuur(ur,re)}"
pre_word_container = "container{container(s)}"
pre_word_invoice = "invoice{invoice(s)}"

faktuur = pre_word_faktuur.format_map(data)
container = pre_word_container.format_map(data)
invoice = pre_word_invoice.format_map(data)
FAKTUUR = faktuur.upper()
CONTAINER = container.upper()
INVOICE = invoice.upper()
print (invoice)

tree = ET.parse('config.xml')
print(tree)
ROOT = tree.getroot()
print(ROOT)
login_name = ROOT.find('.login/name').text
print(login_name)
login_password = ROOT.find('.login/password').text
# connects to xml settings file,

def temp_from_xml(type, language, ROOT=ROOT):

    def get_text(xpath_string):
        xpath = (xpath_string).format(type, language)
        template = ROOT.find(xpath).text
        regex = re.compile(r'({).*?(})')
        string = (re.sub(regex, r'\1\2', template))

        regex = re.compile(r'{(.*?)}')
        variables = re.findall(regex, template)
        var_list = []
        for variable in variables:
            var_list.append(globals()[variable])
        return string.format(*var_list)

    subject = get_text('.email/template[@type="{}"][@language="{}"]/subject')
    subject = 'subject=\"'+subject+'\",'

    body = get_text('.email/template[@type="{}"][@language="{}"]/body')
    body = 'body=\"' + body + '\",'
    return subject+body

thunder_afr_normal = temp_from_xml('normal', 'afrikaans')
thunder_eng_normal = temp_from_xml('normal', 'afrikaans')
thunder_afr_cont = temp_from_xml('normal', 'afrikaans')
thunder_eng_cont = temp_from_xml('normal', 'afrikaans')

    # thunder_eng_normal = temp_from_xml('normal', 'english')
    # thunder_afr_cont = temp_from_xml('container', 'afrikaans')
    # thunder_eng_cont = temp_from_xml('container', 'english')

thunder_start = (
    'start thunderbird -compose '
    )

thunder_elements = (
    'to="{}",'
    'cc="{}",'
    'attachment="{}",'
    ).format(email, cc, save_pdf)

def email_client():
    thunder_endx64 = (
        "C:\\Program Files\\Mozilla Thunderbird"
        )
    thunder_endx86 = (
        "C:\\Program Files (x86)\\Mozilla Thunderbird"
        )
    if (os.path.isdir(thunder_endx64)):
        return thunder_endx64
    elif (os.path.isdir(thunder_endx86)):
        return thunder_endx86
    else:
        print('EMAIL CLIENT DIRECTORY NOT FOUND!')

def body_html(type=0, language='afr'):
    if type > 0 and language == 'afr':
        return thunder_afr_cont
    elif type > 0 and language == 'eng':
        return thunder_eng_cont
    elif type == 0 and language == 'eng':
        return thunder_eng_normal
    elif type == 0 and language == 'afr':
        return thunder_afr_normal
    else:
        print('No selection of email BODY or SUBJECT')

thunder_command = thunder_start + thunder_elements + body_html(numb_cont, 'afr') + email_client()
os.system(thunder_command)
print(thunder_command)

def task_input(task=None):
    if task != 's' and task != 'r' and task != 'a' and task != 't':
        print ('Enter s for Statement')
        print ('Enter r for Repair')
        print ('Enter a for Repair and Statement')
        print ('')
        task = input('Enter: s, r, a:')
        if task != 's' and task != 'r' and task != 'a' and task != 't':
            return task_input()
        else:
            return task

client = input('Please enter Client Code:')
input_client = get_this(
    table='CLIENTS',
    out='CLIENTCOMPANY',
    row_equels='CLIENT',
    this_prop=client
    )
print()
print()   
print(input_client, '| Financial email:' )
print('Email:', email_field  )
print('Email:', finance_email  )
task = task_input()

if task is 's':
    app = connect_genhire()
    statement(app, client)
elif task is 'r':
    app = connect_genhire()
    repair(app, client)
    app = connect_genhire()
elif task is 'a':
    app = connect_genhire()
    repair(app, client)
    app = connect_genhire()
    statement(app, client)
elif task is 't':
    app = connect_genhire()
    close_windows(app)

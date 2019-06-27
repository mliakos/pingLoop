from torrequest import TorRequest
import requests, string, random, os, datetime, openpyxl, time, socket

# Utility functions 

# Check connection
REMOTE_SERVER = "www.google.com"
def is_connected(hostname):
  try:
    # see if we can resolve the host name -- tells us if there is
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually
    # reachable
    s = socket.create_connection((host, 80), 2)
    return True
  except:
     pass
  return False

# Countdown timer
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

############################################
  

domains = []

while(True):
    #Choose mode (SEO attack / SEO boost)
    mode = input('Please select script mode (1 or 2): \n   1) SEO attack \n   2) SEO Boost\n')
    if(mode == '1' or mode == '2'):
        break
    else:
        os.system('clear')
        print('Please select a valid mode (1 or 2).')
        

if(mode == '1'):
    urls = int(input('How many different URLs do you want to ping?\n'))
    os.system('clear')
    reqNumber = int(input('How many times to ping each URL?\n'))
    os.system('clear')

    # Importing domains
    try:
        for i in os.listdir():
            if('attack.xls' in i or 'attack.xlsx' in i):
                bookname = i
        # Loading excel book
        book = openpyxl.load_workbook(bookname)
        sheets = book.get_sheet_names()
        sheet = book.get_sheet_by_name(sheets[0])

        for i in range(1,  sheet.max_row+1):
            site = sheet.cell(row=i, column=1).value

            domains.append({'domain':site,'urls':urls,'requests':reqNumber})
        
        print('Paths from excel file were imported\n')
        
    except:
        os.system('clear')
        print('Unkown error occured. You selected SEO Boost mode. Make sure you have a \'boost.xls\' or \'boost.xlsx\' file with the paths, in the same directory.')
        exit()
    

    os.system('clear')
    while(True):
        schedule = input('Do you want to schedule the script? (y/n)\n')
        if(schedule == 'y'):
            sleep_time = input('How often do you want to run this script? (HH:MM:SS)\n')
            break
        else:
            break

    print('Entered info:\n')
    for num, domain in enumerate(domains):
        print('\n' + str(num+1) +'. ' + domain['domain'] + ', ' + str(domain['urls']) + ' URLs, ' + str(domain['requests']) + ' requests per URL\n' )
    print('Script will start in 5 seconds. ')
    time.sleep(5)
    

if(mode == '2'):
    reqNumber = int(input('How many times to ping each URL?\n'))

    try:
        paths=[]
        for i in os.listdir():
            if('boost.xls' in i or 'boost.xlsx' in i):
                bookname = i
        # Loading excel book
        book = openpyxl.load_workbook(bookname)
        sheets = book.get_sheet_names()
        sheet = book.get_sheet_by_name(sheets[0])

        for i in range(1,  sheet.max_row+1):
            paths.append(sheet.cell(row=i, column=1).value)
        
        urls = len(paths)
        print('Paths from excel file were imported\n')
        
    except:
        os.system('clear')
        print('Unkown error occured. You selected SEO Boost mode. Make sure you have a \'boost.xls\' or \'boost.xlsx\' file with the paths, in the same directory.')
        exit()

os.system('clear')
print('Script started.')
urls_pinged = 0


# Setting up TOR
tr=TorRequest(password='0000')

#Cleaning up
os.system('clear')

current_ip = requests.get('http://ipecho.net/plain').text

print('\n\nCurrent IP: ' + current_ip + '\n')

allchars = string.ascii_letters + string.digits



def seoAttack(urls, reqNumber, domain):
    import time
    logfile_name = domain[domain.index('/')+2:]+'_attack_'+str(time.time()).split('.')[0]+'.txt'
    # Opening log file
    f = open(logfile_name, 'a')
    global urls_pinged
    urls_pinged = 0


    for i in range(urls):
        path =  "".join(random.choice(allchars) for x in range(random.randint(5,5)))

        print('Changing IP...\n')
        # Resetting IP
        tr.reset_identity()

        #Creating empty session object
        session = requests.session()
        session.proxies = {}

        # Adding proxies to session
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'

        #Changing request headers
        headers = {}
        headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        print('Request headers were set.\n') 

        try:
            new_ip = session.get('http://ipecho.net/plain').text
            
            print('Pinging URL number ' + str(i+1) + ' from IP: ' + new_ip + '...\n')
        except:
            while(True):
                        if(is_connected(REMOTE_SERVER) == False):
                            print('Network error occured. Rechecking connection in 5 seconds...')
                            time.sleep(5)
                        else:
                            print('Connection established. Resuming script.')
                            break
        

        # Executing requests loop
        for i in range(0, reqNumber):

            full_url = domain+'/'+path
            while(True):
                try:

                    #Executing request and assigning response status code
                    status_code = session.get(full_url).status_code

                    print('Request number ' + str(i+1) + ' status code: ' + str(status_code))

                    # Request logging
                    time = 'Date: ' + str(datetime.datetime.now())[0:10] + '\nTime: ' + str(datetime.datetime.now())[11:19] 
                    f.write(

                    time +'\n' +
                    'Request sent to ' + full_url + ' from IP: ' + new_ip + '.\nResponse status code: ' + str(status_code) +'\nUser-agent header: '+ headers['User-agent'] + '\n*******************************************************************************************\n\n'

                    )
                    break

                except:
                    # Logging
                    stats = 'Total URLs pinged: ' + str(urls_pinged) +'\n' + 'Total requests made per URL: ' + str(reqNumber) +'\n' + 'Total number of requests: ' + str(urls_pinged*reqNumber) + '\n' +'Original IP: ' + current_ip + '\n' + 'IPs changed: ' + str(urls_pinged)
                    f.write(stats)
                    f.close()
                    while(True):
                        if(is_connected(REMOTE_SERVER) == False):
                            print('Network error occured. Rechecking connection in 5 seconds...')
                            time.sleep(5)
                        else:
                            print('Connection established. Resuming script.')
                            break
                
        # Incrementing URL counter
        urls_pinged += 1
        os.system('clear')

    
    # Logging
    stats = 'Total URLs pinged: ' + str(urls_pinged) +'\n' + 'Total requests made per URL: ' + str(reqNumber) +'\n' + 'Total number of requests: ' + str(urls_pinged*reqNumber) + '\n' +'Original IP: ' + current_ip + '\n' + 'IPs changed: ' + str(urls_pinged)
    f.write(stats)
    f.close()
    print('\nSuccessfully executed ' + str(urls_pinged*reqNumber) + ' requests in total (' + str(reqNumber) + '/URL)')

def seoBoost(urls, reqNumber):
    import time
    logfile_name = 'boost_'+str(time.time()).split('.')[0]+'.txt'
    # Opening log file
    f = open(logfile_name, 'a')
    global urls_pinged
    urls_pinged = 0

    for i in range(urls):
        counter = i

        print('Changing IP...\n')
        # Resetting IP
        tr.reset_identity()

        #Creating empty session object
        session = requests.session()
        session.proxies = {}

        # Adding proxies to session
        session.proxies['http'] = 'socks5h://localhost:9050'
        session.proxies['https'] = 'socks5h://localhost:9050'

        #Changing request headers
        headers = {}
        headers['User-agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
        print('Request headers were set.\n') 

        try:
            new_ip = session.get('http://ipecho.net/plain').text
            
            print('Pinging URL number ' + str(i+1) + ' from IP: ' + new_ip + '...\n')
        except:
            while(True):
                        if(is_connected(REMOTE_SERVER) == False):
                            print('Network error occured. Rechecking connection in 5 seconds...')
                            time.sleep(5)
                        else:
                            print('Connection established. Resuming script.')
                            break
        

        # Executing requests loop
        for i in range(0, reqNumber):

            full_url = paths[counter]
            
            while(True):
                try:
                    #Executing request and assigning response status code
                    status_code = session.get(full_url).status_code

                    print('Request number ' + str(i+1) + ' status code: ' + str(status_code))

                    # Request logging
                    time = 'Date: ' + str(datetime.datetime.now())[0:10] + '\nTime: ' + str(datetime.datetime.now())[11:19] 
                    f.write(

                    time +'\n' +
                    'Request sent to ' + full_url + ' from IP: ' + new_ip + '.\nResponse status code: ' + str(status_code) +'\nUser-agent header: '+ headers['User-agent'] + '\n*******************************************************************************************\n\n'

                    )
                    break
                    
                except:
                    # Logging
                    stats = 'Total URLs pinged: ' + str(urls_pinged) +'\n' + 'Total requests made per URL: ' + str(reqNumber) +'\n' + 'Total number of requests: ' + str(urls_pinged*reqNumber) + '\n' +'Original IP: ' + current_ip + '\n' + 'IPs changed: ' + str(urls_pinged)
                    f.write(stats)
                    f.close()
                    while(True):
                        if(is_connected(REMOTE_SERVER) == False):
                            print('Network error occured. Rechecking connection in 5 seconds...')
                            time.sleep(5)
                        else:
                            print('Connection established. Resuming script.')
                            break

        # Incrementing URL counter
        urls_pinged += 1
        os.system('clear')


    
    # Logging
    stats = 'Total URLs pinged: ' + str(urls_pinged) +'\n' + 'Total requests made per URL: ' + str(reqNumber) +'\n' + 'Total number of requests: ' + str(urls_pinged*reqNumber) + '\n' +'Original IP: ' + current_ip + '\n' + 'IPs changed: ' + str(urls_pinged)
    f.write(stats)
    f.close()
    print('\nSuccessfully executed ' + str(urls_pinged*reqNumber) + ' requests in total (' + str(reqNumber) + '/URL)')
    

if(mode == '2'):
    seoBoost(urls, reqNumber)
# If mode == 1 (SEO attack)
else:
    if(schedule == 'y'):
        sleep_timeSeconds = int(sleep_time[:2]) * 3600 + int(sleep_time[3:5]) * 60 + int(sleep_time[6:])
    while(True):
        # Try to set sleep time (if exists)
        try:
            print('Script will run every ' + sleep_time)
            for domain in domains:
                seoAttack(domain['urls'], domain['requests'], domain['domain'])
                countdown(sleep_timeSeconds)
        except NameError:
            for domain in domains:
                seoAttack(domain['urls'], domain['requests'], domain['domain'])
                break





    





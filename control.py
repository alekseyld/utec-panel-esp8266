import socket
import gc
import webpage
import json
#for PC
#import re
import ure as re

import uasyncio as asyncio

namedPinsList = list()

def parsePinNum(url):
    m = re.search('/?(\d)=', url)
    if m:
        try:
            return int(m.group(1))
        except ValueError:
            return -1
    else:
        return -1

def saveSettings(settings):
    f = open('settings.json', 'w')
    f.write(json.dumps(settings))
    f.close()

def getSettings():
    f = open('settings.json', 'r')
    sjson = f.read()
    f.close()

    if len(sjson) > 0:
        return json.loads(sjson)
    
    return {'mode':'ap',
            'wifi-name':'',
            'wifi-pass':'',
            'ap-name':'ESP_Alekseyld',
            'ap-pass':'123456789'
            }

def normalizeSettings(settings):
    if not 'mode' in settings:
        settings['mode'] = 'ap'
    if not 'wifi-name' in settings:
        settings['wifi-name'] = ''
    if not 'wifi-pass' in settings:
        settings['wifi-name'] = ''
    if not 'ap-name' in settings:
        settings['wifi-name'] = 'ESP_Alekseyld' 
    if not 'ap-pass' in settings:
        settings['wifi-name'] = '123456789'
    return settings

def parseSettings(request):
    return normalizeSettings(
        dict(x.split('=') for x in request.replace('/admin?','').split('&'))
    )

def sendResponse(conn, response, end = False):
    try:
        conn.sendall(response)
    except:
        printD('Error on send response')
        pass
    
    if end:
        conn.close()
        gc.collect() 

def pinRequest(conn):
    pinNum = parsePinNum(request)
    print('pinNum =  %s' % str(pinNum))

    if pinNum == -1 or pinNum > len(namedPinsList):
        return webpage.controlPage(namedPinsList)

    pin = namedPinsList[pinNum]

    gpio_on = request.find('/?' + str(pinNum) + '=on')
    print('gpio_on = ' + str(gpio_on))

    if gpio_on != -1 and gpio_on < 10:
        print(str(pinNum) + 'is ON')
        pin.on()
    else:
        gpio_off = request.find('/?' + str(pinNum) + '=off') != -1
        if gpio_off:
            print(str(pinNum) + 'is OFF')
            pin.off()
    
    return webpage.controlPage(namedPinsList)        

def adminRequest(conn, request):
    if (len(request) > 7):
        saveSettings(parseSettings(request))
        
    return webpage.adminPage(getSettings())

def stripRequect(request):
    indexHTTP = request.find('HTTP')
    if indexHTTP != -1:
        request = request[0:indexHTTP]

    indexGET = request.find('GET')

    if indexGET != -1:
        return request[indexGET + 3:len(request)].strip()
    else:
        indexPOST = request.find('POST')
        if indexPOST != -1:
            return request[indexPOST + 4:len(request)].strip()
    return request.strip()

async def web_handler(conn, stripedRequest):
    respBody = b'_'
    code = b'';

    headers = b'Connection: keep-alive' 
    
    if stripedRequest.find('admin', 0, 20) != -1:
        respBody = adminRequest(conn, request)
    else:
        respBody = pinRequest(conn, request)
        
    headers += b'\nContent-Length: ' + str(len(respBody)).encode('utf-8')
    
    sendResponse(conn, b'HTTP/1.1 ' + code + b'\n')
    sendResponse(conn, headers)
    sendResponse(conn, b'\n')
    sendResponse(conn, b'\n' + respBody, True)

def accept_client(s):
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = stripRequect(str(request))
    print('URL = "%s"' % request)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(web_handler(conn, request))

async def web_loop(s):
    while True:
        try:
            accept_client(s)
	        
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
            gc.collect()

def start_web():
    s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s.bind(addr)
    s.listen(1)
    
    loop = asyncio.get_event_loop()
    loop.create_task(web_loop(s)) # Schedule ASAP
    loop.run_forever()

gc.enable()

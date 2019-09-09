
title = 'Макет ТЭЦ'
titleEncode = title.encode('utf-8')

def controlPage(namedPinsList):
    return header(True) + controlContent(namedPinsList) + footer()

def adminPage(settings = {'mode':'ap',
                          'wifi-name':'',
                          'wifi-pass':'',
                          'ap-name':'ESP_Alekseyld',
                          'ap-pass':'123456789'
                          }):
    return header(False) + adminContent(settings) + footer()

def footer():
    return b'</div><hr color="#EBEBEB"><footer>@Alekseyld 2018</footer></body></html>'

def adminContent(settings):
    isSTA = settings['mode'].find('sta') != -1
    
    return b'<form action="/admin">\xd0\xa0\xd0\xb5\xd0\xb6\xd0\xb8\xd0\xbc \xd1\x80\xd0\xb0\xd0\xb1\xd0\xbe\xd1\x82\xd1\x8b:<br><input type="radio" name="mode" value="sta" %s> \xd0\xa0\xd0\xb5\xd0\xb6\xd0\xb8\xd0\xbc WiFi<br><input type="radio" name="mode" value="ap" %s> \xd0\xa0\xd0\xb5\xd0\xb6\xd0\xb8\xd0\xbc "\xd0\xa2\xd0\xbe\xd1\x87\xd0\xba\xd0\xb0 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x83\xd0\xbf\xd0\xb0"<br><br><label for="wifi-name">\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 WiFi:</label><input type="text" name="wifi-name" value="%s"><br><label for="wifi-pass">\xd0\x9f\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8c \xd0\xbe\xd1\x82 WiFi:</label><input type="text" name="wifi-pass" value="%s"><br><br><label for="ap-name">\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x82\xd0\xbe\xd1\x87\xd0\xba\xd0\xb8 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb0:</label><input type="text" name="ap-name" value="%s"><br><label for="ap-pass">\xd0\x9f\xd0\xb0\xd1\x80\xd0\xbe\xd0\xbb\xd1\x8c \xd0\xbe\xd1\x82 \xd1\x82\xd0\xbe\xd1\x87\xd0\xba\xd0\xb8 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb0:</label><input type="text" name="ap-pass" value="%s"><br><br><input type="submit" value="\xd0\xa1\xd0\xbe\xd1\x85\xd1\x80\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x82\xd1\x8c"></form>' % ((b'checked' if isSTA else b''), (b'checked' if not isSTA else b''), settings['wifi-name'].encode('utf-8'), settings['wifi-pass'].encode('utf-8'), settings['ap-name'].encode('utf-8'), settings['ap-pass'].encode('utf-8'))

def controlContent(namedPinsList):
    head = b'<div class="control-table"><div class="header"><div>\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5</div><div>\xd0\x9a\xd0\xbe\xd0\xbc\xd0\xb0\xd0\xbd\xd0\xb4\xd0\xb0</div></div>'
    i = 0
    for namedPin in namedPinsList:
        head += (b'<div %s><div class="text">%s</div><div><a href="/?%s=%s"><button class="button %s">%s</button></a></div></div>' % ((b'class="table-r"' if i % 2 != 0 else b''), namedPin.name, str(i), (b'off' if namedPin.value() else b'on'), (b'on' if namedPin.value() else ''), (b'ON' if namedPin.value() else b'OFF')))
        i += 1
    return head

def header(isPanel):
    return b'<!DOCTYPE html><html><head><title>%s</title><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="Content-Type"content="text/html; charset=utf-8" /><link rel="icon" href="data:,"><style>%s</style></head><body><div><h1 class="left">%s</h1><div class="right"><a href="/panel"><div class="button-menu %s">\xd0\x9f\xd0\xb0\xd0\xbd\xd0\xb5\xd0\xbb\xd1\x8c</div></a><a href="/admin"><div class="button-menu %s">\xd0\x9d\xd0\xb0\xd1\x81\xd1\x82\xd1\x80\xd0\xbe\xd0\xb9\xd0\xba\xd0\xb8</div></a></div></div><div class="clear"></div><div class="panel"><p class="header-panel">%s</p>' % (titleEncode, (cssPanel() if isPanel else cssAdmin()), titleEncode, (b'active' if isPanel else b''), (b'active' if not isPanel else b''), (b'\xd0\x9f\xd0\xb0\xd0\xbd\xd0\xb5\xd0\xbb\xd1\x8c \xd1\x83\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f' if isPanel else b'\xd0\x9d\xd0\xb0\xd1\x81\xd1\x82\xd1\x80\xd0\xbe\xd0\xb9\xd0\xba\xd0\xb8'))

def cssAdmin():
    return b'html{font-family:Roboto;display:inline-block;margin:0 auto}h1{color:#767676;float:left;margin-left:10px}p{font-size:1.5rem}.button-menu{display:inline-block;border:none;border-radius:4px;padding:12px 40px;text-decoration:none;font-size:1.5rem;margin:2px;cursor:pointer;color:#3F79B5}.active{background-color:#3F79B5;color:white}.right{margin-top:.5em;float:right}.clear{clear:both}.panel{background-color:#EEE;margin-top:20px;margin-left:10px;margin-right:10px;padding-right:10px;padding-left:10px;padding-top:1px;border:none;border-radius:4px;padding-bottom:20px}.header-panel{text-align:center;color:#7F7F7F;font-weight:100}footer{margin-left:10px;margin-right:10px;color:#A9A9A9;padding:5px}input[type=text]{width:100%;padding:12px 20px;margin:8px 1px 0 1px;box-sizing:border-box}input[type=submit]{font-size:1em}a{text-decoration:none}@media (max-width:600px){h1{font-size:1.5em;text-align:center;float:none}.right{display:block;float:none;width:100%}.button-menu{display:block;margin:0,auto;font-size:1.5rem;padding:10px 15px}}'    
def cssPanel():
    return b'html{font-family:Roboto;display:inline-block;margin:0 auto}h1{color:#767676;float:left;margin-left:10px}p{font-size:1.5rem}.button{display:inline-block;background-color:#CC4A45;border:none;border-radius:4px;color:#fff;padding:8px 20px;font-size:1rem;margin:2px;cursor:pointer;min-width:200px}.button-menu{display:inline-block;border:none;border-radius:4px;padding:12px 40px;font-size:1.5rem;margin:2px;cursor:pointer;color:#3F79B5}.active{background-color:#3F79B5;color:#fff}.on{background-color:#5AA853}.right{margin-top:.5em;float:right}.clear{clear:both}.panel{background-color:#EEE;margin:20px 10px;padding:1px 10px 20px;border:none;border-radius:4px}.header-panel{text-align:center;color:#7F7F7F;font-weight:100}.header div{background-color:#EEE!important;font-weight:700;margin-bottom:2px!important;margin-top:0!important}.control-table{width:100%;background-color:#DDD}.control-table div{display:flex;justify-content:space-around}.control-table div div{width:100%;background-color:#FBF8E3;display:inline-block;margin-top:1px;padding:5px}.table-r div{background-color:#E0F0D8!important}footer{margin:0 10px;color:#A9A9A9;padding:5px}a{text-decoration:none}@media (max-width: 600px){h1{font-size:1.5em;text-align:center;float:none}.right{display:block;float:none;width:100%}.button-menu{display:block;padding:10px 15px}.button{min-width:100px}}'


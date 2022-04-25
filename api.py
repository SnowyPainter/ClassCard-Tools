import requests, bs4

def createList(val, size):
    r = []
    for i in range(0, size):
        r.append(val)
    return r
def orderingList(size):
    r = []
    for i in range(0, size):
        r.append(str(i+1))
    return r
def getWordData(session, word):
    payload = {
        'word':word,
        'word_lang': 'en',
        'is_word': 1,
        'is_image': 0,
        'set_type': 1
    }
    r = session.post('https://www.classcard.net/CreateWord/suggest', data=payload)
    msg = r.json()['msg']
    return {
        'audio_path':msg['audio_path'],
        'back':msg['meaning'],
        'front':word
    }

def login(id, pw):
    html = requests.get('https://www.classcard.net/Login').text
    doc = bs4.BeautifulSoup(html, 'html.parser')
    h = doc.find("input", {"name":"sess_key"})
    sess_key = h['value']
    s = requests.Session()
    payload = {
        'sess_key': sess_key,
        'redirect': '',
        'login_id': id,
        'login_pwd': pw,
        'id_remember': 'on'
    }
    r = s.post("https://www.classcard.net/LoginProc", data=payload)
    result = r.json()
    if(result['result'] == 'ok'):
        return {'result':'ok', 'userId':result['msg'], 'session':s}
    else:
        return result

def createEmptySet(loginedSession, userId, setName):
    payload = {
        'set_idx': -1,
        'user_idx': userId,
        'login_user_idx': userId,
        'set_type': 1,
        'front_lang': 'en',
        'back_lang': 'ko',
        'open_yn': 0,
        'allow_edit_yn': 0,
        'footer_yn': 0,
        'footer_text': '',
        'bg_path': '/images/pattern01.jpg',
        'map_type': 1,
        'map_box_color': '',
        'map_img_path': '',
        'card_cnt': 1,
        'is_copy': 0,
        'copy_from_set_idx': -1,
        'dir_idx': 0,
        'is_battle_page': 0,
        'from': '',
        'video_url': '',
        'video_start': 0,
        'video_end': 0, 
        'caption': '',
        'caption_type': '',
        'ptn_idx': 0,
        'tsl': -1,
        'ts': -1,
        'name': setName,
        'set_url':'' 
    }
    r = loginedSession.post('https://www.classcard.net/CreateWord/saveSet', data=payload)
    result = r.json()
    if(result['result'] == 'ok'):
        return {'result': 'ok','setId': result['msg']}
    else:
        return result

def fillSetContentWithWords(loginedSession, setId, userId, wordsWithMeaning):
    wordsLen = len(wordsWithMeaning)
    audiopaths = []
    meanings = []
    words = []
    minus1List = createList("-1", wordsLen)
    zeroList = createList("0", wordsLen)
    emptyStrList = createList("", wordsLen)
    orderList = orderingList(wordsLen)
    payload = {"set_idx":str(setId),"user_idx":str(userId),"login_user_idx":str(userId),"set_type":"1","footer_yn":"0","front_lang":"en","img_path":emptyStrList,"audio_path":[],"card_idx":minus1List,"map_bubble_type":emptyStrList,"deleted":zeroList,"card_order":orderList,"upload_idx":minus1List,"image_type":minus1List,"external_url":emptyStrList,"img_idx":minus1List,"es_idx":minus1List,"front":[],"back":[],"example":emptyStrList}
    for wordData in wordsWithMeaning:
        d = getWordData(loginedSession, wordData[0])
        audiopaths.append(d['audio_path'])
        if(wordData[1] == ''):
            meanings.append(d['back'])
        else:
            meanings.append(wordData[1])
        words.append(d['front'])
    payload['front'] = words
    payload['back'] = meanings
    payload['audio_path'] = audiopaths

    strp = str(payload)
    strp = strp.replace("'", '"')
    strp = strp.replace(' ', '')
    payload = {"data_obj":strp}
    r = loginedSession.post('https://www.classcard.net/CreateWord/saveCard2', data=payload)
    return r.json()
import requests, bs4, re

Languages = {
    'chinese':'zh',
    'english':'en',
    'korean':'ko',
    'japanese':'ja',
    'arabic':'ar'
}

DataType = {
    '1':"영어 단어 세트",
    '2':"일반 단어 세트"
}

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

def getSetContents(setId):
    url = "https://www.classcard.net/set/"+setId
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('div', {'class':'card-content'})
    i = 0;
    front = []
    back = []
    for tag in tags:
        val = tag.text.strip()
        if(i%2 == 0):
            front.append(val)
        else:
            back.append(val)
        i+=1
    return front, back

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

def _getSets(loginedSession, token):
    html = loginedSession.get("https://www.classcard.net/"+token).text
    doc = bs4.BeautifulSoup(html, 'html.parser')
    sets = doc.find_all("div", {"class":"set-items set-items-h-60"})
    return sets

def getMySets(loginedSession):
    sets = _getSets(loginedSession, "make")    
    result = []
    for s in sets:
        result.append({
            "name": s.find_all("span", {"class":"set-name-copy-text"})[0].text.strip(),
            "id": s['data-idx'],
            "count": s['data-cnt'],
            "type": s['data-type']
        })
    return result

def getUsedSets(loginedSession):
    sets = _getSets(loginedSession, "Main")    
    result = []
    for s in sets:
        result.append({
            "name": s.find_all("span", {"class":"set-name-copy-text"})[0].text.strip(),
            "id": s['data-idx'],
            "count": s['data-cnt'],
            "type": s['data-type']
        })
    return result

def createEmptySet(loginedSession, userId, setName, startLanguage, endLanguage):
    payload = {
        'set_idx': -1,
        'user_idx': userId,
        'login_user_idx': userId,
        'set_type': 2,
        'front_lang': startLanguage,
        'back_lang': endLanguage,
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

def createEmptyEnglishSet(loginedSession, userId, setName):
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

def fillSetContentWithEnglishWords(loginedSession, setId, userId, wordsWithMeaning):
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

def fillSetContent(loginedSession, setId, userId, words, meanings):
    wordsLen = len(words)
    minus1List = createList("-1", wordsLen)
    zeroList = createList("0", wordsLen)
    emptyStrList = createList("", wordsLen)
    orderList = orderingList(wordsLen)
    payload = {"set_idx":str(setId),"user_idx":str(userId),"login_user_idx":str(userId),"set_type":"1","footer_yn":"0","front_lang":"en","img_path":emptyStrList,"audio_path":emptyStrList,"card_idx":minus1List,"map_bubble_type":emptyStrList,"deleted":zeroList,"card_order":orderList,"upload_idx":minus1List,"image_type":minus1List,"external_url":emptyStrList,"img_idx":minus1List,"es_idx":minus1List,"front":[],"back":[],"example":emptyStrList}
    payload['front'] = words
    payload['back'] = meanings
    strp = str(payload)
    strp = strp.replace("'", '"')
    strp = strp.replace(' ', '')
    strp = strp.replace('\t',' ')
    payload = {"data_obj":strp}
    r = loginedSession.post('https://www.classcard.net/CreateWord/saveCard2', data=payload)
    return r.json()

def setSetAllowance(loginedSession, setId, public, allowEdit):
    payload = {
        'set_idx': setId,
        'open_yn': int(public),
        'allow_edit_yn': int(allowEdit)
    }
    return loginedSession.post("https://www.classcard.net/AuthAsync/set_open_allow_yn", data=payload).json()
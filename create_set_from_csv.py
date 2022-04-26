import api

def main(id, pw, words):
    result = api.login(id, pw)
    if(result['result'] != 'ok'):
        print(result)
        return
    
    session = result['session']
    userId = result['userId']
    result = api.createEmptySet(session, userId, "Test")
    if(result['result'] != 'ok'):
        print(result)
        return
    setId = result['setId']
    result = api.fillSetContentWithWords(session, setId, userId, words)
    if(result['result'] == 'ok'):
        result = api.setSetAllowance(session, setId, True, False)
        print("Created Set; Id {} User {}".format(setId, userId))
    else:
        print(result)

if __name__ == "__main__":
    main("", "", [["hello", ""], ["word", "단어"]])
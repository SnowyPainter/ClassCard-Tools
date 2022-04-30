import api
import include_csv
import logindata

def main(id, pw, words):
    result = api.login(id, pw)
    if(result['result'] != 'ok'):
        print(result)
        return
    
    session = result['session']
    userId = result['userId']
    result = api.createEmptyEnglishSet(session, userId, "Test")
    if(result['result'] != 'ok'):
        print(result)
        return
    setId = result['setId']
    result = api.fillSetContentWithEnglishWords(session, setId, userId, words)
    if(result['result'] == 'ok'):
        result = api.setSetAllowance(session, setId, True, False)
        print("Created Set; Id {} User {}".format(setId, userId))
    else:
        print(result)

if __name__ == "__main__":
    words = include_csv.getWordsAndMeaningsPairColumnData("./voc.csv")
    main(logindata.UserId, logindata.UserPw, words)
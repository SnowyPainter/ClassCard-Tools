import api
import logindata
import csv

def main(id, pw, words, meanings):
    result = api.login(id, pw)
    if(result['result'] != 'ok'):
        print(result)
        return
    
    session = result['session']
    userId = result['userId']
    result = api.createEmptySet(session, userId, "한자 214", api.Languages['chinese'], api.Languages['korean'])
    if(result['result'] != 'ok'):
        print(result)
        return
    setId = result['setId']
    result = api.fillSetContent(session, setId, userId, words, meanings)
    if(result['result'] == 'ok'):
        result = api.setSetAllowance(session, setId, True, False)
        print("Created Set; Id {} User {}".format(setId, userId))
    else:
        print(result)

if __name__ == "__main__":
    hanjalist = []
    meanings = []
    with open("hanja.csv", newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            s = row[0]
            m = s[1:]
            m = m.replace(' ', '\t')
            hanjalist.append(s[0])
            meanings.append(m)
    main(logindata.UserId, logindata.UserPw, hanjalist, meanings)
import api
import logindata
import csv

def main(setId):
    front, back = api.getSetContents(setId)

    result = api.login(logindata.UserId, logindata.UserPw)
    if(result['result'] != 'ok'):
        print(result)
        return
    
    session = result['session']
    print(api.getUsedSets(session))
if __name__ == "__main__":
    main("8871451")
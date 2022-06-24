import api
import logindata
import csv

def main(setId):
    front, back = api.getSetContents(setId)
    l = len(front)
    for i in range(0, l):
        print(front[i])
        print(back[i])
        print("(",i,"/",l,")")
        input()
    
if __name__ == "__main__":
    result = api.login(logindata.UserId, logindata.UserPw)
    if(result['result'] != 'ok'):
        print(result)
    else:
        session = result['session']
        datas = api.getUsedSets(session)
        d = {}
        i = 1
        for data in datas:
            d[i] = data['id']
            print(i,".",api.DataType[data['type']], " ",data['name'], " (", data['count'], "자)")
            i+=1
        main(d[int(input("Which one to load: "))])
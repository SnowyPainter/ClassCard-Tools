import api
import logindata
from datetime import datetime
import csv

def main(setIds):
    header = ['word', 'meaning']
    with open('./'+datetime.now().strftime("%m%d%Y%H%M%S")+'.csv', 'w', encoding='UTF-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for setId in setIds:
            front, back = api.getSetContents(setId)
            for i in range(0, len(front)):
                writer.writerow([front[i], back[i]])
    
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
        print("Split number of set with space")
        s = input("Set Ids : ")
        main(list(map(lambda e: d[int(e)], s.split(' '))))
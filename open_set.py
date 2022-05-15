import api
import logindata
import csv

def main(setId):
    front, back = api.getSetContents(setId)
    print(front)
    print(back)
if __name__ == "__main__":
    main("8871451")
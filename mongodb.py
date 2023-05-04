import pymongo
from datetime import datetime

myclient = pymongo.MongoClient("mongodb+srv://jackwrion12345:trongtin2002@jwrcluster.ucweufu.mongodb.net/test")
mydb = myclient["DoAnDaNganhDB"]
MemberColl = mydb["Member"]


def getInfo(ID):
    ID = str(ID)

    if MemberColl.count_documents({'ID': ID}) == 0:
        return
    else:
        mydoc = MemberColl.find({'ID': ID})
        return mydoc.next()

def addMember(image_input, name_input, ID_input):
    MemberColl.insert_one( { 'ID': ID_input, 'name': name_input ,'status': 0, 'path' : image_input , 'type' : 'reg'  ,'date':  datetime.now() }  )
    return 0



def checkin(ID_input, name_input):
    doc = MemberColl.find_one_and_update( {'ID': ID_input, 'type' : 'reg', 'status': 0 }, {"$set": {'status': 1}} )
    
    if doc:
        #print (doc)
        MemberColl.insert_one( { 'ID': ID_input, 'name': name_input ,'status': 1, 'type' : 'in'  ,'date':  datetime.now() }  )
        return 0
    else:
        return 1


def checkout(ID_input, name_input):
    doc = MemberColl.find_one_and_update( {'ID': ID_input, 'type' : 'reg', 'status': 1 }, {"$set": {'status': 0}} )

    if doc:
        #print (doc)
        MemberColl.insert_one( { 'ID': ID_input, 'name': name_input ,'status': 0, 'type' : 'out'  ,'date':  datetime.now() }  )

        count = MemberColl.count_documents( { 'status': 1, 'type' : 'reg' } )
        if (count == 0):
            print("DB says: 'No one in house'")

        return 0, count
    else:
        return 1,-1




"""---Using for dashboard data----""" 
#def dashboard_data():



#print(checkout("16122002", "NguyenTrongTin"))

# doc = MemberColl.find(  { 'type' : 'reg' }          )
# for x in doc:
#     print(x)


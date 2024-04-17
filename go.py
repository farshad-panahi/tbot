from pymongo import MongoClient

client=MongoClient('mongodb://localhost:27017/')

db = client['mydatabase']

collection = db['users']
# user1={'name':'farshad','age':30,'email':'frshdpnhi@gmail.com'}
# user2={'name':'rebeca','age':40, 'email':'rebeca.fergosen@gmail.com'}
# user3 = {"name": "rebeca", "age": 40, "email": "rebeca.fergosen@gmail.com"}
# user4 = {"name": "brad pit", "age": 40, "email": "rebeca.fergosen@gmail.com"}
# user5 = {"name": "rebeca", "age": 40, "email": "rebeca.fergosen@gmail.com"}

# result=collection.insert_one(user1)
# print('Inserted id:', result.inserted_id)

# result=collection.insert_many([user3, user4, user5])

# print('Inserted ids:', result.inserted_ids)

result = collection.find({'name':40})
print(list(result))
# print('docs')
# results = collection.find()
# for document in results:
#   if document['name'] == result['name']:
#     print('* => ' ,document)


# collection.update_one({'name':'farshad'}, {'$set':{'age':0}})
# collection.delete_many({'name':'farshad'})

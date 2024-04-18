import pymongo
from bson import ObjectId

class AdsMongoClient:
    def __init__(
        self,
        host: str,
        port: int,
        db_name: str = "telegram_bot",
        ads_collection_name: str = "ads",
        categories_collection_name: str = "categories",
    ):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client.get_database(db_name)
        self.ads_collection = self.db.get_collection(ads_collection_name)
        self.categories_collection = self.db.get_collection(categories_collection_name)

    def add_category(self, category: str):
        self.categories_collection.insert_one(
            {
                "category": category,
            }
        )
    def get_categories(self) -> list:
        categories = list(self.categories_collection.find({}))
        return [item['category'] for item in categories]
    
    def delete_category(self, category):
        self.categories_collection.delete_one({'category':category})

    def add_advertising(
        self, user_id: int, photo_url: str, category: str, description: str
    ):
        self.ads_collection.insert_one(
            {
                "user_id": user_id,
                "description": description,
                "category": category,
                "photo_url": photo_url,
            }
        )

    def delete_advertising(self, user_id: int, doc_id: str):
        self.ads_collection.delete_one(
            {
                "_id": ObjectId(doc_id),
                "user_id": user_id,
            }
        )

    def get_ads_by_user_id(self, user_id: int):
        result = list(self.ads_collection.find({'user_id':user_id}))
        data = []
        for item in result:
            data.append({
                  "id": str(item["_id"]),
                  "photo_url": item["photo_url"],
                  "category": item["category"],
                  "description": item["description"],
          })
        return data

    def get_ads_by_category(self, category: str):
        result = list(self.ads_collection.find({'category': str(category)}))
        return [
            {
                "id": str(item["_id"]),
                "photo_url": item["photo_url"],
                "category": item["category"],
                "description": item["description"],
            }
            for item in result
            if item["category"] == str(category)
        ]



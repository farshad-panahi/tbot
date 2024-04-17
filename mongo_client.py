import pymongo


class ExpenseMongoClient:
    def __init__(
        self,
        host: str,
        port: int,
        db_name: str = "telegram_bot",
        collection_name: str = "expenses",
    ):
        self.client = pymongo.MongoClient(host, port)
        self.db = self.client.get_database(db_name)
        self.collection = self.db.get_collection(collection_name)

    def add_expense(self, user_id: int, amount: int, category: str, description: str):
        # write your code here
        user = {
            "user_id": user_id,
            "amount": amount,
            "category": category,
            "description": description,
        }
        self.collection.insert_one(user)

    def get_expenses(self, user_id: int) -> list:
        # write your code here
        return list(self.collection.find({"user_id": user_id}))

    def get_categories(self, user_id: int) -> list:
        # write your code here
        res = self.collection.find({"user_id": user_id})
        my_list = []
        for item in res:
            my_list.append(item["category"])
        return my_list

    def get_expenses_by_category(self, user_id: int, category: str) -> list:
        # write your code here
        return list(self.collection.find({"user_id": user_id, "category": category}))

    def get_total_expense(self, user_id: int):
        # write your code here
        res = self.collection.find({"user_id": user_id})
        my_sum = 0
        for item in res:
            my_sum += item["amount"]
        return my_sum

    def get_total_expense_by_category(self, user_id: int):
        # write your code here
        res = self.collection.find({"user_id": user_id})
        my_dict = {}
        for i in res:
            if i["category"] in my_dict:
                my_dict[i["category"]] += i["amount"]
            else:
                my_dict[i["category"]] = i["amount"]

        return my_dict


# if __name__ == "__main__":
#     expense_mongo_client = ExpenseMongoClient("localhost", 27017)
#     expense_mongo_client.add_expense(123, 100, "غذا", "ناهار")
#     expense_mongo_client.add_expense(123, 200, "غذا", "شام")
#     expense_mongo_client.add_expense(123, 300, "سفر", "پرواز")
#     expense_mongo_client.add_expense(321, 400, "غذا", "ناهار")
#     expense_mongo_client.add_expense(321, 500, "سفر", "پرواز")

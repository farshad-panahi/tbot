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
        self.collection.insert_one(
            {
                "user_id": user_id,
                "amount": amount,
                "category": category,
                "description": description,
            }
        )

    def get_expenses(self, user_id: int) -> list:
        results = self.collection.find()
        res = []
        for result in results:
            if result['user_id'] == user_id:
                res.append(
                    {
                        "amount": result["amount"],
                        "category": result["category"],
                        "description": result["description"],
                    }
                )
        return res 

    def get_categories(self, user_id: int) -> list:
        results = list(self.collection.find({"user_id": user_id}))
        return [item['category'] for item in results]

    def get_expenses_by_category(self, user_id: int, category: str) -> list:
        results = self.collection.find()
        res = []
        for result in results:
            if result["user_id"] == user_id and result['category'] == category:
                res.append(
                    {
                        "amount": result["amount"],
                        "category": result["category"],
                        "description": result["description"],
                    }
                )
        return res

    def get_total_expense(self, user_id: int):
        user_costs = list(self.collection.find({'user_id': user_id}))
        return sum(item['amount'] for item in user_costs)

    def get_total_expense_by_category(self, user_id: int):
        users_match = list(self.collection.find({"user_id": user_id}))
        return {user['category']:sum(item['amount'] for item in users_match if item['category']==user['category']) for user in users_match}

# if __name__ == "__main__":
#     expense_mongo_client = ExpenseMongoClient("localhost", 27017)
#     expense_mongo_client.add_expense(123, 100, "غذا", "ناهار")
#     expense_mongo_client.add_expense(123, 200, "غذا", "شام")
#     expense_mongo_client.add_expense(123, 300, "سفر", "پرواز")
#     expense_mongo_client.add_expense(321, 400, "غذا", "ناهار")
#     expense_mongo_client.add_expense(321, 500, "سفر", "پرواز")

#     print("Expenses of 123")
#     print(expense_mongo_client.get_expenses(123))

#     print("Categories of 123")
#     print(expense_mongo_client.get_categories(123))

#     print("Total expense of 321")
#     print(expense_mongo_client.get_total_expense(321))

#     print("Total expense by category of 321")
#     print(expense_mongo_client.get_total_expense_by_category(321))

#     print("Expenses by category of 123")
#     print(expense_mongo_client.get_expenses_by_category(123, "غذا"))

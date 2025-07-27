use testdb
db.createCollection("users")
db.users.insert({ name: "Abhishek", role: "admin" })
db.users.find().pretty()

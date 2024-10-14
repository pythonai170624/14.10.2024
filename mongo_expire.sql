
// new collection activities
db.activities.insertOne({
  action: "game_started",
  username: "amelia_sunshine",
  description: "User started a new game",
  created_at: new Date()  // Important for TTL
})

db.activities.createIndex(
  { "created_at": 1 },
  { expireAfterSeconds: 60 }
)

db.activities.getIndexes()

db.activities.insertOne({
  action: "user_login",
  username: "bob_walker",
  description: "User logged into the system",
  created_at: new Date()
})

db.activities.insertOne({
  action: "view_stats",
  username: "arya_stark",
  description: "User viewed game statistics",
  created_at: new Date()
})

db.activities.find({})  // wait after 1 minute and run again ...


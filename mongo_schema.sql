// schema

db.createCollection("users", {
   validator: {
      $jsonSchema: {
         bsonType: "object",
         required: [ "username", "email" ],
         properties: {
            username: {
               bsonType: "string",
               description: "must be a string and is required",
               minLength: 3
            },
            email: {
               bsonType: "string",
               description: "must be a string and is required",
               pattern: "^.+@.+\..+$"  // Simple email pattern
            },
            age: {
               bsonType: "int",
               description: "must be an integer and greater than 0",
               minimum: 1
            }
         }
      }
   }
})

// will work -- fits schema
db.users.insertOne({
   username: "Alice",
   email: "alice@example.com",
   age: 25
})

// will fail -- does not fit schema
db.users.insertOne({
   username: "Al",
   email: "aliceexample.com",
   age: -5
})


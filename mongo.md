## to switch to another database and create a db
```
  use db (dbname)
```
## to view databases
```
 show dbs 
```
## Create collection
```
  db.Movies.InsertMany[]
```
## to show documents (rows)
```
  show table
```

## Inserts multiple documents in the collection
```
 db.movies.insertMany([])
```
## 3. returns all the documents (rows) Read
```
 db.movies.find()
```
## SQL for the above
```
 select * from collection
```
## 4. fitering the data with id 100
```
db.collection.find({
  "name": "RRR"
})
```
## SQL for the above
```
 select * from collection
 where id = 100
```
## 5. filter movies with rating of 8
```
db.collection.find({
  "rating": 8
})
```
## SQL for the above
```
 select * from collection
 where rating = 8
```

## 6. All movies with rating of more than 8
### comaparisoon opeartions
```
db.collection.find({
  "rating": {
    "$gt": 8
  }
})
```
## SQL for the above
```
 select * from collection
 where rating > 8
```
## 7. All movies with rating of more than 8 and equal
```
db.collection.find({"rating":{"$gte": 8}})
```
## SQL for the above
```
 select * from collection
 where rating >= 8
```
## 8. less than 8
```
db.collection.find({
  rating: {
    "$lt": 8
  }
})
```
## SQL for the above
```
 select * from collection
 where rating < 8
```

## 9. less and including 8
```
db.collection.find({
  rating: {
    "$lte": 8
  }
})
```
## SQL for the above
```
 select * from collection
 where rating <= 8
```
## 10. All the movies which rating 8.4, 7, 8.1
```
db.collection.find({
  "rating": {
    "$in": [7, 8.1,8.4]}
})
```
## in sql 
```
    select * from movies
    where rating in (7, 8.1, 8.4)
```

## negetive of the above
```
db.collection.find({
  "rating": {
    "$nin": [
      7,
      8.1,
      8.4
    ]
  }
})
```
## in sql 
```
    select * from movies
    where rating not in (7, 8.1, 8.4)
```
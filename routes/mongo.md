```
  use db
```

```
 show dbs
```
## Inserts myltiple documents in the collection
```
 db.movies.insertMany([])
```
## returns all the documents (rows) Read
```
 db.movies.find()
```
## fitering the data with id 100
```
db.collection.find({
  "name": "RRR"
})
```

## filter movies with rating of 8
```
db.collection.find({
  "rating": 8
})
```

## All movies with rating of more than 8
```
db.collection.find({
  "rating": {
    "$gt": 8
  }
})
```
## All movies with rating of more than 8 and equal
```
db.collection.find({"rating":{"$gte": 8}})
```
## less tha 8
```
db.collection.find({
  rating: {
    "$lt": 8
  }
})
```

## less and including 8
```
db.collection.find({
  rating: {
    "$lte": 8
  }
})
```
## [03:49 pm] Ragav Kumar V (Unverified)

10. All the movies which rating 8.4, 7, 8.1
```
db.collection.find({
  "rating": {
    "$in": [7, 8.1,8.4]}
})

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
    where rating in [7, 8.1, 8.4]
```
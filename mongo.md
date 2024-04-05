## to switch to another database and create a db
```
  use (dbname)
```
## to view databases
```
 show dbs 
```
## Create collection (you are in the database you want to insert the collection in)
```
  db.Movies.InsertMany[]
```
## to the documents (tables)
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
# projections
## projections- inclusion > includes the keys if it is 1 but the id is included all the time
```
 db.movies.find({}, {name: 1, rating:1})
```

## Projection -exclusion > excludes the keys if 0, and returns all
```
 db.movies.find({}, {trailer: 0, poster:0})
```

##  Note you cannot mix inclusion and exclusion This is only possible if you exclude the id and include others
```
db.movies.find({}, {trailer: 0, poster:0, rating:1}) ❌
db.movies.find({}, {_id:0,name: 1, rating:1) ✅
```

## get the movie with rating above 8.5 and only return the name and the rating exluding the id
```
db.movies.find({rating :{"$gt": 8.5}}, {_id:0 , name:1, rating : 1})
```

# sorting

## sorting rating in ascending order
```
db.movies.find({}).sort({rating: 1})
```

## sorting rating in descending order
```
db.movies.find({}).sort({rating: -1})
```

## sorting plus projection
```
db.movies.find({},  {_id:0 , name:1, rating : 1}).sort({rating: 1})
```

## sort by rating, if equal rating, sort by name (compound sorting)
```
db.movies.find({},  {_id:0 , name:1, rating : 1}).sort({rating: -1, name:1})
```
## returning the first 3 (limit)
```
db.movies.find({},  {_id:0 , name:1, rating : 1}).sort({rating: -1, name:1}).limit(3)
```
## skipping the first 3 (skip)
```
db.movies.find({},  {_id:0 , name:1, rating : 1}).sort({rating: -1, name:1}).skip(3)
```

# A database cannot be both fast at inserting and fast reading.
## mongo is fast at reading but takes time to insert
## sql is a balanced database 

# Aggregation  
## in sql
```
select id, productName,  sum(quantity)
from orders
where status = "urgent"
group by productName
```

## in mongo The output of stage one is the input of stage 2
```
db.collection.aggregate(
  stage1, 
  stage2, 
  stage3
)

db.orders.aggregate([
  {$match : {status : "urgent"}},  #returns al the urgent orders
  {$group: {_id: "$productname", totalquantities: {$sum : '$quantity}}  #always say _id
])

db.orders.aggregate([
  {$match: {status: "urgent"}},  
  {$group: {_id: "$productName", totalquantities: {$sum: "$quantity"}}}  #case sensetive
])
```

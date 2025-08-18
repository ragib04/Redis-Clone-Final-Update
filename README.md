 ![enter image description here](https://img.shields.io/badge/python-3.8-blue.svg)
# Redis-Clone
This is a prototype for Redis with some basic functionalities. It can be used like any REST API. 
### Table of Contents
---
 <details>
   <summary>Click to expand!</summary>

   ##### Redis-Clone
   1. Usage
   2. Overview
   3. Functions Implemented
      * GET()
      * SET()
      * EXPIRE()
      * ZADD()
      * ZRANGE()
      * ZRANK()
      * DELETE()
      * ZREVRANK()
      * ZREVRANGE()
      * TTL()
      * PING()
   4. Questions
 </details>
 
### Usage
---
 To use the app the dependencies mentioned in the requirements.txt must be satisfed. 
Once the dependencies have been satisfied, app.py can directly be executed via any CLI. 

    python3 app.py
The server will then be live on [http://localhost:5002/]([http://localhost:5001/](http://192.168.1.2:5002))

### **Overview**
---
This prototype is an attempt to give Redis like functionalities. 11 different Redis functions have been implemented in this prototype. The most difficult part in this prototype was to attain persistence. 
#### Persistence
---
This was a major problem that arose during the development of the project. This problem is solved in a very novel way in this prototype. 
This problem is solved by logging. Here is the algorithm that was used to solve this problem:

1. A local txt file is created that will log all the queries that can alter the database(Ex: SET, DELETE, EXPIRE). A snapshot of a log file is shown below. 

![enter image description here](https://github.com/ragib04/Redis-Clone/blob/main/log_file.png)

2. Once the server is stopped then the complete database is erased(State Lost). But when the server is live again then first all the queries present in the log are executed to gain the lost state. 

Thus persistence is achieved in this way. 
This technique is used by Redis and is called Logging. 
Another method called Snapshotting is also used by Redis on demand of the user. This is not implemented here due to lack of time. 
Logging has some disadvantages which is discussed in Questions section


### **Functions Implemented**
---
### 1. GET()

##### How to use?

`GET key`

##### Time Complexity: O(1)

This function simply checks if the string value exist for the given key. If the key is not present "None" is returned. If the value at the key is not string(suppose sorted set is present at the key) then an error is returned.

---
### 2. SET()

##### How to use?

`SET key value [EX seconds|PX milliseconds] [NX|XX] [KEEPTTL]`

##### Time Complexity: O(1)

This function is used to insert value with given key. If key is already holding a value it is overriden. It can operate in all different modes like a redis SET. 

---
### 3. EXPIRE()

##### How to use?

`EXPIRE key seconds`

##### Time Complexity: O(1)

This can be used to add timeout on any key irrespective of the value it is holding. This is also used as a special mode in SET as discussed above. The algorithm used for expiring is as follows :-

 1. Whenever SET was used to insert any value in the DataBase any entry in 'expire' table was also created with the same key. The value to this was initialised as infinite.
 2. Now when we give an expiration time for any key, the value in this 'expire' table is set as current time + expiration time.
 3. Now when we call a GET method for any key, it is first checked whether the key has already expired by just comparing current time with expiration time of the key. if it is expired then it is deleted otherwise returned.

This technique is called lazy deletion.
Although this technique works well but there is an issue of increasing size of our Database. Because we are only deleting an expired when it called via GET. if any expired key is not called for a long time it may reside in our database thus increasing the size of our database. 
To limit the increasing size of the database what Redis does is it randomly selects keys and checks if it has expired. A similar random algorithm has been implemented to control the increasing size of the DataBase. This check only happens when the keys in our hash table > 100. 

---
### 4. ZADD()

##### How to use?

`ZADD key [NX|XX] [CH] [INCR] score member [score member ...]`

##### Time Complexity: O(log(N)) (N represents number of items present in our Sorted Set)

Adds all the specified members with the specified scores to the sorted set stored at key. It is possible to specify multiple score / member pairs. If a specified member is already a member of the sorted set, the score is updated and the element reinserted at the right position to ensure the correct ordering.

If key does not exist, a new sorted set with the specified members as the sole member is created. If the key exists but does not hold a sorted set, an error is returned. 

---
### 5. ZRANGE()

##### How to use?

`ZRANGE key start stop [WITHSCORES]`

##### Time Complexity: O(log(N)+M)
		 N being the number of elements in the sorted set and M the number of elements returned.

Returns the specified range of elements in the sorted set stored at key. The elements are considered to be ordered from the lowest to the highest score. Lexicographical order is used for elements with equal score.

---
### 6. ZRANK()

##### How to use?

`ZRANK key member`

##### Time Complexity: O(log(N))

Returns the rank of member in the sorted set stored at key, with the scores ordered from low to high. The rank (or index) is 0-based, which means that the member with the lowest score has rank 0.

---
### 7. DELETE()

##### How to use?

`DEL key`

##### Time Complexity: O(1)

This functions deletes the given key. If it successfully deletes the key then '1' is returned otherwise '0'. 

---
### 8. ZREVRANK()

##### How to use?

`ZREVRANK key member`

##### Time Complexity: O(log(N))

Returns the rank of member in the sorted set stored at key, with the scores ordered from high to low. The rank (or index) is 0-based, which means that the member with the highest score has rank 0.

---
### 9. ZREVRANGE()

##### How to use?

`ZRANGE key start stop [WITHSCORES]`

##### Time Complexity: O(log(N)+M)
		 N being the number of elements in the sorted set
		 M the number of elements returned.

Returns the specified range of elements in the sorted set stored at key. The elements are considered to be ordered from the highest to the lowest score. Lexicographical order is used for elements with equal score.

---
### 10. TTL()

##### How to use?

`TTL key`

##### Time Complexity: O(1)

This function return the remaning time of any key. If the key does not exist or has infinite TTL then 'None' is returned.

---
### 11. PING()

##### How to use?

`Ping`

##### Time Complexity: O(1)

This function is useful for checking if server is alive. Returns PONG if server is active. 

---

## Questions

#### 1. Why python language has been used?
Ans: Python has support for various inbuilt functionalities and data structures that makes the development very logic focused. Also it has various modules available like Flask which help in making development very fast. And since the given time was very less, Python language was the obvious candidate.

#### 2. What are the further improvements that can be made?
Ans: Various improvements can be done in this prototype. Some improvements that was planned by me but was not implemented due to lack of time are as follows:-
- Log Query Optimisation: Combining the queries present in log file for faster load during startup
- Threading: Writing in file can be done parallely with main thread 
- Snapshotting: Saving the actual database when log files gets too big or on request of user

#### 3. What Data Structures have been used and Why?
Ans: Various data structures have been used in this prototype. They are as follows:-
- Dictionary(Hashtable/Unordered Map): This holds the main Database, expire table
- Red Black Tree: For implementing Sorted Set Data Strucutre. It is used as a Balanced BST
- Tuples: For storing (score, value) pair which acts as node for RB Tree
- Arrays: Temporary intermediate Calculation and Input

#### 4. Does your implementation support multi-threaded operations?
Ans: Currently it does not support multithreading due to lack of time. But the prototype can be multithreaded. One place where it can multithreaded is while writing into the log files. Since this operation is an I/O operation and is also independent of other parts of the program it can be multi threaded. Multithreading can also be used in snapshotting. Snapshotting is saving the state of the DB into the hard drive. A third thread can be used in log query optimisation in the background. 


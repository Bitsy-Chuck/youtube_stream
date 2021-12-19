# What is this about?  
  
# How to setup locally  
### Database 
I have used postgresql db and psycog2 db connector in the application. To set it up please follow [official instructions](https://www.postgresql.org/download/). After downloading create a database of your choice and update the name in the `.env` file. Run db insertion commands listed in `public/1.sql` which will insert your google project API key into the database which will be used to fetch content from youtube. 
 ### Messaging Queue
 I have used [RabbitMQ](https://www.rabbitmq.com/) to implement the queuing mechanism for async processing in the backend. To setup rabbitmq follow [official instructions](https://www.rabbitmq.com/download.html)
 ### Other requirements
 Install other dependencies listed in requirements.txt file by `pip install -r requirements.txt`
 Also create a .env file with the following variables 

    DB_USER_NAME=  
    DB_PASSWORD=  
    DB_HOST=  
    DB_PORT=  
    DB_NAME=


### To run
use `flask run` to start the flask application and hit the APIs

# API ROUTES

|  METHOD|ROUTE  | REQUEST | RESPONSE	  | COMMENT   |
|--|--|--| -- | -- |
|  GET| /fetch/{keyword}  | Keyword -> word to fetch | {"success": true}   | This API will start fetching videos from youtube async   |
|  GET| /video/info/{keyword}  | Keyword -> word to fetch | [{"default_thumbnail_url":"None","description":"desc","fetched_from_key":1,"high_thumbnail_url":"None","id":11,"keyword":"jai","medium_thumbnail_url":"None","publish_time":"2021-12-22 12:00:00","title":"title"}]   | This API will start fetching video meta from db |
# SUPPLY_CHAIN
Web Scraping for Data Engineer Supply Chain Project

The supply chain project contents several paths of action which start on
- Collecting the data by using Web Scraping
- Data Modeling with ElasticSearch Database
- Data Consumption
- Going to production
- Automation flow

## I. Collecting data
The collecting data will collect two types of data through web scraping (using Beautiful Soup).
First type of data is gathering general information about companies (the domain, the number of reviews, the Trustscore, the percentages on each class of reviews which included the percentage of Excellent reviews). The companies are organized in themes **https://www.trustpilot.com/categories/financial_institution** which list different companies in the field

The other type of data grouping all the comments of a company with more than 10000 reviews with the information related to the review (number of stars, if the company has responded to the negative review)

NOTE:
- In term of practical. This web scraping will store data into 3 databases such as **MongoDB**, **MySQL** and **ElasticSearch**


## Deployment step

1.   Prepare your database (**MongoDB**, **MySQL** and **ElasticSearch**) environment using **docker** and run those **database containers**
2.   Download this project to your personal computer and execute file "**testing_database.py**" to ensure our project has been properly connected to database
3.   Execution file "**scraping_execution.py**" for starting execution web scraping and wait until complete the whole process

## Setting execution
You can adjust execution setting in file "**util/constants.py**" following below Details:

- constants.mongodb.exec = "True" if you would like to store data(domains and comments) to "Mongo" database else you can set to "False"
- constants.mongodb.host = **<<MongoDB_IP>>**, You can replace the value by IP of your mongo database (Default setting is localhost)
- constants.mongodb.port = **<<MongoDB_Port>>**, You can replace the value by PORT of your mongo database (Default setting is 27017)

  
- constants.mysqldb.exec = "True" if you would like to store data(domains and comments) to "MySQL" database else you can set to "False"
- constants.mysqldb.host = **<<MySQL_IP>>**, You can replace the value by IP of your mongo database (Default setting is localhost)
- constants.mysqldb.port = **<<MySQL_Port>>**, You can replace the value by PORT of your mongo database (Default setting is 9306)
- constants.mysqldb.db_username = **<<Your_DB_Username>>**, You can replace the value with username of your MySQL database (Default 'user')
- constants.mysqldb.db_password = **<<Your_DB_Password>>**, You can replace the value with password of your MySQL database (Default 'pass')

  
- constants.elastic.exec = "True" if you would like to store data(domains and comments) to "ElasticSearch" database else you can set to "False"
- constants.elastic.host = **<<URL_ElasticSearch>>**, You can replace the value by IP of your mongo database (Default setting is 'https://127.0.0.1:9200')
- constants.elastic.db_username = **<<Your_DB_Username>>**, You can replace the value with username of your ElasticSearch database (Default 'elastic')
- constants.elastic.db_password = **<<Your_DB_Password>>**, You can replace the value with password of your ElasticSearch database

NOTE:
- Password of ElasticSearch can be set to each user by execute file '**bin/elasticsearch-reset-password**' in Elastic container

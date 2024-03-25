# Documentation HotelManager

## Requirements
 
- Python 3.11.x
- Docker Desktop v4.16.3

### Installing the required packages.

**Optional** Use a virtual environment to separate different projects.

Change to the project directory and type in

```
pip3 install -r requirements.txt
```

## Quickstart

Start Docker with following command

```
docker compose up
```
In another terminal or use screen/nohup for the previous command

```
uvicorn HotelManager.HotelManagerController:app
```

The website should run under http://127.0.0.1:8000

## Decisions while developing

### Database

I chose PostgreSQL since the data is structured and the performance and simplicity of PostgreSQL is beneficial.

### Backend

The programming langauge is Python, which is easy to use and has a lot of powerful libraries. This Application was developed in Python 3.11.3, but it should be compatible from Python versions >= 3.8

### Frontend

For dynamically generating tables Jinja2 was used which can generate HTML code with Python like syntax. 

To make the page load elements dynamically with JavaScript it uses HTMX which uses functions found here https://htmx.org/docs/

### Design of the Website

The website is a one page solution, where it is possible to do all required operations on a single page without reloading using HTMX.

### Architecture Backend

For the architecture I chose the Onion Architecture, since it provides a clear hierarchy and gives a clear path to change out components.

### FastApi

The Controller is coded with FastAPI which provides a fast asynchronous connection to a client.

### Persistence Layer

Queries to the database can cost money when the database is on a cloud service provider like AWS. 
To reduce potential costs two strategies where chosen

#### Indexing columns

Indexing a column can dramatically increase the time and reduce the number of operations to query a table. 
Downside is that it costs performance and operations to update the columns.
Since the properties hotel rooms aren't frequently changed, the upsides with faster query outweigh the downside of longer updates.

#### Caching Requests

Frequently used queries can be cached and directly returned without using a database.
Given that even the biggest hotels in the world have around 10.000 rooms, that means the data can be easily filled into the RAM of a server.
Using a Least Recently Used cache the results of the previous 10 queries are saved and returned when the hash of a query is found in the cache.

### Psycog2

For querying the database psycog2 is used. 
It is possible to use Python commands to query the database with SQL. 
Using native SQL can be more performant then ORM-Frameworks like SQLAlchemy, since it saves the mapping step.

### SQL Injection Prevention

Since there are no text inputs, it is not possible to Inject SQL using the website. 
But there is a possibility to maliciously make REST requests to the backend API.
To combat this the Database Service checks every query to prevent any attacks.
A lot of parameters are already cast as an Enum or Integer before, but the SQL checking should be contained in one place.

# Project Overview

## Technologies Used:
- Flask
- Gunicorn
- OpenAI
- ChromaDB
- Nginx

### Project Purpose
This project provides recipes and their analysis. These recipes are created with the help of a model I have trained.

### Flask
Flask supports the activity to produce real-time responses, i.e., streaming. Flask is used to create a RESTful API that handles HTTP requests and responds with the necessary data in real-time, providing an interactive and dynamic interface for users.

### ChromaDB
ChromaDB is a vector database that helps generate reports for any recipe in the world. ChromaDB allows efficient storage and querying of vector data, facilitating rapid and accurate analysis of recipes.

### OpenAI
I have trained a model from OpenAI for this project. The trained OpenAI model is used to generate recipes and perform their analysis, ensuring high-quality and relevant content for users.

### Nginx
Nginx facilitates the movement of requests from the client, handling the request management. Nginx is used as a web server and reverse proxy, distributing traffic to the Flask backend, thus ensuring efficient and fast request flow.

### Gunicorn
Gunicorn is used as a WSGI server to run the Flask application. Gunicorn manages multiple worker processes, providing high performance and scalability for the web application.

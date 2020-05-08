# API Reference

## **Getting Started**

- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at your local  machine (http://localhost:5000/), which is set as a proxy in the frontend configuration.

- Authetication: This version of the application does not requiere authenticationn or API Keys.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## **Error Handling**

Errors are returned  as JSON objects in the following format:

```
{
    'success': True,
    'error': 404,
    'message': 'Not Found'
}
```

The API will return two error types when a request fail:

- 404 Resource Not Found
- 422 Unprocessable

## **Enpoints**

### **GET /categories**
- General :
    - Returns a list of all categories, id:type  (key:value) 
- Sample: curl http://localhost:5000/categories

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```
### **GET /questions**
- General :
    - Returns a list of all questions, all categories, currrent_category, and total_questions
    - Results are paginated in groups of 10. include a request argument to choose page number, starting from 1. 
- Sample: curl http://localhost:5000/questions/

```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "current_category": 1, 
  "questions": [
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }, 
    {
      "answer": "Uruguay", 
      "category": 6, 
      "difficulty": 4, 
      "id": 11, 
      "question": "Which country won the first ever soccer World Cup in 1930?"
    }, 
    {
      "answer": "George Washington Carver", 
      "category": 4, 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Lake Victoria", 
      "category": 3, 
      "difficulty": 2, 
      "id": 13, 
      "question": "What is the largest lake in Africa?"
    }, 
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 14, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }, 
    {
      "answer": "Agra", 
      "category": 3, 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ], 
  "success": true, 
  "total_questions": 19
}
```

### **DELETE /questions/question_id**
- General :
    - Deletes a specific question
    - Returns a message if delete is complete with success = True, else success = False 
- Sample: curl http://localhost:5000/questions/1 -X DELETE

```
{
    'success': True,
    'message': 'Delete is completed'
}    
```

### **POST /questions/**
- General :
    - Create a question
    - Returns a message if create is complete with success = True, else success = False 
- Sample: curl http://localhost:5000/questions/ -X POST -H 'Content-type: application/json' -d "{'question': 'What is my name?', 'answer': 'Andres?, 'difficulty': '1', 'category': '1'}" 

```
{
    'success': True,
    'message': 'Create is completed'
}    
```

### **POST /questions/search**
- General :
    - Search questions and the search is case-insensitive
    - Returns all questions with the given word, the number of total_questions with that frase and the current_category
- Sample: curl http://localhost:5000/questions/1 -X POST -H 'Content-Type: application/json' -d "{'searchterm' : 'what'}

```
{
    'success': True,
    'questions': [],
    'total_questions': 2,
    'current_category': '1'
}    
```

### **GET /categories/1/questions**
- General :
    - Returns all questions in a given catgory, the number of total_questions in that category and the current_category
- Sample: curl http://localhost:5000/category/1/questions 

```
{
    'success': True,
    'questions': [],
    'total_questions': 2,
    'current_category': '1'
    
}
```

### **POST /quizzes**
- General :
    - Start the quizz game. This consist in answer 5 questions in a given category
    - Return five random questions with the category selected
- Sample: curl http://localhost:5000/questions/1 -X POST -H 'Content-Type: application/json' -d "{'quiz_category' : {'id': 1}} (id = 1 = Science)

```
{
    'success': True,
    'question': {'question': 'what charge have the electron?', 'answer': 'Negative charge', 'category': '1', 'id': '23'},
}    
```
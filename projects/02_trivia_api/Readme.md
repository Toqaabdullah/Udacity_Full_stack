# Trivia API Project

This project aims to help many people to test and upgrade their knowledge in many categories as well as having fun. That is in a web application which have many features.

# Feartures

- View questions (10 questions per page).
- View answers of the questions once the user clicks on this option, the answers will be displayed immediately.
- Filter questions by category.
- Add new question.
- Delete a question.
- Search for a question.
- Play a quiz game which can be clssified by category.

# Install project requirements

pip install -r requirements.txt

# Create database

- dropdb trivia
- createdb trivia
- psql trivia < trivia.psql

# Backend command

- set FLASK_APP=flaskr

- set FLASK_ENV=development

- python -m flask run

# Backend URL

http://127.0.0.1:5000

# Frontend start

- npm install (first time only)
- npm start

# Frontend URL

http://localhost:3000/


# Error handling :-
The Erros found in this project are:
-404 : Not Found
-400 : Bad Request
-422 : Unprocessable
-500 : Internal server error
-405 : Method not allowed

## Error Message :-

```json
      {
        "success": "False",
        "error": 405,
        "message": "Method Not allowed",
      }
```

# Endpoints :-

## GET /questions

- General : Returns all questions paginated to be ten questions per single page. Also categories and total number of questions are displayed.
- Sample: `curl http://127.0.0.1:5000/questions`<br>

```json
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "questions": [
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
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "Muhammad Ali",
            "category": 4,
            "difficulty": 1,
            "id": 9,
            "question": "What boxer's original name is Cassius Clay?"
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
    "total_questions": 24
}
```
## GET/categories

- General : Returns all available categories.
- Sample: `curl http://127.0.0.1:5000/categories`<br>

```json
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
## DELETE /questions/<int:id>

- General : Deletes a specific question according to a given question ID and displays the total number of questions after the deletion.
- Sample: `curl http://127.0.0.1:5000/questions/2 -X DELETE`<br>

```json
        { 
            "success": true,
            "deleted": 2,
            "total_questions": 23
        }
```

## POST /questions

- General : Adds a new question and returns its ID and the total number of questions after its addition.
- Sample: `curl -d '{"question":"How many continents on earth?", "answer":"Seven", "category":"3","difficulty":"1"}' -H "Content-Type: application/json" -X POST http://127.0.0.1:5000/questions `<br>

```json
        { 
            "success": true,
            "created": 25,
            "total_questions": 24
        }
```
## GET /categories/<int:id>/questions

- General : Gets the questions according to a given category ID.
- Sample : `curl http://127.0.0.1:5000/categories/1/questions`<br>

```json
{
    "questions": [
        {
            "answer": "The Liver",
            "category": 1,
            "difficulty": 4,
            "id": 20,
            "question": "What is the heaviest organ in the human body?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Blood",
            "category": 1,
            "difficulty": 4,
            "id": 22,
            "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
            "answer": "Africa",
            "category": 1,
            "difficulty": 2,
            "id": 27,
            "question": "Where is the reiver Nile?"
        },
        {
            "answer": "Four",
            "category": 1,
            "difficulty": 1,
            "id": 30,
            "question": "How many seasons in the year?"
        }
    ],
    "success": true,
    "total_questions": 5
}
```

## POST /questions/search

- General : search for  questions according to the entered keyword.
- Sample: `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"keyword": "who"}'`<br>

```json
{
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer": "George Washington Carver",
            "category": 4,
            "difficulty": 2,
            "id": 12,
            "question": "Who invented Peanut Butter?"
        },
        {
            "answer": "Alexander Fleming",
            "category": 1,
            "difficulty": 3,
            "id": 21,
            "question": "Who discovered penicillin?"
        },
        {
            "answer": "Toka",
            "category": 5,
            "difficulty": 2,
            "id": 25,
            "question": "Who said hello?"
        },
        {
            "answer": "Mo Salah",
            "category": 6,
            "difficulty": 1,
            "id": 35,
            "question": "Who is the Egyptian King in Liverpool?"
        }
    ],
    "success": true,
    "total_questions": 5
}
```

## POST /questions/quiz

- General : Play a quiz game by displaying random questions without displaying the previuos question and belongs to the given category if found.
- Sample: `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [12], "quiz_category": {"type": "History", "id": "4"}}'`<br>

```json
{
    "question": {
        "answer": "Scarab",
        "category": 4,
        "difficulty": 4,
        "id": 23,
        "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    "success": true
}
```

# Authors

- Udacity team implameted the template found here: https://github.com/udacity/FSND/tree/master/projects/02_trivia_api/starter
- Toka Abdullah Awad completed the project to be functional after following the Readme instructions of Udacity team


# support

For inquiries, feel free to contact the author at :tokaabdullah97@gmail.com

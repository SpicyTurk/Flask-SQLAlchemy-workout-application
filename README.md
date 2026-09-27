# Workout Tracker API

## Description
A Flask-SQLAlchemy backend for tracking workouts and the exercises performed
during each one. Supports creating, viewing, and deleting workouts and
exercises, and associating exercises with a workout (including reps, sets,
and duration for that exercise in that specific workout).

## Installation
1. Clone this repository.
2. Install dependencies: `pipenv install`
3. Activate the virtual environment: `pipenv shell`
4. From the `server/` directory, set up the database:

flask db upgrade head
python seed.py


## Running the App
From the `server/` directory:

flask run

The API will be available at `http://127.0.0.1:5555`.

## Endpoints

GET: `/workouts` -list all workouts 
GET: `/workouts/<id>` -shows a single workout, including its exercises with reps/sets/duration 
POST: `/workouts` -create a workout (`date`, `duration_minutes`, `notes`) 
DELETE: `/workouts/<id>` -delete a workout and its associated workout-exercise data
GET: `/exercises` -list all exercises 
GET: `/exercises/<id>` -show an exercise and the workouts it's been part of 
POST: `/exercises` -create an exercise (`name`, `category`, `equipment_needed`) 
DELETE: `/exercises/<id>` -delete an exercise and its associated workout-exercise data
POST: `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` -add an exercise to a workout, with optional `reps`, `sets`
`duration_seconds`
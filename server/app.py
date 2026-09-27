from flask import Flask, request, jsonify
from flask_migrate import Migrate
from marshmallow import ValidationError

from models import db, Exercise, Workout, WorkoutExercise
from schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return jsonify(workouts_schema.dump(workouts)), 200


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    workout_dict = workout_schema.dump(workout)
    workout_dict['exercises'] = [
        {
            'id': we.exercise.id,
            'name': we.exercise.name,
            'category': we.exercise.category,
            'reps': we.reps,
            'sets': we.sets,
            'duration_seconds': we.duration_seconds,
        }
        for we in workout.workout_exercises
    ]
    return jsonify(workout_dict), 200


@app.route('/workouts', methods=['POST'])
def create_workout():
    try:
        data = workout_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        workout = Workout(**data)
        db.session.add(workout)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400

    return jsonify(workout_schema.dump(workout)), 201


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.filter_by(id=id).first()
    if workout is None:
        return jsonify({"error": "Workout not found"}), 404

    db.session.delete(workout)
    db.session.commit()
    return jsonify({}), 204

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return jsonify(exercises_schema.dump(exercises)), 200


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    exercise_dict = exercise_schema.dump(exercise)
    exercise_dict['workouts'] = [
        {'id': workout.id, 'date': workout.date.isoformat()}
        for workout in exercise.workouts
    ]
    return jsonify(exercise_dict), 200


@app.route('/exercises', methods=['POST'])
def create_exercise():
    try:
        data = exercise_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    try:
        exercise = Exercise(**data)
        db.session.add(exercise)
        db.session.commit()
    except ValueError as err:
        db.session.rollback()
        return jsonify({"errors": [str(err)]}), 400

    return jsonify(exercise_schema.dump(exercise)), 201

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.filter_by(id=id).first()
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    db.session.delete(exercise)
    db.session.commit()
    return jsonify({}), 204

@app.route(
    '/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises',
    methods=['POST'],
)
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    if workout is None:
        return jsonify({"error": "Workout not found"}), 404
    if exercise is None:
        return jsonify({"error": "Exercise not found"}), 404

    json_data = request.get_json() or {}
    try:
        data = workout_exercise_schema.load(json_data, partial=True)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=data.get('reps'),
        sets=data.get('sets'),
        duration_seconds=data.get('duration_seconds'),
    )
    db.session.add(workout_exercise)
    db.session.commit()

    return jsonify(workout_exercise_schema.dump(workout_exercise)), 201

if __name__ == '__main__':
    app.run(port=5555, debug=True)
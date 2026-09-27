from datetime import date

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

db = SQLAlchemy()


class Exercise(db.Model):
    __tablename__ = 'exercises'

    __table_args__ = (
        UniqueConstraint('name', name='uq_exercise_name'),
    )

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan'
    )
    workouts = association_proxy('workout_exercises', 'workout')
    VALID_CATEGORIES = ['Cardio', 'Strength', 'Flexibility', 'Balance']

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Exercise name is required.")
        return name

    @validates('category')
    def validate_category(self, key, category):
        if category not in self.VALID_CATEGORIES:
            raise ValueError(
                f"Category must be one of: {', '.join(self.VALID_CATEGORIES)}."
            )
        return category

    def __repr__(self):
        return f'<Exercise {self.id}, {self.name}, {self.category}>'


class Workout(db.Model):
    __tablename__ = 'workouts'

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='ck_workout_duration_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, default=date.today)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship(
        'WorkoutExercise', back_populates='workout', cascade='all, delete-orphan'
    )
    
    exercises = association_proxy('workout_exercises', 'exercise')

    @validates('duration_minutes')
    def validate_duration_minutes(self, key, duration_minutes):
        if duration_minutes is None or duration_minutes <= 0:
            raise ValueError("Workout duration must be a positive number of minutes.")
        return duration_minutes

    def __repr__(self):
        return f'<Workout {self.id}, {self.date}, {self.duration_minutes} min>'


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps > 0', name='ck_workout_exercise_reps_positive'),
        CheckConstraint('sets IS NULL OR sets > 0', name='ck_workout_exercise_sets_positive'),
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def __repr__(self):
        return (
            f'<WorkoutExercise {self.id}, workout={self.workout_id}, '
            f'exercise={self.exercise_id}>'
        )
from datetime import date

from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()
    db.session.commit()

    push_up = Exercise(name="Push-Up", category="Strength", equipment_needed=False)
    squat = Exercise(name="Squat", category="Strength", equipment_needed=False)
    treadmill_run = Exercise(name="Treadmill Run", category="Cardio", equipment_needed=True)
    yoga_stretch = Exercise(name="Yoga Stretch", category="Flexibility", equipment_needed=False)
    db.session.add_all([push_up, squat, treadmill_run, yoga_stretch])
    db.session.commit()

    workout1 = Workout(
        date=date(2026, 9, 20), duration_minutes=45,
        notes="Upper/lower body strength day",
    )
    workout2 = Workout(
        date=date(2026, 9, 22), duration_minutes=30,
        notes="Cardio session with a cooldown stretch",
    )
    db.session.add_all([workout1, workout2])
    db.session.commit()

    db.session.add_all([
        WorkoutExercise(workout=workout1, exercise=push_up, reps=15, sets=3),
        WorkoutExercise(workout=workout1, exercise=squat, reps=12, sets=4),
        WorkoutExercise(workout=workout2, exercise=treadmill_run, duration_seconds=1200),
        WorkoutExercise(workout=workout2, exercise=yoga_stretch, duration_seconds=300),
    ])
    db.session.commit()

    print("Seed data created successfully!")
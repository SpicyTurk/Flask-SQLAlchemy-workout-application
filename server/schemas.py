from marshmallow import Schema, fields, validate


class ExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    category = fields.String(
        required=True,
        validate=validate.OneOf(['Cardio', 'Strength', 'Flexibility', 'Balance']),
    )
    equipment_needed = fields.Boolean(load_default=False)


class WorkoutSchema(Schema):
    id = fields.Integer(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Integer(
        required=True, validate=validate.Range(min=1, max=600)
    )
    notes = fields.String(allow_none=True, validate=validate.Length(max=1000))


class WorkoutExerciseSchema(Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(dump_only=True)
    exercise_id = fields.Integer(dump_only=True)
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=0))

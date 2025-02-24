from marshmallow import Schema, fields

class StudentSchema(Schema):
    id = fields.Int()
    first_name = fields.Str()
    last_name = fields.Str()
    email = fields.Str()

class CourseSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    description = fields.Str()

class EnrollmentSchema(Schema):
    id = fields.Int()
    student_id = fields.Int()
    course_id = fields.Int()

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    role = fields.Str(required=True)
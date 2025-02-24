from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, Student, Course, Enrollment
from app.schemas import StudentSchema, CourseSchema, EnrollmentSchema
from app.auth import  role_required

main = Blueprint('main', __name__)


@main.route('/students', methods=['POST'])
@role_required("admin")
@jwt_required()
def add_student():
    data = request.get_json()
    
    required_fields = ["first_name", "last_name", "email"]
    empty_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if empty_fields:
        return jsonify({"message": f"These fields cannot be empty: {', '.join(empty_fields)}"}), 400
        
    new_student = Student(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email']
    )
    db.session.add(new_student)
    db.session.commit()
    return jsonify(StudentSchema().dump(new_student)), 201


@main.route('/students/<int:student_id>', methods=['PUT'])
@role_required('staff')
@jwt_required()
def update_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.get_json()
    if "first_name" in data:
        student.first_name = data["first_name"]
    if "last_name" in data:
        student.last_name = data["last_name"]
    if "email" in data:
        student.email = data["email"]

    db.session.commit()
    return jsonify(StudentSchema().dump(student)), 200


@main.route('/students/<int:student_id>', methods=['DELETE'])
@role_required("admin")
@jwt_required()
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    current_user = get_jwt_identity()
    if not isinstance(current_user, dict) or "role" not in current_user:
        return jsonify({"message": "Invalid token format"}), 401
      
    if current_user["role"] != "admin":
        return jsonify({"message": "Only admins can delete students"}), 403

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": f"Student ID {student_id} deleted successfully!"}), 200


@main.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    students = Student.query.all()
    return jsonify(StudentSchema(many=True).dump(students))


@main.route('/students/<int:id>', methods=['GET'])
@jwt_required()
def get_student(id):
    student = Student.query.get_or_404(id)
    return jsonify(StudentSchema().dump(student))


@main.route('/courses', methods=['POST'])
@jwt_required()
def add_course():
    data = request.get_json()
    
    required_fields = ["name", "description"]
    empty_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if empty_fields:
        return jsonify({"message": f"These fields cannot be empty: {', '.join(empty_fields)}"}), 400
        
    new_course = Course(
        name=data['name'],
        description=data['description']
    )
    db.session.add(new_course)
    db.session.commit()
    return jsonify(CourseSchema().dump(new_course)), 201


@main.route('/courses/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    data = request.get_json()
    if "name" in data:
        course.name = data["name"]
    if "description" in data:
        course.description = data["description"]

    db.session.commit()
    return jsonify(CourseSchema() .dump(course)), 200


@main.route('/courses/<int:course_id>', methods=['DELETE'])
@jwt_required()
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    current_user = get_jwt_identity()
    if not isinstance(current_user, dict) or "role" not in current_user:
        return jsonify({"message": "Invalid token format"}), 401

    if current_user["role"] != "admin":
        return jsonify({"message": "Only admins can delete courses"}), 403

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": f"Course ID {course_id} deleted successfully!"}), 200


@main.route('/enroll', methods=['POST'])
@jwt_required()
def enroll_student():
    data = request.get_json()
    
    required_fields = ["student_id", "course_id"]
    empty_fields = [field for field in required_fields if field not in data or not data[field].strip()]
    if empty_fields:
        return jsonify({"message": f"These fields cannot be empty: {', '.join(empty_fields)}"}), 400
        
    new_enrollment = Enrollment(
        student_id=data['student_id'],
        course_id=data['course_id']
    )
    db.session.add(new_enrollment)
    db.session.commit()
    return jsonify(EnrollmentSchema().dump(new_enrollment)), 201

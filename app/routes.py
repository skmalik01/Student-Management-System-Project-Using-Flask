from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.models import db, Student, Course, Enrollment
from app.schemas import StudentSchema, CourseSchema, EnrollmentSchema
from app.auth import  role_required

main = Blueprint('main', __name__)


@main.route('/students', methods=['POST'])
@role_required("admin", "staff")
def add_student():
    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  
        
        if claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admin and staff can update students"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    
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
@role_required("admin", "staff")
def update_student(student_id):
    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  

        if claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admin and staff can update students"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    
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
@role_required("admin", "staff")
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  

        if claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admin and staff can delete students"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": f"Student ID {student_id} deleted successfully!"}), 200


@main.route('/students', methods=['GET'])
@role_required('admin', 'staff')
def get_students():
    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  
        
        if claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admin and staff can update students"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    
    students = Student.query.all()
    return jsonify(StudentSchema(many=True).dump(students))


@main.route('/students/<int:id>', methods=['GET'])
@role_required('admin', 'staff')
def get_student(id):
    student = Student.query.get_or_404(id)
    if not student:
        return jsonify({"message" : "Student Not Found"})
    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  
        
        if claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admin and staff can update students"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    
    return jsonify(StudentSchema().dump(student))


@main.route('/courses', methods=['POST'])
@role_required('admin')
def add_course():
    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  
        
        if claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admin can update Course"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    
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
@role_required('admin')
def update_course(course_id):
    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  
        
        if claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admin can update course"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401
    
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    data = request.get_json()
    if "name" in data:
        course.name = data["name"]
    if "description" in data:
        course.description = data["description"]

    db.session.commit()
    return jsonify(CourseSchema().dump(course)), 200


@main.route('/courses/<int:course_id>', methods=['DELETE'])
@role_required('admin')
def delete_course(course_id):
    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": "Course not found"}), 404

    try:
        claims = get_jwt() 
        current_user_id = get_jwt_identity()  
        
        if claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admin can update course"}), 403
        
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401

    db.session.delete(course)
    db.session.commit()
    return jsonify({"message": f"Course ID {course_id} deleted successfully!"}), 200


@main.route('/enroll', methods=['POST'])
@role_required('admin')
def enroll_student():
    try:
        claims = get_jwt()
        current_user = get_jwt_identity()

        if "role" not in claims or claims["role"] not in ["admin", "staff"]:
            return jsonify({"message": "Only admins and staff can enroll students"}), 403

    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 401

    data = request.get_json()

    required_fields = ["student_id", "course_id"]
    empty_fields = [field for field in required_fields if field not in data or (isinstance(data[field], str) and not data[field].strip())]

    if empty_fields:
        return jsonify({"message": f"These fields cannot be empty: {', '.join(empty_fields)}"}), 400

    try:
        student_id = int(data["student_id"])
        course_id = int(data["course_id"])
    except ValueError:
        return jsonify({"message": "Student ID and Course ID must be integers"}), 400

    student = Student.query.get(student_id)
    if not student:
        return jsonify({"message": f"Student with ID {student_id} not found"}), 404

    course = Course.query.get(course_id)
    if not course:
        return jsonify({"message": f"Course with ID {course_id} not found"}), 404

    existing_enrollment = Enrollment.query.filter_by(student_id=student_id, course_id=course_id).first()
    if existing_enrollment:
        return jsonify({"message": "Student is already enrolled in this course"}), 409

    new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
    db.session.add(new_enrollment)
    db.session.commit()

    return jsonify({"message": "Student successfully enrolled!", "enrollment": EnrollmentSchema().dump(new_enrollment)}), 201


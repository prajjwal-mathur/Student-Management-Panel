from flask import request, jsonify, render_template
from app import app
from config import db
from schema import ClassSchema, SubjectSchema, ClassSubjectSchema, StudentSchema, StudentMarksSchema
from model import Class, Subject, ClassSubjects, Students, StudentMarks
from marshmallow import ValidationError
from loguru import logger

if not Class.table_exists():
    db.create_tables([Class])

if not Subject.table_exists():
    db.create_tables([Subject])

if not ClassSubjects.table_exists():
    db.create_tables([ClassSubjects])

if not Students.table_exists():
    db.create_tables([Students])

if not StudentMarks.table_exists():
    db.create_tables([StudentMarks])

###########################CLASS###########################################


@app.route('/class', methods=['GET'])
def get_class():
    try:
        classes = Class.select()
        return render_template('page.html', classes=ClassSchema(many=True).dump(classes))
        # return jsonify(ClassSchema(many=True).dump(classes)), 200
    except ValidationError as e:
        logger.exception(e)


@app.route('/class', methods=['POST'])
def add_class():
    try:
        data = request.get_json()
        result = ClassSchema().load(data)
        result.save()
        response = {
            'status': 'HTTP_201_CREATED',
            'message': 'Student data successfully saved to the database',
            'data': ClassSchema().dump(result)
        }
        return jsonify(response), 201
    except ValidationError as e:
        return str(e.messages), 500

############################### SUBJECTS #########################################


@app.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        subject = Subject.select()
        return jsonify(SubjectSchema(many=True).dump(subject)), 200
    except ValidationError as e:
        logger.exception(e)


@app.route('/subjects', methods=['POST'])
def add_subjects():
    try:
        data = request.get_json()
        if isinstance(data, list):
            result = SubjectSchema(many=True).load(data)
            for subject in result:
                subject.save()
            logger.debug(data)
            response = {
                'status': 'HTTP_201_CREATED',
                'message': f'{len(result)} subjects stored successfully saved to the database',
                'data': SubjectSchema(many=True).dump(result)
            }
            return jsonify(response), 201
        if isinstance(data, dict):
            result = SubjectSchema().load(data)
            logger.debug(data)
            result.save()
            response = {
                'status': 'HTTP_201_CREATED',
                'message': 'Subject data successfully saved to the database',
                'data': SubjectSchema().dump(result)
            }
            return jsonify(response), 201

    except ValidationError as e:
        return str(e.messages), 500


####################################STUDENTS########################################


@app.route('/students', methods=['GET'])
def get_students():
    try:
        student = Students.select()
        return jsonify(StudentSchema(many=True).dump(student)), 200
    except ValidationError as e:
        logger.exception(e)


@app.route('/students', methods=['POST'])
def add_students():
    try:
        data = request.get_json()
        if isinstance(data, list):
            result = StudentSchema(many=True).load(data)
            for student in result:
                student.save()
            logger.debug(data)
            response = {
                'status': 'HTTP_201_CREATED',
                'message': f'{len(result)} students data successfully saved to the database',
                'data': StudentSchema(many=True).dump(result)
            }
            return jsonify(response), 201
        if isinstance(data, dict):
            result = StudentSchema().load(data)
            logger.debug(data)
            result.save()
            response = {
                'status': 'HTTP_201_CREATED',
                'message': 'Student data successfully saved to the database',
                'data': StudentSchema().dump(result)
            }
            return jsonify(response), 201

    except ValidationError as e:
        return str(e.messages), 500

#######################################CLASS ALLOTTED SUBJECTS########################################


@app.route('/class-subjects', methods=['GET'])
def get_class_subjects():
    try:
        classSubjects = ClassSubjects(many=True).select()
        return jsonify(ClassSubjectSchema(many=True).dump(classSubjects)), 200
    except ValidationError as e:
        logger.exception(e)


@app.route('/class-subjects', methods=['POST'])
def add_class_subjects():
    try:
        data = request.get_json()
        if isinstance(data, list):
            # ClassSubjectSchema().context['subject_id'] = data['subject_id']
            result = ClassSubjectSchema(many=True).load(data)
            for subject in result:
                subject.save()
            logger.debug(data)
            response = {
                'status': 'HTTP_201_CREATED',
                'message': f'{len(result)} subjects mapped successfully',
                'data': ClassSubjectSchema(many=True).dump(result)
            }
            return jsonify(response), 201
        if isinstance(data, dict):
            contextor = ClassSubjectSchema()
            contextor.context['subject_id'] = data['subjectId']
            result = contextor.load(data)
            logger.debug(data)
            result.save()
            response = {
                'status': 'HTTP_201_CREATED',
                'message': 'Subject data successfully saved to the database',
                'data': ClassSubjectSchema().dump(result)
            }
            return jsonify(response), 201

    except ValidationError as e:
        return str(e.messages), 500


if __name__ == '__main__':
    db.get_tables('classes')
    db.get_tables('subjects')
    db.get_tables('class_subjects')
    db.get_tables('students')
    db.get_tables('student_marks')
    app.run(debug=True)

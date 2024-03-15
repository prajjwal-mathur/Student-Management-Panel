from functools import wraps
import hashlib

from flask import request, jsonify, make_response, render_template, session, redirect
import jwt
from datetime import datetime, timedelta

from supportPy.schema import ClassSchema, SubjectSchema, ClassSubjectSchema, StudentSchema, MarksSchemaV2, \
    StudentDetailsSchema, MarksSchemaV3, UserSchema
from marshmallow import ValidationError
from loguru import logger
from peewee import fn, JOIN

from supportPy.app import app
from supportPy.config import db
from supportPy.model import Class, Subject, ClassSubjects, Students, Marks, Users

if not Class.table_exists():
    db.create_tables([Class])

if not Subject.table_exists():
    db.create_tables([Subject])

if not ClassSubjects.table_exists():
    db.create_tables([ClassSubjects])

if not Students.table_exists():
    db.create_tables([Students])

if not Marks.table_exists():
    db.create_tables([Marks])

if not Users.table_exists():
    db.create_tables([Users])


# ##########################CLASS###########################################
def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        logger.debug(request.headers)
        if 'Authorization' not in request.headers or not request.headers['Authorization']:
            return jsonify({'Alert!': 'Token missing!!'}), 403

        token = request.headers['Authorization'][7:]  # Remove "Bearer " prefix
        if not token:
            return jsonify({'Alert!': 'Token missing!!'}), 403

        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        logger.debug(payload)
        logger.debug(payload["expiry"])
        logger.debug(datetime.now().timestamp())
        if payload["expiry"] < datetime.now().timestamp():
            return jsonify({'Alert!': 'Session Over!! Login again'}), 403

        return func(*args, **kwargs)  # Call the decorated function

    return decorated


@app.route('/class', methods=['GET'])
# @token_required 
def get_class():
    try:
        classes = Class.select()
        response = {
            "data": ClassSchema(many=True).dump(classes),
            "message": 200
        }
        return jsonify(response), 200
    except ValidationError as e:
        return jsonify(e.messages), 401


@app.route('/class/<int:id>', methods=['GET'])
def get_a_class(id):
    fetcher = Class().get_or_none(Class.id == id)
    if fetcher is None:
        response = {'status': 'HTTP_204_NO_CONTENT',
                    'message': 'Make sure you have entered an existing class'}
        return jsonify(response), 420
    payload = {
        "classNo": fetcher.class_no
    }
    return jsonify(payload), 200


@app.route('/class', methods=['POST'])
def add_class():
    try:
        data = request.get_json()
        result = ClassSchema().load(data)
        result.save()

        schema = ClassSubjectSchema()
        for i in result.subject_no:
            payload = {
                "classId": result.id,
                "subjectId": i
            }
            details = schema.load(payload)
            details.save()

        response = {
            'status': 'HTTP_201_CREATED',
            'message': 'Class data successfully saved to the database',
            'data': ClassSchema().dump(result)
        }
        return jsonify(response), 201
    except ValidationError as e:
        return jsonify(e.messages), 400


@app.route('/class/<int:cl>', methods=['PUT'])
def update_class(cl):
    try:
        data = request.get_json()
        result = ClassSchema().load(data)
        fetcher = Class.get_or_none(Class.id == cl)
        if fetcher is None:
            response = {'status': 'HTTP_204_NO_CONTENT',
                        'message': 'Make sure you have entered an existing class'}
            return jsonify(response), 420

        fetcher.class_no = data['classNo']
        fetcher.save()

        response = {
            'status': 'HTTP_200_OK',
            'message': 'Class data successfully updated!',
            'data': ClassSchema().dump(fetcher)
        }
        return jsonify(response), 200
    except ValidationError as err:
        return jsonify(err.messages), 500


@app.route('/class/<int:cl>', methods=['DELETE'])
def delete_class(cl):
    try:
        fetcher = Class.get_or_none(Class.id == cl)
        if fetcher is None:
            response = {'status': 'HTTP_204_NO_CONTENT',
                        'message': 'Make sure you have entered an existing class'}
            return jsonify(response), 420
        fetcher.delete_instance()
        response = {
            'status': 'HTTP_200_OK',
            'message': 'Class successfully deleted!'
        }
        return jsonify(response), 200
    except ValidationError as err:
        return jsonify(err.messages), 500


# ############################## SUBJECTS #########################################

@app.route('/subjects', methods=['GET'])
def get_subjects():
    try:
        subject = Subject.select()
        response = {"data": SubjectSchema(many=True).dump(subject), "message": 200}
        return jsonify(response), 200
    except ValidationError as e:
        return jsonify(e.messages)


@app.route('/subjects', methods=['POST'])
def add_subjects():
    try:
        data = request.get_json()
        subject_schema = SubjectSchema()
        response = {}
        if isinstance(data, list):
            result = subject_schema.load(data, many=True)
            for subject in result:
                subject.save()
            response = {
                'status': 'HTTP_201_CREATED',
                'message': f'{len(result)} subjects stored successfully saved to the database',
                'data': subject_schema.dump(result)
            }
        elif isinstance(data, dict):
            result = subject_schema.load(data)
            result.save()
            response = {
                'status': 'HTTP_201_CREATED',
                'message': 'Subject data successfully saved to the database',
                'data': subject_schema.dump(result)
            }
        return jsonify(response), 201

    except ValidationError as e:
        return jsonify(e.messages), 400


@app.route('/subjects/<int:num>', methods=["PUT"])
def update_subjects(num):
    try:
        data = request.get_json()
        SubjectSchema().load(data)
        fetcher = Subject.get_or_none(Subject.id == num)
        if fetcher is None:
            response = {'status': 'HTTP_204_NOT_FOUND',
                        'message': 'This subject does not exists!!'}
            return jsonify(response), 205

        fetcher.name = data['name']
        fetcher.passing = data['passing']
        fetcher.total = data['total']

        fetcher.save()

        response = {
            'status': 'HTTP_200_OK',
            'message': 'Class data successfully updated!',
            'data': SubjectSchema().dump(fetcher)
        }
        return jsonify(response), 200

    except ValidationError as err:
        return jsonify(err.messages), 500


@app.route('/subjects/<int:num>', methods=['DELETE'])
def delete_subject(num):
    try:
        fetcher = Subject.get_or_none(Subject.id == num)
        if fetcher is None:
            response = {'status': 'HTTP_204_NO_CONTENT',
                        'message': 'This subject does not exist'}
            return jsonify(response), 420
        fetcher.delete_instance()
        response = {
            'status': 'HTTP_200_OK',
            'message': 'Subject successfully deleted!'
        }
        return jsonify(response), 200
    except ValidationError as err:
        return jsonify(err.messages), 500


# ######################################CLASS ALLOTTED SUBJECTS########################################


@app.route('/class-subjects', methods=['GET'])
def get_class_subjects():
    try:
        fetcher = (Class.select(Class.id, Class.class_no, fn.GROUP_CONCAT(Subject.name).alias('subject_names')).
                   join(ClassSubjects, JOIN.LEFT_OUTER, on=(Class.id == ClassSubjects.class_id)).
                   join(Subject, JOIN.LEFT_OUTER, on=(Subject.id == ClassSubjects.subject_id))).group_by(Class.class_no)

        response = {"data": ClassSubjectSchema(many=True).dump(fetcher), "message": 200}
        return jsonify(response)
    except ValidationError as e:
        return jsonify(e.messages)


@app.route('/class-subjects', methods=['POST'])
def add_class_subjects():
    try:
        data = request.get_json()

        result = ClassSchema().load(data)
        result.save()

        schema = ClassSubjectSchema()
        for i in result.subject_no:
            payload = {
                "classId": result.id,
                "subjectId": i
            }
            details = schema.load(payload)
            details.save()

        response = {
            'status': 'HTTP_201_CREATED',
            'message': 'Class data successfully saved to the database',
            'data': ClassSchema().dump(result)
        }
        return jsonify(response), 201

    except ValidationError as e:
        return jsonify(e.messages), 500


@app.route('/class-subjects/<int:id>', methods=['PUT'])
def update_class_subjects(id):
    try:
        data = request.get_json()
        obj_class = ClassSchema()
        obj_class.context['id'] = id
        result = obj_class.load(data)

        fetcher = Class.get_or_none(Class.id == id)
        if fetcher is None:
            response = {'status': 'HTTP_204_NO_CONTENT',
                        'message': 'This class does not exist'}
            return jsonify(response), 420

        ClassSubjects.delete().where(ClassSubjects.class_id == id).execute()

        schema = ClassSubjectSchema()
        for i in result.subject_no:
            payload = {
                "classId": id,
                "subjectId": i
            }
            details = schema.load(payload)
            details.save()

        response = {
            'status': 'HTTP_201_CREATED',
            'message': 'Class data successfully saved to the database',
            'data': ClassSchema().dump(result)
        }
        return jsonify(response), 201

    except ValidationError as err:
        return jsonify(err.messages), 500


@app.route('/class-subjects/<int:id>', methods=['DELETE'])
def delete_class_subjects(id):
    try:
        fetcher = Class.get_or_none(Class.id == id)
        if fetcher is None:
            response = {'status': 'HTTP_204_NO_CONTENT',
                        'message': 'This class does not exist'}
            return jsonify(response), 420
        fetcher.delete_instance()

        map_remover = ClassSubjects.get_or_none(ClassSubjects.class_id == id)
        if map_remover is None:
            response = {'status': 'HTTP_204_NO_CONTENT',
                        'message': 'These subjects map does not exist'}
            return jsonify(response), 420
        ClassSubjects.delete().where(ClassSubjects.class_id == id).execute()
        response = {
            'status': 'HTTP_200_OK',
            'message': 'Class successfully deleted!'
        }
        return jsonify(response), 200

    except ValidationError as err:
        return jsonify(err.messages), 500


# ###################################STUDENTS########################################


@app.route('/students', methods=['GET'])
def get_students():
    try:
        # student = (((Students().select(Students.id, Students.name, Students.admission_year, Class.class_no).
        #              join(Class, on=(Class.id == Students.class_id)))
        #             .where(Students.id == id))
        #            .join(Marks, on=(Marks.student_id == Students.id)))
        query = (Students
                 .select(Students.id, Students.name, Students.admission_year,
                         Class.class_no, fn.SUM(Marks.marks).alias("total_marks"))
                 .join(Class, JOIN.LEFT_OUTER, on=(Class.id == Students.class_id))
                 .switch(Students)
                 .join(ClassSubjects, JOIN.LEFT_OUTER, on=(ClassSubjects.class_id == Class.id))
                 .switch(Students)
                 .join(Subject, JOIN.LEFT_OUTER, on=(Subject.id == ClassSubjects.subject_id))
                 .switch(Students)
                 .join(Marks, JOIN.LEFT_OUTER,
                       on=((Marks.student_id == Students.id) & (Marks.subject_id == Subject.id)))
                 .switch(Students)
                 .group_by(Students.id))
        result = StudentDetailsSchema(many=True).dump(query)

        response = {"data": result, "message": 200}
        return jsonify(response), 200
    except ValidationError as e:
        return jsonify(e.messages), 401


@app.route('/students', methods=['POST'])
def add_students():
    try:
        data = request.get_json()
        # if isinstance(data, list):
        #     result = StudentSchema(many=True).load(data)
        #     for student in result:
        #         student.save()
        #
        #     response = {
        #         'status': 'HTTP_201_CREATED',
        #         'message': f'{len(result)} students data successfully saved to the database',
        #         'data': StudentSchema(many=True).dump(result)
        #     }
        #     return jsonify(response), 201
        if isinstance(data, dict):
            result = StudentSchema().load(data)
            result.save()

            fetch_class_name = Class.get_or_none(Class.id == result.class_id)
            fetch_class_name = fetch_class_name.class_no
            result = {
                "id": result.id,
                "name": result.name,
                "admissionYear": result.admission_year,
                "className": fetch_class_name
            }
            # result2 = MarksSchema().load(data)
            response = {
                'status': 'HTTP_201_CREATED',
                'message': 'Student data successfully saved to the database',
                'data': result
            }
            return jsonify(response), 201

    except ValidationError as e:
        return jsonify(e.messages), 500


@app.route('/students/<int:rollNo>', methods=['PUT'])
def update_student(rollNo):
    try:
        data = request.get_json()
        StudentSchema().load(data)
        fetcher = Students.get_or_none(Students.id == rollNo)
        if fetcher is None:
            response = {'status': 'HTTP_204_NO_CONTENT',
                        'message': 'This subject does not exist'}
            return jsonify(response), 420

        fetcher.name = data['name']
        fetcher.admission_year = data['admissionYear']
        fetcher.class_no = data['classNo']

        fetcher.save()
        response = {
            'status': 'HTTP_200_OK',
            'message': 'Student data successfully updated!',
            'data': StudentSchema().dump(fetcher)
        }
        return jsonify(response), 200

    except ValidationError as err:
        return jsonify(err.messages), 500


@app.route('/students/<int:rollNo>', methods=['DELETE'])
def delete_student(rollNo):
    try:
        fetcher = Students.get_or_none(Students.id == rollNo)
        if fetcher is None:
            response = {'status': 'HTTP_204_NO_CONTENT',
                        'message': 'This student does not exist'}
            return jsonify(response), 420
        query = Students.delete().where(Students.id == rollNo)
        query.execute()
        query = Marks.delete().where(Marks.student_id == rollNo)
        query.execute()
        response = {
            'status': 'HTTP_200_OK',
            'message': 'Student successfully deleted!'
        }
        return jsonify(response), 200

    except ValidationError as err:
        return jsonify(err.messages), 500


# ####Know Marks
@app.route('/marks/<int:rollNo>', methods=['GET'])
def get_marks(rollNo):
    try:
        # fetcher = ((Marks().select().join(Students, on=(Students.id == Marks.student_id))
        #             .where(Marks.student_id == rollNo))
        #            .join(ClassSubjects, on={(ClassSubjects.class_id == Students.class_id),
        #                                     (ClassSubjects.class_id == Students.class_id)}))
        query = (Students
                 .select(Students.id, Students.name, Students.admission_year,
                         Class.class_no, Subject.id.alias("subject_id"), Subject.name.alias("subject_name"),
                         fn.IF(Marks.marks == None, None, Marks.marks).alias("marks"))
                 .join(Class, JOIN.LEFT_OUTER, on=(Class.id == Students.class_id))
                 .switch(Students)
                 .join(ClassSubjects, JOIN.LEFT_OUTER, on=(ClassSubjects.class_id == Class.id))
                 .switch(Students)
                 .join(Subject, JOIN.LEFT_OUTER, on=(Subject.id == ClassSubjects.subject_id))
                 .switch(Students)
                 .join(Marks, JOIN.LEFT_OUTER,
                       on=((Marks.student_id == Students.id) & (Marks.subject_id == Subject.id)))
                 .switch(Students)
                 .where(Students.id == rollNo))
        # query2 = Marks.select(fn.SUM(marks).alias("total_marks")).where(Marks.subject_id == rollNo).group_by(Marks.student_id)

        result = StudentDetailsSchema(many=True).dump(query)
        # total = StudentDetailsSchema().dump(query2)

        data_formatter = {
            "rollNo": result[0]["id"],
            "name": result[0]["name"],
            "admissionYear": result[0]["admissionYear"],
            "classNo": result[0]["classNo"],
            # "totalMarks": total,
            "subjects": [
                {
                    "subjectId": i["subjectId"],
                    "subjectName": i["subjectName"],
                    "marks": i["marks"]
                } for i in result
            ]
        }

        response = {
            'data': data_formatter,
            'response': 200
        }

        return jsonify(response)
    except ValidationError as err:
        return jsonify(err.messages), 500


@app.route('/marks/<int:rollNo>', methods=['POST'])
def add_marks(rollNo):
    try:
        data = request.get_json()

        schema = MarksSchemaV2()
        schema.context['student_id'] = rollNo
        result = schema.load(data)

        with db.atomic():
            Marks.insert_many(result['subjects']).execute()

        response = {
            'status': 'HTTP_201_CREATED',
            'message': f'Student marks for {len(data['subjects'])} subjects for roll number {rollNo} successfully '
                       f'saved to the database'
        }
        return jsonify(response), 201

    except ValidationError as e:
        return jsonify(e.messages), 500


@app.route('/marks/<int:rollNo>', methods=['PUT'])
def update_marks(rollNo):
    try:
        data = request.get_json()
        data = data["data"]
        # First check if that student even has subject marks added
        checker = Marks.get_or_none(Marks.student_id == rollNo)

        schema = MarksSchemaV2()
        schema.context['student_id'] = rollNo
        payload = {
            "subjects": [
                {'subjectId': data['subjects'][i],
                 'marks': data['marks'][i]
                 } for i in range(len(data["subjects"]))
            ]
        }
        result = schema.load(payload)
        with db.atomic():
            if checker is None:
                schema.context['PUT'] = False
                (Marks.insert_many(result['subjects'])).execute()
                message = {
                    "message": f"Marks of Student with roll number {rollNo} successfully updated!",
                    "status": "HTTP_201_CREATED"
                }
                message = jsonify(message)
                return message, 201
            else:
                schema = MarksSchemaV3()
                schema.context['PUT'] = True
                logger.debug(schema.context['PUT'])
                for i in payload["subjects"]:
                    fetcher = Marks.get_or_none(Marks.student_id == rollNo, Marks.subject_id == i['subjectId'])
                    fetcher.marks = i['marks']
                    fetcher.save()
                message = {
                    "message": f"Marks of Student with roll number {rollNo} successfully updated!",
                    "status": "HTTP_201_CREATED"
                }
                message = jsonify(message)
                return message, 201
    except ValidationError as e:
        message = e.messages['subjects']
        error = []
        for key in message:
            error.append(message[key]['_schema'][0])
        error = {
            "error": error
        }
        return jsonify(error), 410


@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        schema = UserSchema()
        result = schema.load(data)
        result.password = hashlib.sha256(result.password.encode()).hexdigest()
        logger.debug(result.password)
        result.save()
        response = {
            "message": "User successfully created!",
            "status": "HTTP_201_CREATED"
        }
        return jsonify(response), 201
    except ValidationError as e:
        return jsonify(e.messages), 410


# ################LOGIN

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = Users.get_or_none(Users.username == data['username'],
                                 Users.password == hashlib.sha256(data['password'].encode()).hexdigest())
    logger.debug(username)
    if username is not None:
        session['logged_in'] = True
        token_made = {
            'id': username.id,
            'username': data['username'],
            'expiry': (datetime.now() + timedelta(seconds=10)).timestamp()
        }
        token = jwt.encode(token_made, app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token,
                        'status_code': 201,
                        'WWW-Authenticate': 'Basic realm:"Authentication Successful!"',
                        'message': "You are logged in. Ready(3) Get Set(2) GOOO(1)..."}), 201
    else:
        return jsonify({'message': 'Unable to verify credentials',
                        "token": "",
                        'status_code': 403,
                        'WWW-Authenticate': 'Basic realm:"Authentication Failed!!"'}), 403


if __name__ == '__main__':
    db.get_tables('classes')
    db.get_tables('subjects')
    db.get_tables('class_subjects')
    db.get_tables('students')
    db.get_tables('student_marks')
    app.run(debug=True)

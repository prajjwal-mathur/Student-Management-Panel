import string

from loguru import logger
from marshmallow import Schema, fields, post_load, validate, pre_dump, ValidationError, validates, pre_load
from peewee import PrimaryKeyField

from supportPy.model import Subject, Class, ClassSubjects, Students, Marks, Users


class ClassSchema(Schema):
    id = fields.Integer(dump_only=True)
    class_no = fields.String(required=True,
                             attribute='class_no',
                             data_key='classNo')
    subjectNo = fields.List(fields.Integer,
                            load_only=True,
                            required=True,
                            attribute='subject_no',
                            data_key='subjectNo',
                            )

    @validates('class_no')
    def validate_name(self, class_no):
        if class_no is None:
            raise ValidationError({'error': 'Class value is required!'})
        if 'id' in self.context:
            retrieve = Class.get_or_none(Class.class_no == class_no, Class.id != self.context.get('id'))
        else:
            logger.debug("else reached")
            retrieve = Class.get_or_none(Class.class_no == class_no)
            logger.debug(retrieve)
            if retrieve:
                raise ValidationError({'error': 'This class already exists'})

    @validates('subjectNo')
    def validate_subject_no(self, subjectNo):
        if subjectNo is None:
            raise ValidationError({'error': 'Enter the subjects!!'})
        # counter = Counter(subjectNo)
        # for values in counter.values():
        #     if values > 1:
        #         raise ValidationError({'error': 'Duplicates found :('})
        if len(subjectNo) != len(set(subjectNo)):
            raise ValidationError({'error': 'Duplicates found :('})

    @pre_dump()
    def pre_dump(self, data, **kwargs):
        return data

    @post_load()
    def post_dump(self, data, **kwargs):
        return Class(**data)


class SubjectSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True,
                         attribute='name',
                         data_key='name')
    total = fields.Float(required=True,
                         attribute='total',
                         data_key='total',
                         validate=validate.Range(min=0, max=100),
                         error_message='Marks between 0 to 100'
                         )
    passing = fields.Float(required=True,
                           attribute='passing',
                           data_key='passing',
                           validate=validate.Range(min=0, max=100),
                           error_message='Marks between 0 to 100'
                           )

    @validates('name')
    def validate_name(self, name):
        if name is None:
            raise ValidationError('Enter subject name')
        if not isinstance(name, str):
            raise ValidationError('Subject name must be a string')
        if not name.istitle():
            raise ValidationError('First letter of the alphabet must be capitalized')
        retrieve = Subject.get_or_none(name=name)
        if retrieve:
            raise ValidationError('This subject already exists')

    @validates('passing')
    def validate_passing(self, passing):
        if not isinstance(passing, float):
            raise ValidationError('Passing marks must be a float')

    @validates('total')
    def validate_total(self, total):
        if not isinstance(total, float):
            raise ValidationError('Total marks must be a float')

    @pre_dump()
    def pre_dump(self, data, **kwargs):
        return data

    @post_load()
    def post_load(self, data, **kwargs):
        return Subject(**data)


class ClassSubjectSchema(Schema):
    id = fields.Integer()
    class_id = fields.Integer(required=True, attribute='class_id', data_key='classId')
    subject_id = fields.Integer(required=True, attribute='subject_id', data_key='subjectId')

    class_schemaId = fields.Integer(dump_only=True, attribute='class.id', data_key='classSchemaId')
    class_name = fields.String(dump_only=True, attribute='class_no', data_key='classNo')
    subject_names = fields.String(dump_only=True, attribute='subject_names', data_key='subjectNames')

    @pre_dump
    def pre_dump(self, data, **kwargs):
        return data

    @post_load()
    def pre_load(self, data, **kwargs):
        return ClassSubjects(**data)


class StudentSchema(Schema):
    id = fields.Integer()
    name = fields.String(required=True,
                         attribute='name',
                         data_key='name')
    admission_year = fields.Integer(required=True,
                                    attribute='admission_year',
                                    data_key='admissionYear',
                                    validate=validate.Range(min=1900, max=4000),
                                    error_message='Enter admission year between 1900 and 4000')
    class_id = fields.Integer(load_only=True,
                              required=True,
                              attribute='class_id',
                              data_key='classId')

    @pre_dump()
    def pre_dump(self, data, **kwargs):
        return data

    @post_load()
    def post_load(self, data, **kwargs):
        return Students(**data)


# class MarksSchema(Schema):
#     id = fields.Integer()
#     student_id = fields.Integer(required=True,
#                                 attribute='student_id',
#                                 data_key='studentId')
#     subject_id = fields.Integer(required=True,
#                                 attribute='subject_id',
#                                 data_key='subjectId')
#     marks = fields.Integer(required=True,
#                            attribute='marks',
#                            data_key='marks')
#
#     @post_load()
#     def post_load(self, data, **kwargs):
#         return Marks(**data)


class MarksSchemaV2(Schema):
    subjects = fields.List(fields.Nested('MarksSchemaV3'),
                           required=True,
                           attribute="subjects",
                           data_key='subjects')

    @pre_load()
    def pre_load(self, data, **kwargs):
        new_data = {"subjects": []}
        for i in range(len(data["subjects"])):
            json_data = {
                "studentId": self.context.get('student_id'),
                "subjectId": data["subjects"][i]["subjectId"],
                "marks": data["subjects"][i]["marks"]
            }
            new_data['subjects'].append(json_data)
        logger.debug(new_data)
        return new_data


class MarksSchemaV3(Schema):
    student_id = fields.Integer(required=True,
                                attribute='student_id',
                                data_key='studentId')
    subject_id = fields.Integer(required=True,
                                attribute='subject_id',
                                data_key='subjectId')
    marks = fields.Float(required=True,
                         attribute='marks',
                         data_key='marks')

    @validates('student_id')
    def validate_roll_no(self, student_id):
        retrieve = Students.get_or_none(Students.id == student_id)
        if retrieve is None:
            raise ValidationError(f"Student with this roll number doesn't exists!")

    @pre_load()
    def pre_load(self, data, **kwargs):
        logger.debug(data)
        stud = Students.get_or_none(Students.id == data['studentId'])
        comb = ClassSubjects.get_or_none(ClassSubjects.class_id == stud.class_id,
                                         ClassSubjects.subject_id == data['subjectId'])
        if comb is None:
            raise ValidationError(f"This class doesn't have this subject")
        if self.context.get('PUT'):
            # To check if combination of student_id and subject_id already exists: ONLY FOR POST METHOD
            combi = Marks.get_or_none(Marks.subject_id == data['subjectId'], Marks.student_id == data['studentId'])
            if combi is not None:
                subject = Subject.get_or_none(Subject.id == data['subjectId'])
                raise ValidationError(
                    f"This student already has {subject.name} subject "
                    f"marked. Use edit button to alter their marks")

        fetcher = Subject.get_or_none(Subject.id == data['subjectId'])
        # To check if marks entered are lesser than total marks
        if data['marks'] >= fetcher.total:
            raise ValidationError(f"{fetcher.name} marks should be lesser than or equal to {fetcher.total}")
        return data


class StudentDetailsSchema(Schema):
    id = fields.Int(dump_only=True,
                    data_key='id')
    name = fields.String(dump_only=True,
                         attribute='name',
                         data_key='name')
    admission_year = fields.Int(dump_only=True,
                                attribute='admission_year',
                                data_key='admissionYear')
    class_no = fields.String(dump_only=True,
                             attribute='class.class_no',
                             data_key='classNo')
    subject_id = fields.Int(dump_only=True,
                            attribute='subject.subject_id',
                            data_key='subjectId')
    subject_name = fields.String(dump_only=True,
                                 attribute='subject.subject_name',
                                 data_key='subjectName')
    marks = fields.Int(dump_only=True,
                       attribute='marks',
                       data_key='marks')
    total_marks = fields.Integer(dump_only=True,
                                 attribute='total_marks',
                                 data_key='totalMarks')

    @pre_dump()
    def pre_dump(self, data, **kwargs):
        return data


class UserSchema(Schema):
    id = PrimaryKeyField()
    username = fields.String(attribute="username",
                             data_key='username')
    password = fields.String(attribute="password",
                             data_key='password')

    @validates('username')
    def validate_username(self, username):
        if username is None or len(username) == 0:
            raise ValidationError('Username is required')
        if Users.get_or_none(Users.username == username):
            raise ValidationError('This username already exists!!')

    @validates('password')
    def validate_password(self, password):
        if password is None or len(password) < 8:
            raise ValidationError('Password should be more than 8 characters')
        upper, lower, digit, special = 0, 0, 0, 0
        for i in range(len(password)):
            if password[i].isalpha():
                if password[i].isupper():
                    upper += 1
                elif password[i].islower():
                    lower += 1
            elif password[i].isdigit():
                digit += 1
            else:
                special += 1
        if upper == 0 or lower == 0 or digit == 0 or special == 0:
            raise ValidationError('Enter at least one A-Z, a-z, 0-9 and special characters(!, @, #, $, %, ^, &, *)')

    @post_load()
    def post_load(self, data, **kwargs):
        return Users(**data)

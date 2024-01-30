import loguru
from marshmallow import Schema, fields, post_load, pre_load, validate, pre_dump, ValidationError, validates
from model import Subject, Class, ClassSubjects, Students, StudentMarks


class ClassSchema(Schema):
    id = fields.Integer(dump_only=True)
    class_no = fields.String(required=True,
                             attribute='class_no',
                             data_key='classNo')

    @validates('class_no')
    def validate_name(self, class_no):
        if class_no is None:
            raise ValidationError('Enter class')
        retrieve = Class.get_or_none(class_no=class_no)
        if retrieve:
            raise ValidationError('This class already exists')

    @pre_dump()
    def pre_dump(self, data, **kwargs):
        return data

    @post_load()
    def post_dump(self, data, **kwargs):
        return Class(**data)


class SubjectSchema(Schema):
    id = fields.Integer()
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
        if not name.istitle():
            raise ValidationError('First letter of the alphabet must be capitalized')
        retrieve = Subject.get_or_none(name=name)
        if retrieve:
            raise ValidationError('This subject already exists')

    @pre_dump()
    def pre_dump(self, data, **kwargs):
        return data

    @post_load()
    def post_load(self, data, **kwargs):
        return Subject(**data)


class ClassSubjectSchema(Schema):
    id = fields.Integer()
    class_id = fields.Integer(required=True,
                              attribute='class_id',
                              data_key='classId')
    subject_id = fields.Integer(required=True,
                                attribute='subject_id',
                                data_key='subjectId')

    @validates('class_id')
    def validate_id(self, class_id):
        loguru.logger.info(f'Class ID: {class_id}, Subject ID: {self.context}')
        retrieve = ClassSubjects.get_or_none(ClassSubjects.class_id == class_id,
                                             ClassSubjects.subject_id == self.context['subject_id'])
        if retrieve:
            raise ValidationError('This subject already exists in this class')

    @pre_dump()
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
    class_id = fields.Integer(required=True,
                              attribute='class_id',
                              data_key='classId')

    @pre_dump()
    def pre_dump(self, data, **kwargs):
        return data

    @post_load()
    def post_load(self, data, **kwargs):
        return Students(**data)


class StudentMarksSchema(Schema):
    id = fields.Integer()
    student_id = fields.Integer(required=True)
    subject_id = fields.Integer(required=True)
    marks = fields.Float(required=True,
                         attribute='marks',
                         data_key='marks',
                         validate=validate.Range(min=0, max=100))

    @validates('student_id')
    def validate_roll_no(self, student_id):
        retrieve = StudentMarks.get_or_none(student_id=student_id, subject_id=self.context.get('subject_id'))
        if retrieve:
            raise ValidationError(f'Student with id:{student_id} already has subject: {self.context.get("subject_id")}')

    @pre_dump()
    def pre_dump(self, data, **kwargs):
        return data

    @post_load()
    def post_load(self, data, **kwargs):
        return StudentMarks(**data)

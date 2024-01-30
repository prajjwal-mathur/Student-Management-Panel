from peewee import Model, CharField, PrimaryKeyField, IntegerField, FloatField
from config import db


class Class(Model):
    id = PrimaryKeyField()
    class_no = CharField()

    class Meta:
        database = db
        db_table = 'classes'


class Subject(Model):
    id = PrimaryKeyField()
    name = CharField()
    total = FloatField()
    passing = FloatField()

    class Meta:
        database = db
        db_table = 'subjects'


class ClassSubjects(Model):
    id = PrimaryKeyField()
    class_id = IntegerField()
    subject_id = IntegerField()

    class Meta:
        database = db
        db_table = 'class_subjects'


class Students(Model):
    id = PrimaryKeyField()
    name = CharField()
    admission_year = IntegerField()
    class_id = IntegerField()

    class Meta:
        database = db
        db_table = 'students'


class StudentMarks(Model):
    id = PrimaryKeyField()
    student_id = IntegerField()
    subject_id = IntegerField()
    marks = IntegerField()

    class Meta:
        database = db
        db_table = 'student_marks'
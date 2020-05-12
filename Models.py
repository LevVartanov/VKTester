from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test = Column(Text)
    length = Column(Text)
    type = Column(Text)
    file_name = Column(Text)


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Integer)
    answer = Column(Text)
    marker = Column(Integer)


class Question(Base):
    __tablename__ = 'questions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text)


class ResultInquirer(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    result = Column(Text)
    answers = Column(Text)


class Criterion(Base):
    __tablename__ = 'criterions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    mark = Column(Text)
    criterion = Column(Integer)


class ResultExam(Base):
    __tablename__ = 'results1'
    answers = Column(Text, primary_key=True)

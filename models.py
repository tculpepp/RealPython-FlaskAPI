# models.py

# imports the datetime object from the datetime module that comes with Python.
# This gives you a way to create a timestamp in the Person class in lines 11 to 13.
from datetime import datetime
from marshmallow_sqlalchemy import fields

# imports db, an instance of SQLAlchemy that you defined in the config.py module.
# This gives models.py access to SQLAlchemy attributes and methods.
from config import db, ma

class Note(db.Model):
    __tablename__ = "note"
    id = db.Column(db.Integer, primary_key=True)
    person_id = db.Column(db.Integer, db.ForeignKey("person.id"))
    content = db.Column(db.String, nullable=False)
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        sqla_session = db.session
        include_fk = True
# You’re referencing Note from within NoteSchema, so you must place NoteSchema underneath your Note class 
# definition to prevent errors. You also instantiate NoteSchema to create an object that you’ll refer to later.

# defines the Person class. Inheriting from db.Model gives Person the SQLAlchemy 
# features to connect to the database and access its tables.
class Person(db.Model):
    __tablename__ = "person" #connects the class definition to the person database table.
    id = db.Column(db.Integer, primary_key=True) #declares the id column containing an integer acting as the primary key for the table.

    # defines the last name field with a string value. This field must 
    # be unique because you’re using lname as the identifier for a person in a REST API URL.
    lname = db.Column(db.String(32), unique=True)
    fname = db.Column(db.String(32)) #defines the first name field with a string value.

    # define a timestamp field with a datetime value.
    timestamp = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    notes = db.relationship(
        Note,
        backref="person",
        cascade="all, delete, delete-orphan",
        single_parent=True,
        order_by="desc(Note.timestamp)"
    )

class PersonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Person
        load_instance = True
        sqla_session = db.session
        include_relationships = True #include linked data in other tables
    notes = fields.Nested(NoteSchema, many=True)

note_schema = NoteSchema()
person_schema = PersonSchema()
people_schema = PersonSchema(many=True)

# Line 35: Similar to what you’ve done for other attributes of the class, here you create a new attribute called .notes and set it equal to an instance of an object called db.relationship. This object creates the relationship that you’re adding to the Person class, and it’s created with all of the parameters defined in the lines that follow.
# Line 36: The parameter Note defines the SQLAlchemy class that the Person class will be related to. The Note class isn’t defined yet, so it won’t work at the moment. Sometimes it might be easier to refer to classes as strings to avoid issues with which class is defined first. For example, you could use "Note" instead of Note here.
# Line 37: The backref="person" parameter creates what’s known as a backwards reference in Note objects. Each instance of Note will contain an attribute called .person. The .person attribute references the parent object that a particular Note instance is associated with. Having a reference to the parent object (Person in this case) in the child can be very useful if your code iterates over notes and has to include information about the parent.
# Line 38: The cascade="all, delete, delete-orphan" parameter determines how to treat Note instances when changes are made to the parent Person instance. For example, when a Person object is deleted, SQLAlchemy will create the SQL necessary to delete the Person object from the database. This parameter tells SQLAlchemy to also delete all the Note instances associated with it. You can read more about these options in the SQLAlchemy documentation.
# Line 39: The single_parent=True parameter is required if delete-orphan is part of the previous cascade parameter. This tells SQLAlchemy not to allow an orphaned Note instance—that is, a Note without a parent Person object—to exist, because each Note has a single parent.
# Line 40: The order_by="desc(Note.timestamp)" parameter tells SQLAlchemy how to sort the Note instances associated with a Person object. When a Person object is retrieved, by default the notes attribute list will contain Note objects in an unknown order. The SQLAlchemy desc() function will sort the notes in descending order from newest to oldest, rather than the default ascending order.
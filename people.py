# people.py

# from datetime import datetime
from flask import abort, make_response

from config import db
from models import Person, people_schema, person_schema

# # helper function, generates a string representation of the current timestamp.
# def get_timestamp():
#     return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

# PEOPLE = {
#     "Fairy": {
#         "fname": "Tooth",
#         "lname": "Fairy",
#         "timestamp": get_timestamp(),
#     },
#     "Ruprecht": {
#         "fname": "Knecht",
#         "lname": "Ruprecht",
#         "timestamp": get_timestamp(),
#     },
#     "Bunny": {
#         "fname": "Easter",
#         "lname": "Bunny",
#         "timestamp": get_timestamp(),
#     }
# }

def read_all():
    # return list(PEOPLE.values())
    people = Person.query.all()
    return people_schema.dump(people)

def create(person):
    new_person = person_schema.load(person, session=db.session)
    db.session.add(new_person)
    db.session.commit()
    return person_schema.dump(new_person), 201

def read_one(person_id):
    person = Person.query.get(person_id)

    if person is not None:
        return person_schema.dump(person)
    else:
        abort(404, f"Person with ID {person_id} not found")

def update(person_id, person):
    existing_person = Person.query.get(person_id)

    if existing_person:
        update_person = person_schema.load(person, session=db.session)
        existing_person.fname = update_person.fname
        existing_person.lname = update_person.lname
        db.session.merge(existing_person)
        db.session.commit()
        return person_schema.dump(existing_person), 201
    else:
        abort(404, f"Person with ID {person_id} not found")

def delete(lname):
    existing_person = Person.query.get(person_id)

    if existing_person:
        db.session.delete(existing_person)
        db.session.commit()
        return make_response(f"{person_id} successfully deleted", 200)
    else:
        abort(404, f"Person with ID {person_id} not found")
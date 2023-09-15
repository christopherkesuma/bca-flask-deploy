from flask import make_response, abort
from note_model import Note
from person_model import Person, PersonSchema
from config import db
from datetime import datetime
from flask import request

# /api/people
def read_all():
    people = Person.query.all()
    print(people)
    person_schema = PersonSchema(many=True)
    return person_schema.dump(people)

def read_one(person_id):
    """
    This function responds to a request for /api/people/{person_id}
    with one matching person from people

    :param person_id:   Id of person to find
    :return:            person matching id
    """
    # Build the initial query
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    # Did we find a person?
    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        data = person_schema.dump(person)
        return data

    # Otherwise, nope, didn't find that person
    else:
        abort(404, f"Person not found for Id: {person_id}")

def update(person_id, person_data):
    updated_person = Person.query.get(person_id)

    if updated_person is None:
        abort(
            404, f"person with id {person_id} is not found"
        )
    else:
        # lname = person_data.get('lname')
        # fname = person_data.get('fname')

        # updated_person.lname = lname
        # updated_person.fname = fname

        schema = PersonSchema()

        updated_person.fname = person_data['fname']
        updated_person.lname = person_data['lname']

        # update = Person(person_id=person_id,
        # fname=person_data['fname'], 
        # lname=person_data['lname'], 
        # timestamp=updated_person.timestamp)

        # db.session.merge(updated_person)
        # db.session.commit()
        updated_person.update()

        return schema.dump(updated_person)
    # return f"successfully update person {fname} {lname}"

def delete(person_id):
    to_be_deleted = Person.query.get(person_id)

    if to_be_deleted is None:
        abort(
            404, f"person with id {person_id} is not found"
        )
    else:
        to_be_deleted.delete()
        return f"person with id {person_id} is deleted"

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))


def create():
    person_data = request.get_json()
    new_born = Person(
        fname = person_data['fname'],
        lname = person_data['lname']
    )

    

    # app.logger.info(new_born.person_id)

    new_born.create()

    schema = PersonSchema()

    return schema.dump(new_born)

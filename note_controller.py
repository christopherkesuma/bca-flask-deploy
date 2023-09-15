from note_model import Note, NoteSchema
from person_model import Person, PersonSchema
from flask import abort, request
from config import db

# GET /notes
# [
#     {
#         "note_id": 
#         "content" : 
#         "timestamp" : 
#         "person" : {
#             "lname":
#             "fname":
#             "person_id":
#         }
#     }
# ]
def read_all():
    notes = Note.query.outerjoin(Person).all()
    notes_schema = NoteSchema(many=True)
    return notes_schema.dump(notes)


# POST /people/{person_id}/notes
def create(person_id):
    note = request.get_json()
    #find person
    person = (
        Person.query.filter(Person.person_id == person_id)
        .outerjoin(Note)
        .one_or_none()
    )

    if person is None:
        abort(
            404,
            f"Person with id {person_id} is not found"
        )
    
    # content = note.get('content')
    content = note['content']
    new_note = Note(content = content, person_id = person.person_id)

    person.notes.append(new_note)

    person.save()

    note_schema = NoteSchema()
    result = note_schema.dump(new_note)

    return result

# GET /people/{person_id}/notes/{note_id}
def read_one(person_id, note_id):
    note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
            .filter(Note.note_id == note_id)
            # .filter(Person.person_id == person_id)
            .one_or_none()
    )

    if note is None:
        abort(
            404,
            f"note with id {note_id} own by person {person_id} is not found"
        )
    
    note_schema = NoteSchema()
    
    return note_schema.dump(note)


# PUT /people/{person_id}/notes/{note_id}
def update(person_id, note_id, note):
    found_note = (
        Note.query.join(Person, Person.person_id == Note.person_id)
            .filter(Note.note_id == note_id)
            # .filter(Person.person_id == person_id)
            .one_or_none()
    )

    if found_note is None:
        abort(
            404,
            f"note with id {note_id} own by person {person_id} is not found"
        )

    found_note.content = note.get('content')

    found_note.update()

    note_schema = NoteSchema()

    return note_schema.dump(found_note)


# DELETE /people/{people_id}/notes/{note_id}
def delete():
    pass
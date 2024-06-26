# Note: chat_id's are stored as strings because the int is too large to be stored in a PSQL database.
import threading

from sqlalchemy import Column, String, Boolean, UnicodeText, Integer, func, distinct

from pyrobot.helper_functions.sql_helpers import SESSION, BASE


class Notes(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    name = Column(UnicodeText, primary_key=True)
    d_message_id = Column(Integer)

    def __init__(self, chat_id, name, d_message_id):
        self.chat_id = str(chat_id)  # ensure string
        self.name = name
        self.d_message_id = d_message_id

    def __repr__(self):
        return f"<Note {self.name}>"


Notes.__table__.create(checkfirst=True)

NOTES_INSERTION_LOCK = threading.RLock()


def add_note_to_db(chat_id, note_name, note_message_id):
    with NOTES_INSERTION_LOCK:
        if prev := SESSION.query(Notes).get((str(chat_id), note_name)):
            SESSION.delete(prev)
        note = Notes(str(chat_id), note_name, note_message_id)
        SESSION.add(note)
        SESSION.commit()


def get_note(chat_id, note_name):
    try:
        return SESSION.query(Notes).get((str(chat_id), note_name))
    finally:
        SESSION.close()


def rm_note(chat_id, note_name):
    with NOTES_INSERTION_LOCK:
        if note := SESSION.query(Notes).get((str(chat_id), note_name)):
            SESSION.delete(note)
            SESSION.commit()
            return True
        else:
            SESSION.close()
            return False


def get_all_chat_notes(chat_id):
    try:
        return SESSION.query(Notes).filter(Notes.chat_id == str(chat_id)).order_by(Notes.name.asc()).all()
    finally:
        SESSION.close()


def num_notes():
    try:
        return SESSION.query(Notes).count()
    finally:
        SESSION.close()


def num_chats():
    try:
        return SESSION.query(func.count(distinct(Notes.chat_id))).scalar()
    finally:
        SESSION.close()

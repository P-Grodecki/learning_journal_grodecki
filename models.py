from datetime import datetime, date

from peewee import *

DATABASE = SqliteDatabase('journal.db')


class Entry(Model):
    entry_id = PrimaryKeyField()
    entry_title = CharField(max_length=255)
    entry_time_spent = IntegerField()
    entry_learned = TextField()
    entry_references = TextField()
    user_id = IntegerField(default=1)
    entry_date = DateField()

    class Meta():
        database = DATABASE
    
    def journal_stream(self):
        qry = Entry.select().order_by(Entry.entry_date).limit(5)
        return qry

    @classmethod
    def create_entry(cls, form_dict):
        """Takes the values from a form and inserts 
        them as a new row in the database."""
        with DATABASE.transaction():
            cls.create(
                entry_title = form_dict["title"],
                entry_date = form_dict["date"],
                entry_time_spent = form_dict["timeSpent"],
                entry_learned = form_dict["whatILearned"],
                entry_references = form_dict["ResourcesToRemember"]
            )


def update_entry(row, form_dict):
    """Given a dictionary object, update an existing row in database """
    print('Title '+row.entry_title)
    row.entry_title = form_dict["title"]
    row.entry_date = form_dict["date"]
    row.entry_time_spent = int(form_dict["timeSpent"])
    row.entry_learned = form_dict["whatILearned"]
    row.entry_references = form_dict["ResourcesToRemember"]
    row.save()


def remove_entry(id):
    """Given the entry ID of a journal, delete the entry from the table."""
    q = Entry.delete().where(Entry.entry_id == id)
    q.execute()
    return True


def long_date_str(row):
    """Returns a formatted string date from table row"""
    return datetime.combine(
        row.entry_date,
        datetime.min.time()
    ).strftime('%B %d, %Y')


def sample_entry():
    """Create sample journal entry data dictionary"""
    entry_row = {
        "title":"This is a Sample Entry",
        "timeSpent":2,
        "whatILearned":"This is what i learned.", 
        "ResourcesToRemember":"These are references to remember\n- Reference 1\n- Reference 2\n- Reference 3",
        "date":date(datetime.now().year,datetime.now().month,datetime.now().day)
    }
    return entry_row


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Entry], safe=True)
    DATABASE.close()

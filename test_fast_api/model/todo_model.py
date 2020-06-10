from mongoengine import Document
from mongoengine import StringField
from mongoengine import DateTimeField
from mongoengine import BooleanField
from mongoengine import ReferenceField
from mongoengine import CASCADE


class ToDictMixin:
    def to_dict(self):
        d = self.to_mongo().to_dict()
        d['id'] = str(d['_id'])
        return d


class TodoListModel(Document, ToDictMixin):
    name = StringField(required=True, max_length=128)
    description = StringField(max_length=1024, null=True)


class TodoItemModel(Document, ToDictMixin):
    text = StringField(required=True, max_length=1024)
    due_date = DateTimeField()
    finished_status = BooleanField()
    todo_list = ReferenceField(TodoListModel, required=True, reverse_delete_rule=CASCADE)

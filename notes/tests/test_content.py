from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.constants import NOTES_COUNT
from notes.models import Note


User = get_user_model()


class TestListPage(TestCase):

    LIST_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='John Snow')
        Note.objects.bulk_create(
            Note(
                title=f'Заметка {index}',
                text='Просто текст',
                author=cls.author,
                slug=index
            )
            for index in range(NOTES_COUNT)
        )

    def test_notes_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, NOTES_COUNT)

from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .constants import NOTES_COUNT
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

    def get_object_list(self):
        self.client.force_login(self.author)
        response = self.client.get(self.LIST_URL)
        return response.context['object_list']

    def test_notes_count(self):
        """Метод проверяет, что на странице список заметок
        отображаются все заметки автора
        """
        object_list = self.get_object_list()
        notes_count = object_list.count()
        self.assertEqual(notes_count, NOTES_COUNT)

    def test_notes_order(self):
        """Метод проверяет, что заметки отсортированы от
        самой первой к последней по id.
        """
        object_list = self.get_object_list()
        # Получаем id  заметок в том порядке, как они выведены на странице.
        id_list_on_page = [note.id for note in object_list]
        sorted_id = sorted(id_list_on_page)
        self.assertEqual(id_list_on_page, sorted_id)

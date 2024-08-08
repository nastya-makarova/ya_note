from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='John Snow')
        cls.notes = Note.objects.create(
            title='Название заметки',
            text='Текст заметки',
            author=cls.author
        )

    def test_pages_availability(self):
        """Метод тестирует доступность для анонимных пользователей главной страницы,
        cтраницы регистрации пользователей,
        страниц входа в учётную запись и выхода из неё.
        """
        urls = (
            'notes:home',
            'users:login',
            'users:logout',
            'users:signup'
        )
        for name in urls:
            with self.subTest(name=name):
                url = reverse(name)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_pages_availability_for_author(self):
        """Метод проверяет доступность автору страниц:
        страницы отдельной заметки, страницы списка заметок,
        страниц удаления и редактирования заметки.
        """
        # Логиним пользователя в клиенте:
        self.client.force_login(self.author)

        # Создаём набор тестовых данных - кортеж кортежей.
        # Каждый вложенный кортеж содержит два элемента:
        # имя пути и позиционные аргументы для функции reverse().
        urls = (
            ('notes:detail', (self.notes.slug,)),
            ('notes:list', None),
            ('notes:edit', (self.notes.slug,)),
            ('notes:delete', (self.notes.slug,)),

        )

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

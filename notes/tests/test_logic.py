from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .constants import (EXPECTED_REDIRECT_URL, NOTE_ADD_URL,
                        NOTE_SLUG, NOTE_TEXT, NOTE_TITLE, NEW_NOTE_TEXT)
from notes.models import Note


User = get_user_model()


class TestNoteCreation(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='Sansa Stark')
        cls.auth_client = Client()
        cls.auth_client.force_login(cls.user)
        cls.form_data = {'title': NOTE_TITLE, 'text': NOTE_TEXT}

    def test_anonymous_user_cant_create_note(self):
        """Метод проверяет, что анонимный пользователь 
        не может создать заметку
        """
        self.client.post(NOTE_ADD_URL, data=self.form_data)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    def test_user_can_create_note(self):
        """Метод проверяет, что залогиненный пользователь 
        может создать заметку
        """
        response = self.auth_client.post(
            NOTE_ADD_URL,
            data=self.form_data
        )
        self.assertRedirects(response, EXPECTED_REDIRECT_URL)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)
        note = Note.objects.get()
        self.assertEqual(note.title, NOTE_TITLE)
        self.assertEqual(note.text, NOTE_TEXT)
        self.assertEqual(note.author, self.user)

    def test_validate_slug(self):
        """Метод проверяет, если пользователь не указал слаг,
        он автоматически создается из названия заметки
        """
        self.auth_client.post(
            NOTE_ADD_URL,
            data=self.form_data
        )
        note = Note.objects.get()
        self.assertEqual(note.slug, NOTE_SLUG)


class TestNoteEditDelete(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.author = User.objects.create(username='Автор заметки')
        cls.reader = User.objects.create(username='Чиатель')
        cls.note = Note.objects.create(
            title=NOTE_TITLE,
            text=NOTE_TEXT,
            author=cls.author
        )
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.reader_client = Client()
        cls.reader_client.force_login(cls.reader)

        cls.edit_url = reverse('notes:edit', args=(cls.note.slug,))
        cls.delete_url = reverse('notes:delete', args=(cls.note.slug,))

        cls.form_data = {'title': NOTE_TITLE, 'text': NEW_NOTE_TEXT} 

    def test_author_can_delete_note(self):
        """Метод проверяет, что авторизованный пользователь может
        удалять свои заметки.
        """
        response = self.author_client.delete(self.delete_url)
        self.assertRedirects(response, EXPECTED_REDIRECT_URL)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 0)

    def test_user_cant_delete_note_of_another_user(self):
        """Метод проверяет, что авторизованный пользователь
        не может удалять чужие заметки.
        """
        response = self.reader_client.delete(self.delete_url)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        note_count = Note.objects.count()
        self.assertEqual(note_count, 1)

    def test_user_cant_edit_note_of_another_user(self):
        """Метод проверяет, что авторизованный пользователь
        не может редактировать чужие заметки.
        """
        response = self.reader_client.post(self.edit_url, data=self.form_data)
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, NOTE_TEXT)

    def test_author_can_edit_note(self):
        """Метод проверяет, что авторизованный пользователь
        может редактировать чужие заметки.
        """
        response = self.author_client.post(self.edit_url, data=self.form_data)
        self.assertRedirects(response, EXPECTED_REDIRECT_URL)
        self.note.refresh_from_db()
        self.assertEqual(self.note.text, NEW_NOTE_TEXT)

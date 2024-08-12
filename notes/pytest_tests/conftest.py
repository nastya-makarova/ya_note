import pytest

from django.test.client import Client

from notes.models import Note


@pytest.fixture
def author(django_user_model):
    """Фиктсутра возвращает автора заметки."""
    return django_user_model.objects.create(username='Автор')


@pytest.fixture
def not_author(django_user_model):
    """Фиктсутра возвращает обычного пользователя, не автора заметки."""
    return django_user_model.objects.create(username='Не автор')


@pytest.fixture
def author_client(author):  # Вызываем фикстуру автора.
    """Фикстура возвращает клиента, авторизованного для автора."""
    # Создаём новый экземпляр клиента, чтобы не менять глобальный.
    client = Client()
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def not_author_client(not_author):
    """Фикстура возвращает клиента, авторизованного 
    для обычного пользователя не автора.
    """
    client = Client()
    client.force_login(not_author)
    return client


@pytest.fixture
def note(author):
    """Фикстура возвращает объект заметки."""
    note = Note.objects.create(
        title='Заголовок',
        text='Текст заметки',
        slug='note-slug',
        author=author,
    )
    return note


@pytest.fixture
def slug_for_args(note):
    return (note.slug,)


@pytest.fixture
def form_data():
    """Фикстура возвращает словарь модели Note"""
    return {
        'title': 'Новый заголовок',
        'text': 'Новый текст',
        'slug': 'new-slug'
    }

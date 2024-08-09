from django.urls import reverse

NOTES_COUNT = 10
NOTE_TITLE = 'Название заметки'
NOTE_TEXT = 'Текст заметки'
NOTE_ADD_URL = reverse('notes:add')
NOTE_SLUG = 'nazvanie-zametki'
EXPECTED_REDIRECT_URL = reverse('notes:success')
NEW_NOTE_TEXT = 'Новый текст заметки'
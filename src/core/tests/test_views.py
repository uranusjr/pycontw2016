import os

import pytest

from django.utils.translation import activate


def test_index_page(client):
    response = client.get('/en-us/')
    assert response.status_code == 200
    assert 'PyCon' in response.content.decode('utf-8')


@pytest.mark.parametrize('path,expected', [
    ('/en-us/speaking/cfp/',   200),
    ('/en-us/speaking/talk/',  200),
    ('/en-us/speaking/base/',  404),
    ('/en-us/speaking/_base/', 404),
])
def test_speaking_pages(client, path, expected):
    assert client.get(path).status_code == expected


def content_page_path_gen():
    from django.conf import settings
    checked = set()
    for template_setting in settings.TEMPLATES:
        for template_dir in template_setting['DIRS']:
            for lang in ['en', 'zh']:
                contents_path = os.path.join(template_dir, 'contents', lang)
                os.chdir(contents_path)
                for dirpath, _, filenames in os.walk('.'):
                    if os.path.basename(dirpath).startswith('_'):
                        continue
                    for filename in filenames:
                        if filename.startswith('_'):
                            continue
                        root, ext = os.path.splitext(filename)
                        if ext != '.html':
                            continue
                        comps = [c for c in dirpath.split(os.sep) if c != '.']
                        path = '/'.join([''] + comps + [root, ''])
                        if path in checked:
                            continue
                        yield path
                        checked.add(path)


@pytest.fixture(params=content_page_path_gen())
def content_page_path(request):
    return request.param


def language_gen():
    from django.conf import settings
    for lang_code, _ in settings.LANGUAGES:
        yield lang_code


@pytest.fixture(params=language_gen())
def language(request, settings):
    lang = request.param

    def activate_default_language():
        activate(settings.LANGUAGE_CODE)

    request.addfinalizer(activate_default_language)
    activate(lang)
    return lang


def test_content_pages(client, language, content_page_path):
    path = '/' + language + '/' + content_page_path
    response = client.get(path)
    assert response.status_code == 200, path

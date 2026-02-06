"""Test view to debug locale middleware"""
from django.http import HttpResponse
from django.utils.translation import get_language
from django.conf import settings


def test_language_view(request):
    """View to test which language is detected"""
    current_lang = get_language()
    path = request.path
    get_lang = request.GET.get('lang', 'not in GET')
    session_lang = request.session.get(settings.LANGUAGE_SESSION_KEY, 'not in session')
    
    html = f"""
    <html>
    <head><title>Language Test</title></head>
    <body>
        <h1>Language Debug Info</h1>
        <p><strong>Request Path:</strong> {path}</p>
        <p><strong>Current Language (get_language()):</strong> {current_lang}</p>
        <p><strong>GET Parameter (lang):</strong> {get_lang}</p>
        <p><strong>Session Language:</strong> {session_lang}</p>
        <p><strong>LANGUAGE_CODE Setting:</strong> {settings.LANGUAGE_CODE}</p>
        <p><strong>All Available Languages:</strong></p>
        <ul>
            {''.join(f'<li><a href="/{code}/">Go to {name} ({code})</a></li>' for code, name in settings.LANGUAGES)}
        </ul>
    </body>
    </html>
    """
    return HttpResponse(html)

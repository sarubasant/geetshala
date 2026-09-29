10. Setup — Live Along¶

python3 -m venv myenv
source myenv/bin/activate        # Windows: myenv\Scripts\activate
pip install django
django-admin --version           # verify
A virtual environment is an isolated Python environment, so dependencies for different projects never conflict. Commands installed inside it are available only inside it.

Virtual Environment¶
A virtual environment is an isolated Python environment that allows you to manage dependencies for different projects separately. This helps avoid conflicts between packages required by different projects.

To create and activate a virtual environment, you can use the following commands:


python -m venv myenv
source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
Try to run django-admin --version to check if Django is installed in your virtual environment.
If Django is not installed, you can install it using pip:

pip install django

11. Starting the Project¶

django-admin startproject geetshala
cd geetshala
python manage.py runserver

12. Anatomy of the Project¶

geetshala/            ← project root (just a folder)
    manage.py         ← CLI entry point for this project
    geetshala/        ← the Python package (import as geetshala.settings)
        __init__.py   ← marks the directory as a package
        settings.py   ← configuration for the whole project
        urls.py       ← the site's "table of contents"
        wsgi.py       ← entry point for WSGI servers
        asgi.py       ← entry point for ASGI servers

# 18. URLconfs and Loose Coupling¶
A URLconf is a Python list named urlpatterns containing path() definitions.
-- dont forget from django.urls import include
geetshala/urls.py — project level

urlpatterns = [
    path('admin/', admin.site.urls),
    path('songs/', include('songs.urls')),   # hand off to the app
]
songs/urls.py — app level

urlpatterns = [
    path('', views.song_list, name='song_list'),                 # /songs/
    path('<int:song_id>/', views.song_detail, name='song_detail'),  # /songs/1/
]
Loose coupling — URLs are decoupled from view logic, so either side can change alone:

Point /songs/123/ at a maintenance page without touching the URL structure
Rename /songs/123/ to /geet/123/ without touching the view
19. Dynamic URLs¶
One pattern, many requests — the URL captures a variable part and passes it as an argument.

songs/urls.py

path('<int:song_id>/', views.song_detail, name='detail')
songs/views.py

def song_detail(request, song_id):
    return HttpResponse(f"You are viewing Song ID: {song_id}")
Visiting /songs/543/ makes Django call song_detail(request, song_id=543).


# 21. The Django Template System¶
    Django's built-in mechanism for generating HTML, XML, or other text formats
    Separates how data looks from how data is processed — the MTV split
    Templates are .html files: static markup + dynamic placeholders
    Where templates live

templates/ inside each app (default), or
one global project-level templates/ directory registered in settings.py:

TEMPLATES = [{ ..., 'DIRS': [BASE_DIR / 'templates'], ... }]

# 22. Variables, Tags, Filters¶
Variables — {{ ... }} placeholders for dynamic content:


<h1>{{ song.title }}</h1>
<p>Artist: {{ song.artist.name }}</p>
Tags — control flow and framework hooks:

Tag	Purpose
{% if ... %}	Conditional statements
{% for item in items %}	Loop over iterables
{% csrf_token %}	Security tag — required in every POST form
{% url 'name' arg %}	Look up a URL by name instead of hardcoding it
Filters — modify how a value displays, applied with |:

{{ song.release_date|date:"F j, Y" }} · {{ name|default:"Anonymous" }} · {{ comments|length }} · {{ html_content|safe }}

→ Tags and filters in detail

# 23. Templates in Views¶
What exactly does a View do?
The render() shortcut

def song_list(request):
    songs = Song.objects.all()
    return render(request, 'songs/song_list.html', {'songs': songs})
render(request, template_name, context=None, ...) combines a template with a context dictionary and returns an HttpResponse.

Under the hood — manual rendering

template = loader.get_template('songs/song_list.html')
return HttpResponse(template.render({'songs': songs}, request))

25. Template Inheritance — DRY in Action¶
Define common elements once in a base template; children fill in the blocks.

base.html

<title>{% block title %}Welcome to Geetshala{% endblock %}</title>
<main>
  {% block content %}{% endblock %}
</main>
child.html

{% extends "base.html" %}
{% block title %}Home - Geetshala{% endblock %}
{% block content %}
  <h2>List of Songs</h2>
{% endblock %}
Header, nav, and footer are written once — every page inherits them.

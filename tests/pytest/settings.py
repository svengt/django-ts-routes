SECRET_KEY = "test"

ROOT_URLCONF = "tests.pytest._testsite.urls"

USE_TZ = True
LANGUAGE_CODE = "en"
LANGUAGES = [("en", "English")]

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.sessions",
    "django.contrib.sitemaps",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "ts_routes",
    "django.contrib.admin",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    },
]

TS_ROUTES_INCLUSION_LIST = [
    "included_test_with_args",
    "ping",
    "ping_with_args",
    "ping_with_kwargs",
    "ping_with_optional_character",
    "ping_with_optional_group",
    "ping_with_optional_kwarg",
    "ping_with_path",
    "ping_with_paths",
    "ping_with_re_path",
    "ping_with_path_without_converter",
    "ping_i18n",
]

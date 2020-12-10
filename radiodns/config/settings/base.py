"""
Django settings for radiodns project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import environ

# Load operating system environment variables and then prepare to use them
env = environ.Env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
SETTINGS_DIR = environ.Path(__file__) - 1
BASE_DIR = SETTINGS_DIR - 2  # brave30 directory


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "%eea1za680a5x$ah=ts7u+!96=m#%%h1(b4s$w!v_%q1%!o^h*"

# SECURITY WARNING: don"t run with debug turned on in production!
DEBUG = env.bool("DJANGO_DEBUG", False)


ALLOWED_HOSTS = []

# Use custom user model
AUTH_USER_MODEL = "radiodns_auth.User"

# Redirect to trailing slash to avoid linking problems
APPEND_SLASH = True

# Application definition
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

LOCAL_APPS = [
    "common",
    "apps.radiodns_auth",
    "apps.channels",
    "apps.clients",
    "apps.stations",
    "apps.system",
    "apps.manager",
    "apps.radioepg",
    "apps.radiovis",
    "apps.localization",
]

INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS

# Two custom middlewares were implemented - check login, and check whether organisation is set up
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.radiodns_auth.middleware.LoginRequiredMiddleware",
    "apps.manager.middleware.SetupRequiredMiddleware",
]

# URLs, where user does not need to be logged in
LOGIN_EXEMPT_URLS = ["xml-metadata", "/static/", "auth/login/saml"]



ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(BASE_DIR.path("common/templates"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTHENTICATION_BACKENDS = [
    "social_core.backends.saml.SAMLAuth",
    "django.contrib.auth.backends.ModelBackend",
]

LOGIN_URL = "login/"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/
LANGUAGE_CODE = "en-us"


TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SETUP_EXEMPT_URLS = ["setup_error/", "admin/", "xml-metadata/", "static/"]

DOMAIN = os.environ.get("DOMAIN", "127.0.0.1")

# Default Service URLs for RadioDNS Services
RADIOVIS_DNS = os.environ.get("RADIOVIS_DNS", "127.0.0.1")
RADIOEPG_DNS = os.environ.get("RADIOEPG_DNS", "127.0.0.1")
RADIOTAG_DNS = os.environ.get("RADIOTAG_DNS", "127.0.0.1")
RADIOSPI_DNS = os.environ.get("RADIOSPI_DNS", "127.0.0.1")

RADIOVIS_PORT = os.environ.get("RADIOVIS_PORT", "61613")
RADIOEPG_PORT = os.environ.get("RADIOEPG_PORT", "5000")
RADIOTAG_PORT = os.environ.get("RADIOTAG_PORT", "5000")
RADIOSPI_PORT = os.environ.get("RADIOSPI_PORT", "5000")

RADIOVIS_SERVICE_DEFAULT = RADIOVIS_DNS + ":" + RADIOVIS_PORT
RADIOEPG_SERVICE_DEFAULT = RADIOEPG_DNS + ":" + RADIOEPG_PORT
RADIOTAG_SERVICE_DEFAULT = RADIOTAG_DNS + ":" + RADIOTAG_PORT
RADIOSPI_SERVICE_DEFAULT = RADIOSPI_DNS + ":" + RADIOSPI_PORT
RADIOTAG_ENABLED = "True" == os.environ.get("RADIOTAG_ENABLED", "False")



# SAML Integration
# ------------------------------------------------------------------------------

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)


SOCIAL_AUTH_SAML_ENABLED_IDPS = {
    "ebu": {
        "entity_id": "https://sso-qual.ebu.ch:443/auth",
        "url": "https://sso-qual.ebu.ch:443/auth/SSORedirect/metaAlias/idp",
        "x509cert": "MIIDkzCCAnugAwIBAgIEZIYnaDANBgkqhkiG9w0BAQsFADB6MQswCQYDVQQGEwJDSDEPMA0GA1UECBMGR0VORVZBMRAwDgYDVQQHEwdVbmtub3duMQ8wDQYDVQQKEwZlYnUuY2gxEDAOBgNVBAsTB1Vua25vd24xJTAjBgNVBAMTHGh0dHBzOi8vc3NvLXF1YWwuZWJ1LmNoL2F1dGgwHhcNMTYwMzE2MDkwNjM4WhcNMjEwMzE1MDkwNjM4WjB6MQswCQYDVQQGEwJDSDEPMA0GA1UECBMGR0VORVZBMRAwDgYDVQQHEwdVbmtub3duMQ8wDQYDVQQKEwZlYnUuY2gxEDAOBgNVBAsTB1Vua25vd24xJTAjBgNVBAMTHGh0dHBzOi8vc3NvLXF1YWwuZWJ1LmNoL2F1dGgwggEiMA0GCSqGSIb3DQEBAQUAA4IBDwAwggEKAoIBAQCyAXbm8LEng6l5uMOD5tM5BtDlrvmbIgx9HdDT2P1nfhx5uSOnBC1UC0ea96au+nRGSxg0eH7ba5CwjzpLg/0Ouut9oTYkX2PrzIXkxYBx5XpRanNUWu0CdWdWkr4EXd0wCr+n7YbONJg/kJAs S2u//uX8ToYcjb9cP5/Z0IneA8MDsID3s6nAFE5yAn5h9aTJDwALH9WJKt3qb91l+dYKOymDyxXZMIg3c6KyMl0I7Ct4VdUfa+wJsPyah4X5jelbvj4ElwLykem8dsfI4WuZxn4shCV5yrO7zGB/Texc0HYrM52NUf6qGUmKwjytzcfHnavySxqhLgypWxzgPIoXAgMBAAGjITAfMB0GA1UdDgQWBBR+cAgjZplk51Yzeh/vKHsks1t2BzANBgkqhkiG9w0BAQsFAAOCAQEAjpufYWBbGtck0V9cuX4+cjPxiyEe27baHUMy7JSz3C9aR3ZiwZ4QOESP3dxL61IHIP8SMxThED/C8MxYm7Ah+l/xdePUdfRJn4QWVXkCmh8JMxWpojnVzkcOTMduv94NMuafiwl+POzoBIz9P4gl4kGRGH/HHN7caP8UDYmVyco0RzezVVpFXQoqqUKuOEcnM9094lsYZsMSBfZ/gC1BL9K8tvIiF7B0aXDkZVl4M+tO7YEzxXhQrCoBwZkMXpMlQzyXyR9p1/Eg7gmC55wHzIfyS2jzQbHtOEnmt2IKuUmYX/l4+XYxTzKw/V0MHU5YGyn7knI0P+30STdvl76JyA==",
        "attr_user_permanent_id": 'id',
        "attr_username": "username",
        "attr_email": "email",
        "attr_first_name": "first_name",
        "attr_last_name": "last_name",
    }
}




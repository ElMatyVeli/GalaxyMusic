"""
Configuración de Django para el proyecto GalaxyMusic.

Generado por 'django-admin startproject' utilizando Django 5.0.6.

Para obtener más información sobre este archivo, consulte
https://docs.djangoproject.com/es/5.0/topics/settings/

Para obtener la lista completa de configuraciones y sus valores, consulte
https://docs.djangoproject.com/es/5.0/ref/settings/
"""

from pathlib import Path
import MySQLdb

# Función para crear la base de datos si no existe
def create_database_if_not_exists():
    # Configuración de la base de datos
    db_config = {
        'NAME': 'GalaxyMusic1',  # Nombre de la base de datos
        'USER': 'root',           # Usuario de la base de datos
        'PASSWORD': '123456',     # Contraseña de la base de datos
        'HOST': '35.202.240.176', # Host de la base de datos
        'PORT': '3306',           # Puerto de la base de datos
    }
    db_name = db_config['NAME']
    db_user = db_config['USER']
    db_password = db_config['PASSWORD']
    db_host = db_config['HOST']
    db_port = db_config['PORT']

    try:
        # Establecer conexión con la base de datos
        connection = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            port=int(db_port)
        )
        cursor = connection.cursor()
        # Crear la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        cursor.close()
        connection.close()
        # Imprimir un mensaje indicando que la base de datos ha sido creada o ya existe
        print(f"Base de datos {db_name} creada o ya existente.")
    except MySQLdb.Error as e:
        # Manejar cualquier error que ocurra durante la creación de la base de datos
        print(f"Error al crear la base de datos: {e}")

# Llama a la función para crear la base de datos si no existe
create_database_if_not_exists()

# Construye las rutas dentro del proyecto de esta manera: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Configuraciones de inicio rápido para desarrollo - no adecuadas para producción
# Consulta https://docs.djangoproject.com/es/5.0/howto/deployment/checklist/

# ¡ADVERTENCIA DE SEGURIDAD! Mantén la clave secreta utilizada en producción en secreto.
SECRET_KEY = 'django-insecure-%+17wv$a5d)=rr@+r!j9!_h^wb--0k^jykw+hsd_ce$f778=md'

# ¡ADVERTENCIA DE SEGURIDAD! No ejecutes con debug activado en producción.
DEBUG = True

ALLOWED_HOSTS = []


# Definición de aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tienda',
    'sweetify',
]

# Middleware de la aplicación
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URL raíz
ROOT_URLCONF = 'GalaxyMusic.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Aplicación WSGI
WSGI_APPLICATION = 'GalaxyMusic.wsgi.application'


# Base de datos
# https://docs.djangoproject.com/es/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'GalaxyMusic1',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '35.202.240.176',
        'PORT': '3306',
    }
}


# Validación de contraseñas
# https://docs.djangoproject.com/es/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internacionalización
# https://docs.djangoproject.com/es/5.0/topics/i18n/

LANGUAGE_CODE = 'es-es'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Archivos estáticos (CSS, JavaScript, Imágenes)
# https://docs.djangoproject.com/es/5.0/howto/static-files/
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'imgs',
]

# Tipo de campo de clave primaria predeterminado
# https://docs.djangoproject.com/es/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

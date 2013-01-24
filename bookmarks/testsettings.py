DEBUG = True
DEBUG_TEMPLATE = True
SITE_ID = 1
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': '/tmp/asgard-bookmarks-devel.db'
	}
}
INSTALLED_APPS = [
	'django.contrib.auth',
	'django.contrib.comments',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.admin',
	'django.contrib.sites',
	'django.contrib.sitemaps',
	
	'taggit',
	'django_markup',
	'south',
	
	'bookmarks',
]
ROOT_URLCONF = 'bookmarks.testurls'
SECRET_KEY = 'kz!=swngn%ifjrcru3rzovmhvbc@jlu3y5y#i=7%+--az%=+*%'
from django.core.management.base import BaseCommand
from django.urls import URLResolver, URLPattern
from django.urls.exceptions import NoReverseMatch

class Command(BaseCommand):
    help = 'Display all available URLs in your Django project'

    def handle(self, *args, **options):
        self.show_urls(self.get_urlpatterns())

    def get_urlpatterns(self, urlconf=None):
        """
        Return a list of URL patterns in the given URLconf module.
        """
        if urlconf is None:
            urlconf = 'myportfolio.urls'  # Replace with your actual project's URL configuration module

        # Import the URL configuration dynamically
        try:
            if isinstance(urlconf, str):
                urlconf = __import__(urlconf, {}, {}, [''])
            patterns = getattr(urlconf, 'urlpatterns', urlconf)
        except Exception as e:
            raise ValueError(f"Couldn't import URL configuration '{urlconf}': {e}")

        return patterns

    def show_urls(self, patterns, prefix=''):
        """
        Recursively display all available URLs.
        """
        for pattern in patterns:
            if isinstance(pattern, URLResolver):
                self.show_urls(pattern.url_patterns, prefix + pattern.pattern.regex.pattern)
            elif isinstance(pattern, URLPattern):
                try:
                    # Try reversing the URL and printing it
                    url_name = pattern.name
                    if url_name:
                        url = self.get_url(prefix, pattern.pattern.regex.pattern)
                        self.stdout.write(f'{url_name}: {url}')
                except NoReverseMatch:
                    pass

    def get_url(self, prefix, pattern):
        """
        Get the full URL for a given pattern with prefix.
        """
        if prefix:
            return prefix.rstrip('/') + '/' + pattern.lstrip('/')
        else:
            return pattern
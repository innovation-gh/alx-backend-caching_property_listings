from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'

    def ready(self):
        """
        Import signal handlers when the app is ready.
        This ensures that signal handlers are registered and active.
        """
        try:
            import properties.signals
        except ImportError:
            pass
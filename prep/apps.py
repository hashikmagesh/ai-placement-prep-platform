from django.apps import AppConfig


class PrepConfig(AppConfig):  # change PrepConfig to your app name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'prep'  # change to your app name

    def ready(self):
        import prep.signals
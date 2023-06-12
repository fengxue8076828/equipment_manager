from django.apps import AppConfig


class PostsaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'postsale'

    def ready(self):
        from .scheduler import start_scheduler
        start_scheduler()

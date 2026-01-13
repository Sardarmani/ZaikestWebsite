import os
from django.contrib.auth import get_user_model
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_superuser(sender, **kwargs):
    if os.environ.get("CREATE_SUPERUSER") != "1":
        return

    User = get_user_model()

    username = os.environ.get("SU_NAME", "admin")
    email = os.environ.get("SU_EMAIL", "admin@example.com")
    password = os.environ.get("SU_PASSWORD", "admin123")

    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print("✅ Superuser created successfully")
    else:
        print("ℹ️ Superuser already exists")

import time

from blog.models import (
    Post,
)  # Replace "myapp" with the actual name of your application
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from mimesis import Generic


class Command(BaseCommand):
    """автоматически созадет посты"""

    generic = Generic("ru")

    def handle(self, *args, **options):
        generic = Generic()
        while True:
            title = generic.text.word()
            author = User.objects.order_by("?").first()
            body = generic.text.text(quantity=3)
            status = "PB"
            slug = generic.text.word().replace(" ", "-")
            post = Post(
                title=title, slug=slug, author=author, body=body, status=status
            )
            post.save()
            print(f"Added a random post: {post.id}")
            time.sleep(10)

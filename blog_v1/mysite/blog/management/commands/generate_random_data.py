import random
import time

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from mimesis import Generic
from taggit.models import Tag

from ...models import Post


class Command(BaseCommand):
    """Скрипт автоматического созадания постов"""

    generic = Generic("ru")

    def handle(self, *args, **options):
        generic = Generic()
        tags = ["django", "human", "jazz", "music", "space", "tech", "test"]
        while True:
            title = generic.text.word()
            author = User.objects.order_by("?").first()
            body = generic.text.text(quantity=3)
            status = "PB"
            slug = generic.text.word().replace(" ", "-")
            post = Post(
                title=title,
                slug=slug,
                author=author,
                body=body,
                status=status,
            )

            post.save()
            post.tags.add(random.choice(tags))
            print(f"Added a random post: {post.id}")
            time.sleep(10)

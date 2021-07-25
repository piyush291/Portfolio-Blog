import os,django,random

os.environ.setdefault("DJANGO_SETTINGS_MODULE","portfolio.settings")
django.setup()

from faker import Faker
from blog.models import post
from django.contrib.auth.models import User
from django.utils import timezone

def create_post(n):
    fake=Faker()
    for _ in range(n):
        id=random.randint(1,4)
        title=fake.name()
        status=random.choice(['Published','Draft'])

        post.objects.create(title=title + "post!!!",
        author=User.objects.get(id=id),
        slug="-".join(title.lower().split()),
        body=fake.text(),
        created=timezone.now(),
        updated=timezone.now(),
        )


create_post(10)
print("data is populated successfully")
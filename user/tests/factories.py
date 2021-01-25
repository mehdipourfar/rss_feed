import factory
from factory.django import DjangoModelFactory

from user.models import User


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('user_name')

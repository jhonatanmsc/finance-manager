import factory
from django.contrib.auth import get_user_model

from goals.models import Contribution, Goal, Supplier


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@mail.com")
    password = factory.PostGenerationMethodCall("set_password", "123456")


class SupplierFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.Sequence(lambda n: f"supplier{n}")


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker("word")
    value = factory.Faker("pydecimal", left_digits=2, positive=True)


class ContributionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Contribution

    title = factory.Faker("word")
    value = factory.Faker("pydecimal", left_digits=2, positive=True)
    goal = factory.SubFactory(GoalFactory)
    supplier = factory.SubFactory(SupplierFactory)

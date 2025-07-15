import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken

from goals.tests.factories import (
    ContributionFactory,
    GoalFactory,
    SupplierFactory,
    UserFactory,
)


@pytest.fixture
def super_user():
    return UserFactory(username="super", email="super@mail.com", is_staff=True, is_superuser=True)


@pytest.fixture
def auth_client(super_user):
    token = AccessToken.for_user(super_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {str(token)}")
    return client


@pytest.fixture
def goal_1(super_user):
    goal = GoalFactory()
    goal.users.set([super_user])
    return goal


@pytest.fixture
def suppler_1(super_user):
    sup = SupplierFactory()
    sup.users.set([super_user])
    return sup


@pytest.fixture
def contribution_1():
    return ContributionFactory()


@pytest.fixture
def contribution_2():
    return ContributionFactory()

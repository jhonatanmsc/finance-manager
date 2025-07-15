import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list_goals(auth_client):
    url = reverse("goal-list")
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_goals(auth_client, goal_1):
    url = reverse("goal-detail", kwargs={"pk": goal_1.pk})
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_goal(auth_client, goal_1, suppler_1):
    url = reverse("goal-list")
    data = {
        "title": "teste",
        "value": 9999.0,
        "goal": goal_1.pk,
        "supplier": suppler_1.pk,
    }
    response = auth_client.post(url, data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_goal(auth_client, goal_1):
    url = reverse("goal-detail", kwargs={"pk": goal_1.pk})
    data = {
        "title": "updated",
        "value": 9999.0,
    }
    response = auth_client.put(url, data=data)
    print(response.content)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_goal(auth_client, goal_1):
    url = reverse("goal-detail", kwargs={"pk": goal_1.pk})
    data = {"reason": "teste"}
    response = auth_client.delete(url, data=data)
    assert response.status_code == 204
    goal_1.refresh_from_db()
    assert len(goal_1.history) == 1

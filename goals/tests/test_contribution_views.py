from datetime import datetime
from decimal import Decimal

import pytest
from django.urls import reverse

from src.utils import br_tz


@pytest.mark.django_db
def test_list_contributions(auth_client, contribution_1, contribution_2):
    url = reverse("contribution-list")
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_contribution(auth_client, contribution_1):
    url = reverse("contribution-detail", kwargs={"pk": contribution_1.pk})
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_contribution(auth_client, goal_1, supplier_1):
    url = reverse("contribution-list")
    data = {
        "title": "string",
        "description": "string",
        "discount": 20.0,
        "value": 783.0,
        "quantity": 1.0,
        "goal": goal_1.pk,
        "concluded_at": datetime.now(br_tz).strftime("%Y-%m-%d"),
        "supplier": supplier_1.pk,
    }
    response = auth_client.post(url, data=data)
    assert response.content == 1
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_contribution(auth_client, contribution_1, goal_1, supplier_1):
    url = reverse("contribution-detail", kwargs={"pk": contribution_1.pk})
    data = {
        "title": "string",
        "description": "string",
        "discount": Decimal(0.8),
        "value": "7783",
        "quantity": Decimal(1.0),
        "goal": goal_1.pk,
        "concluded_at": "2025-07-22",
        "supplier": supplier_1.pk,
    }
    response = auth_client.put(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_contribution(auth_client, contribution_1):
    url = reverse("contribution-detail", kwargs={"pk": contribution_1.pk})
    data = {"reason": "teste"}
    response = auth_client.delete(url, data=data)
    assert response.status_code == 204
    contribution_1.refresh_from_db()
    assert len(contribution_1.list_log_entries()) == 1

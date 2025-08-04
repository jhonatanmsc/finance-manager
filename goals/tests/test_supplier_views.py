import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list_suppliers(auth_client, supplier_1):
    url = reverse("supplier-list")
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_detail_supplier(auth_client, supplier_1):
    url = reverse("supplier-detail", kwargs={"pk": supplier_1.pk})
    response = auth_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_supplier(auth_client):
    url = reverse("supplier-list")
    data = {
        "name": "teste",
        "description": "",
        "rating": 4,
    }
    response = auth_client.post(url, data=data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_supplier(auth_client, supplier_1):
    url = reverse("supplier-detail", kwargs={"pk": supplier_1.pk})
    data = {
        "name": "updated",
        "description": "",
        "rating": 4,
    }
    response = auth_client.put(url, data=data)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_supplier(auth_client, supplier_1):
    url = reverse("supplier-detail", kwargs={"pk": supplier_1.pk})
    data = {"reason": "teste"}
    response = auth_client.delete(url, data=data)
    assert response.status_code == 204
    supplier_1.refresh_from_db()
    assert len(supplier_1.list_log_entries()) == 1

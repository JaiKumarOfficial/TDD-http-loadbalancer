from loadBalancer import loadbalancer

import pytest


@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client


def test_host_routing_dal(client):
    result = client.get("/", headers={"Host": "www.dal.ca"})
    assert b"reply from DAL server" in result.data


def test_host_routing_apple(client):
    result = client.get("/", headers={"Host": "www.apple.ca"})
    assert b"reply from APPLE server" in result.data


def test_host_routing_notfound(client):
    result = client.get("/", headers={"Host": "www.xyz.com"})
    assert b"Not Found" in result.data
    assert 404 == result.status_code


def test_path_routing_staff(client):
    result = client.get("/staff")
    assert b"This is the staff application." in result.data


def test_path_routing_srudent(client):
    result = client.get("/student")
    assert b"This is the student application." in result.data


def test_path_routing_notfound(client):
    result = client.get("/error")
    assert b"Not Found" in result.data
    assert 404 == result.status_code

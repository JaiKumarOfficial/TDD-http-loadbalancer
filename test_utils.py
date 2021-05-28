from utils import fetch_healthy_server, convert_obj_server_list, Server, get_server_list

import pytest


def test_convert_obj_server_list():
    input = get_server_list("servers.json")
    output = convert_obj_server_list(input)
    assert list(output.keys()) == ["www.dal.ca", "www.apple.ca", "/staff", "/student"]
    assert output["www.dal.ca"][0] == Server("localhost:8081")
    assert output["www.dal.ca"][1] == Server("localhost:8082")
    assert output["www.dal.ca"][2] == Server("localhost:8083")
    assert output["www.apple.ca"][0] == Server("localhost:7071")
    assert output["www.apple.ca"][1] == Server("localhost:7072")
    assert output["www.apple.ca"][2] == Server("localhost:7073")
    assert output["/staff"][0] == Server("localhost:7071")
    assert output["/staff"][1] == Server("localhost:7072")
    assert output["/staff"][2] == Server("localhost:7073")
    assert output["/student"][0] == Server("localhost:8081")
    assert output["/student"][1] == Server("localhost:8082")
    assert output["/student"][2] == Server("localhost:8083")


def test_fetch_healthy_server():
    host = "www.apple.ca"
    healthy_server = Server("localhost:8081")
    unhealthy_server = Server("localhost:8082")
    unhealthy_server.healthy = False
    register = {
        "www.dal.ca": [healthy_server, unhealthy_server],
        "www.apple.ca": [healthy_server, healthy_server],
        "/staff": [healthy_server, unhealthy_server],
        "/student": [unhealthy_server, unhealthy_server],
    }
    assert fetch_healthy_server(register, "www.dal.ca") == healthy_server
    assert fetch_healthy_server(register, "www.apple.ca") == healthy_server
    assert fetch_healthy_server(register, "/staff") == healthy_server
    assert fetch_healthy_server(register, "/student") == None

from flask import Flask, request
import requests, random
from utils import (
    get_server_list,
    convert_obj_server_list,
    check_server_health,
    fetch_healthy_server,
)


loadbalancer = Flask(__name__)


######## Handle test REQUESTS #######


@loadbalancer.route("/")
def router():
    host_header = request.headers["Host"]
    if host_header == "www.dal.ca":
        return "reply from DAL server"
    elif host_header == "www.apple.ca":
        return "reply from APPLE server"
    return "Not Found", 404


@loadbalancer.route("/<path>")
def path_router(path):
    if path == "staff":
        return "This is the staff application"
    elif path == "student":
        return "This is the student application"
    return "Not Found", 404


# ---------- PHASE 2 ---------#
######## Load Balance incoming REQUESTS #######

# Pool of backend servers
dal_servers = ["localhost:8081", "localhost:8082"]
apple_servers = ["localhost:7071", "localhost:7072"]

# ------ Host Based REQUEST ------#
@loadbalancer.route("/")
def router():
    host_header = request.headers["Host"]
    if host_header == "www.dal.ca":
        response = requests.get("http://%s" % random.choice(dal_servers))
        return response.content
    elif host_header == "www.apple.ca":
        response = requests.get("http://%s" % random.choice(apple_servers))
        return response.content
    return "Not Found", 404


# ------ Path Based REQUEST ------#
@loadbalancer.route("/<path>")
def path_router(path):
    if path == "student":
        response = requests.get("http://%s" % random.choice(dal_servers))
        return response.content
    elif path == "staff":
        response = requests.get("http://%s" % random.choice(apple_servers))
        return response.content
    return "Not Found", 404


# ---------- PHASE 3 ---------#
######## Load Balance incoming REQUESTS via picking healthy server from given server list #######

server_dict = get_server_list("server.json")
server_obj_list = convert_obj_server_list(server_dict)

# ------ Host Based REQUEST ------#
@loadbalancer.route("/")
def router():
    updated_server_obj_list = check_server_health(server_obj_list)
    host_header = request.headers["Host"]
    if host_header == "www.dal.ca":
        healthy_server = fetch_healthy_server(updated_server_obj_list, host_header)
        if healthy_server:
            response = requests.get("http://%s" % healthy_server.endpoint)
            return response.content
        return "No Healthy Backend server available"
    elif host_header == "www.apple.ca":
        healthy_server = fetch_healthy_server(updated_server_obj_list, host_header)
        if healthy_server:
            response = requests.get("http://%s" % healthy_server.endpoint)
            return response.content
        return "No Healthy Backend server available"
    return "Not Found", 404


# ------ Path Based REQUEST ------#
@loadbalancer.route("/<path>")
def path_router(path):
    updated_server_obj_list = check_server_health(server_obj_list)
    if path == "student":
        healthy_server = fetch_healthy_server(updated_server_obj_list, "/" + path)
        if healthy_server:
            response = requests.get("http://%s" % healthy_server.endpoint)
            return response.content
        return "No Healthy Backend server available"
    elif path == "staff":
        healthy_server = fetch_healthy_server(updated_server_obj_list, "/" + path)
        if healthy_server:
            response = requests.get("http://%s" % healthy_server.endpoint)
            return response.content
        return "No Healthy Backend server available"
    return "Not Found", 404


if __name__ == "__main__":
    loadbalancer.run(host="0.0.0.0", debug=True)

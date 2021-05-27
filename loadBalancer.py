from flask import Flask, request
import requests, random


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


if __name__ == "__main__":
    loadbalancer.run(host="0.0.0.0", debug=True)

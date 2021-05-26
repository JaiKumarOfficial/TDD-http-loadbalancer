from flask import Flask, request
import os


loadbalancer = Flask(__name__)


@loadbalancer.route("/")
def router():
    host_header = request.headers["Host"]
    if host_header == "www.dal.ca":
        return "reply from DAL server"
    elif host_header == "www.apple.ca":
        return "reply from APPLE server"
    return "Not Found", 404


if __name__ == "__main__":
    loadbalancer.run(host="0.0.0.0", debug=True)

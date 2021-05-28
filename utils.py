import json, requests, random


def get_server_list(path):
    with open(path, "r") as f:
        servers = f.read()
    return json.loads(servers)


class Server:
    def __init__(self, endpoint):
        self.endpoint = endpoint
        self.path = "/healthcheck"
        self.healthy = True
        self.timeout = 1
        self.proto = "http://"

    def update_health(self):
        try:
            response = requests.get(
                self.proto + self.endpoint + self.path, timeout=self.timeout
            )
            if response.ok:
                self.healthy = True
            else:
                self.healthy = False
        except:
            self.healthy = False

    def __repr__(self):
        return "<Server: %s %s %s>" % (self.endpoint, self.healthy, self.timeout)

    def __eq__(self, other):
        if isinstance(other, Server):
            return self.endpoint == other.endpoint
        return False


########
# Convert server list to Server list with Server's class object,
# which holds information regarding health etc. for that server endpoint
########
def convert_obj_server_list(server_dict):
    obj_servers = {}
    for key in server_dict:
        if key == "hosts":
            if isinstance(server_dict[key], list):
                for elem in server_dict[key]:
                    obj_servers.update(
                        {elem["host"]: [Server(server) for server in elem["servers"]]}
                    )
            else:
                obj_servers.update(
                    {
                        server_dict[key]["host"]: [
                            Server(server) for server in server_dict[key]["servers"]
                        ]
                    }
                )
        if key == "paths":
            if isinstance(server_dict[key], list):
                for elem in server_dict[key]:
                    obj_servers.update(
                        {elem["path"]: [Server(server) for server in elem["servers"]]}
                    )
            else:
                obj_servers.update(
                    {
                        server_dict[key]["path"]: [
                            Server(server) for server in server_dict[key]["servers"]
                        ]
                    }
                )
    return obj_servers


########
# Check server endpoint's health and update the health if unhealthy
########
def check_server_health(server_obj_list):
    for key in server_obj_list:
        for server_obj in server_obj_list[key]:
            server_obj.update_health()
    return server_obj_list


########
# Randomly select healthy server of host/path
########
def fetch_healthy_server(servers_detail, host):
    try:
        return random.choice(
            [server for server in servers_detail[host] if server.healthy]
        )
    except IndexError:
        return None

from flask import Flask
import sys

port = sys.argv[1]
app = Flask(__name__)


@app.route("/")
def router():
    return str("This is apple server 1 on port %s" % port)


if __name__ == "__main__":
    app.run("0.0.0.0", port=port, debug=True)

import logging

from flask import Flask, jsonify, request

from encoder import CustomJSONEncoder
from models import Motherboard, Memory, Cpu, Gpu, Owner, HDD, SSD

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# resources
engine = create_engine('postgresql://babou:testing@postgres/mycomputer_app')

# create a configured "Session" class
Session = sessionmaker(bind=engine)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder

logger = logging.getLogger(__name__)


@app.route('/hello', methods=["GET"])
def hello():
    return jsonify("Hello World")


@app.route('/memories', methods=["GET"])
def get_memories():
    memories = session.query(Memory).all()
    return jsonify(memories)


@app.route('/gpus', methods=["GET"])
def get_gpus():
    gpus = session.query(Gpu).all()
    return jsonify(gpus)


@app.route('/cpus', methods=["GET"])
def get_cpus():
    cpus = session.query(Cpu).all()
    return jsonify(cpus)


@app.route('/motherboards', methods=["GET"])
def get_motherboards():
    motherboards = session.query(Motherboard).all()
    return jsonify(motherboards)


@app.route('/owners/<int:id>', methods=["PUT", "DELETE"])
@app.route('/owners', methods=["GET", "POST"])
def get_owners():
    if request.method == "GET":
        owners = session.query(Owner).all()
        return jsonify(owners)
    elif request.method == "POST":
        payload = []
        return jsonify(payload)


@app.route('/ssds', methods=["GET"])
def get_ssds():
    ssds = session.query(SSD).all()
    return jsonify(ssds)


@app.route('/hdds', methods=["GET"])
def get_hdds():
    hdds = session.query(HDD).all()
    return jsonify(hdds)


if __name__ == "__main__":
    # create session
    session = Session()
    # run the app
    app.run(host="0.0.0.0", port="8000", debug=True)

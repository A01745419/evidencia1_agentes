# TC2008B. Sistemas Multiagentes y Gráficas Computacionales
# Python flask server to interact with Unity. Based on the code provided by Sergio Ruiz.
# Octavio Navarro. October 2021

from flask import Flask, request, jsonify
from robotCajas import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

# Size of the board:
# ancho = 15
# alto = 15
# robots = 5
# cajas = 20
# pasos = 5000000
# grid = CanvasGrid(ancho, alto, 750, 750)

app = Flask("Traffic example")

# @app.route('/', methods=['POST', 'GET'])

@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, randomModel, number_agents, width, height

    if request.method == 'POST':
        number_agents = int(request.form.get('NAgents'))
        width = int(request.form.get('width'))
        height = int(request.form.get('height'))
        cajas = int(request.form.get('cajas'))
        pasos = int(request.form.get('pasos'))  
        currentStep = 0

        print(request.form)
        print(number_agents, width, height)
        randomModel = AcomodarCajasModel(width, height, number_agents, cajas, pasos)

        return jsonify({"message":"Parameters recieved, model initiated."})

@app.route('/getAgents', methods=['GET'])
def getAgents():
    global randomModel

    if request.method == 'GET':
        agentPositions = [{"id": str(agent.unique_id), "x": x, "y": 1, "z": z, "tieneCaja": bool(agent.tieneCaja)} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, RobotAgent)]

        return jsonify({'positions':agentPositions})

@app.route('/getObstacles', methods=['GET'])
def getObstacles():
    global randomModel

    if request.method == 'GET':
        carPositions = [{"id": str(agent.unique_id), "x": x, "y":1, "z":z} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, ParedAgent) ]

        return jsonify({'positions':carPositions})

@app.route('/getCajas', methods=['GET'])
def getCajas():
    global randomModel

    if request.method == 'GET':
        boxPosition = [{"id": str(agent.unique_id), "x": x, "y": 1, "z": z, "tipo": agent.tipo} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, CajaAgent)]

        return jsonify({'positions': boxPosition})

@app.route('/getPilas', methods=['GET'])
def getPilas():
    global randomModel

    if request.method == 'GET':
        pilaPosition = [{"id": str(agent.unique_id), "x": x, "y": 1, "z": z, "numCajas": agent.numCajas} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, PilaAgent)]

        return jsonify({'positions': pilaPosition})

@app.route('/getPared', methods=['GET'])
def getPared():
    global randomModel

    if request.method == 'GET':
        doorPosition = [{"id": str(agent.unique_id), "x": x, "y":1, "z":z} for (a, x, z) in randomModel.grid.coord_iter() for agent in a if isinstance(agent, PuertaAgent) ]

        return jsonify({'positions':doorPosition})

@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, randomModel
    if request.method == 'GET':
        randomModel.step()
        currentStep += 1
        return jsonify({'message':f'Model updated to step {currentStep}.', 'currentStep':currentStep})

if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)

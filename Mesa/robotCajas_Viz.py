from robotCajas import *
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

def agent_portrayal(agent):
    '''
    Define el color que tendra cada agente en cierto estado.
    '''
    portrayal = {"Shape": "circle",
                 "Filled": "false",
                 "Layer": 0,
                 "Color": "gray",
                 "r": 0.8}

    portrayal2 = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "black",
                 "r": 0.8}

    portrayal3 = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "blue",
                 "r": 0.8}

    portrayal4 = {"Shape": "circle",
                  "Filled": "true",
                 "Layer": 0,
                 "Color": "brown",
                 "r": 0.5}

    portrayal5 = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "brown",
                 "r": 0}

    if agent.tipo == "robot":
        return portrayal
    elif agent.tipo == "robotCaja":
        return portrayal2
    elif agent.tipo == "pila":
        return portrayal3
    elif agent.tipo == "caja":
        return portrayal4
    else:
        return portrayal5

ancho = 15
alto = 15
robots = 5
cajas = 20
pasos = 50
grid = CanvasGrid(agent_portrayal, ancho, alto, 750, 750)
server = ModularServer(AcomodarCajasModel,
                       [grid],
                       "Robot Acomoda Cajas",
                       {"width":ancho, "height":alto, "agents": robots, "boxes": cajas, "steps": pasos})
server.port = 8521 # The default
server.launch()

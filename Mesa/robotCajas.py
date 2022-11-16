"""
Logica de Acomodo de Cajas con Robot que incluye agentes y modelo
Autores: Jose Luis Madrigal, Cesar Emiliano Palome, Christian Parrish y Jorge Blanco
Noviembre 15, 2022
"""
# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import MultiGrid

# Con `SimultaneousActivation` hacemos que todos los agentes se activen de manera simultanea.
from mesa.time import SimultaneousActivation
import numpy as np
from mesa.datacollection import DataCollector

class RobotAgent(Agent):
    '''
    Representa a un robot que acomoda cajas en pilas.
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "robot"
        #self.caja = False
        self.movimientos = 0

    def move(self):
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True,
            include_center=False,
            radius = 1)
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        caja = False
        
        if len(cellmates) != 0:
            for i in cellmates:
                if i.tipo == "caja":
                    caja = True
                    self.tipo = "robotCaja"
                    i.tipo = "vacio"
                elif i.tipo == "pila":
                    caja = False
                    self.tipo = "robot"
                    i.tipo = "pila"
                    self.model.cajas -= 1

        if len(cellmates) == 0 or caja == False:
            new_position = self.random.choice(possibleSteps)
            cellmatesNewPos = self.model.grid.get_cell_list_contents([new_position])
            if len(cellmatesNewPos) == 1:
                if cellmatesNewPos[0].tipo != "robot" and cellmatesNewPos[0].tipo != "robotCaja":
                    self.model.grid.move_agent(self, new_position)
                    self.movimientos += 1
            elif len(cellmatesNewPos) == 0:
                self.model.grid.move_agent(self, new_position)
                self.movimientos += 1
                    
    
    def step(self):
        if self.model.pasosTotales > 0 and self.model.cajas > 0:
            self.move()
            self.model.pasosTotales -= 1
        else:
            print("FIN DE SIMULACION")


class CajaAgent(Agent):
    '''
    Representa a una caja que estara en el almacen(grid).
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "caja"
        self.movimientos = 0

class PilaAgent(Agent):
    '''
    Representa a una pila que contiene cajas (max 5).
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "pila"
        self.numCajas = 0
        self.movimientos = 0

class AcomodarCajasModel(Model):
    '''
    Representa el modelo que genera agentes y sus comportamientos en su ambiente.
    '''
    def __init__(self, width, height, agents, boxes, steps):
        self.ancho = width
        self.alto = height
        self.agentes = agents
        self.cajas = boxes
        self.pasosTotales = steps * agents
        self.grid = MultiGrid(width, height, True)
        self.schedule = SimultaneousActivation(self)
        self.running = True
        celdas = []
        self.pilas = boxes // agents
        #self.maxPilas = 5

        for (content, x, y) in self.grid.coord_iter():
            celdas.append([x, y])

        for i in range(self.agentes):
            a = RobotAgent(i, self)
            self.schedule.add(a)
            #self.grid.place_agent(a, (1, 1))
            pos = self.random.choice(celdas)
            self.grid.place_agent(a, (pos[0], pos[1]))
            celdas.remove(pos) 
        
        for i in range(self.cajas):
            a = CajaAgent(i, self)
            #self.schedule.add(a)
            # Add the agent to a random grid cell
            pos = self.random.choice(celdas)
            self.grid.place_agent(a, (pos[0], pos[1])) 
            celdas.remove(pos)
        
        for i in range(self.pilas):
            a = PilaAgent(i, self)
            #self.schedule.add(a)
            # Add the agent to a random grid cell
            pos = self.random.choice(celdas)
            self.grid.place_agent(a, (pos[0], pos[1])) 
            celdas.remove(pos)

    def step(self):
        self.schedule.step()
        print("Cajas restantes para acomodar: ", self.cajas)
        print("Movimientos restantes: ", self.pasosTotales)
        print(" ")

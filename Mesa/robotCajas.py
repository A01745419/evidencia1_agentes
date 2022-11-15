"""
Logica de Acomodo de Cajas con Robot que incluye agentes y modelo
Autores: Jose Luis Madrigal, Cesar Emiliano Palome, Christian Parrish y Jorge Blanco
Noviembre 15, 2022
"""
# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Debido a que necesitamos un solo agente por celda elegimos `SingleGrid` que fuerza un solo objeto por celda.
from mesa.space import SingleGrid

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
        self.tipo = 0
        self.caja = False
        self.movimientos = 0

    def move(self):
        ...
    
    def step(self):
        ...

class CajaAgent(Agent):
    '''
    Representa a una caja que estara en el almacen(grid).
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = 1
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
        self.pasos = steps

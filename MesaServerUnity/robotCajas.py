"""
Logica de Acomodo de Cajas con Robots que incluye agentes y modelo
Autores: Jose Luis Madrigal, Cesar Emiliano Palome, Christian Parrish y Jorge Blanco
Creado: Noviembre 15, 2022
"""
# La clase `Model` se hace cargo de los atributos a nivel del modelo, maneja los agentes. 
# Cada modelo puede contener múltiples agentes y todos ellos son instancias de la clase `Agent`.
from mesa import Agent, Model 

# Debido a que necesitamos varios agentes por celda elegimos `MultiGrid` que no fuerza un solo objeto por celda.
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
        self.tieneCaja = False
        self.movimientos = 0
        self.cajasRestantes = self.model.cajas

    def actualizarAgentes(self):
        '''
        Actualiza los tipos de cada agente para representar su color
        o prefab en unity.
        '''
        cellmates = self.model.grid.get_cell_list_contents([self.pos])

        if len(cellmates) != 0:
            for i in cellmates:
                if i.tipo == "caja" and self.tipo == "robot":
                    self.tieneCaja = True
                    self.tipo = "robotCaja"
                    i.tipo = "vacio"

                elif i.tipo == "pila":
                    if self.tipo == "robotCaja":
                        self.tipo = "robot"
                        self.tieneCaja = False

                elif i.tipo == "pilaLlena" and self.tieneCaja == True:
                    self.tieneCaja = True
                    self.tipo = "robotCaja"
                    i.tipo = "pilaLlena"


    def buscarCajas(self):
        '''
        Se mueve en posicion aleatoria en las cuatro direcciones
        dando un solo paso para encontrarse con una caja.
        '''
        possibleSteps = self.model.grid.get_neighborhood(
            self.pos,
            moore=False,
            include_center=False,
            radius=1)
        new_position = self.random.choice(possibleSteps)
        cellmatesNewPos = self.model.grid.get_cell_list_contents([new_position])

        if len(cellmatesNewPos) == 1:
            if cellmatesNewPos[0].tipo != "robot" and \
                cellmatesNewPos[0].tipo != "robotCaja" and \
                cellmatesNewPos[0].tipo != "pared" and \
                cellmatesNewPos[0].tipo != "pila" and \
                cellmatesNewPos[0].tipo != "pilaLlena" and \
                cellmatesNewPos[0].tipo != "puerta":
                self.model.grid.move_agent(self, new_position)
                self.movimientos += 1

        elif len(cellmatesNewPos) == 0:
            self.model.grid.move_agent(self, new_position)
            self.movimientos += 1


    def irPila(self):
        '''
        Se dirige a una pila acomodandose en los ejes x, y
        para dejar una caja.
        '''
        diffX = self.pos[0] - self.model.posicionesPilas[0][0]
        diffY = self.pos[1] - self.model.posicionesPilas[0][1]
        
        if diffX > 0:
            newPos = (self.pos[0] - 1, self.pos[1])
            cellmatesNewPos = self.model.grid.get_cell_list_contents([newPos])

            if len(cellmatesNewPos) == 1:
                if cellmatesNewPos[0].tipo != "robot" and \
                cellmatesNewPos[0].tipo != "robotCaja" and \
                cellmatesNewPos[0].tipo != "pared" and \
                cellmatesNewPos[0].tipo != "puerta":
                    self.model.grid.move_agent(self, newPos)
                    self.movimientos += 1
            elif len(cellmatesNewPos) == 0:
                self.model.grid.move_agent(self, newPos)
                self.movimientos += 1

        elif diffX < 0:
            newPos = (self.pos[0] + 1, self.pos[1])
            cellmatesNewPos = self.model.grid.get_cell_list_contents([newPos])

            if len(cellmatesNewPos) == 1:
                if cellmatesNewPos[0].tipo != "robot" and \
                cellmatesNewPos[0].tipo != "robotCaja" and \
                cellmatesNewPos[0].tipo != "pared" and \
                cellmatesNewPos[0].tipo != "puerta":
                    self.model.grid.move_agent(self, newPos)
                    self.movimientos += 1
            elif len(cellmatesNewPos) == 0:
                self.model.grid.move_agent(self, newPos)
                self.movimientos += 1

        elif diffY > 0:
            newPos = (self.pos[0], self.pos[1] - 1)
            cellmatesNewPos = self.model.grid.get_cell_list_contents([newPos])

            if len(cellmatesNewPos) == 1:
                if cellmatesNewPos[0].tipo != "robot" and \
                cellmatesNewPos[0].tipo != "robotCaja" and \
                cellmatesNewPos[0].tipo != "pared" and \
                cellmatesNewPos[0].tipo != "puerta":
                    self.model.grid.move_agent(self, newPos)
                    self.movimientos += 1
            elif len(cellmatesNewPos) == 0:
                self.model.grid.move_agent(self, newPos)
                self.movimientos += 1

        elif diffY < 0:
            newPos = (self.pos[0], self.pos[1] + 1)
            cellmatesNewPos = self.model.grid.get_cell_list_contents([newPos])

            if len(cellmatesNewPos) == 1:
                if cellmatesNewPos[0].tipo != "robot" and \
                cellmatesNewPos[0].tipo != "robotCaja" and \
                cellmatesNewPos[0].tipo != "pared" and \
                cellmatesNewPos[0].tipo != "puerta":
                    self.model.grid.move_agent(self, newPos)
                    self.movimientos += 1
            elif len(cellmatesNewPos) == 0:
                self.model.grid.move_agent(self, newPos)
                self.movimientos += 1


    def step(self):
        self.cajasRestantes = self.model.cajas
        self.actualizarAgentes()

        if self.model.pasosTotales > 0 and self.model.cajas > 0:
            if self.tieneCaja == True:
                self.irPila()
                self.model.pasosTotales -= 1
            else:
                self.buscarCajas()
                self.model.pasosTotales -= 1
            cellmates = self.model.grid.get_cell_list_contents([self.pos])

            for i in cellmates:
                if i.tipo == "pilaLlena":
                    if self.tieneCaja == True:
                        self.irPila()
                        self.model.pasosTotales -= 1
                elif i.tipo == "pila":
                    if self.tieneCaja == True:
                        if i.numCajas == 4:
                            i.numCajas = 5
                            print(f'PILA llena: {i.numCajas} cajas')
                            i.tipo = "pilaLlena"
                            posLlena = [i.pos[0], i.pos[1]]
                            self.model.posicionesPilas.remove(posLlena)
                            self.tipo = "robot"
                            self.tieneCaja = False
                            self.model.cajas -= 1
                        elif i.numCajas < 4:
                            i.numCajas += 1
                            print(f'Numero de cajas PILA: {i.numCajas}')
                            self.tipo = "robot"
                            self.tieneCaja = False
                            self.model.cajas -= 1
                    

class CajaAgent(Agent):
    '''
    Representa a una caja que estara en el almacen(grid).
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "caja"


class PilaAgent(Agent):
    '''
    Representa a una pila que contiene cajas (max 5).
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "pila"
        self.numCajas = 0


class ParedAgent(Agent):
    '''
    Representa a una pared que se encontrara en el contorno.
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "pared"


class PuertaAgent(Agent):
    '''
    Representa una puerta que estara entre la pared.
    '''
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.tipo = "puerta"


class AcomodarCajasModel(Model):
    '''
    Representa el modelo de robots acomodando cajas
    que genera agentes y sus comportamientos.
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
        self.pilas = (boxes // 5) + 1
        self.posicionesPilas = []
        self.dataCollectorMovements = DataCollector(
            model_reporters={"Total Movements":AcomodarCajasModel.calculateMovements},
            agent_reporters={}
        )
        self.dataCollectorBoxes = DataCollector(
            model_reporters={"Boxes Left":AcomodarCajasModel.calculateBoxes},
            agent_reporters={}
        )

        # Guarda posiciones de celdas para poder actualizar su disponibilidad.
        for (content, x, y) in self.grid.coord_iter():
            celdas.append([x, y])

        # Hace el muro eje y completo izquierda, derecha
        for i in range(0, height):
            a = ParedAgent(i, self)
            self.grid.place_agent(a, (0, i))
            self.grid.place_agent(a, (width - 1, i))
            pos = [0, i]
            pos2 = [width - 1, i]
            celdas.remove(pos)
            celdas.remove(pos2)

        # Hace el muro eje x completo arriba
        for i in range(1, width - 1):
            a = ParedAgent(i, self)
            self.grid.place_agent(a, (i, height - 1))
            pos = [i, height - 1]
            celdas.remove(pos)

        # Hace el muro eje x parte 1 abajo
        for i in range(1, (width // 2)):
            a = ParedAgent(i, self)
            self.grid.place_agent(a, (i, 0))
            pos = [i, 0]
            celdas.remove(pos)

        # Hace puerta entre muro abajo
        a = PuertaAgent(1, self)
        self.grid.place_agent(a, ((width // 2), 0))
        pos = [(width // 2), 0]
        celdas.remove(pos)

        # Hace el muro eje x parte 2 abajo
        for i in range((width // 2) + 1, width - 1):
            a = ParedAgent(i, self)
            self.grid.place_agent(a, (i, 0))
            pos = [i, 0]
            celdas.remove(pos)

        # Hace las pilas que son estanterias
        for i in range(self.pilas):
            a = PilaAgent(i, self)
            pos = self.random.choice(celdas)
            self.grid.place_agent(a, (pos[0], pos[1]))
            self.posicionesPilas.append(pos)
            celdas.remove(pos)

        # Hace robots
        for i in range(self.agentes):
            a = RobotAgent(i, self)
            self.schedule.add(a)
            pos = self.random.choice(celdas)
            self.grid.place_agent(a, (pos[0], pos[1]))
            celdas.remove(pos)
        
        # Hace cajas
        for i in range(self.cajas):
            a = CajaAgent(i, self)
            pos = self.random.choice(celdas)
            self.grid.place_agent(a, (pos[0], pos[1])) 
            celdas.remove(pos)

    def calculateMovements(model):
        '''
        Regresa los movimientos totales que van realizando todos los agentes
        robot en cada step.
        '''
        totalMovements = 0
        movementsReport = [agent.movimientos for agent in model.schedule.agents]
        for x in movementsReport:
            totalMovements += x
        return totalMovements

    def calculateBoxes(model):
        '''
        Regresa las cajas restantes para acomodar en cada step.
        '''
        boxesReport = [agent.cajasRestantes for agent in model.schedule.agents]
        for x in boxesReport:
            return x 

    def step(self):
        self.schedule.step()
        self.dataCollectorMovements.collect(self)
        self.dataCollectorBoxes.collect(self)
        print("Cajas restantes para acomodar: ", self.cajas)
        print("Movimientos restantes para todos los agentes: ", self.pasosTotales)
        print(" ")

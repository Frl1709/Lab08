import copy
from time import time
from database.DAO import DAO


class Model:
    def __init__(self):
        self._solBest = []
        self._listNerc = None
        self._listEvents = None
        self.loadNerc()
        self.n_persone = 0
        self.primo_anno = float('inf')
        self.ultimo_anno = 0
        self.best_solution = ""
        self.ore = 0

    def worstCase(self, nerc_value, maxY, maxH):
        for nerc in self._listNerc:
            if nerc_value == nerc.value:
                self.loadEvents(nerc)
        self.primo_anno = float('inf')
        self.ultimo_anno = 0
        start_time = time()
        self.ricorsione([], maxY, maxH, self._listEvents)
        end_time = time()
        t = end_time - start_time
        print(t)

    def ricorsione(self, parziale, maxY, maxH, pos):
        if len(pos) == 0:
            self.calcola_persone(parziale)
            return

        else:
            new_event = copy.deepcopy(pos)
            flag = False
            for i in pos:
                parziale.append(i)
                new_event.remove(i)
                if self.is_soluzione(parziale, maxH, maxY):
                    flag = True
                    self.ricorsione(parziale, maxY, maxH, new_event)
                parziale.pop()
            if not flag:
                self.ricorsione(parziale, maxY, maxH, new_event)

    def is_soluzione(self, parziale, maxH, maxY):
        n_ore = 0
        for i in parziale:
            # Calcolo ore disservizio
            durata = i.date_event_finished - i.date_event_began
            n_ore += (durata.total_seconds() // 3600) + (((durata.total_seconds() % 3600)//60)/60)
            # Calcolo ultimo anno
            if i.date_event_began.year > self.ultimo_anno:
                self.ultimo_anno = i.date_event_began.year
            # Calcolo primo anno
            if i.date_event_finished.year < self.primo_anno:
                self.primo_anno = i.date_event_began.year
        # Vincolo ore massime di disservizio
        if n_ore > int(maxH):
            return False

        # Vincolo massimo degli anni
        if self.ultimo_anno - self.primo_anno > int(maxY):
            return False

        return True

    def calcola_persone(self, parziale):
        pers = 0
        ore = 0
        for p in parziale:
            pers += p.customers_affected
            durata = p.date_event_finished - p.date_event_began
            ore += (durata.total_seconds() // 3600) + (((durata.total_seconds() % 3600) // 60) / 60)
        if pers > self.n_persone:
            self.n_persone = pers
            self.best_solution = copy.deepcopy(parziale)
            self.ore = ore

    def loadEvents(self, nerc):
        self._listEvents = DAO.getAllEvents(nerc)

    def loadNerc(self):
        self._listNerc = DAO.getAllNerc()


    @property
    def listNerc(self):
        return self._listNerc

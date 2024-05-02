import flet as ft

from model.nerc import Nerc


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._idMap = {}
        self.fillIDMap()

    def handleWorstCase(self, e):
        nerc_value = self._view._ddNerc.value
        max_Y = self._view._txtYears.value
        max_H = self._view._txtHours.value
        self._model.worstCase(nerc_value, max_Y,max_H)

        self._view._txtOut.clean()
        self._view._txtOut.controls.append(ft.Text(f"Tot people affected {self._model.n_persone} \nTot hours of outages: {self._model.ore}"))
        self._view.update_page()

        for i in self._model.best_solution:
            self._view._txtOut.controls.append(ft.Text(i))
            self._view.update_page()


    def fillDD(self):
        nercList = self._model.listNerc

        for n in nercList:
            self._view._ddNerc.options.append(ft.dropdown.Option(n))
        self._view.update_page()

    def fillIDMap(self):
        values = self._model.listNerc
        for v in values:
            self._idMap[v.value] = v

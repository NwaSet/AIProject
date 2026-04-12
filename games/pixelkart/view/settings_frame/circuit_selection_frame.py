from tkinter import *
import games.pixelkart.dao.pixelKart_dao as dao
from ..circuit_editor_view import CircuitEditor


class circuitSelection(Frame):

    def __init__(self, parent, controler=None):
        super().__init__(parent, bg="#d4f5d0", bd=1, relief="solid")

        self.controler = controler
        bg = "#d4f5d0"

        # récupération des circuits depuis le dao
        self.all_circuits = dao.get_all()
        self.circuit_names = list(self.all_circuits.keys())

        # si aucun circuit n'existe encore
        if not self.circuit_names:
            self.circuit_names = ["Aucun circuit"]

        # titre
        self.label = Label(self, text="Circuit Selection", font=("Arial", 20), bg=bg)
        self.label.pack()

        # -------------------------
        # choix du circuit
        # -------------------------
        self.circuit_label = Label(self, text="Choose a circuit:", bg=bg)
        self.circuit_label.pack()

        self.selected_circuit = StringVar()
        self.selected_circuit.set(self.circuit_names[0])

        self.circuit_dropdown = OptionMenu(
            self,
            self.selected_circuit,
            *self.circuit_names
        )
        self.circuit_dropdown.pack()

        # -------------------------
        # nombre de tours
        # -------------------------
        self.lap_label = Label(self, text="Number of laps:", bg=bg)
        self.lap_label.pack()

        self.nb_laps = IntVar(value=1)

        self.lap_spinbox = Spinbox(
            self,
            from_=1,
            to=100,
            textvariable=self.nb_laps,
            width=10
        )
        self.lap_spinbox.pack()

        # -------------------------
        # bouton circuit editor
        # -------------------------
        self.circuit_editor_button = Button(
            self,
            text="Open Circuit Editor",
            width=50,
            command=self.open_circuit_editor
        )
        self.circuit_editor_button.pack(pady=(10, 10))

    def open_circuit_editor(self):
        """
        Ouvre la fenêtre d'édition des circuits.
        """
        CircuitEditor(self, callback=self.set_selected_circuit)

    def set_selected_circuit(self, circuit_name):
        """
        Met à jour le circuit sélectionné après un choix dans le CircuitEditor.
        """
        self.refresh_circuit_list()
        if circuit_name in self.circuit_names:
            self.selected_circuit.set(circuit_name)

    def refresh_circuit_list(self):
        """
        Recharge la liste des circuits depuis le dao
        et met à jour le menu déroulant.
        """
        self.all_circuits = dao.get_all()
        self.circuit_names = list(self.all_circuits.keys())

        if not self.circuit_names:
            self.circuit_names = ["Aucun circuit"]

        menu = self.circuit_dropdown["menu"]
        menu.delete(0, "end")

        for name in self.circuit_names:
            menu.add_command(
                label=name,
                command=lambda value=name: self.selected_circuit.set(value)
            )

        if self.selected_circuit.get() not in self.circuit_names:
            self.selected_circuit.set(self.circuit_names[0])

    def get_selected_circuit(self):
        """
        Retourne le nom du circuit sélectionné.
        """
        return self.selected_circuit.get()

    def get_number_of_laps(self):
        """
        Retourne le nombre de tours choisi.
        """
        try:
            return int(self.nb_laps.get())
        except ValueError:
            return 3
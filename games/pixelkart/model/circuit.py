import games.pixelkart.dao.pixelKart_dao as dao


class Circuit:
    def __init__(
        self, 
        name: str,
        grid: list = None 
        ):

        self.name = name
        self.grid = grid

        self.grid_str = ""

        if self.grid is not None:
            self.grid_str = ",".join("".join(row) for row in self.grid)
        else:
            self.load_circuit(self.name)

    def load_circuit(self, target_circuit):
        circuit_str = dao.get_by_name(target_circuit)
        if circuit_str is None:
            raise ValueError(f"Unknown circuit: {target_circuit}")

        self.name = target_circuit
        self.grid_str = circuit_str
        self.grid = [list(row) for row in circuit_str.split(",")]
    
    @property
    def width(self):
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self):
        return len(self.grid) if self.grid else 0

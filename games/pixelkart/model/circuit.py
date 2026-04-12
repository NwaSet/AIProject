class Circuit:
    def __init__(
        self, 
        name: str = None,
        grid: list = None 
        ):

        self.name = name
        self.grid = grid

    def load_circuit(self, target_circuit):
        with open("games/pixelkart/dao/circuits.txt","r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                name, grid_str = line.split(":")

                if name == target_circuit:
                    self.name = name
                    self.grid = [list(row) for row in grid_str.split(",")]
    
    @property
    def width(self):
        return len(self.grid[0]) if self.grid else 0

    @property
    def height(self):
        return len(self.grid) if self.grid else 0

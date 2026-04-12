from pathlib import Path

FILE_PATH = Path(__file__).with_name("circuits.txt")


def _parse_circuit_line(line):
    line = line.strip()
    if not line or ":" not in line:
        return None, None
    return line.split(":", 1)


def get_all():
    """Retrieve all circuits from the file as a dictionary {name: str}."""
    circuits = {}
    if FILE_PATH.exists():
        with FILE_PATH.open("r", encoding="utf-8") as file:
            for line in file:
                name, circuit = _parse_circuit_line(line)
                if name:
                    circuits[name] = circuit
    return circuits

def get_by_name(name):
    """Retrieve a circuit by its name."""
    circuits = get_all()
    return circuits.get(name)

def save_circuit(name, string):
    """Save a new circuit to the file."""
    if not name:
        raise ValueError("Circuit name cannot be empty.")
    circuits = get_all()
    if name in circuits:
        raise ValueError(f"The circuit '{name}' already exists.")
    existing_content = FILE_PATH.read_text(encoding="utf-8") if FILE_PATH.exists() else ""
    prefix = "\n" if existing_content and not existing_content.endswith("\n") else ""
    with FILE_PATH.open("a", encoding="utf-8") as file:
        file.write(f"{prefix}{name}:{string}")

def delete_circuit(name):
    """Delete a circuit by its name."""
    if not name:
        raise ValueError("Circuit name cannot be empty.")

    circuits = get_all()
    if name not in circuits:
        raise ValueError(f"The circuit '{name}' does not exist.")

    del circuits[name]
    
    with FILE_PATH.open("w", encoding="utf-8") as file:
        for n, c in circuits.items():
            file.write(f"{n}:{c}\n")

def update_circuit(name, string):
    """Update the name of an existing circuit."""
    circuits = get_all()
    if name not in circuits:
        raise ValueError(f"The circuit '{name}' does not exist.")
    
    circuits[name] = string
    with FILE_PATH.open("w", encoding="utf-8") as file:
        for n, c in circuits.items():
            file.write(f"{n}:{c}\n")

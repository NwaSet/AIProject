from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


class Dao:
    def __init__(self, ai_name: str = None):
        self.engine = None
        self.session = None
        self.ai_name = None
        self.current_row = None
        self.data_table = None

        if ai_name:
            self.connect_player_db(ai_name)

    def connect_player_db(self, ai_name):
        # connexion + création auto du fichier
        self.engine = create_engine(f"sqlite:///games/Cubee/DAO/{ai_name}.db")
        self.engine.connect()

        # création session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.ai_name = ai_name
        self.init_column()

    def init_column(self):
        metadata = MetaData()

        self.data_table = Table(
            "data",
            metadata,
            Column("current_player", Integer),
            Column("player1_coord", Integer),
            Column("player2_coord", Integer),
            Column("grid", String),
            Column("grid_size", Integer),
            Column("up", Float),
            Column("down", Float),
            Column("left", Float),
            Column("right", Float),
            Column("id", Integer, primary_key=True, autoincrement=True)
        )

        metadata.create_all(self.engine)

    # gestion des donnée joueur
    def add_row(self, dto_ai):
        """
        Ajoute une ligne uniquement si elle n'existe pas déjà.
        """

        # Vérifie si la ligne existe déjà
        existing = self.select_row_by_dto(dto_ai)

        if existing is not None:
            print("Row already exists, skip insert")
            return

        # Sinon on insert
        row = self.data_table.insert().values(**dto_ai)
        self.session.execute(row)
        self.session.commit()

    def select_row_by_dto(self, dto):
        """
        return un dict (up = x, ...) si la row exsiste sinon null.
        """
        row = select(self.data_table).where(
            self.data_table.c.current_player == dto["current_player"],
            self.data_table.c.player1_coord == dto["player1_coord"],
            self.data_table.c.player2_coord == dto["player2_coord"],
            self.data_table.c.grid == dto["grid"],
        )

        self.current_row = self.session.execute(
            row
        ).fetchone()  # fetchone => return le premier result, fetchall => return tous sous forme d'une liste [row1, row2, ...]

        if self.current_row:
            return {
                "up": self.current_row.up,
                "down": self.current_row.down,
                "left": self.current_row.left,
                "right": self.current_row.right,
            }
        else:
            return None

    def update_row(self, dto):
        """
        pré condition, il faut un select pour update current view, si current view = none error ...
        """
        if self.current_row is None:
            print("x")
            return 0

        row = (
            update(self.data_table)
            .where(self.data_table.c.id == self.current_row.id)
            .values(
                up=dto["up"], down=dto["down"], left=dto["left"], right=dto["right"]
            )
        )

        self.session.execute(row)
        self.session.commit()

if __name__ == "__main__" :
    test = Dao("test_db")
    test.add_row(
        {
            "current_player": 1,
            "player1_coord": 5,
            "player2_coord": 9,
            "grid": "001020010",
            "grid_size": 3,
            "up": 10,
            "down": -2,
            "left": 4,
            "right": 7,
        }
    )
    test.add_row(
        {
            "current_player": 1,
            "player1_coord": 20,
            "player2_coord": 9,
            "grid": "001020010",
            "grid_size": 3,
            "up": 10,
            "down": -2,
            "left": 4,
            "right": 7,
        }
    )

    print(
        test.select_row_by_dto(
            {
                "current_player": 1,
                "player1_coord": 20,
                "player2_coord": 9,
                "grid": "001020010",
                "grid_size": 3,
                "up": 10,
                "down": -2,
                "left": 4,
                "right": 7,
            }
        )
    )
    test.update_row({"up": 5, "down": 5, "left": 5, "right": 5})
    print(
        test.select_row_by_dto(
            {
                "current_player": 1,
                "player1_coord": 20,
                "player2_coord": 9,
                "grid": "001020010",
                "grid_size": 3,
                "up": 10,
                "down": -2,
                "left": 4,
                "right": 7,
            }
        )
    )
    test.add_row(
        {
            "current_player": 1,
            "player1_coord": 5,
            "player2_coord": 9,
            "grid": "001020010",
            "grid_size": 3,
            "up": 10,
            "down": -2,
            "left": 4,
            "right": 7,
        }
    )

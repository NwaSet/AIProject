from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


class Dao:
    """
    class that permit to communicate between the game model and a db
    """

    def __init__(self, db_name: str = None) -> None:
        """
        initialize a dao

        Args :
        ai_name : name of the ai
        """

        self.engine = None
        self.session = None
        self.db_name = None
        self.current_row = None
        self.data_table = None

        if db_name:
            self.connect_player_db(db_name)

    def connect_player_db(self, db_name: str) -> None:
        """
        connect to the db if it existe, else create a new one
        """

        self.engine = create_engine(f"sqlite:///games/cubee/dao/{db_name}.db")
        self.engine.connect()

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        self.db_name = db_name
        self.init_column()

    def init_column(self) -> None:
        """
        init the table of the db
        """

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
            Column("id", Integer, primary_key=True, autoincrement=True),
        )

        metadata.create_all(self.engine)

    def add_row(self, dto_ai: dict) -> None:
        """
        add a row, only if it does not exist
        """

        existing = self.select_row_by_dto(dto_ai)

        if existing is not None:
            print("Row already exists, skip insert")
            return

        row = self.data_table.insert().values(**dto_ai)
        self.session.execute(row)
        self.session.commit()

    def select_row_by_dto(self, dto: dict) -> None:
        """
        return a dict (up = x, ...) of the row if it exist, else return None
        """

        row = select(self.data_table).where(
            self.data_table.c.current_player == dto["current_player"],
            self.data_table.c.player1_coord == dto["player1_coord"],
            self.data_table.c.player2_coord == dto["player2_coord"],
            self.data_table.c.grid == dto["grid"],
        )

        self.current_row = self.session.execute(row).fetchone()

        if self.current_row:
            return {
                "up": self.current_row.up,
                "down": self.current_row.down,
                "left": self.current_row.left,
                "right": self.current_row.right,
            }
        else:
            return None

    def update_row(self, state: dict, q_values: dict) -> None:
        """
        update the row matching the given state
        """

        row = (
            update(self.data_table)
            .where(
                self.data_table.c.current_player == state["current_player"],
                self.data_table.c.player1_coord == state["player1_coord"],
                self.data_table.c.player2_coord == state["player2_coord"],
                self.data_table.c.grid == state["grid"],
                self.data_table.c.grid_size == state["grid_size"],
            )
            .values(
                up=q_values["up"],
                down=q_values["down"],
                left=q_values["left"],
                right=q_values["right"],
            )
        )

        result = self.session.execute(row)
        self.session.commit()

        if result.rowcount == 0:
            print("x")


if __name__ == "__main__":
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


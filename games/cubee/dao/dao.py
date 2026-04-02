from sqlalchemy import *
from sqlalchemy.orm import sessionmaker


class Dao:
    """
    DAO used to communicate between the game model and the database.

    Optimizations:
    - in-memory cache for already seen states
    - update does not depend on a previous select
    - batched commits
    """

    def __init__(self, db_name: str = None, commit_every: int = 100) -> None:
        self.engine = None
        self.session = None
        self.db_name = None
        self.data_table = None

        self.cache: dict[tuple, dict[str, float]] = {}
        self.commit_every = commit_every
        self.pending_writes = 0

        if db_name:
            self.connect_player_db(db_name)

    def connect_player_db(self, db_name: str) -> None:
        """
        Connect to the database if it exists, else create a new one.
        """

        self.engine = create_engine(f"sqlite:///games/cubee/dao/{db_name}.db")
        self.engine.connect()

        Session = sessionmaker(bind=self.engine, autoflush=False, autocommit=False)
        self.session = Session()

        self.db_name = db_name
        self.init_column()

    def init_column(self) -> None:
        """
        Initialize the table in the database.
        """

        metadata = MetaData()

        self.data_table = Table(
            "data",
            metadata,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("current_player", Integer, nullable=False),
            Column("player1_coord", Integer, nullable=False),
            Column("player2_coord", Integer, nullable=False),
            Column("grid", String, nullable=False),
            Column("grid_size", Integer, nullable=False),
            Column("up", Float, nullable=False),
            Column("down", Float, nullable=False),
            Column("left", Float, nullable=False),
            Column("right", Float, nullable=False),
        )

        metadata.create_all(self.engine)

    def _state_key(self, dto: dict) -> tuple:
        """
        Build a stable key for a state.
        """

        return (
            dto["current_player"],
            dto["player1_coord"],
            dto["player2_coord"],
            dto["grid"],
            dto["grid_size"],
        )

    def _extract_q_values(self, row) -> dict[str, float]:
        """
        Extract Q-values from a SQLAlchemy row.
        """

        return {
            "up": row.up,
            "down": row.down,
            "left": row.left,
            "right": row.right,
        }

    def _register_write(self) -> None:
        """
        Count writes and commit in batches.
        """

        self.pending_writes += 1

        if self.pending_writes >= self.commit_every:
            self.session.commit()
            self.pending_writes = 0

    def flush(self) -> None:
        """
        Force commit pending writes.
        Call this at the end of training.
        """

        if self.session is not None and self.pending_writes > 0:
            self.session.commit()
            self.pending_writes = 0

    def close(self) -> None:
        """
        Flush pending writes and close the session.
        """

        if self.session is not None:
            self.flush()
            self.session.close()
            self.session = None

    def select_row_by_dto(self, dto: dict) -> dict | None:
        """
        Return Q-values of the row if it exists, else return None.
        Cache is checked first.
        """

        key = self._state_key(dto)

        if key in self.cache:
            return self.cache[key].copy()

        row = select(self.data_table).where(
            self.data_table.c.current_player == dto["current_player"],
            self.data_table.c.player1_coord == dto["player1_coord"],
            self.data_table.c.player2_coord == dto["player2_coord"],
            self.data_table.c.grid == dto["grid"],
            self.data_table.c.grid_size == dto["grid_size"],
        )

        result = self.session.execute(row).fetchone()

        if result is None:
            return None

        q_values = self._extract_q_values(result)
        self.cache[key] = q_values.copy()
        return q_values.copy()

    def add_row(self, dto_ai: dict) -> None:
        """
        Add a row only if it does not already exist.
        """

        key = self._state_key(dto_ai)

        if key in self.cache:
            return

        existing = self.select_row_by_dto(dto_ai)
        if existing is not None:
            return

        row = self.data_table.insert().values(**dto_ai)
        self.session.execute(row)

        self.cache[key] = {
            "up": dto_ai["up"],
            "down": dto_ai["down"],
            "left": dto_ai["left"],
            "right": dto_ai["right"],
        }

        self._register_write()

    def update_row(self, state: dict, q_values: dict) -> None:
        """
        Update the row matching the given state.
        Does not require a previous select.
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

        self.session.execute(row)

        self.cache[self._state_key(state)] = {
            "up": q_values["up"],
            "down": q_values["down"],
            "left": q_values["left"],
            "right": q_values["right"],
        }

        self._register_write()
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    Float,
    String,
    UniqueConstraint,
    select,
    update,
    event,
)
from sqlalchemy.orm import sessionmaker


class Dao:
    """
    DAO used to store Q-values with staged writes to reduce DB access.
    """

    def __init__(self, db_name: str = None) -> None:
        """
        Initialize the DAO and connect to the database if a name is given.
        """
        self.engine = None
        self.session = None
        self.db_name = None
        self.data_table = None

        self.pending_inserts = {} # insert en attente
        self.pending_updates = {} # update en attente -> pas trouvé mieux ? 

        if db_name:
            self.connect_player_db(db_name)

    def connect_player_db(self, db_name: str) -> None:
        """
        Connect to the SQLite DB and initialize the table.
        """
        self.engine = create_engine(
            f"sqlite:///games/cubee/dao/{db_name}.db",
            future=True,
        )

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(
            dbapi_connection: object,
            connection_record: object,
        ) -> None:
            """
            Apply SQLite pragmas for faster staged writes.
            """
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.execute("PRAGMA temp_store=MEMORY;")
            cursor.close()

        Session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            future=True,
        )

        self.session = Session()
        self.db_name = db_name
        self.init_column()

    def init_column(self) -> None:
        """
        Create the table if it does not exist.
        """
        metadata = MetaData()

        self.data_table = Table(
            "data",
            metadata,
            Column("current_player", Integer, nullable=False),
            Column("player1_coord", Integer, nullable=False),
            Column("player2_coord", Integer, nullable=False),
            Column("grid", String, nullable=False),
            Column("grid_size", Integer, nullable=False),
            Column("up", Float, nullable=False),
            Column("down", Float, nullable=False),
            Column("left", Float, nullable=False),
            Column("right", Float, nullable=False),
            Column("id", Integer, primary_key=True, autoincrement=True),
            UniqueConstraint(
                "current_player",
                "player1_coord",
                "player2_coord",
                "grid",
                "grid_size",
                name="uq_state",
            ),
        )

        metadata.create_all(self.engine)

    def state_key(self, dto: dict) -> tuple:
        """
        Immutable key for one state.
        """
        return (
            dto["current_player"],
            dto["player1_coord"],
            dto["player2_coord"],
            dto["grid"],
            dto["grid_size"],
        )

    def select_row_by_dto(self, dto: dict) -> dict | None:
        """
        Return Q-values if the row exists, else None.

        Checks pending updates/inserts first to avoid unnecessary DB reads.
        """
        key = self.state_key(dto)

        if key in self.pending_updates:
            data = self.pending_updates[key]
            return {
                "up": data["up"],
                "down": data["down"],
                "left": data["left"],
                "right": data["right"],
            }

        if key in self.pending_inserts:
            data = self.pending_inserts[key]
            return {
                "up": data["up"],
                "down": data["down"],
                "left": data["left"],
                "right": data["right"],
            }

        stmt = (
            select(
                self.data_table.c.up,
                self.data_table.c.down,
                self.data_table.c.left,
                self.data_table.c.right,
            )
            .where(
                self.data_table.c.current_player == dto["current_player"],
                self.data_table.c.player1_coord == dto["player1_coord"],
                self.data_table.c.player2_coord == dto["player2_coord"],
                self.data_table.c.grid == dto["grid"],
                self.data_table.c.grid_size == dto["grid_size"],
            )
        )

        row = self.session.execute(stmt).fetchone()

        if row is None:
            return None

        return {
            "up": row.up,
            "down": row.down,
            "left": row.left,
            "right": row.right,
        }

    def stage_insert_if_missing(self, dto_ai: dict) -> None:
        """
        Stage an insert only if the state does not already exist.
        """
        key = self.state_key(dto_ai)

        if key in self.pending_inserts or key in self.pending_updates:
            return

        if self.select_row_by_dto(dto_ai) is None:
            self.pending_inserts[key] = dto_ai.copy()

    def stage_q_update(self, state: dict, q_values: dict) -> None:
        """
        Stage Q-values update without immediate commit.
        """
        key = self.state_key(state)

        data = {
            "current_player": state["current_player"],
            "player1_coord": state["player1_coord"],
            "player2_coord": state["player2_coord"],
            "grid": state["grid"],
            "grid_size": state["grid_size"],
            "up": q_values["up"],
            "down": q_values["down"],
            "left": q_values["left"],
            "right": q_values["right"],
        }

        if key in self.pending_inserts:
            self.pending_inserts[key] = data
        else:
            self.pending_updates[key] = data

    def flush(self) -> None:
        """
        Write all pending inserts/updates in batch.
        """
        if not self.pending_inserts and not self.pending_updates:
            return

        try:
            if self.pending_inserts:
                self.session.execute(
                    self.data_table.insert(),
                    list(self.pending_inserts.values()),
                )

            for data in self.pending_updates.values():
                stmt = (
                    update(self.data_table)
                    .where(
                        self.data_table.c.current_player == data["current_player"],
                        self.data_table.c.player1_coord == data["player1_coord"],
                        self.data_table.c.player2_coord == data["player2_coord"],
                        self.data_table.c.grid == data["grid"],
                        self.data_table.c.grid_size == data["grid_size"],
                    )
                    .values(
                        up=data["up"],
                        down=data["down"],
                        left=data["left"],
                        right=data["right"],
                    )
                )
                self.session.execute(stmt)

            self.session.commit()
            self.pending_inserts.clear()
            self.pending_updates.clear()

        except Exception:
            self.session.rollback()
            raise

    def close(self) -> None:
        """
        Flush and close session.
        """
        self.flush()
        self.session.close()

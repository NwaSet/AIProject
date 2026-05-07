from sqlalchemy import (
    Column,
    Float,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
    create_engine,
    event,
    select,
    update,
)
from sqlalchemy.orm import sessionmaker


class Dao:
    """
    DAO used to store PixelKart Q-values with staged writes.
    """

    ACTION_COLUMNS = (
        "pass_turn",
        "turn_left",
        "turn_right",
        "accelerate",
        "decelerate",
    )

    STATE_COLUMNS = (
        "coord_row",
        "coord_col",
        "direction",
        "speed",
        "front_1",
        "front_2",
        "front_3",
        "left_1",
        "left_2",
        "left_3",
        "right_1",
        "right_2",
        "right_3",
        "back_1",
    )

    def __init__(self, db_name: str | None = None) -> None:
        self.engine = None
        self.session = None
        self.db_name = None
        self.data_table = None

        self.pending_inserts = {}
        self.pending_updates = {}

        if db_name:
            self.connect_player_db(db_name)

    def connect_player_db(self, db_name: str) -> None:
        """
        Connect to the SQLite DB and initialize the table.
        """
        self.engine = create_engine(
            f"sqlite:///games/pixelkart/dao/ai_db/{db_name}.db",
            future=True,
        )

        @event.listens_for(self.engine, "connect")
        def set_sqlite_pragma(
            dbapi_connection: object,
            connection_record: object,
        ) -> None:
            cursor = dbapi_connection.cursor()
            cursor.execute("PRAGMA journal_mode=WAL;")
            cursor.execute("PRAGMA synchronous=NORMAL;")
            cursor.execute("PRAGMA temp_store=MEMORY;")
            cursor.close()

        session = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
            future=True,
        )

        self.session = session()
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
            Column("coord_row", Integer, nullable=False),
            Column("coord_col", Integer, nullable=False),
            Column("direction", String, nullable=False),
            Column("speed", Integer, nullable=False),
            Column("front_1", String, nullable=False),
            Column("front_2", String, nullable=False),
            Column("front_3", String, nullable=False),
            Column("left_1", String, nullable=False),
            Column("left_2", String, nullable=False),
            Column("left_3", String, nullable=False),
            Column("right_1", String, nullable=False),
            Column("right_2", String, nullable=False),
            Column("right_3", String, nullable=False),
            Column("back_1", String, nullable=False),
            Column("pass_turn", Float, nullable=False),
            Column("turn_left", Float, nullable=False),
            Column("turn_right", Float, nullable=False),
            Column("accelerate", Float, nullable=False),
            Column("decelerate", Float, nullable=False),
            Column("id", Integer, primary_key=True, autoincrement=True),
            UniqueConstraint(*self.STATE_COLUMNS, name="uq_state"),
        )

        metadata.create_all(self.engine)

    def state_to_row(self, state: tuple) -> dict:
        """
        Convert one PixelKart state tuple into DB row fields.
        """
        coord, direction, speed, *cells = state
        row, col = coord

        return {
            "coord_row": row,
            "coord_col": col,
            "direction": direction,
            "speed": speed,
            "front_1": cells[0],
            "front_2": cells[1],
            "front_3": cells[2],
            "left_1": cells[3],
            "left_2": cells[4],
            "left_3": cells[5],
            "right_1": cells[6],
            "right_2": cells[7],
            "right_3": cells[8],
            "back_1": cells[9],
        }

    def state_key(self, state: tuple) -> tuple:
        """
        Immutable key for one state.
        """
        row = self.state_to_row(state)
        return tuple(row[column] for column in self.STATE_COLUMNS)

    def select_row_by_state(self, state: tuple) -> dict | None:
        """
        Return Q-values if the row exists, else None.
        """
        key = self.state_key(state)

        if key in self.pending_updates:
            data = self.pending_updates[key]
            return {column: data[column] for column in self.ACTION_COLUMNS}

        if key in self.pending_inserts:
            data = self.pending_inserts[key]
            return {column: data[column] for column in self.ACTION_COLUMNS}

        row = self.state_to_row(state)

        stmt = (
            select(*(getattr(self.data_table.c, column) for column in self.ACTION_COLUMNS))
            .where(
                self.data_table.c.coord_row == row["coord_row"],
                self.data_table.c.coord_col == row["coord_col"],
                self.data_table.c.direction == row["direction"],
                self.data_table.c.speed == row["speed"],
                self.data_table.c.front_1 == row["front_1"],
                self.data_table.c.front_2 == row["front_2"],
                self.data_table.c.front_3 == row["front_3"],
                self.data_table.c.left_1 == row["left_1"],
                self.data_table.c.left_2 == row["left_2"],
                self.data_table.c.left_3 == row["left_3"],
                self.data_table.c.right_1 == row["right_1"],
                self.data_table.c.right_2 == row["right_2"],
                self.data_table.c.right_3 == row["right_3"],
                self.data_table.c.back_1 == row["back_1"],
            )
        )

        result = self.session.execute(stmt).fetchone()

        if result is None:
            return None

        return {column: getattr(result, column) for column in self.ACTION_COLUMNS}

    def stage_insert_if_missing(self, state: tuple, q_values: dict) -> None:
        """
        Stage an insert only if the state does not already exist.
        """
        key = self.state_key(state)

        if key in self.pending_inserts or key in self.pending_updates:
            return

        if self.select_row_by_state(state) is not None:
            return

        data = self.state_to_row(state)
        for column in self.ACTION_COLUMNS:
            data[column] = q_values[column]

        self.pending_inserts[key] = data

    def stage_q_update(self, state: tuple, q_values: dict) -> None:
        """
        Stage Q-values update without immediate commit.
        """
        key = self.state_key(state)
        data = self.state_to_row(state)

        for column in self.ACTION_COLUMNS:
            data[column] = q_values[column]

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
                        self.data_table.c.coord_row == data["coord_row"],
                        self.data_table.c.coord_col == data["coord_col"],
                        self.data_table.c.direction == data["direction"],
                        self.data_table.c.speed == data["speed"],
                        self.data_table.c.front_1 == data["front_1"],
                        self.data_table.c.front_2 == data["front_2"],
                        self.data_table.c.front_3 == data["front_3"],
                        self.data_table.c.left_1 == data["left_1"],
                        self.data_table.c.left_2 == data["left_2"],
                        self.data_table.c.left_3 == data["left_3"],
                        self.data_table.c.right_1 == data["right_1"],
                        self.data_table.c.right_2 == data["right_2"],
                        self.data_table.c.right_3 == data["right_3"],
                        self.data_table.c.back_1 == data["back_1"],
                    )
                    .values({column: data[column] for column in self.ACTION_COLUMNS})
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

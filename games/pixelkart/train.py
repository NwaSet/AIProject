from multiprocessing import Pool, freeze_support
import os
import csv
import psutil
import traceback
import sys

# err when launch with python -m ...
# solution by chatgpt 
if __package__ in (None, ""):
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.append(project_root)
    from games.pixelkart.model.ai import Ai
    from games.pixelkart.model.circuit import Circuit
    from games.pixelkart.model.race import Race
else:
    from .model.ai import Ai
    from .model.circuit import Circuit
    from .model.race import Race

train_games = 1_000_000
test_games = 10_000
checkpoint_step = 100_000
epsilon_step = 5000
epsilon_decay = 0.95
min_epsilon = 0.05
circuit_name = "Large"
nb_laps = 1

params = [
    (0.01, 0.40),
    (0.01, 0.50),
    (0.01, 0.60),

    (0.03, 0.45),
    (0.03, 0.55),
    (0.03, 0.65),

    (0.05, 0.45),
    (0.05, 0.55),
    (0.05, 0.65),

    (0.07, 0.45),
    (0.07, 0.55),
    (0.07, 0.65),

    (0.10, 0.50),
    (0.10, 0.60),
]

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
counter_file = os.path.join(data_path, "last.txt")


def train_ai() -> None:
    """
    Train one AI pair for each parameter set, testing every checkpoint.
    """
    print("train_ai start")
    os.makedirs(data_path, exist_ok=True)

    nb_cores = psutil.cpu_count(logical=True)
    nb_processes = min(len(params), nb_cores if nb_cores is not None else len(params))

    for trained_games in range(0, train_games, checkpoint_step):
        next_checkpoint = min(trained_games + checkpoint_step, train_games)
        chunk_games = next_checkpoint - trained_games
        args = []

        for i, (initial_lr, gamma) in enumerate(params):
            args.append(
                (
                    i,
                    chunk_games,
                    trained_games,
                    initial_lr,
                    gamma,
                    epsilon_at(trained_games),
                    epsilon_step,
                )
            )

        print(f"train checkpoint {trained_games} -> {next_checkpoint}")
        with Pool(processes=nb_processes) as pool:
            pool.map(train_worker, args)

        print(f"test checkpoint {next_checkpoint}")
        test_ai(next_checkpoint)

    print("train_ai end")


def train_worker(args: tuple[int, int, int, float, float, float, int]) -> None:
    """
    Train one worker with its own learning parameters.
    """
    (
        core_id,
        nb_game,
        trained_games_start,
        initial_lr,
        gamma,
        epsilon,
        step,
    ) = args

    try:
        print(
            f"worker start core={core_id} "
            f"learning_rate={initial_lr} "
            f"gamma={gamma} epsilon={epsilon}"
        )
        train(
            nb_game,
            trained_games_start,
            initial_lr,
            gamma,
            epsilon,
            step,
        )
        print(
            f"worker end core={core_id} "
            f"learning_rate={initial_lr} gamma={gamma}"
        )

    except Exception as e:
        print("erreur dans train_worker :", e)
        traceback.print_exc()
        raise


def epsilon_at(trained_games: int) -> float:
    """
    Return the epsilon value after the already trained game count.
    """
    nb_decay = trained_games // epsilon_step
    return max(min_epsilon, epsilon_decay ** nb_decay)


def db_name_for(initial_lr: float, gamma: float) -> str:
    """
    Stable database name for a parameter set.
    """
    return f"lr{initial_lr}_g{gamma}"


def build_race(bot1: Ai, bot2: Ai) -> Race:
    """
    Build a fresh PixelKart race for one training or test episode.
    """
    return Race(Circuit(circuit_name), nb_laps, False, bot1, bot2)


def train(
    nb_game: int,
    trained_games_start: int,
    learning_rate: float,
    gamma: float,
    epsilon: float,
    nb_espilone: int,
) -> None:
    """
    Train two PixelKart AIs against each other.
    """
    bot1 = Ai(
        1,
        f"b1_{learning_rate}_{gamma}",
        epsilon=epsilon,
        lr=learning_rate,
        gamma=gamma,
        db_name=db_name_for(learning_rate, gamma),
    )
    bot2 = Ai(
        2,
        f"b2_{learning_rate}_{gamma}",
        epsilon=epsilon,
        lr=learning_rate,
        gamma=gamma,
        db_name=db_name_for(learning_rate, gamma),
    )

    for i in range(nb_game):
        if i % nb_espilone == 0 and i != 0:
            bot1.next_epsilon(epsilon_decay, min_epsilon)
            bot2.next_epsilon(epsilon_decay, min_epsilon)
            print(i)

        game = build_race(bot1, bot2)
        game.play()

    bot1.force_commit()
    bot2.force_commit()


def test_ai(checkpoint_games: int | None = None) -> None:
    """
    Test all trained parameter sets against each other.
    """
    print("test_ai start")
    os.makedirs(data_path, exist_ok=True)

    n = len(params)
    matrix = [["X" for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            print(f"eval {i} vs {j}")

            lr1, gamma1 = params[i]
            lr2, gamma2 = params[j]
            bot1 = Ai(
                1,
                f"b1_{lr1}_{gamma1}",
                epsilon=0,
                lr=lr1,
                gamma=gamma1,
                learning_enabled=False,
                db_name=db_name_for(lr1, gamma1),
            )
            bot2 = Ai(
                2,
                f"b2_{lr2}_{gamma2}",
                epsilon=0,
                lr=lr2,
                gamma=gamma2,
                learning_enabled=False,
                db_name=db_name_for(lr2, gamma2),
            )

            for _ in range(test_games):
                game = build_race(bot1, bot2)
                game.play()

            matrix[i][j] = bot1.nb_win / test_games
            matrix[j][i] = bot2.nb_win / test_games
            print(
                "bot1 --> tie :",
                bot1.nb_tie,
                " | win :",
                bot1.nb_win,
                " | lose :",
                bot1.nb_lose,
            )
            print(
                "bot2 --> tie :",
                bot2.nb_tie,
                " | win :",
                bot2.nb_win,
                " | lose :",
                bot2.nb_lose,
            )

    save_matrix(matrix, checkpoint_games)
    print("test_ai end")


def save_matrix(matrix: list[list[object]], checkpoint_games: int | None = None) -> None:
    """
    Save the comparison matrix to a CSV file.
    """
    if not os.path.exists(counter_file):
        current = 1
    else:
        with open(counter_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            current = int(content) + 1 if content else 1

    if checkpoint_games is None:
        csv_name = f"data_{current}.csv"
    else:
        csv_name = f"data_{current}_{checkpoint_games}.csv"

    csv_path = os.path.join(data_path, csv_name)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        header = [""]
        for i, (lr, gamma) in enumerate(params):
            header.append(f"bot_{i} ({lr} - {gamma})")
        writer.writerow(header)

        for i, row in enumerate(matrix):
            lr, gamma = params[i]
            writer.writerow([f"bot_{i} ({lr} - {gamma})"] + row)

    with open(counter_file, "w", encoding="utf-8") as f:
        f.write(str(current))

    print(f"csv cree : {csv_path}")


def test() -> None:
    """
    Run training with checkpoint tests.
    """
    train_ai()


if __name__ == "__main__":
    freeze_support()
    test()

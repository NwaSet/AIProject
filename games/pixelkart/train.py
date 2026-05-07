from multiprocessing import Pool, freeze_support
import os
import csv
import psutil
import traceback

from .model.ai import Ai
from .model.circuit import Circuit
from .model.race import Race

train_games = 1_000_000
test_games = 10_000
checkpoint_step = 100_000
epsilon_step = 5000
epsilon_decay = 0.95
min_epsilon = 0.05
min_learning_rate_ratio = 0.10
circuit_name = "Basic"
nb_laps = 1

params = [
    (0.01, 0.70),
    (0.01, 0.80),
    (0.01, 0.90),

    (0.03, 0.75),
    (0.03, 0.85),
    (0.03, 0.95),

    (0.05, 0.75),
    (0.05, 0.85),
    (0.05, 0.95),

    (0.10, 0.75),
    (0.10, 0.85),
    (0.10, 0.95),

    (0.15, 0.80),
    (0.20, 0.90),
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
                    learning_rate_at(initial_lr, trained_games),
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


def train_worker(args: tuple[int, int, int, float, float, float, float, int]) -> None:
    """
    Train one worker with its own learning parameters.
    """
    (
        core_id,
        nb_game,
        trained_games_start,
        initial_lr,
        current_lr,
        gamma,
        epsilon,
        step,
    ) = args

    try:
        print(
            f"worker start core={core_id} "
            f"initial_lr={initial_lr} current_lr={current_lr} "
            f"gamma={gamma} epsilon={epsilon}"
        )
        train(
            nb_game,
            trained_games_start,
            initial_lr,
            current_lr,
            gamma,
            epsilon,
            step,
        )
        print(
            f"worker end core={core_id} "
            f"initial_lr={initial_lr} current_lr={current_lr} gamma={gamma}"
        )

    except Exception as e:
        print("erreur dans train_worker :", e)
        traceback.print_exc()
        raise


def learning_rate_at(initial_lr: float, trained_games: int) -> float:
    """
    Linearly decay the learning rate from its initial value to 10%.
    """
    progress = min(trained_games / train_games, 1.0)
    min_lr = initial_lr * min_learning_rate_ratio
    return initial_lr - ((initial_lr - min_lr) * progress)


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
    initial_learning_rate: float,
    current_learning_rate: float,
    gamma: float,
    epsilon: float,
    nb_espilone: int,
) -> None:
    """
    Train two PixelKart AIs against each other.
    """
    bot1 = Ai(
        1,
        f"b1_{initial_learning_rate}_{gamma}",
        epsilon=epsilon,
        lr=current_learning_rate,
        gamma=gamma,
        db_name=db_name_for(initial_learning_rate, gamma),
    )
    bot2 = Ai(
        2,
        f"b2_{initial_learning_rate}_{gamma}",
        epsilon=epsilon,
        lr=current_learning_rate,
        gamma=gamma,
        db_name=db_name_for(initial_learning_rate, gamma),
    )

    for i in range(nb_game):
        if i % nb_espilone == 0 and i != 0:
            bot1.next_epsilon(epsilon_decay, min_epsilon)
            bot2.next_epsilon(epsilon_decay, min_epsilon)
            current_learning_rate = learning_rate_at(
                initial_learning_rate,
                trained_games_start + i,
            )
            bot1.learning_rate = current_learning_rate
            bot2.learning_rate = current_learning_rate
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
            trained_games = checkpoint_games or train_games

            bot1 = Ai(
                1,
                f"b1_{lr1}_{gamma1}",
                epsilon=0,
                lr=learning_rate_at(lr1, trained_games),
                gamma=gamma1,
                learning_enabled=False,
                db_name=db_name_for(lr1, gamma1),
            )
            bot2 = Ai(
                2,
                f"b2_{lr2}_{gamma2}",
                epsilon=0,
                lr=learning_rate_at(lr2, trained_games),
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
            header.append(f"bot_{i} ({lr}, {gamma})")
        writer.writerow(header)

        for i, row in enumerate(matrix):
            lr, gamma = params[i]
            writer.writerow([f"bot_{i} ({lr}, {gamma})"] + row)

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

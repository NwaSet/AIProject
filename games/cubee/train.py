from multiprocessing import Pool, freeze_support
import os
import csv
import psutil
import traceback

from .model.ai import Ia
from .model.cubee_model import GameModel

train_games = 100_000
test_games = 1_000
epsilon_step = 5000
grid_size = 5

params = [
    (0.05, 0.80),
    (0.05, 0.90),
    (0.10, 0.80),
    (0.10, 0.90),
    (0.15, 0.85),
    (0.15, 0.95),
    (0.20, 0.80),
    (0.20, 0.90),
    (0.25, 0.85),
    (0.25, 0.95),
    (0.30, 0.80),
    (0.30, 0.90),
    (0.35, 0.85),
    (0.35, 0.95),
]

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, "data")
counter_file = os.path.join(data_path, "last.txt")


def train_ai():
    print("train_ai start")
    os.makedirs(data_path, exist_ok=True)

    args = []
    nb_cores = psutil.cpu_count(logical=True)
    nb_processes = min(len(params), nb_cores if nb_cores is not None else len(params))

    for i, (lr, gamma) in enumerate(params):
        args.append((i, train_games, lr, gamma, epsilon_step))

    print("avant pool.map")
    with Pool(processes=nb_processes) as pool:
        pool.map(_train_worker, args)
    print("après pool.map")


def _train_worker(args):
    core_id, nb_game, lr, gamma, step = args

    try:
        print(f"worker start core={core_id} lr={lr} gamma={gamma}")
        train(nb_game, lr, gamma, step)
        print(f"worker end core={core_id} lr={lr} gamma={gamma}")

    except Exception as e:
        print("erreur dans _train_worker :", e)
        traceback.print_exc()
        raise


def train(nb_game, learning_rate, gamma, nb_espilone):
    bot1 = Ia(
        1, f"b1_{learning_rate}_{gamma}", epsilon=1, lr=learning_rate, gamma=gamma
    )
    bot2 = Ia(
        2, f"b2_{learning_rate}_{gamma}", epsilon=1, lr=learning_rate, gamma=gamma
    )

    game = GameModel(grid_size, False, bot1, bot2)

    for i in range(nb_game):
        if i % nb_espilone == 0 and i != 0:
            bot1.next_epsilon()
            bot2.next_epsilon()
            print(i)

        game.play()
        game.reset()

    bot1.force_commit()
    bot2.force_commit()


def test_ai():
    print("test_ai start")
    os.makedirs(data_path, exist_ok=True)

    n = len(params)
    matrix = [["X" for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            print(f"eval {i} vs {j}")

            lr1, gamma1 = params[i]
            lr2, gamma2 = params[j]

            bot1 = Ia(1, f"b1_{lr1}_{gamma1}", epsilon=0, lr=lr1, gamma=gamma1)
            bot2 = Ia(2, f"b2_{lr2}_{gamma2}", epsilon=0, lr=lr2, gamma=gamma2)

            for _ in range(test_games):
                game = GameModel(grid_size, False, bot1, bot2)
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

    save_matrix(matrix)
    print("test_ai end")


def save_matrix(matrix):
    if not os.path.exists(counter_file):
        current = 1
    else:
        with open(counter_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            current = int(content) + 1 if content else 1

    csv_path = os.path.join(data_path, f"data_{current}.csv")

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

    print(f"csv créé : {csv_path}")


def test():
    train_ai()
    test_ai()


if __name__ == "__main__":
    freeze_support()
    test()

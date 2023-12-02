from multiprocessing import Process

from leaderboard.seeds import run as run_leaderboard_seed
from reward.seeds import run as run_reward_seed
from metadata.seeds import run as run_metadata_seed


def run():
    processes = [
        Process(target=run_reward_seed),
        Process(target=run_leaderboard_seed),
        Process(target=run_metadata_seed),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

from multiprocessing import Process

import reward.seed as reward
import metadata.seed as metadata
import leaderboard.seed as leaderboard


def run():
    processes = [
        Process(target=reward.up),
        Process(target=metadata.up),
        Process(target=leaderboard.up),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

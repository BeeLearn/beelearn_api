from multiprocessing import Process

import reward.seed as reward
import payment.seed as payment
import metadata.seed as metadata
import catalogue.seed as catalogue
import messaging.seed as messaging
import leaderboard.seed as leaderboard


def run():
    processes = [
        Process(target=payment.down),
        Process(target=reward.down),
        Process(target=metadata.down),
        Process(target=catalogue.down),
        Process(target=messaging.down),
        Process(target=leaderboard.down),
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()

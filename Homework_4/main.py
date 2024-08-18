import asyncio
from random import randint


class Fork:

    def __init__(self, idx):
        self.idx = idx
        self.lock = asyncio.Lock()

    async def take(self, philosopher_idx):
        await self.lock.acquire()
        print(f'Philosopher #{philosopher_idx} picked up the fork {self.idx}.')

    def put_down(self, philosopher_idx):
        self.lock.release()
        print(f'Philosopher #{philosopher_idx} put down the fork {self.idx}.')


class Philosopher:

    def __init__(self, idx, left_fork, right_fork):
        self.idx = idx
        self.left_fork = left_fork
        self.right_fork = right_fork

    @property
    def is_odd(self):
        return self.idx % 2 == 1

    async def think(self):
        think_time = randint(1, 5)
        print(f'Philosopher #{self.idx} - Thinking....{think_time} seconds')
        await asyncio.sleep(think_time)

    async def eat(self):
        eat_time = randint(1, 5)
        print(f'Philosopher #{self.idx} - Eating....{eat_time} seconds')
        await asyncio.sleep(eat_time)


    async def dine(self):
        while True:
            await self.think()

            if self.is_odd:
                await self.left_fork.take(self.idx)
                await self.right_fork.take(self.idx)
            else:
                await self.right_fork.take(self.idx)
                await self.left_fork.take(self.idx)

            await self.eat()

            self.left_fork.put_down(self.idx)
            self.right_fork.put_down(self.idx)

def assign_right_fork_idx(idx, n):
    return (idx + 1) % n


async def main():
    forks = [Fork(i) for i in range(5)]

    philosophers = []

    for idx in range(5):
        left_fork = forks[idx]
        right_fork = forks[assign_right_fork_idx(idx, 5)]
        philosophers.append(Philosopher(idx, left_fork, right_fork))

    await asyncio.gather(*[philosopher.dine() for philosopher in philosophers])


asyncio.run(main())

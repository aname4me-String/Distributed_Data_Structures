from celery import Celery

app = Celery('tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0')

@app.task
def find_primes_task(start, end):
    return [n for n in range(start, end)
            if n >= 2 and all(n % i != 0
               for i in range(2, int(n**0.5) + 1))]
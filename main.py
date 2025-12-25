import time

from application_logs import generate

while True:
    time.sleep(1)
    print(generate())
import a0
import time

p = a0.Publisher("topic")
for i in range(10):
    payload = f"here (ts={i})"
    print(f"publishing: {payload}")
    p.pub(payload)
    time.sleep(1)

print("Done!")

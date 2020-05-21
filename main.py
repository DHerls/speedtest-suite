from providers.xfinity import Xfinity
from providers.mlab import MLabNDT
from providers.fast import Fast

def run():
    down, up, latency = Fast().run_test()
    print(f'Down: {down}Mbps\tUp: {up}Mbps\tLatency: {latency}ms')

if __name__ == "__main__":
    run()
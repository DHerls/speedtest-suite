from common import SpeedTest
import os
import subprocess
import json

class OoklaBinary(SpeedTest):

    def __init__(self):
        super().__init__()
        bin_directory = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), "bin")
        self.binary_path = os.path.join(bin_directory, "ookla")
        if os.path.isfile(self.binary_path):
            return
        self.binary_path += ".exe"
        if os.path.isfile(self.binary_path):
            return
        raise Exception("Cannot find ookala binary in bin/")
        

    def run_test(self):
        response = subprocess.run([self.binary_path, "-f", "json", "-p", "no"], capture_output=True)
        if response.returncode != 0:
            raise Exception()
        data = json.loads(response.stdout)
        down = data['download']['bandwidth'] * 8 / 1e6
        up = data['upload']['bandwidth'] * 8 / 1e6
        latency = data['ping']['latency']
        return (down, up, latency)

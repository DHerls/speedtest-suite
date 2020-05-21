from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

class SpeedTest():

    label = "not_implemented"

    def run_test(self):
        return (-1, -1, -1)


class BrowserSpeedTest(SpeedTest):

    def __init__(self):
        super().__init__()
        opts = Options()
        opts.headless = True
        self.browser = Firefox(options=opts)


class TestTimeoutException(BaseException):

    def __init__(self, test, timeout, context=None):
        super().__init__(self)
        self.test = test
        self.timeout = timeout
        self.context = context

        if context is None:
            self.msg = 'Test "{}" timed out after {} seconds'.format(test, timeout)
        else:
            self.msg = 'Test "{}" timed out while {} after {} seconds'.format(test, context, timeout)
    
    def __str__(self):
        return self.msg


def convert_to_mbps(speed: float, unit: str) -> float:
    """Return speed in megabits per second by converting from other units.
    
    Currently supported: kbps

    :param speed: Speed in the given unit
    :param unit: String representation of the current unit
    """
    unit = unit.strip().lower()
    if unit in ["mbps", "mb/s"]:
        return speed
    
    if unit in ["kbps", "kb/s"]:
        return speed / 1000
    
    raise Exception('Units "{}" not supported'.format(unit))


def convert_to_ms(latency: float, unit: str) -> float:
    """Return latency in milliseconds by converting from other units."""
    unit = unit.strip().lower()
    if unit == "ms":
        return latency
    if unit == "s":
        return latency * 1000
    
    raise Exception('Units "{}" not supported'.format(unit))
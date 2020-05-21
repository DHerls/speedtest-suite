from common import BrowserSpeedTest, TestTimeoutException, convert_to_mbps, convert_to_ms
import time
from selenium.common.exceptions import NoSuchElementException

class Fast(BrowserSpeedTest):

    label = "fast.com"
    max_timeout = 30
    
    def run_test(self):
        self.browser.get("https://fast.com")
        start = time.time()
        while time.time() - start < self.max_timeout:
            try:
                self.browser.find_element_by_css_selector("#speed-value.succeeded")
                break
            except NoSuchElementException:
                time.sleep(1)
        else:
            raise TestTimeoutException(self.label, self.max_timeout, "downloading")
        down_speed = float(self.browser.find_element_by_css_selector("#speed-value.succeeded").text)
        down_units = self.browser.find_element_by_css_selector("#speed-units.succeeded").text
        down = convert_to_mbps(down_speed, down_units)

        self.browser.find_element_by_id("show-more-details-link").click()
        start = time.time()
        while time.time() - start < self.max_timeout:
            try:
                self.browser.find_element_by_css_selector("#upload-value.succeeded")
                break
            except NoSuchElementException:
                time.sleep(1)
        else:
            raise TestTimeoutException(self.label, self.max_timeout, "uploading")
        up_speed = float(self.browser.find_element_by_css_selector("#upload-value.succeeded").text)
        up_units = self.browser.find_element_by_css_selector("#upload-units.succeeded").text
        up = convert_to_mbps(up_speed, up_units)

        latency_value = float(self.browser.find_element_by_id('latency-value').text)
        latency_units = self.browser.find_element_by_id('latency-units').text
        latency = convert_to_ms(latency_value, latency_units)

        return (down, up, latency)

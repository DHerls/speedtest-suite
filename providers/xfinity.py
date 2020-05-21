import time

from common import BrowserSpeedTest, TestTimeoutException, convert_to_mbps
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException


class Xfinity(BrowserSpeedTest):
    
    label = "xfinity"

    speedtest_url = "https://speedtest.xfinity.com/"
    max_timeout = 30

    def run_test(self):
        self.browser.get(self.speedtest_url)
        try:
            start_button = self.browser.find_element_by_xpath("//button[@class='btn btn--rounded btn--dark btn--primary']")
        except NoSuchElementException:
            raise Exception()
        
        counter = 0
        while counter < self.max_timeout:
            try:
                start_button.click()
                break
            except ElementClickInterceptedException:
                time.sleep(1)
                counter += 1
        else:
            raise TestTimeoutException(self.label, self.max_timeout, "loading")


        counter = 0
        results = None
        while counter < self.max_timeout:
            try:
                results = self.browser.find_element_by_xpath("//div[@data-bid='RESULTS']")
                break
            except NoSuchElementException:
                time.sleep(1)
                counter += 1
        else:
            raise TestTimeoutException(self.label, self.max_timeout, "downloading")
            
        # Text is in the format ##.##Mbps
        down_speed = float(results.find_element_by_css_selector("summary dd").text[:-4])
        down_units = results.find_element_by_css_selector("summary dd").text[-4:]
        down = convert_to_mbps(down_speed, down_units)

        self.browser.find_element_by_css_selector('summary p.pr-3.font-500.text-grey-12').click()

        finished = False
        counter = 0
        while counter < self.max_timeout:
            upload = results.find_element_by_css_selector('details dl div:nth-child(1) dd')
            if len(upload.find_elements_by_css_selector("*")) > 0:
                counter += 1
                time.sleep(1)
            else:
                break
        else:
            raise TestTimeoutException(self.label, self.max_timeout, "uploading")
        
        # Text is in the format ##.## Mbps (note the space here but not in the download results)
        up_speed = float(upload.text[:-5])
        up_units =upload.text[-4:]
        up = convert_to_mbps(up_speed, up_units)
        # Text is in the format ### ms
        latency = int(results.find_element_by_css_selector('details dl div:nth-child(2) dd').text[:-3])
        return (down, up, latency)

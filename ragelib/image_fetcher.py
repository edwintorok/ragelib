from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

class ImageFetcher():
    def __init__(self, data, geckodriver_path, logger):
        self.data = data
        self.logger = logger

        options = Options()
        options.add_argument('-headless')

        logger.info(f"Using {geckodriver_path} for geckodriver")
        serv = Service(geckodriver_path)
        self.driver = Firefox(service=serv, options=options)

    def get_graph_screenshot(self, url, driver):
        wait = WebDriverWait(driver, timeout=60)
        self.logger.debug(f"Begun fetching url {url}")
        driver.get(url)
        
        wait.until(expected.visibility_of_element_located((By.ID, 'graph_title')))
        self.logger.debug("Element #graph_title now visible, graph loading")
        
        alert = expected.alert_is_present()(driver)
        if alert:
            if "About to plot" in alert.text:
                alert.accept()
                self.logger.warn("Many points alert box accepted")
            else:
                alert.dismiss()
                self.logger.warn("Unexpected alert box dismissed")
            
        # On draw starting the progress_img element appears (spinner) and the graph title is unhidden. 
        # When done it disappears.
        wait.until(expected.invisibility_of_element_located((By.ID, 'progress_img')))
        self.logger.debug("Element #progress_img now invisible, graph loaded")

        canvas = driver.find_element(By.TAG_NAME, 'canvas')
        canvas_bytes = canvas.screenshot_as_base64

        return canvas_bytes

    def fetch_images(self):
        for item in tqdm(self.data, desc='Fetching graphs...'):
            try:
                item['graph_bytes'] = self.get_graph_screenshot(item['graph_link'], self.driver)
                item['graph_exception'] = None
            except TimeoutException:
                self.logger.warn("Failed while fetching image for link "+item['graph_link'])
                item['graph_exception'] = "TimeoutException"
                item['graph_bytes'] = None
            except Exception as e:
                self.logger.warn("Failed while fetching image for link "+item['graph_link'])
                print(e)
                item['graph_exception'] = str(e)
                item['graph_bytes'] = None

        self.driver.quit()
        return self.data

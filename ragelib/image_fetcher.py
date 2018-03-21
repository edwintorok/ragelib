from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
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
        self.driver = Firefox(executable_path=geckodriver_path, firefox_options=options)


    def get_graph_screenshot(self, url, driver):
        wait = WebDriverWait(driver, timeout=60)
        self.logger.debug(f"Begun fetching url {url}")
        driver.get(url)

        # On draw starting the progress_img element appears (spinner). When done it disappears.
        wait.until(expected.visibility_of_element_located((By.ID, 'progress_img')))
        self.logger.debug("Element #progress_img now visible, graph loading")
        wait.until(expected.invisibility_of_element_located((By.ID, 'progress_img')))
        self.logger.debug("Element #progress_img now invisible, graph loaded")

        canvas = driver.find_element_by_tag_name('canvas')
        canvas_bytes = canvas.screenshot_as_base64

        return canvas_bytes


    def fetch_images(self):
        for item in tqdm(self.data, desc='Fetching graphs...'):
            try:
                item['graph_bytes'] = self.get_graph_screenshot(item['graph_link'], self.driver)
            except Exception as e:
                self.logger.warn("Failed while fetching image for link "+item['graph_link'])
                print(e)
                item['graph_bytes'] = None

        self.driver.quit()
        return self.data
from selenium import webdriver

import os
class _Driver:
    def options(self):
        dir_path = os.getcwd()
        folder_cache='profile'
        profile = os.path.join(dir_path, folder_cache, 'profile')
        options = webdriver.ChromeOptions()
        options.add_argument(f'user-data-dir={profile}')
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        return options
    
    def open(self):
        import os
        return webdriver.Chrome(executable_path=os.getenv('driver'),options=self.options()) 


agent_driver = _Driver()


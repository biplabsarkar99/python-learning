my_file = (os.path.join(os.getcwd(), 'setup.cfg'))
config.read(my_file)

# Reading the browser type from the configuration file for Selenium test automation
helper_func = get_browser(config.get('Environment', 'Browser'))
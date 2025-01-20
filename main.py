import tls_client 
import random
import time
import toml
import ctypes
import threading
import string

from solver.solver import get_turnstile_token
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import wraps
from logmagix import Logger, Home

with open('input/config.toml') as f:
    config = toml.load(f)

DEBUG = config['dev'].get('Debug', False)
log = Logger()


def debug(func_or_message, *args, **kwargs) -> callable:
    if callable(func_or_message):
        @wraps(func_or_message)
        def wrapper(*args, **kwargs):
            result = func_or_message(*args, **kwargs)
            if DEBUG:
                log.debug(f"{func_or_message.__name__} returned: {result}")
            return result
        return wrapper
    else:
        if DEBUG:
            log.debug(f"Debug: {func_or_message}")

def debug_response(response) -> None:
    debug(response.headers)
    debug(response.text)
    debug(response.status_code)


class Miscellaneous:
    @debug
    def get_proxies(self) -> dict:
        try:
            if config['dev'].get('Proxyless', False):
                return None
                
            with open('input/proxies.txt') as f:
                proxies = [line.strip() for line in f if line.strip()]
                if not proxies:
                    log.warning("No proxies available. Running in proxyless mode.")
                    return None
                
                proxy_choice = random.choice(proxies)
                proxy_dict = {
                    "http": f"http://{proxy_choice}",
                    "https": f"http://{proxy_choice}"
                }
                log.debug(f"Using proxy: {proxy_choice}")
                return proxy_dict
        except FileNotFoundError:
            log.failure("Proxy file not found. Running in proxyless mode.")
            return None

    @debug 
    def generate_password(self):
        password = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/", k=16))
        return password
    
    @debug 
    def generate_username(self):
        return ''.join(random.choices(string.ascii_lowercase, k=16))
    
    @debug 
    def generate_email(self, domain: str = "hoppala.xyz"):
        username = f"{''.join(random.choices(string.ascii_lowercase + string.digits, k=20))}"
        email = f"{username}@{domain}"
        return email
    
    @debug 
    def randomize_user_agent(self) -> str:
        platforms = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 10.0; WOW64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_2_3",
            "X11; Linux x86_64",
            "X11; Linux i686",
            "X11; Ubuntu; Linux x86_64",
        ]
        
        browsers = [
            ("Chrome", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
            ("Firefox", f"{random.randint(80, 115)}.0"),
            ("Safari", f"{random.randint(13, 16)}.{random.randint(0, 3)}"),
            ("Edge", f"{random.randint(90, 140)}.0.{random.randint(1000, 4999)}.0"),
        ]
        
        webkit_version = f"{random.randint(500, 600)}.{random.randint(0, 99)}"
        platform = random.choice(platforms)
        browser_name, browser_version = random.choice(browsers)
        
        if browser_name == "Safari":
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"Version/{browser_version} Safari/{webkit_version}"
            )
        elif browser_name == "Firefox":
            user_agent = f"Mozilla/5.0 ({platform}; rv:{browser_version}) Gecko/20100101 Firefox/{browser_version}"
        else:
            user_agent = (
                f"Mozilla/5.0 ({platform}) AppleWebKit/{webkit_version} (KHTML, like Gecko) "
                f"{browser_name}/{browser_version} Safari/{webkit_version}"
            )
        
        return user_agent

    class Title:
        def __init__(self) -> None:
            self.running = False

        def start_title_updates(self, total, start_time) -> None:
            self.running = True
            def updater():
                while self.running:
                    self.update_title(total, start_time)
                    time.sleep(0.5)
            threading.Thread(target=updater, daemon=True).start()

        def stop_title_updates(self) -> None:
            self.running = False

        def update_title(self, total, start_time) -> None:
            try:
                elapsed_time = round(time.time() - start_time, 2)
                title = f'discord.cyberious.xyz | Total: {total} | Time Elapsed: {elapsed_time}s'

                sanitized_title = ''.join(c if c.isprintable() else '?' for c in title)
                ctypes.windll.kernel32.SetConsoleTitleW(sanitized_title)
            except Exception as e:
                log.debug(f"Failed to update console title: {e}")

class AccountCreator:
    def __init__(self, proxies: dict = None) -> None:
        self.session = tls_client.Session("chrome_131", random_tls_extension_order=True)
        self.session.headers = {'content-type': 'application/json'}
        self.session.proxies = proxies
    
    @debug
    def create_account(self, username: str, email: str, password: str):
        result = get_turnstile_token(
        url="https://zenix.vast.sh",
        sitekey="0x4AAAAAAA5uSgCPW0Bgjzmf",
        invisible=True,
        debug=DEBUG
    )
        json_data = {
            'username': username,
            'email': email,
            'password': password,
            "captchaResponse": result["turnstile_value"]
        }
        debug(json_data)
        response = self.session.post('https://zenix.vast.sh/api/auth/register', json=json_data)
        
        debug_response(response)

        if response.status_code == 201:
            return True
        else:
            log.failure(f"Failed to create account: {response.text}, {response.status_code}")

@debug
def create_account():
    try:
        account_start_time = time.time()

        Misc = Miscellaneous()
        proxies = Misc.get_proxies()
        Account_Generator = AccountCreator(proxies)
        
        email = Misc.generate_email()
        username = Misc.generate_username()
        password = config["data"].get("password") or Misc.generate_password()

        log.info(f"Starting a new account creation process for {email[:8]}...")
        if Account_Generator.create_account(username, email, password):
            log.message("Zenix", f"Account successfully created {username} | {email[:8]}... | {password[:8]}...", account_start_time, time.time())
            with open("output/accounts.txt", "a") as f:
                f.write(f"{email}:{password}\n")
            
            return True
        return False
    except Exception as e:
        log.failure(f"Error creating account: {e}")
        return False

def main() -> None:
    try:
        start_time = time.time()
        
        # Initialize basic classes
        Misc = Miscellaneous()
        Banner = Home("Zenix Generator", align="center", credits="discord.cyberious.xyz")
        
        # Display Banner
        Banner.display()

        total = 0
        thread_count = config['dev'].get('Threads', 1)

        # Start updating the title
        title_updater = Misc.Title()
        title_updater.start_title_updates(total, start_time)
        
        with ThreadPoolExecutor(max_workers=thread_count) as executor:
            while True:
                futures = [
                    executor.submit(create_account)
                    for _ in range(thread_count)
                ]

                for future in as_completed(futures):
                    try:
                        if future.result():
                            total += 1
                    except Exception as e:
                        log.failure(f"Thread error: {e}")

    except KeyboardInterrupt:
        log.info("Process interrupted by user. Exiting...")
    except Exception as e:
        log.failure(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import random
import string
import time
import json
from selenium.webdriver.common.keys import Keys

# Path to the ChromeDriver
driver_path = "path/to/chromedriver"

# Set up Chrome option
chrome_options = webdriver.ChromeOptions()
# session_path = "D:/selenium"  # Change this with your path
# chrome_options.add_argument(f"user-data-dir={session_path}")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--log-level=3")  # Set log level to suppress INFO and WARNING messages
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--mute-audio")
chrome_options.add_argument("--incognito")
driver = webdriver.Chrome(options=chrome_options)


def add_user(username, password):
    # Buka file JSON
    try:
        with open('users.json', 'r') as file:
            users_data = json.load(file)
    except FileNotFoundError:
        # Jika file tidak ditemukan, buat file baru
        users_data = {'users': []}

    # Cek apakah pengguna sudah ada dalam data pengguna sebelumnya
    user_exists = False
    for user in users_data['users']:
        if user['username'] == username:
            user_exists = True
            break

    # Jika pengguna belum ada, tambahkan pengguna baru ke dalam struktur data JSON
    if not user_exists:
        users_data['users'].append({
            'username': username,
            'password': password
        })

        # Tulis kembali struktur data JSON ke dalam file
        with open('users.json', 'w') as file:
            json.dump(users_data, file, indent=4)
        print("Data pengguna berhasil ditambahkan.")
    else:
        print("Pengguna sudah ada dalam database.")


# Fungsi untuk mengambil alamat email sementara
def get_temp_email():
    url = "https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if len(data) > 0:
            return data[0]
        else:
            print("Gagal mendapatkan alamat email sementara.")
    else:
        print("Gagal menghubungi API. Status code:", response.status_code)
    return None


# Fungsi untuk mengambil pesan dari alamat email sementara
def get_messages(login, domain):
    url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={login}&domain={domain}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Gagal mengambil pesan. Status code:", response.status_code)
        return None


# Fungsi untuk membaca isi pesan berdasarkan ID
def read_message(login, domain, message_id):
    url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={login}&domain={domain}&id={message_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print("Gagal membaca pesan. Status code:", response.status_code)
        return None


# Fungsi untuk mengambil link verifikasi dari isi pesan dalam format HTML
def extract_verification_link(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a', href=True)
    for link in links:
        if 'Verify' in link.text:
            return link['href']
    return None


# Fungsi untuk mengambil nama pengguna secara acak dari API
def get_random_username():
    url = "https://randomuser.me/api/"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        username = data['results'][0]['name']['first']
        return username
    else:
        print("Gagal mengambil data pengguna acak dari API.")
    return None


# Fungsi untuk menghasilkan kata sandi acak
def generate_random_password():
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for i in range(10))


def Regist():
    url = "https://onmi.io/?invite_code=HkkP24JRvQqn"
    driver.get(url)
    time.sleep(5)

    # Klik tombol masuk
    login_button = driver.find_element(By.XPATH, '/html/body/div/header/div[3]/button[2]')
    login_button.click()

    # Dapatkan alamat email sementara
    temp_email = get_temp_email()
    if not temp_email:
        print("Gagal mendapatkan alamat email sementara.")
        return

    email_input = driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[1]/input')
    if email_input.get_attribute("value"):
        # Jika sudah diisi, hapus isinya
        email_input.clear()
    email_input.send_keys(temp_email)

    login, domain = temp_email.split('@')
    # Dapatkan password acak
    random_password = generate_random_password()
    password_input = driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[2]/input')
    password_input.send_keys(random_password)

    # Dapatkan nama pengguna acak
    random_username = get_random_username()
    username_input = driver.find_element(By.XPATH, '//*[@id="form-submit"]/div[4]/input')
    username_input.send_keys(random_username)

    # Klik tombol submit
    submit_button = driver.find_element(By.XPATH, '//*[@id="form-confirm"]')
    submit_button.click()
    print("Berhasil Daftar")
    print("Menunggu Email Verifikasi")
    time.sleep(5)

    # Coba untuk mendapatkan email verifikasi
    for _ in range(30):  # Cobalah 30 kali, dengan interval 1 detik
        messages = get_messages(login, domain)
        if messages:
            # Proses email jika ditemukan
            for message in messages:
                message_content = read_message(login, domain, message['id'])
                if message_content:
                    verification_link = extract_verification_link(message_content['htmlBody'])
                    if verification_link:
                        print("Link Verifikasi:", verification_link)
                        driver.get(verification_link)
                        ref(temp_email, random_password)
                        return
        print("Menunggu pesan masuk")
        time.sleep(1)
    
    # Jika tidak ada email verifikasi setelah 30 detik, beri tahu pengguna
    print("Gagal mendapat email verifikasi.")
    return



def ref(mail, pas):
    add_user(mail, pas)
    time.sleep(2)
    ref_button = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div/div/div[2]/button') 
    ref_button.click()

    # Isi password yang dibuat saat mendaftar sebelumnya
    password_input = driver.find_element(By.XPATH, '//*[@id="form-auth"]/div[2]/input')
    password_input.send_keys(pas)

    # Klik tombol login
    login_button = driver.find_element(By.XPATH, '//*[@id="form-next"]')
    login_button.click()

    driver.get("https://onmi.io/profile")

    time.sleep(1)
    login_button = driver.find_element(By.XPATH, '/html/body/div/header/div[3]/button[1]')
    login_button.click()

    # Isi password yang dibuat saat mendaftar sebelumnya
    password_input = driver.find_element(By.XPATH, '//*[@id="form-auth"]/div[2]/input')
    password_input.send_keys(pas)

    # Klik tombol submit
    submit_button = driver.find_element(By.XPATH, '//*[@id="form-next"]')
    submit_button.click()
    # Klik tombol untuk membuka tab baru
    buttons_xpath = [
        '/html/body/div/main/div/div[3]/div[2]/div/div/div/div/div[3]/div[1]/a',
        '/html/body/div/main/div/div[3]/div[2]/div/div/div/div/div[3]/div[2]/a',
        '/html/body/div/main/div/div[3]/div[2]/div/div/div/div/div[3]/div[3]/a',
        '/html/body/div/main/div/div[3]/div[2]/div/div/div/div/div[3]/div[4]/a'
    ]

    time.sleep(6)

    task = driver.find_element(By.XPATH, '/html/body/div/main/div/div[2]/div[4]/div[2]/button')
    task.click()
    for button_xpath in buttons_xpath:
        button = driver.find_element(By.XPATH, button_xpath)
        button.send_keys(Keys.CONTROL + Keys.RETURN)
    # Hapus tab yang dibuat sebelumnya
    while len(driver.window_handles) > 1:
        driver.switch_to.window(driver.window_handles[-1])
        driver.close()
    driver.switch_to.window(driver.window_handles[0])

    close = driver.find_element(By.XPATH, '/html/body/div/main/div/div[3]/div[2]/div/div/div/button')
    close.click()

    div = driver.find_element(By.XPATH, '/html/body/div/main/div/div[1]')
    driver.delete_all_cookies()
    print("Refferal Success \n")
    print("=============================================================")
    driver.refresh()
    Regist()

if __name__ == "__main__":
    while True:
        Regist()


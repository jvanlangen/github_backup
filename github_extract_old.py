__author__ = "Jeroen van Langen"
__copyright__ = "Copyright (C) 2024 Jeroen van Langen"
__license__ = "MIT"
__version__ = "1.0"

import schedule
import urllib.request
import json
import subprocess
import os
import time
import pytz
from urllib.parse import urlparse
from datetime import datetime
from functools import partial

# auto flush
print = partial(print, flush=True)

# Read TIMEZONE environment variable, for example: Europe/Amsterdam
desired_timezone = os.getenv("TIMEZONE", "")

# Check if the organization name is set
if not desired_timezone:
    raise ValueError(
        "desired_timezone is not set. Please provide a timezone using the " +
        "TIMEZONE environment variable. for example: Europe/Amsterdam")


# Organization name and GitHub access token
organization = os.getenv('ORGANIZATION', '')

# Check if the organization name is set
if not organization:
    raise ValueError(
        "Organization name is not set. Please provide an organization name " +
        "using the ORGANIZATION environment variable.")


personal_access_token = os.getenv('ACCESS_TOKEN', '')

# Check if the personal access token is set
if not personal_access_token:
    raise ValueError(
        "Personal access token is not set. Please provide a valid access token " +
        "using the ACCESS_TOKEN environment variable.")


# Default backup time is set to 2:00
backup_time = os.getenv('BACKUP_TIME', '2:00')

# GitHub credentials
git_username = os.getenv('USERNAME', '')
git_email = os.getenv('EMAIL', '')

# Set Git global user name and email
subprocess.run(['git', 'config', '--global', 'user.name', git_username])
subprocess.run(['git', 'config', '--global', 'user.email', git_email])


# Definieer de omgevingsvariabelen
#env = {
#    'GIT_SSL_NO_VERIFY': 'true'
#}

# if os.getenv("USECREDENTIALHELPER", ""):
 #   subprocess.run(['git', 'config', '--global', 'credential.helper', 'store --file ~/.git-credentials'], check=True)

#    credential_helper_script = f'!f() {{ echo "username={git_username}"; echo "password={personal_access_token}"; }}; f'
#    subprocess.run(['git', 'config', '--global', 'credential.helper', credential_helper_script], shell=True, check=True)

    # Commando om credential.helper te verwijderen
    #subprocess.run(["git", "config", "--system", "--unset", "credential.helper"], shell=True, check=True)

    # Commando om http.sslverify uit te schakelen
    #subprocess.run(["git", "config", "--system", "http.sslverify", "false"], shell=True, check=True)

    # Commando om http.sslcainfo in te stellen
    #subprocess.run(["git", "config", "--system", "http.sslcainfo", "C:\\Program Files (x86)\\Git\\mingw32\\ssl\\certs\\ca-bundle.crt"], shell=True, check=True)

# Parse the desired timezone
timezone = pytz.timezone(desired_timezone)
os.environ["TZ"] = desired_timezone

# Construct GitHub API URL
url = f'https://api.github.com/orgs/{organization}/repos'

def add_credentials_to_clone_url(clone_url, username, token):
    """Add username and token to the clone URL if not already present."""
    parsed_url = urlparse(clone_url)
    if parsed_url.scheme != 'https' or '@' in parsed_url.netloc:
        # Return the original URL if it's not HTTPS or already contains user credentials
        return clone_url
    else:
        # Add user credentials to the URL
        credentials = f'{username}:{token}@'
        new_netloc = credentials + parsed_url.netloc
        new_url = parsed_url._replace(netloc=new_netloc).geturl()
        return new_url

def backup_job():
    """Perform organization repository synchronization."""
    global url, timezone, env

    current_time = datetime.now(timezone)
    print('##################################################')
    print(f"Start backup at {current_time}")

    # Make an HTTP request and add the personal access token to the headers
    request = urllib.request.Request(url)
    request.add_header('Authorization', f'token {personal_access_token}')

    # Execute the request
    with urllib.request.urlopen(request) as response:
        if response.status == 200:
            repositories = json.loads(response.read())

            for repository in repositories:
                name = repository['name']
                url = repository['clone_url']
                print('**************************************************')
                print(url)

                # add the username and token to the url
                url = add_credentials_to_clone_url(url, git_username, personal_access_token)

                if not os.path.exists("/data"):
                    os.makedirs("/data")

                folder_name = f"/data/{name}"
                # Check if the repository is already cloned, if not, clone it
                if not os.path.exists(f"{folder_name}/.git"):
                    try:
                        print(f'Cloning {name}')
                        subprocess.run(['git', 'clone', url, folder_name], check=True)
                        print(f'{name} is cloned')
                    except subprocess.CalledProcessError:
                        print(f'! Failed to clone {name}')
                else:
                    try:
                        # If the repository is already cloned, perform a 'git pull' to update
                        print(f'Updating {name}')
                        subprocess.run(['git', 'pull'], cwd=folder_name, check=True)
                        print(f'{name} is updated')
                    except subprocess.CalledProcessError:
                        print(f'! Failed to update {name}')
        else:
            print('Error fetching repositories:', response.status)

    end_time = datetime.now(timezone)
    print(f"Ready at {current_time}")

    # Minuten en seconden uit het totaal aantal seconden halen
    # Het totale aantal seconden berekenen
    total_seconds = (end_time - current_time).total_seconds()
    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)


    print(f"The backup took {minutes}:{str(seconds).zfill(2)}")

# Convert backup time to UTC
time_object = datetime.strptime(backup_time, "%H:%M").time()
utc_time = timezone.localize(datetime.combine(datetime.today(), time_object)).astimezone(pytz.utc)
time_string = time_object.strftime("%H:%M")

# Set schedule to run every day at the specified time in the desired timezone
schedule.every().day.at(time_string).do(backup_job).timezone = timezone

print(f"Using user {git_username} with email {git_email} for git.")
print(f"URL: {url}")

print(f"Cloning/Updating every day at {time_string} - {desired_timezone}")

# Print timezone information
print(f"Current timezone: {time.tzname[0]}")

# Get current time
current_time = datetime.now(timezone)
print(f"Current time: {current_time}")

# test launch
# backup_job()

while True:
    # Check schedule
    schedule.run_pending()
    # Wait for a minute
    time.sleep(60)

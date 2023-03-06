import requests 
import hashlib
import os
import subprocess

def main():

    file_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe'

    sha_url = 'http://download.videolan.org/pub/videolan/vlc/3.0.18/win64/vlc-3.0.18-win64.exe.sha256'

    # Get the expected SHA-256 hash value of the VLC installer
    expected_sha256 = get_expected_sha256(sha_url)

    # Download (but don't save) the VLC installer from the VLC website
    installer_data = download_installer(file_url)

    # Verify the integrity of the downloaded VLC installer by comparing the
    # expected and computed SHA-256 hash values
    if installer_ok(installer_data, expected_sha256):

        # Save the downloaded VLC installer to disk
        installer_path = save_installer(installer_data)

        # Silently run the VLC installer
        run_installer(installer_path)
        print('Ran the installer')

        # Delete the VLC installer from disk
        delete_installer(installer_path)
        print('Deleted the installer')

def get_expected_sha256(sha_url):

    resp_msg = requests.get(sha_url)

    if resp_msg.status_code == requests.codes.ok:

        file_content = resp_msg.text
        file_hash = file_content[0:64] 
        
        
    return file_hash

def download_installer(file_url):

    resp_msg = requests.get(file_url)

    if resp_msg.status_code == requests.codes.ok:

        file_content = resp_msg.content 

    return file_content


def installer_ok(installer_data, expected_sha256):

    download_hash = hashlib.sha256(installer_data).hexdigest()

    if expected_sha256 == download_hash:
        print('Hash values match')
        return True
    else:
        print('Possible malware: Hash Values do not match')
        exit(1)

def save_installer(installer_data):

    path = r'C:\Users\joeln\Downloads\VLC.exe'

    with open(path, 'wb') as file:
        file.write(installer_data)

    return path


def run_installer(installer_path):
    subprocess.run([installer_path, '/L=1033', '/S'])
    return
    
def delete_installer(installer_path):
    os.remove(installer_path)
    return

if __name__ == '__main__':
    main()
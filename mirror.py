import urllib.request
import subprocess
import os

versions = {
    "15":"https://aka.ms/vs/15/release/",
    "16":"https://aka.ms/vs/16/release/"
}
editions = {
    "community": "vs_community.exe",
    "professional": "vs_professional.exe",
    "enterprise": "vs_enterprise.exe",
    "buildtools": "vs_buildtools.exe"
}

def download(version, edition, local_path, language="en-US"):
    url = versions[version] + editions[edition]
    local_file = "vs_" + edition + "_" + version + ".exe"
    print(f"Downloading {url} to {local_file}")
    urllib.request.urlretrieve(url, filename=local_file)

    cmd = f"{local_file} --layout {local_path} --lang {language} --all --wait"
    print(cmd)
    subprocess.call(cmd)

if __name__ == "__main__":
    download("16", "buildtools", os.path.abspath("vs_buildtools_16"))
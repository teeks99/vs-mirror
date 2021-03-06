import urllib.request
import subprocess
import os
import json
import shutil
import argparse

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

    cmd = f"{local_file} --layout {os.path.abspath(local_path)}"
    cmd += f" --lang {language} --all --wait --passive --quiet"
    print(cmd)
    subprocess.call(cmd)


def get_version_num(local_path):
    j = None
    manifest = os.path.join(local_path, "ChannelManifest.json")
    with open(manifest, "r", encoding="utf-8") as f:
        j = json.load(f)
    version = j["info"]["productDisplayVersion"]
    return version


def rename_version(edition, local_path):
    version_num = get_version_num(local_path)
    new_dir = "vs_" + edition + "_" + version_num

    shutil.move(local_path, new_dir)
    return new_dir


def create_zip(dir_name):
    archive = shutil.make_archive(dir_name, "zip", base_dir=dir_name)
    print(f"Created archive: {archive}")
    return archive


def mirror_one(version, edition, cleanup=True):
    print(f"Mirroring Visual Studio {version}, {edition}")
    temp_path = "vs_" + edition + "_" + version
    download(version, edition, temp_path)
    named_path = rename_version(edition, temp_path)
    create_zip(named_path)
    if cleanup:
        shutil.rmtree(named_path)


if __name__ == "__main__":
    mirror_versions = versions.keys()
    mirror_editions = editions.keys()

    p = argparse.ArgumentParser()
    p.add_argument('--ver', action="append", help="Visual Studio Version")
    p.add_argument('--edition', action="append", help="Edition. Can be" +
                   "community professional enterprise or buildtools")

    args = p.parse_args()
    
    if args.ver:
        mirror_versions = args.ver

    if args.edition:
        mirror_editions = args.edition

    for version in mirror_versions:
        for edition in mirror_editions:
            mirror_one(version, edition)
import requests
import subprocess
import git 
import os
import docker
import shutil

client = docker.from_env()
# local memory storage
filename = '/opt/autogptconfig/AutoGpt.json'
# workspace for Autogpt
directory_path= '/opt/autogptconfig/auto_gpt_workspace'
# mode for AutoGpt.json
mode = 0o777
# Command to run dockerimage
docrun = "#! /bin/bash \ndocker run -it --env-file=/opt/autogptconfig/./.env -v /opt/autogptconfig/AutoGpt.json:/home/appuser/AutoGpt.json -v /opt/autogptconfig/auto_gpt_workspace:/home/appuser/auto_gpt_workspace -v /opt/autogptconfig/ai_settings.yaml:/home/appuser/ai_settings.yaml autogptnew"
repo_name = "Significant-Gravitas/Auto-GPT" 
# URL of the Git repository
repo_url = "https://github.com/Significant-Gravitas/Auto-GPT.git"

# Local directory to clone the repository to
local_dir = "/home/autogpt"

# Name of the stable branch to checkout
stable_branch = "stable"
# Url to get last release
url = f"https://api.github.com/repos/Significant-Gravitas/Auto-GPT/releases/latest"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    last_release_tag = data['tag_name']
    # file is for hold last release version. Create if not exist. File content is like this: v0.2.2
    # you can rewrite this part. To get latest current version run: git describe --tags --abbrev=0
    f = open("/opt/autogptconfig/releasegpt.txt", "r")
    checkver = f.read()
    # compare version from saved in file and from link
    if checkver == last_release_tag:
      print(f"Nothing to do. {checkver} is {last_release_tag}")
    else:
       # Clone autogpt repo and checkout to stable branch
       shutil.rmtree(local_dir) 
       repo = git.Repo.clone_from(repo_url, local_dir)
       repo.git.checkout(stable_branch)
       # create AutoGpt.json
       if not os.path.exists(filename):
          open(filename, 'w').close()
       os.chmod(filename, mode)
       # create /auto_gpt_workspace 
       if not os.path.exists(directory_path):
         os.makedirs(directory_path)
       os.chmod(directory_path, 0o777)
       # delete existing docker image
       image = client.images.get("autogptnew")
       client.images.remove(image.id, force=True)
       # create docker image
       image, logs = client.images.build(path='/home/autogpt', tag='autogptnew')
       # create runscript
       scriptrun = open("/usr/bin/autogptdocker", "w")
       scriptrun.write(docrun)
       os.chmod("/usr/bin/autogptdocker", 0o755)
       # paste new relese version to file
       fi = open("/opt/autogptconfig/releasegpt.txt", "w")
       fi.write(last_release_tag)
       fi.close()
       print (f"Done!")


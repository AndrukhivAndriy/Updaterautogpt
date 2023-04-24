# Updaterautogpt
This is Python script to update AutoGPT ( automatically update https://github.com/Significant-Gravitas/Auto-GPT.git )

## Requirements 

Script was tested:

1. Ubuntu 22.04
2. Python 3.10

## Install

1. Install all necessary Python libraries:

$ pip install { docker, shutil, os, git, subprocess }

2. Create at /opt/autogptconfig:

a) Auto-GPT config (.env)

b) ai_settings.yaml :

        ai_goals:
        - your goal1
        - your goal2
        - your goal3
        ai_name: Define your AI name
        ai_role: Define your AI role
        
c) create file releasegpt.txt with content, for example: v0.2.1  . Or you can paste here any chars

3. Run : python3 check.py or add to cron

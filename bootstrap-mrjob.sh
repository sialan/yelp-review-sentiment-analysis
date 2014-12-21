#!/bin/bash
sudo yum install -y python-devel
sudo yum install -y python-pip
sudo pip install mrjob numpy nltk
sudo python -m nltk.downloader -d /usr/share/nltk_data all
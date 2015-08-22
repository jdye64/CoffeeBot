** Crossbar.io Server Portion **

Using and installing Crossbar.io requires Python 2.7.x. Some EC2 instances only have Python 2.6.x however. Amazon Linux
AMI which we are using happens to be one of those distributions. Since we are using virtual env we just need to make
sure that we install the python 2.7 and that the virtualenv is created to use Python 2.7

TODOL Document have to install python 2.7? sudo yum install python.27?

Debian Based
```sudo apt-get install build-essential libssl-dev libffi-dev python-dev```

RedHat Based
```yum install libffi-devel -y```
```pip upgrade twisted
pip install ez_setup
pip install six
pip install pyopenssl
pip install pycrypto
pip install wsaccel
pip install ujson
pip upgrade distribute```

```mkvirtualenv -p /usr/bin/python2.7 coffee```
```pip install -r ~/coffee/crossbar/requirements.txt``` Make sure you use this requirements.txt file for the crossbar server
and not the one for the Raspberry PI components.

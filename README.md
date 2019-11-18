# pittl-client
Raspberry Pi TTL Controller Client, 0.1.0  
nGelwan | 2019

## Introduction
PiTTL is a collection of schematics and code which can be used to cheaply build a remotely-controllable random TTL sequence generator using a Raspberry Pi 4 (https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) and a couple of additional hardware components. It consists of two parts, the PiTTL controller (https://github.com/edderkoppen/pittl-ctlr), and the PiTTL client, contained in this repository. When pushed to the extreme, PiTTL supports generating sequences which run for at least a month consisting of pulses of less than 10ms duration. 

## Overview
The PiTTL client is a command-line interface used for interacting with a running PiTTL controller accessible on the network. Refer to https://github.com/edderkoppen/pittl-ctlr/blob/master/README.md#overview for an overview of the PiTTL controller. The concepts detailed there are essential in understanding how to make the most use out of the PiTTL client.

## Installation
The PiTTL client has been tested on Windows 7+, on a couple common Debian- and Fedora-based Linux distros, and on MacOS. It only requires python >=3.4 and python-setuptools as a prerequisite.

For those not used to using the command-line interface on Windows, the commands indicated in this guide should be entered at the prompt of cmd.exe or powershell.exe.

### Windows Installation
1. Make sure python is installed (https://www.python.org/downloads/). Your python installation may be confirmed with

> python --version

You should see an output indicating that python version >=3.4 is installed. 

2. Download this repository as a zip, or use git for windows (gitforwindows.org) to clone the repository.

3. To install the PiTTL client command-line interface, navigate to the repository root and run

> python setup.py install

Confirm the installation with

> pittl -h

You should see output indicating how to use the command-line tool.

### \*NIX-based Installation
1. Use your package manager of choice to install python >=3.4 and python3-setuptools. Confirm the installation with

> python3 --version

2. Install git. Use git to clone this repository. Navigate to the folder in which you want to house it and run

> git clone https://github.com/edderkoppen/pittl-client

3. To install the PiTTL client command-line interface, navigate to the repository root and run

> python3 setup.py install

Confirm the installation with

> pittl -h

You should see output indicating how to use the command-line tool.

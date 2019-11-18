# pittl-client
Raspberry Pi TTL Controller Client, 0.1.0  
nGelwan | 2019

## Introduction
PiTTL is a collection of schematics and code which can be used to cheaply build a remotely-controllable random TTL sequence generator using a Raspberry Pi 4 (https://www.raspberrypi.org/products/raspberry-pi-4-model-b/) and a couple of additional hardware components. It consists of two parts, the PiTTL controller (https://github.com/edderkoppen/pittl-ctlr), and the PiTTL client, contained in this repository. When pushed to the extreme, PiTTL supports generating sequences which run for at least a month consisting of pulses of less than 10ms duration. 

## Overview
The PiTTL client is a command-line interface used for interacting with a running PiTTL controller accessible on the network. Refer to https://github.com/edderkoppen/pittl-ctlr/blob/master/README.md#overview for an overview of the PiTTL controller. The concepts detailed there are essential in understanding how to make the most use out of the PiTTL client.

## Installation
The PiTTL client has been tested on Windows 7+, on a couple common Debian- and Fedora-based Linux distros, and on MacOS. It only requires python3 (>=3.4) and python3-setuptools as a prerequisite.

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

## Usage
Refer to https://github.com/edderkoppen/pittl-ctlr/blob/master/README.md#usage for the essential concepts in interacting with a PiTTL controller.

The PiTTL command-line interface works by specifying the ip address of the PiTTL controller and a sub-command, i.e.

> pittl ip {stage, query, start, stop}

Note that in order for the PiTTL client to reach a controller at the specified ip address, they both have to be on the same network. Pay attention to the interface that the PiTTL controller is using (e.g. ethernet, wifi) and use your knowledge of the local internet architecture to figure this which network this is. As an example, consider that there is a PiTTL controller whose HAT LCD indicates the ip address is 172.20.172.79. The client may enter a command such as

> pittl 172.20.172.79 stage timing -S 120 0.1 0.05

to specify some timing to stage.

### Sub-commands
#### Staging
Both timing and sequences may be staged with the *stage* sub-command. 

> pittl ip stage {timing, sequence}

##### Timing
The *timing* stage sub-sub-command is invoked with the following signature.

> pittl ip stage timing -D days -H hours -M minutes -S seconds -m milliseconds exposure resolution

Each optional argument adds to specified total time (see https://github.com/edderkoppen/pittl-ctlr/blob/master/README.md#usage) with different units of time. Each accepts floating point values. The *exposure* argument requires a floating point value between 0 and 1 inclusive, representing the specified exposure fraction of the timing. The *resolution* parameter accepts a floating point value in units of seconds.

An example of a valid call would be

> pittl 172.20.172.79 stage timing -H 2.5 -S 30.0 0.1 0.05

and would tell the controller at 172.20.172.79 to stage timing with 2.5 hours and 30 seconds, 10% exposure, and a resolution of 50ms.

##### Sequence
The *sequence* stage sub-sub-command is invoked with the following signature

> pittl ip stage sequence

and tells a remote controller to stage a random sequence. It will fail if the controller has not yet staged any timing.

An example of a valid call would be 

> pittl 172.20.172.79 stage sequence

#### Query
The *query* sub-command is used for querying a variety of data regarding a remote controller. Staged and committed timing and sequences may be queried, as well as the progress of any running programs. This data is returned as json-formatted data. Each of these features may be queried individually, but they may also be queried in batch by specifying multiple arguments. If progress is being queried by itself, it may be continuously followed on the client with an extra flag. As one might expect, the signature is given by

> pittl ip query {timing, sequence, progress} -c

Examples of such queries are

> pittl 172.20.172.79 query timing

which returns the staged and committed timing in the controller at 172.20.172.79, or

> pittl 172.20.172.79 query timing sequence

which returns both the staged and committed timing and the staged and committed sequence in the controller at 172.20.172.79. Note that the data returned by querying for a sequence is often really large, and potentially obscures any other data requested, so it is not generally advised that the response be streamed to stdout. A more reasonable query (on \*NIX-based systems) might be

> pittl 172.20.172.79 query sequence > 20191118_program.txt

where the result of querying for the sequence is piped to a file.

To continuouslt display the progress and eta of a program running on a controller at 172.20.172.79, one would enter

> pittl 172.20.172.79 query progress -c

Note that the continuous flag *-c* does nothing unless *progress* is the only query parameter.

#### Start
If timing and a sequence have already been staged, a program can be started with the *start* sub-command.

> pittl ip start

This will fail if no sequence has been staged. As an example

> pittl 172.20.172.79 start

#### Stop
If a running program needs to be interrupted, a program can be stopped with the *stop* sub-command.

> pittl ip stop

e.g. (perfunctorily)

> pittl 172.20.172.79 stop

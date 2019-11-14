import argparse
from contextlib import closing
from datetime import datetime, timedelta
import pickle
from pprint import pprint
import socket
import sys
import time

from pittl.shared import PORT, Response, Request


# Constants
TIMEOUT = 30
QUERY_DELAY = 2
QUERY_MAP = {'timing': Request.Q_TIME,
             'sequence': Request.Q_SEQ,
             'program': Request.Q_PROG}


# Utils
def remote(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.settimeout(TIMEOUT)
    return s


def receive(conn):
    return pickle.loads(conn.recv(4096))


def stream_receive(conn):
    pass


def send(conn, msg, data=None):
    b = pickle.dumps((msg, data))
    conn.send(b)


def send_and_receive(conn, msg, data=None):
    send(msg, data)
    return receive(conn)


def connect(fn):
    def wrapper(host, *args, **kwargs):
        with closing(remote(host, PORT)) as conn:
            fn(conn, *args, **kwargs)
    return wrapper


# Client routines


@connect
def query(conn, args):
    what = set(args.query_what[0])
    if what != {'program'}:
        args.continuous = False

    if args.continuous:
        # Continuous program query
        try:
            while True:
                rsp, data = send_and_receive(conn, Request.Q_PROG)
                pprint(data)
                time.sleep(QUERY_DELAY)
        except KeyboardInterrupt:
            pass
    else:
        info = {}
        for x in what:
            if x == 'program':
                rsp, data = send_and_receive(conn, Request.Q_PROG)
                info.update(data)
            elif x == 'timing':
                rsp, data = send_and_receive(conn, Request.Q_TIME)
                info.update(data)
            elif x == 'sequence':
                send(conn, Request.Q_SEQ)

                seq = {'staged': [], 'committed': []}
                which = None
                while True:
                    rsp, data = receive(conn)
                    if rsp == Response.SUCCESS:
                        break

                    if rsp == Response.BEGIN:
                        which = data

                    if rsp == Response.DATA:
                        if data is not None:
                            seq[which].append(data)
                info.update({'sequence': seq})

        pprint(info)


@connect
def stage_timing(conn, args):
    td = timedelta(days=args.days,
                   hours=args.hours,
                   minutes=args.minutes,
                   seconds=args.seconds,
                   microseconds=args.milliseconds * 1000)
    total = td.total_seconds()
    event = send_and_receive(conn, Request.STAGE_TIMING,
                             (total, args.exposure, args.resolution))
    pprint(event)


@connect
def stage_sequence(conn, args):
    if args.regular:
        rq = Request.STG_SEQ_REG
    else:
        rq = Request.STG_SEQ_RAND
    event = send_and_receive(conn, rq)
    pprint(event)


@connect
def start(conn, args):
    time.sleep(args.start_wait)
    event = send_and_receive(conn, Request.START)
    pprint(event)


@connect
def stop(conn, args):
    time.sleep(args.stop_wait)
    event = send_and_receive(conn, Request.STOP)
    pprint(event)


def dispatch(args):
    host = args.ip

    if hasattr(args, 'query_what'):
        query(host, args)
    elif hasattr(args, 'resolution'):
        stage_timing(host, args)
    elif hasattr(args, 'regular'):
        stage_sequence(host, args)
    elif hasattr(args, 'start_wait'):
        start(host, args)
    elif hasattr(args, 'stop_wait'):
        stop(host, args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]

    # Main parser
    parser = argparse.ArgumentParser()
    parser.add_argument('ip',
                        help='ip address of pittl pi')
    subparsers = parser.add_subparsers()

    # Query parser
    query_parser = subparsers.add_parser('query', help='query parser')
    query_parser.add_argument('query_what',
                              metavar='w',
                              nargs='+',
                              type=str,
                              help='what to query',
                              choices=['timing',
                                       'sequence',
                                       'program'],
                              action='append')
    query_parser.add_argument('-f', '--format',
                              dest='format',
                              type=str,
                              help='output format',
                              default='text',
                              choices=['text', 'json', 'yaml'])
    query_parser.add_argument('-c', '--continuous',
                              dest='continuous',
                              default=False,
                              action='store_true')

    # Staging parser
    stage_parser = subparsers.add_parser('stage', help='stage parser')
    stage_subparsers = stage_parser.add_subparsers()

    # Parse stage timing
    stage_timing_parser = stage_subparsers.add_parser('timing')
    stage_timing_parser.add_argument('exposure',
                                     metavar='X',
                                     type=float,
                                     help='exposure to be given, in fraction '
                                          'of total program time')
    stage_timing_parser.add_argument('resolution',
                                     metavar='R',
                                     type=float,
                                     help='program resolution, in seconds')
    stage_timing_parser.add_argument('-D', '--days',
                                     type=float,
                                     default=0.0,
                                     help='add days to program time')
    stage_timing_parser.add_argument('-H', '--hours',
                                     type=float,
                                     default=0.0,
                                     help='add hours to program time')
    stage_timing_parser.add_argument('-M', '--minutes',
                                     type=float,
                                     default=0.0,
                                     help='add minutes to program time')
    stage_timing_parser.add_argument('-S', '--seconds',
                                     type=float,
                                     default=0.0,
                                     help='add seconds to program time')
    stage_timing_parser.add_argument('-m', '--milliseconds',
                                     type=float,
                                     default=0.0,
                                     help='add milliseconds to program time')

    # Parse stage sequence
    stage_sequence_parser = stage_subparsers.add_parser('sequence')
    stage_sequence_parser.add_argument('-g', '--regular',
                                       dest='regular',
                                       action='store_true',
                                       default=False,
                                       help='stage a regular sequence instead of '
                                            'a random sequence')

    start_parser = subparsers.add_parser('start', help='start parser')
    start_parser.add_argument('-w', '--wait',
                              dest='start_wait',
                              type=float,
                              default=0.0,
                              help='Wait this many seconds before sending the '
                                   'start signal')

    stop_parser = subparsers.add_parser('stop', help='stop parser')
    stop_parser.add_argument('-w', '--wait',
                             dest='stop_wait',
                             type=float,
                             default=0.0,
                             help='Wait this many seconds before sending the '
                                  'stop signal')

    # Parse args
    ns = parser.parse_args(args)

    # Dispatch
    dispatch(ns)

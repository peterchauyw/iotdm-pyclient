# import argparse
#
# parser = argparse.ArgumentParser(description="Command-line Interface for IoTDM Python Client")
# parser.add_argument(["-o", "--op"])

import argparse
import test
#
# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('integers', metavar='N', type=int, nargs='+',
#                    help='an integer for the accumulator')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                    const=sum, default=max,
#                    help='sum the integers (default: find the max)')
#
# args = parser.parse_args()
# print args.accumulate(args.integers)


parser = argparse.ArgumentParser(description="Command-line Interface for IoTDM Python Client")
parser.add_argument('--op', '-o', help='operation', required=True)
parser.add_argument("operation", choices=['restconf', 'kill', 'create', 'retrieve', 'update', 'delete'], help="Operation", type=str)
parser.add_argument("url", help="Target URL", type=str)
parser.add_argument("ty", help="Resource type", type=str, default=None)
parser.add_argument("rn", help="Resource name", type=str, default=None)
args = parser.parse_args()
if args.operation =='restconf':
    test.restConf(args.url, args.rn, 'admin', 'admin')



# if args.op:
#     print("hi")
# else:
#     print("yo")


# parser = argparse.ArgumentParser(description='Demo')
# parser.add_argument('--verbose',
#     action='store_true',
#     help='verbose flag' )
#
# args = parser.parse_args()
#
# if args.verbose:
#     print("~ Verbose!")
# else:
#     print("~ Not so verbose")

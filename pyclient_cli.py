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

def __main__():
    parser = argparse.ArgumentParser(description="Command-line Interface for IoTDM Python Client")
    parser.add_argument('protocol', help='Protocol for Requests', choices=['http', 'coap'], type=str)
    parser.add_argument('--from', '-fr', dest='from', help='From Which IP Address', type=str)
    parser.add_argument('--to', '-t', dest='host', help='To Which IP Address', type=str)
    parser.add_argument('--path', '-pa', dest='path', help='path', type=str, default='')
    parser.add_argument('--name', '-nm', dest='name', help='Resource Name', type=str)
    parser.add_argument('--op', '-o', dest='operation', help='Operation', choices=['restconf', 'kill', 'create', 'retrieve', 'update', 'delete'], type=str, required=True)
    parser.add_argument('--port', '-p', dest='port', help='Port Number', type=str)
    parser.add_argument('--primitiveContent', '-pc', dest='payload', help='payload', type=str)
    parser.add_argument('--requestIdentifier', '-rqi', dest='rqi', help='Request ID', type=str)
    parser.add_argument('--resourceType', '-ty', dest='ty', help='Resource Type', type=str)

    args = parser.parse_args()

    url = '%s://%s' %(args.protocol, args.host)

    if args.operation == 'restconf':
        test.restConf(url, args.name, 'admin', 'admin')

    if args.operation =='kill':
        test.cleanup(url, 'admin', 'admin')

    if args.operation == 'create':
        url = url + ':%s/%s' %(args.port, args.path)
        test.create(url, args.ty, args.name, args.payload)


    if args.operation == 'retrieve':
        url = url + ':%s/%s' %(args.port, args.path)
        test.retrieve(url)


    if args.operation == 'update':
        url = url + ':%s/%s' %(args.port, args.path)
        test.update(url, args.ty, args.payload)


    if args.operation == 'delete':
        url = url + ':%s/%s' %(args.port, args.path)
        test.delete(url)

if __name__ == '__main__':
    __main__()



'''
script to calculate the minimum distance between any two testpoints in an eagle
XML brd file and to test this distance to be above a optional passable lower
limit
'''

from lxml import objectify
import argparse
import sys
import math
import itertools
import logging as log

def distance(point_0, point_1):
    '''
    calculate the distance between two given coordinates in the form of
    [x,y] each
    '''
    x_distance = point_0[0] - point_1[0]
    y_distance = point_0[1] - point_1[1]
    return math.sqrt((x_distance)**2 + (y_distance)**2)

def parse_args():
    '''
    set available arguments and parse them
    '''
    parser = argparse.ArgumentParser(description='Check eagle files for the \
             distance between testpoints. The printed value is the distance \
             from center to center of the testpads.')

    parser.add_argument('boardfile', action="store",
           type=argparse.FileType('rb'))

    parser.add_argument("-l", "--limit", help="define a value that is used as \
           test condition for the minimum tp distance, a TP distance higher \
           than the limit results in an error", type=float, default=0)

    parser.add_argument('--verbose', '-v', help="show more information",
           action='count')

    args = parser.parse_args(sys.argv[1:])
    return args


def get_tp_coordinates_from_brd(boardfile):
    '''
    opens a file and parses it as eagle XML board file, then extracts the
    coordinates of all testpoints and retrns them as a list of [x,y] tuples
    '''
    eagle_object = objectify.fromstring(boardfile.read())

    #exit if eagle object is not a board
    if eagle_object.drawing.find("board") == None:
        return None

    #find all parts on the PCB that are Testpads (i.e. have the attribute
    #TP_SIGNAL_NAME)
    tp_coordinates = []
    parts_on_brd = eagle_object.drawing.board.elements
    for part in parts_on_brd.element:
        for part_attribute in part.attribute:
            if not part.find("attribute") == None and \
            part_attribute.get('name') == "TP_SIGNAL_NAME":
                tp_coordinates.append([float(part.get("x")),
                                       float(part.get("y"))])

    return tp_coordinates


def min_distance_from_coordinates(coordinate_list):
    '''
    calculates the distance between all coordinates in a list of [x,y] tuples
    and returns the minimum of it
    '''
    min_distance = None
    if len(coordinate_list) >= 2:
        #calculate distance of the first two coordinates in the list as starting
        #value
        min_distance = distance(coordinate_list[0], coordinate_list[1])
        #iterate over all combinations of two testpads
        for point_0, point_1 in itertools.combinations(coordinate_list, 2):
            #if the distance between those two coordinates is smaller
            #than the current minimum save it as the new minimum
            min_distance = min(min_distance, distance(point_0, point_1))

    return min_distance

def main():
    '''
    calls a bunch of functions to get the minimum distance between any two
    testpoints of an eagle brd file
    returns 0 for success
    returns 1 for failure
    '''
    args = parse_args()

    log_format = "%(levelname)s: %(message)s"
    if not args.verbose:
        log_level = log.ERROR
    else:
        if args.verbose == 1:
            log_level = log.WARNING
        elif args.verbose == 2:
            log_level = log.INFO
        else:
            log_format = "%(levelname)s (%(lineno)d): %(message)s"
            log_level = log.DEBUG

    log.basicConfig(format=log_format, level=log_level)

    log.info("limit=" + str(args.limit))

    tp_list = get_tp_coordinates_from_brd(args.boardfile)
    if tp_list == None:
        log.critical("file is not a eagle brd file")
        log.debug("result code is 1")
        sys.exit(1)

    min_distance = min_distance_from_coordinates(tp_list)
    print(min_distance)


    if args.limit == 0:
        #no limit set, automatically succeed
        log.debug("result code is 0")
        sys.exit(0)
    elif min_distance >= args.limit:
        #limit is not exceeded, succeed
        log.debug("result code is 0")
        sys.exit(0)
    else:
        #limit is exceeded, fail
        log.debug("result code is 1")
        sys.exit(1)


if __name__ == "__main__":
    main()

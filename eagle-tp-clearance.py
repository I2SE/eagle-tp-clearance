from lxml import objectify
import argparse
import sys
import math
import itertools
import logging as log

def distance(p0, p1):
    return math.sqrt((p0[0] - p1[0])**2 + (p0[1] - p1[1])**2)

parser = argparse.ArgumentParser(description='Check eagle files for the distance between testpoints. The returned value is the distance from center to center of the testpads.')
parser.add_argument('boardfile', action="store", type=argparse.FileType('rb'))
parser.add_argument("-l", "--limit", help="define a value that is used as test condition for the minimum tp distance, a TP distance higher than the limit results in an error",type=float, default=0)
parser.add_argument('--verbose', '-v', help="show more information", default=0, action='count')
args = parser.parse_args(sys.argv[1:])



if args.verbose == 0:
  log.basicConfig(format="%(levelname)s: %(message)s", level=log.ERROR)
elif args.verbose == 1:
  log.basicConfig(format="%(levelname)s: %(message)s", level=log.WARNING)
elif args.verbose == 2:
  log.basicConfig(format="%(levelname)s: %(message)s", level=log.INFO)
elif args.verbose >= 3:
  log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)

log.info("limit=" + str(args.limit))




eagle_object = objectify.fromstring(args.boardfile.read())

#exit if eagle object is not a board
if eagle_object.drawing.find("board") == None:
  print("file is not a eagle brd file")
  sys.exit(1)

#find all parts on the PCB that are Testpads (i.e. have the attribute TP_SIGNAL_NAME)
testpads_coordinates = []
parts_on_brd = eagle_object.drawing.board.elements
for part in parts_on_brd.element:
  for part_attribute in part.attribute:
    if not part.find("attribute") == None and part_attribute.get('name')=="TP_SIGNAL_NAME":
      testpads_coordinates.append([float(part.get("x")), float(part.get("y"))])

min_distance = 0
if len(testpads_coordinates) >= 2:
  #calculate distance of the first two TPs in the list as starting value
  min_distance = distance(testpads_coordinates[0], testpads_coordinates[1])
  #iterate over all combinations of two testpads
  for p0, p1 in itertools.combinations(testpads_coordinates, 2):
    #if the distance between those two testpads is smaller 
    #than the current minimum save it as the new minimum
    min_distance = min(min_distance, distance(p0, p1))

  print(min_distance)
else:
  print("none")

if args.limit == 0:
  #no limit set, automatically succeed
  log.debug("result code is 0")
  sys.exit(0)
elif min_distance <= args.limit:
  #limit is not exceeded, succeed
  log.debug("result code is 0")
  sys.exit(0)
else:
  #limit is exceeded, fail
  log.debug("result code is 1")
  sys.exit(1)

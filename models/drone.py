import board
import random
from time import sleep

from models.tag import Tag
from models.led_stick import LedStick
from models.objectbox_models import Tag as TagModel

from pypozyx.core import PozyxConnectionError


# The main class - There should be always only one Drone instance
class Drone:
    def __init__(self, anchors, database):
        # init the Drone as inactive
        self.active = False

        # init the database
        self.database = database

        try:
            # init the tag, that tracks the Drone (pozyx)
            self.tag = Tag(anchors)
        except PozyxConnectionError:
            print("No Pozyx Tag found - will mock up position for tests.")
            # if no tag found, set it to None
            self.tag = None

        try:
            from models.yaw_detection import YawDetection
            # import yawDetection class
            self.yaw_detector = YawDetection()
        except ImportError:
            print("couldn't start camera and opencv")
            # if opencv fails, set detector None
            self.yaw_detector = None

        # class, that communicates with the flight controller
        self.control = None
        # current position of the drone (x, y, z)
        self.position = None
        # current orientation of the drone (yaw, roll, pitch)
        self.orientation = None

        # create a Tag in the database and saves the id of the drone tag objects entity
        self.tag_id = database.tag.put(TagModel())
        #print(self.tag_id)
        # create the Tag entity - easy read and write
        self.db_object = database.tag.get(self.tag_id)

        if self.tag is not None:
            # setup for the Tag
            self.tag.setup()

        # TODO: LED
        # LED sticks -> front-left: 4, front-right: 2, back-left: 3, back-right: 1
        self.led_sticks = []

        for i in range(4):
            # init LED sticks for all 4 arms (tag_id identifies drone)
            self.led_sticks.append(LedStick(database, i, self.tag_id))

    def startUpdateLoop(self):
        # set the Drone as active
        self.active = True
        while self.active:
            self.updatePosition()
            sleep(1.0)
            if self.position is not None:
                # saves the position in the database
                self.savePositionToDatabase()
                self.db_object.printPosition()

            if self.orientation is not None:
                # saves the orientation in the database
                self.saveOrientationToDatabase()
                self.db_object.printOrientation()

            self.updateLeds(0)

    def updateLeds(self, arm_nr):
        # update the color of the led sticks
        self.led_sticks[arm_nr].setColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    def updatePosition(self):
        if self.tag is not None:
            # update positon & orientation from the Tag
            self.position = self.tag.getPosition()
            # ToDo: merge OpenCV and Pozyx orientation
            self.orientation = self.tag.getOrientation()
        else:
            # load mocked classes for testing
            self.position = Tag.mockedPosition()
            self.orientation = Tag.mockedOrientation()

        if self.yaw_detector is not None and self.yaw_detector.initVideocapture():
            # Merge detected Angle with pozyx Angle
            print("yaw detector angle: ", self.yaw_detector.getAngle())

    def savePositionToDatabase(self):
        self.db_object = self.database.tag.get(self.tag_id)
        self.db_object.setPosition(self.position.x, self.position.y, self.position.z)
        # update position in database object
        self.database.tag.put(self.db_object)

    def saveOrientationToDatabase(self):
        self.db_object.setOrientation(self.orientation.heading, self.orientation.roll, self.orientation.pitch)
        # update orientation in database object
        self.database.tag.put(self.db_object)

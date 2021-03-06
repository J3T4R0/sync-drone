from objectbox.model import *


@Entity(id=1, uid=1)
class Anchor:

    id = Id(id=1, uid=1001)
    anchor_name = Property(str, id=2, uid=1002)
    pos_x = Property(int, id=3, uid=1003)
    pos_y = Property(int, id=4, uid=1004)
    pos_z = Property(int, id=5, uid=1005)
    latency = Property(float, id=6, uid=1006)
    update_rate = Property(float, id=7, uid=1007)
    success_rate = Property(float, id=8, uid=1008)

    def setAnchorname(self):
        self.anchor_name = ''

    def printAnchorname(self):
        print('Anchor:', self.anchor_name)

    def setPosition(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def printPosition(self):
        print("ANCHOR POSITION (db): X: {p.pos_x} Y: {p.pos_y} Z: {p.pos_z}".format(p=self))


@Entity(id=2, uid=2)
class Tag:

    id = Id(id=1, uid=2001)
    tag_name = Property(str, id=2, uid=2002)
    pos_x = Property(float, id=3, uid=2003)
    pos_y = Property(float, id=4, uid=2004)
    pos_z = Property(float, id=5, uid=2005)
    yaw = Property(float, id=6, uid=2006)
    roll = Property(float, id=7, uid=2007)
    pitch = Property(float, id=8, uid=2008)

    def setTagname(self):
        self.tag_name = ''

    def printTagname(self):
        print('Tag:', self.tag_name)

    def setPosition(self, x, y, z):
        self.pos_x = x
        self.pos_y = y
        self.pos_z = z

    def getPosition(self):
        return {'x': self.pos_x, 'y': self.pos_y, 'z': self.pos_z}

    def printPosition(self):
        print("TAG POSITION (db): X: {p.pos_x} Y: {p.pos_y} Z: {p.pos_z}".format(p=self))

    def setOrientation(self, yaw, roll, pitch):
        self.yaw = yaw
        self.roll = roll
        self.pitch = pitch

    def printOrientation(self):
        print("TAG ORIENTATION (db): yaw: {p.yaw} roll: {p.roll} pitch: {p.pitch}".format(p=self))


@Entity(id=3, uid=3)
class Led:
    id = Id(id=1, uid=3001)
    red = Property(int, id=2, uid=3002)
    green = Property(int, id=3, uid=3003)
    blue = Property(int, id=4, uid=3004)

    def setColor(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

    def getColor(self):
        return {'red': self.red, 'green': self.green, 'blue': self.blue}

    def printColor(self):
        print("COLOR (db): R: {p.red} G: {p.green} B: {p.blue}".format(p=self))

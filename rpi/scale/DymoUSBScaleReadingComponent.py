from __future__ import division
import usb
import time

from twisted.internet.defer import inlineCallbacks
from autobahn.twisted.wamp import ApplicationSession, ApplicationRunner
from autobahn.twisted.util import sleep

class DymoUSBScale():

    VENDOR_ID = 0x0922
    dymoScale = None
    endpoint = None
    serialno = "0081427050447" #Found using python usb

    def __init__(self):
        print "Creating DymoScale USB instance. Searching for attached Dymo scale"
        self.setupDymoScale()

    def setupDymoScale(self):
        devices = usb.core.find(find_all = True, idVendor = self.VENDOR_ID)
        for device in devices:
            print "Found an active kernel driver to the USB scale. Need to detach that kernel driver now"
            if device.is_kernel_driver_active(0) is True:
                device.detach_kernel_driver(0)

            devbus = str(device.bus)
            devaddr = str(device.address)
            productid=str(device.idProduct)

            print "DevBus: " + devbus + " DevAddr: " + devaddr + " ProductID: " + productid

            try:
                if str(usb.util.get_string(device, 256, 3)) == self.serialno:
                    print "Found scale with ID: " + self.serialno
                    print ("device serial:    <" + str(usb.util.get_string(device, 256, 3))) + ">"

                    self.endpoint = device[0][(0, 0)][0]
                    self.dymoScale = device
            except usb.core.USBError as e:
                print "Encountered a USB error!"
                data = None
                if e.args == ('Operation timed out',):
                    print "The operation timed out!"
                    print e
                else:
                    print "Some other sort of USB error occured??"

    def readScaleWeight(self):
        try:
            data = self.dymoScale.read(self.endpoint.bEndpointAddress, self.endpoint.wMaxPacketSize)

            # The raw scale array data
            raw_weight = data[4] + (256 * data[5])
            return raw_weight
        except usb.core.USBError as e:
            print "Encountered a USB error!"
            if e.args == ('Operation timed out',):
                print "The operation timed out!"
            else:
                print "Some other sort of USB error occured??"
            print e


class CoffeeComponent(ApplicationSession):

    dymoScale = None
    scale_read_interval = 2     #Number of seconds between attempts to read from the attached USB scale.

    full_weight = 137
    empty_weight = 56
    full_fluid_weight = 81

    @inlineCallbacks
    def onJoin(self, details):

        #Creates the DymoScale instance once the WAMP connection is established
        self.dymoScale = DymoUSBScale()

        # Subscribes to the annotation defined RPC methods and PUB/SUB events
        yield self.register(self)
        yield self.subscribe(self)

        #Creates an infinite loop to post the heartbeat back to the device registry.
        while True:
            weight = self.dymoScale.readScaleWeight() / 10  # Dividing by 10 gives you the number of ounces read from scale.
            if weight:
                payload = {"raw_weight": weight,
                           "coffee_weight": (weight - self.empty_weight),
                           "measurement_unit": "oz",
                           "timestamp": time.time(),
                           "scale_read_interval_sec": self.scale_read_interval,
                           "predict_percentage_full": ((weight - self.empty_weight) / self.full_fluid_weight)}
                yield self.publish('com.makeandbuild.coffee.weight', payload)
                yield sleep(self.scale_read_interval)


if __name__ == '__main__':
    runner = ApplicationRunner("ws://courier.makeandbuildatl.com:9015/ws", "coffee")
    runner.run(CoffeeComponent)
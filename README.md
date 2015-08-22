** Coffee **

Clever name right?

Coffee application is broken up into 3 major packages. Common which is code that is shared between the crossbar server
components and the RPi (Raspberry PI) components. The ```crossbar``` package which holds all of the components that
run in crossbar. This is really defined as any component that does not need to be ran on the RPi device. We should try
and limit the number of components that are ran on the RPi devices. The the ```rpi``` package holds all of the components
that are required to run on a RPi device. The scale for example must be connected to the RPi device to read the weight.
The iBeacon BLE scanner is another one since it uses the BLE USB dongle on the RPi to locate nearby iBeacons.
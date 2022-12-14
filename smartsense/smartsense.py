"""
Allows for the dynamic switching of the Adafruit Sense Hat API depending on
whether an Adafruit Sense Hat is connected or not.
"""
import warnings
import logging
from typing import Union

import sense_hat
import sense_emu

# SmartSense Code
class SmartSense():
    """
    Takes a bool as an optional input, and returns an instance of sense_hat.SenseHat
    if an Adafruit SenseHat is connected to the pi, and returns an instance of
    sense_emu.SenseHat if an Adafruit SenseHat is not connected to the pi.

    Args:
        force_emu (bool, optional): Allows you to force the emulator to open
        even if an Adafruit Sense Hat is detected. Defaults to False.

    Returns:
        Union[sense_hat.SenseHat,sense_emu.SenseHat]: Returns an instance of
        sense_hat.SenseHat if an Adafruit SenseHat is connected to the pi, and
        returns an instance of sense_emu.SenseHat if an Adafruit SenseHat is
        not connected to the pi, or if force_emu is True.
    """
    def __init__(self, force_emu:bool=False) -> Union[sense_hat.SenseHat,sense_emu.SenseHat]:
        """
        Generates attributes for SmartSense class

        Args:
            force_emu (bool, optional): Forces the class to return the emulated Sense Hat
            even if physical sense hat is connected. Defaults to False.
        """
        self._force_emu = force_emu

        try:
            self.sense = sense_hat.SenseHat()
            if force_emu:
                self.sense = self.set_sense_emu()

        except OSError as no_sense_hat:
            # check if OSError is from a missing sense hat
            if str(no_sense_hat) == "Cannot detect RPi-Sense FB device":
                logging.info("Could not find Sense Hat! Using emulated Sense Hat...")
                self.sense = self.set_sense_emu()

    def set_sense_emu(self) -> sense_emu.SenseHat:
        """
        Returns a sense_emu Sense Hat object, while opening the emulator automatically

        Returns:
            sense_emu.SenseHat: Returns a sense_emu.SenseHat object
        """
        with warnings.catch_warnings(record=True) as caught_warnings:
            emulated_sense = sense_emu.SenseHat()
            warnings.simplefilter("default","No emulator detected")
            if caught_warnings != []:
                logging.info("Opening Sense Emulator GUI...")
        return emulated_sense

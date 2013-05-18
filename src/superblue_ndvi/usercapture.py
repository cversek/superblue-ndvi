################################################################################
import datetime, os, time, argparse, multiprocessing, subprocess
from webcam import Webcam
from gpio import GPIO

DEFAULT_RESOLUTION = "1600x1200"
#DEFAULT_PNG_COMPRESSION = 9 # (-1,0-10)
DEFAULT_FRAME_SKIP = 0
USERHOME_PATH = os.path.expanduser("~") #should be portable
DEFAULT_OUTPUT_PATH = os.sep.join((USERHOME_PATH,"photos"))
DEFAULT_VERBOSE = True
SLEEP_TIME = 0.1 #seconds
SNAP_BUTTON_PIN = 44
SNAP_LED_PIN    = 26
INPUT_PINS  = [SNAP_BUTTON_PIN]
OUTPUT_PINS = [SNAP_LED_PIN]
################################################################################


################################################################################
class Application:
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', DEFAULT_VERBOSE)
        self.webcam = Webcam(**kwargs)
        self.gpio = GPIO(inputs = INPUT_PINS, outputs = OUTPUT_PINS)
            
        
    def main_loop(self):
        i = 0
        try:
            self.gpio.export()
            while True:
                button_state = self.gpio[SNAP_BUTTON_PIN]
                self.gpio[SNAP_LED_PIN] = button_state
                if button_state:
                    dt = datetime.datetime.now()
                    filename_prefix = dt.strftime("%Y-%m-%d_%H_%M_%S")
                    filename_suffix = "_img%03d" % i
                    self.webcam.take_photo(filename_prefix = filename_prefix,
                                           filename_suffix = filename_suffix,
                                           blocking = True,
                                           )
                    self.gpio[SNAP_LED_PIN] = button_state
                time.sleep(SLEEP_TIME)
        except KeyboardInterrupt:
            if self.verbose:
                print "user aborted capture...goodbye"
        finally:
            self.gpio.unexport()

################################################################################
# MAIN
################################################################################
def main():
    import argparse
    parser = argparse.ArgumentParser()
    #optional arguments
    parser.add_argument("-r", "--resolution",
                        help = "set the resolution of the camera",
                        default = DEFAULT_RESOLUTION,
                       )
#    parser.add_argument("-c", "--png_compression",
#                        help = "level of PNG compression (-1,0-10)",
#                        type = int,
#                        choices = (-1,0,1,2,3,4,5,6,7,8,9,10),
#                        default = DEFAULT_PNG_COMPRESSION,
#                       )
    parser.add_argument("-f", "--frame_skip",
                        help = "skip number of frames",
                        type = int,
                        default = DEFAULT_FRAME_SKIP,
                       )
    parser.add_argument("-o", "--output_path",
                        help = "path for img output",
                        default = DEFAULT_OUTPUT_PATH,
                       )
    parser.add_argument("-v", "--verbose",
                        help="increase output verbosity",
                        action="store_true",
                        default = DEFAULT_VERBOSE,
                       )
    args = parser.parse_args()
    #apply configuration arguments to constructor
    app = Application(resolution = args.resolution,
                      #png_compression = args.png_compression,
                      frame_skip = args.frame_skip,
                      output_path = args.output_path,
                      verbose = args.verbose,
                     )
    app.main_loop()
    
#if this module is run directly
if __name__ == "__main__":
    main()

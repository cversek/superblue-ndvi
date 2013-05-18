################################################################################
import datetime, os, time, argparse, multiprocessing, subprocess
from webcam import Webcam

DEFAULT_NUM = 1
DEFAULT_DELAY = 5
DEFAULT_BEEP_TIME = 0
DEFAULT_RESOLUTION = "1600x1200"
#DEFAULT_PNG_COMPRESSION = 9 # (-1,0-10)
DEFAULT_PRE_CAPTURE_DELAY = 0 #seconds
DEFAULT_FRAME_SKIP = 0
USERHOME_PATH = os.path.expanduser("~") #should be portable
DEFAULT_OUTPUT_PATH = os.sep.join((USERHOME_PATH,"photos"))
RAMDISK_PATH = "/tmp/ramdisk"
DEFAULT_VERBOSE = True
SLEEP_TIME = 0.1 #seconds
################################################################################
class Application:
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', DEFAULT_VERBOSE)
        self.webcam = Webcam(**kwargs)
    def capture_sequence(self,
                         num,
                         delay,
                         beep_time = 0,
                         async = False,
                         **kwargs
                        ):
        i = 0
        try:
            while True:
                if beep_time > 0:
                    if self.verbose:
                        print "The capture will begin in %d seconds!" % beep_time
                    beep()
                    time.sleep(beep_time)
                    beep()
                    beep()
                    beep()
                    
                if num > 0 and i >= num: #negative num will never return
                    if self.verbose:
                        print "finished capture...goodbye"
                    return
                dt = datetime.datetime.now()
                filename_prefix = dt.strftime("%Y-%m-%d_%H_%M_%S")
                filename_suffix = "_img%03d" % i
                self.webcam.take_photo(filename_prefix = filename_prefix,
                                       filename_suffix = filename_suffix,
                                       blocking = not async,
                                       )
                if not (i == num-1):
                    time.sleep(delay - beep_time)
                i += 1
        except KeyboardInterrupt:
            if self.verbose:
                print "user aborted capture...goodbye"

################################################################################
# MAIN
################################################################################
def main():
    import argparse
    parser = argparse.ArgumentParser()
    #capture sequence arguments
    parser.add_argument("-n", "--num",
                        help = "number of images in sequence, negative implies infinite",
                        type = int,
                        default = DEFAULT_NUM,
                       )
    parser.add_argument("-d", "--delay",
                        help = "post capture delay for sequence",
                        type = int,
                        default = DEFAULT_DELAY,
                       )
    parser.add_argument("-b", "--beep-time",
                        dest = "beep_time",
                        help = "time to warn before capture",
                        type = int,
                        default = DEFAULT_BEEP_TIME,
                       )
    parser.add_argument("-a", "--async",
                        help = "run both captures in parallel processes",
                        action = "store_true",
                        default = False,
                       )
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
    parser.add_argument("-p", "--pre_capture_delay",
                        help = "pre capture delay (seconds)",
                        type = float,
                        default = DEFAULT_PRE_CAPTURE_DELAY,
                       )
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
                      pre_capture_delay = args.pre_capture_delay, #seconds
                      frame_skip = args.frame_skip,
                      output_path = args.output_path,
                      verbose = args.verbose,
                     )
    #run the capture_sequence
    app.capture_sequence(num = args.num,
                         delay = args.delay,
                         beep_time = args.beep_time,
                         async = args.async,
                         )
#if this module is run directly
if __name__ == "__main__":
    main()

import datetime, os, time, argparse, multiprocessing, subprocess
import SimpleCV

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

def run_cmd(cmd):
        return subprocess.call(cmd, shell=False)
        
def beep():
    os.system("beep")
    
##########################################################################
class Webcam(object):
    def __init__(self,
                 devnum = 0,
                 resolution = DEFAULT_RESOLUTION,
                 #png_compression = DEFAULT_PNG_COMPRESSION,
                 pre_capture_delay = DEFAULT_PRE_CAPTURE_DELAY, #seconds
                 frame_skip = DEFAULT_FRAME_SKIP,
                 output_path = DEFAULT_OUTPUT_PATH,
                 verbose = DEFAULT_VERBOSE,
                ):
        #setup capture options
        self.resolution = resolution
        #self.png_compression = int(png_compression)
        self.pre_capture_delay = int(pre_capture_delay)
        self.frame_skip = int(frame_skip)
        #setup image output directory
        self.output_path = output_path
        if not os.path.isdir(output_path):
            os.mkdir(output_path)
        #make noise?
        self.verbose = verbose
        #setup asynchronous process launching
        count = multiprocessing.cpu_count() #get num of multiprocessors
        self._pool = multiprocessing.Pool(processes=count)
        #configure camera device
        self._dev = "/dev/video%d" % devnum
        self._last_photo_filename = None
    
    def take_photo(self,
                   filename_prefix = None,
                   filename_suffix = None,
                   blocking = True,
                  ):
        if filename_prefix is None:
            dt = datetime.datetime.now()
            filename_prefix = dt.strftime("%Y-%m-%d_%H_%M_%S")
        #build the common capture command options
        base_cmd = ["fswebcam"]
        base_cmd.append("--no-banner")
        base_cmd.append("-r %s" % self.resolution)
        #base_cmd.append("--png %d" % self.png_compression)
        #base_cmd.append("-D %d" % self.pre_capture_delay)
        base_cmd.append("-S %d" % self.frame_skip)
        #update prefix to include the output path
        #filename_prefix = os.sep.join((self.output_path,filename_prefix))
        filename_prefix = os.sep.join((RAMDISK_PATH,filename_prefix))
        #construct the filepaths
        fn = [filename_prefix]
        if not filename_suffix is None:
            fn.append(filename_suffix)
        fn.append(".jpg")
        fn = "".join(fn)
        self._last_photo_filename = fn
        #construct the full capture commands
        cmd = base_cmd[:] #copy list
        cmd.append("--save %s" % fn)
        cmd.append("-d %s" % self._dev)
        cmd = " ".join(cmd)
        #run the commands asynchronously
        if blocking:
            if self.verbose:
                print "running following command:"
                print cmd
                print '-'*40
            run_cmd(cmd.split())
            return self.fetch_image()
        else: #or in sequence
            if self.verbose:
                print "running following commands asynchronously:"
                print cmd
                print '-'*40
            self._pool.map(run_cmd,[cmd.split()])
            return None
            
    def wait_on_image(self):
        if self._last_photo_filename is None: #no photo triggered yet
            return
        while not os.path.isfile(self._last_photo_filename): #image not ready yet
            time.sleep(SLEEP_TIME)
            
    def fetch_image(self, blocking = True):
        if blocking:
            self.wait_on_image()
            return SimpleCV.Image(self._last_photo_filename)
        else:
            if not os.path.isfile(self._last_photo_filename): #image not ready yet
                return None
            else:
                return SimpleCV.Image(self._last_photo_filename)

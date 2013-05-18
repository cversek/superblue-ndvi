GPIO_PATH =  "/sys/class/gpio"
################################################################################
         

def write_file(path,val):
    with open(path,'w') as f:
        f.write(str(val))
    
def read_file(path):
    with open(path,'r') as f:
        return f.read()

################################################################################
class GPIO:
    def __init__(self, inputs = [], outputs = []):
        self.inputs  = inputs
        self.outputs = outputs
    
    def __getitem__(self, pin):
        pin_dir = "%s/gpio%d" % (GPIO_PATH,pin)
        val = read_file(pin_dir+"/value")
        return bool(int(val))
    
    def __setitem__(self, pin, val):
        pin_dir = "%s/gpio%d" % (GPIO_PATH,pin)
        val = int(val)
        write_file(pin_dir+"/value", val)
        
    def export(self):
        for pin in self.inputs:
            write_file(GPIO_PATH+"/export",pin)
            pin_dir = "%s/gpio%d" % (GPIO_PATH,pin)
            write_file(pin_dir+"/direction","in")
        for pin in self.outputs:
            write_file(GPIO_PATH+"/export",pin)
            pin_dir = "%s/gpio%d" % (GPIO_PATH,pin)
            write_file(pin_dir+"/direction","out")
    
    def unexport(self):
        for pin in self.inputs:
            write_file(GPIO_PATH+"/unexport",pin)
        for pin in self.outputs:
            write_file(GPIO_PATH+"/unexport",pin)

import ctre, wpilib, csv, os
from networktables import NetworkTables

class Scoop:
    scoop_motor: ctre.WPI_TalonSRX
    
    '''not in sand or gravel, 1-1.5a'''
    ''' in sand, draw around 6.5a. in gravel, draw around17-18a'''
    #TODO calculate the timing between 2 scoop and timing for one cycle of scoop --> use encoder?
    NOT_DIGGING = 3
    SAND_MIN_CURRENT = 5.5
    SAND_MAX_CURRENT = 6.5
    GRAVEL_MIN_CURRENT = 17
    GRAVEL_MAX_CURRENT = 18
    TIME_BETWEEN_SCOOPS = 5 #seconds
 
    def __init__(self):
        self.enabled = False
        self.currentAmps = 0
        #self.file = open('testfile.txt','w') 
        #self.file.close() 
        
        self.power = 0
        NetworkTables.initialize(server='roborio-190-frc.local')
        self.sd = NetworkTables.getTable('/SmartDashboard')
        self.timer = wpilib.Timer()
        self.timer.start()

    def enable(self):
        '''Causes the shooter motor to spin'''
        self.enabled = True

    def is_ready(self):
        # in a real robot, you'd be using an encoder to determine if the
        # shooter were at the right speed..
        return True

     #TODO is jamming if peaking more than 2 consecutive second   
    def isJamming(self):
        currentAmps = self.scoop_motor.getOutputCurrent()
        
        if (currentAmps > self.GRAVEL_MAX_CURRENT):
            #print ("----------currentAmp: ",currentAmps)
            return True
        return False
    peakCount = 0
    def scoop_down(self,power):
        #print ("is scooping")
        self.power = power
        currentAmps = self.scoop_motor.getOutputCurrent()
        print ("-------------------------currentAmp: ",currentAmps)
        if (currentAmps <= self.NOT_DIGGING):
            self.power = 0
            self.sd.putBoolean('CanExtend', True)
            self.sd.putString('Digging','Nothing')
        else:
            #peakCount += 1
            self.power = 1
            self.sd.putBoolean('CanExtend', False)
            if (currentAmps <= self.SAND_MAX_CURRENT ):
                self.sd.putString('Digging','Sand')
            elif (currentAmps >= self.GRAVEL_MIN_CURRENT ):
                self.sd.putString('Digging','Gravel')
            if (self.isJamming()):
                i = 3
                while (i > 0):
                    self.power = -1
                    i=i-1
    

    def write_CSV(self):
        '''cwd = os.getcwd()  # Get the current working directory (cwd)
        files = os.listdir(cwd)  # Get all the files in that directory
        print("Files in '%s': %s" % (cwd, files))
        #firstrow = ['Time','']'''
        csvData=[self.timer.get(),self.scoop_motor.getOutputCurrent()]
        #csvData=[[1,2,3],[4,5,6]]
        try:
            with open('/home/lvuser/py/eat.csv', 'a') as csvFile:
                print("in csv")
                writer = csv.writer(csvFile)
                writer.writerow(csvData)
            csvFile.close()
        except IOError:
            print('CANNOT OPEN FILE')
        #pass
    def close_CSV(self):
        pass
    ''' this is for teleop'''    
    def run(self, power):
        self.power = power
        
    def execute(self):
        '''This gets called at the end of the control loop'''
        self.scoop_motor.set(ctre.WPI_TalonSRX.ControlMode.PercentOutput,self.power)
        
        
        
        self.update_sd()
        

    def update_sd(self):
        self.sd.putValue('Scoop/Current', self.scoop_motor.getOutputCurrent())
        
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

class springUTS:
    def __init__(self, springDiameter, wireDiameter, activeCoils,
                  length, UTS, UTSerror):
        self.springDiameter = springDiameter
        self.wireDiameter = wireDiameter
        self.activeCoils = activeCoils
        self.length = length
        self.UTS = UTS
        self.UTSerror = UTSerror
    
    def stress(self):
        D = self.springDiameter *1e-3 # in m
        d = self.wireDiameter*1e-3 #in m
        n = self.activeCoils
        l = self.length *1e-3 #in m

        diffL = (l- n*d)
        # spring rate
        G = 75e9 #Pa
        c = (G*d**4)/(8*n*D**3)
        force = c*diffL
        #stress 
        s = (8*D*force)/(np.pi*d**3)
        w = D/d
        correctionFactor = (4*w -1)/(4*w-4)+ 0.615/w
        return s*correctionFactor

    def stressBerg(self):
        D = self.springDiameter *1e-3 # in m
        d = self.wireDiameter*1e-3 #in m
        n = self.activeCoils
        l = self.length *1e-3 #in m
        diffL = (l- n*d)
        # spring rate
        G = 75e9 #Pa
        c = (G*d**4)/(8*n*D**3)
        force = c*diffL
        #stress 
        s = (8*D*force)/(np.pi*d**3)
        w = D/d
        correctionFactor = (w+0.5)/(w-0.75)
        return s*correctionFactor

    def calcFactor(self):
        D = self.springDiameter *1e-3 # in m
        d = self.wireDiameter*1e-3 #in m
        n = self.activeCoils
        l = self.length *1e-3 #in m

        if (l- n*d <= 0 ):
            self.NoSpringWarnig()
            return

        uts = self.UTS *1e6 #Pa
        s = self.stress()

        return (uts + s)/uts
        
    def stress_absorbed_by_spring(self):
        return 0.80*self.stress()*1e-6

    def calcErrors(self):
        err1 = self.UTSerror
        err2 = self.UTS*0.05 #Error propagation (UTS+/- UTSerror) * (0.45 +/- 0.05)
        err3 = self.UTSerror + (np.absolute(self.stress()-self.stressBerg()))*1e-6
        err4 = (self.UTS+self.stress()*1e-6)*0.05 #Error propagation (UTSnew+/- UTSnew_error) * (0.45 +/- 0.05)
        return err1, err2, err3, err4 

    def results(self):
        return (self.UTS, 0.45*self.UTS,
                 self.UTS+self.stress()*1e-6, 0.45*(self.UTS+self.stress()*1e-6))

    def plot(self):
        D = self.springDiameter *1e-3 # in m
        d = self.wireDiameter*1e-3 #in m
        n = self.activeCoils
        l = self.length *1e-3 #in m

        if (l- n*d <= 0 ):
            self.NoSpringWarnig()
            return
          
        uts = self.UTS
        newuts = (uts*1e6 + self.stress())*1e-6

        y0 = np.array([0.9*uts,0.5*uts])
        y1 = np.array([0.9*uts+self.stress()*1e-6, 0.5*uts + self.stress()*1e-6])
        x = [1e4,1e5]

        fig, ax = plt.subplots()

        ax.plot(x, y0, label = "Material Fatigue", color = "blue")
        ax.hlines(y=y0[0], xmin=0, xmax=1e04, color='Blue')
        ax.hlines(y=y0[1], xmin=1e5, xmax=1.5e05, color='Blue')

        ax.plot(x, y1, label = "Material + Spring Fatigue", color = "green")
        ax.hlines(y=y1[0], xmin=0, xmax=1e04, color="green")
        ax.hlines(y=y1[1], xmin=1e5, xmax=1.5e05, color="green")

        #ax.set_xticks([])
        ax.set_xticks([0, 1e5], ['1,000', '1,000,000'])
        ax.set_ylabel("Stress Amplitde (Mpa)")
        ax.set_xlabel("cycles")
        ax.set_title("SN Curve")
        ax.legend()

        # Save the plot to a BytesIO object
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Convert to base64 for embedding in HTML
        image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        return image_base64
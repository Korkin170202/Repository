from tkinter import Tk, Toplevel, Frame, Button, Label, Entry, Menu, Canvas, BooleanVar, Checkbutton
from tkinter.messagebox import showinfo
import scipy
import numpy
import os

Resistor = Tk()
Resistor.minsize(width = 600, height = 400)
Resistor.maxsize(width = 600, height = 400)
Resistor.title('Resistor')

ResistorCanvas = Canvas(Resistor)
ResistorCanvas.place(x = 0, y = 0, width = 400, height = 400)

ResistorButtons = Frame(Resistor)
ResistorButtons.place(x = 400, y = 0, width = 400, height = 400)

resistance_label = Label(ResistorButtons, text = 'There are no resistors')
resistance_label.place(x = 0, y = 80, width = 200, height = 280)

clamp_num = 2
clamp_1 = 0
clamp_2 = 0
ClampsWindow = 0

coord_points = [[10, 200], [380, 200]]
resistors_resistances = []
calculation_info = []

psave_info = []
rsave_info = ['#']

ResistorNum = 1
PointNum = 0

def closest_item(x, y, coord_points):
    min_distance = -1
    returned = -1
    for i in range (len(coord_points)):
        distance = ((coord_points[i][0] - x) ** 2 + (coord_points[i][1] - y) ** 2) ** (1 / 2)
        if distance < min_distance or returned == -1:
            returned = i
            min_distance = distance
    return returned

def label_rewrite(resistors_resistances):
    global resistance_label
                
    in_text = ''
                
    for i in range (len(resistors_resistances)):
        in_text += 'R' + str(i + 1) + ' = ' + str(resistors_resistances[i]) + ' Ohm.\n'
                
    resistance_label.configure(text = in_text, justify = 'left', anchor = 'nw')

class point:
    num = 0
    xpoint = 10
    ypoint = 10
    
    color = 'black'
    
    data = {'x': 0, 'y': 0}
    
    def load_point(self, ResistorCanvas, Resistor):
        global psave_info
        
        self.point = ResistorCanvas.create_oval(self.xpoint + 4, self.ypoint + 4, self.xpoint - 4, self.ypoint - 4, width = 0, tags = 'point' + str(self.num), fill = self.color)
        self.num_in_Canvas = ResistorCanvas.create_text(self.xpoint + 8, self.ypoint, text = str(self.num + 1), justify = 'left', anchor = 'w')
        
        ResistorCanvas.addtag_withtag('point', 'point' + str(self.num))
        
        ResistorCanvas.tag_bind('point' + str(self.num), '<ButtonPress-1>', self.point_press)
        ResistorCanvas.tag_bind('point' + str(self.num), '<ButtonRelease-1>', self.point_release)
        ResistorCanvas.tag_bind('point' + str(self.num), '<B1-Motion>', self.point_motion)
        
        psave_info.append([self.xpoint, self.ypoint, self.color])
    
    def point_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def point_release(self, event):
        global coord_points
        
        coord_points[self.num][0] = self.xpoint
        coord_points[self.num][1] = self.ypoint
        
        self.data['x'] = 0
        self.data['y'] = 0
    
    def point_motion(self, event):
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
            
            self.xpoint += delta_x
            self.ypoint += delta_y
            
            psave_info[self.num][0] = self.xpoint
            psave_info[self.num][1] = self.ypoint
            
            ResistorCanvas.move(self.point, delta_x, delta_y)
            ResistorCanvas.move(self.num_in_Canvas, delta_x, delta_y)
            
            self.data['x'] = event.x
            self.data['y'] = event.y    
    
class resistor:
    num = 1
    xbody = 170
    ybody = 190
    xstart = 0
    ystart = 0
    xend = 0
    yend = 0
    
    startpoint = 0
    endpoint = 1
    
    resistance = 1
    
    data = {'x': 0, 'y': 0}
    
    def load(self, ResistorCanvas, Resistor):
        global coord_points, resistance_label, resistors_resistances, calculation_info, rsave_info
        
        resistors_resistances.append(self.resistance)
        label_rewrite(resistors_resistances)
        
        calculation_info.append([self.startpoint, self.endpoint, self.resistance])
        
        if self.startpoint == 0:
            self.xstart = coord_points[0][0]
            self.ystart = coord_points[0][1]
        if self.endpoint == 1:
            self.xend = coord_points[1][0]
            self.yend = coord_points[1][1]  
        if self.startpoint == 1:
            self.xstart = coord_points[1][0]
            self.ystart = coord_points[1][1]
        if self.endpoint == 0:
            self.xend = coord_points[0][0]
            self.yend = coord_points[0][1]
        
        self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)
        self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)
        self.get1 = ResistorCanvas.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1' + str(self.num), fill = 'black')
        self.get2 = ResistorCanvas.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2' + str(self.num), fill = 'black')
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))
        
        self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))
        
        ResistorCanvas.tag_bind('resistor' + str(self.num), '<ButtonPress-1>', self.body_press)
        ResistorCanvas.tag_bind('resistor' + str(self.num), '<ButtonRelease-1>', self.body_release)
        ResistorCanvas.tag_bind('resistor' + str(self.num), '<B1-Motion>', self.body_motion)
        
        ResistorCanvas.tag_bind('resistor' + str(self.num), '<Button-3>', self.new_resistance)
        
        ResistorCanvas.tag_bind('get1' + str(self.num), '<ButtonPress-1>', self.get1_press)
        ResistorCanvas.tag_bind('get1' + str(self.num), '<ButtonRelease-1>', self.get1_release)
        ResistorCanvas.tag_bind('get1' + str(self.num), '<B1-Motion>', self.get1_motion)
        
        ResistorCanvas.tag_bind('get2' + str(self.num), '<ButtonPress-1>', self.get2_press)
        ResistorCanvas.tag_bind('get2' + str(self.num), '<ButtonRelease-1>', self.get2_release)
        ResistorCanvas.tag_bind('get2' + str(self.num), '<B1-Motion>', self.get2_motion)         
   
        rsave_info.append([self.xbody, self.ybody, self.xstart, self.ystart, self.xend, self.yend, self.startpoint, self.endpoint, self.resistance])
    
    def body_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def body_release(self, event):
        self.data['x'] = 0
        self.data['y'] = 0
        
        ResistorCanvas.delete(self.get1)
        self.get1 = ResistorCanvas.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1' + str(self.num), fill = 'black')        
        
        ResistorCanvas.delete(self.get2)
        self.get2 = ResistorCanvas.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2' + str(self.num), fill = 'black')        
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))
        
        ResistorCanvas.delete(self.resistance_text)
        self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))

    def body_motion(self, event):
        global rsave_info
        
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            ResistorCanvas.itemconfig(self.body, outline = 'gray', fill = 'gray')
            
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
            
            self.xbody += delta_x
            self.ybody += delta_y
            
            rsave_info[self.num][0] = self.xbody
            rsave_info[self.num][1] = self.ybody
            
            ResistorCanvas.move(self.body, delta_x, delta_y)
            ResistorCanvas.move(self.resistance_text, delta_x, delta_y)
            
            ResistorCanvas.delete(self.line1)
            ResistorCanvas.delete(self.line2)
            
            self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)
            self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)
        
            '''
            Can be this:
            ResistorCanvas.move(self.line1, delta_x, delta_y)
            ResistorCanvas.move(self.line2, delta_x, delta_y)
            '''
        
            self.data['x'] = event.x
            self.data['y'] = event.y
    
    def new_resistance(self, event):
        self.ResistanceWindow = Toplevel(Resistor)
        self.ResistanceWindow.grab_set()
        self.ResistanceWindow.focus_force()
        self.ResistanceWindow.minsize(width = 200, height = 100)
        self.ResistanceWindow.maxsize(width = 200, height = 100)
        self.ResistanceWindow.title('Change resistance')        
        
        self.info = Label(self.ResistanceWindow, text = 'Enter the resistance (in Ohms)\nof the resistor No ' + str(self.num) + ':')
        self.info.place(x = 0, y = 0, width = 200, height = 40)
        
        self.input = Entry(self.ResistanceWindow)
        self.input.place(x = 0, y = 40, width = 200, height = 20)
        
        self.OK_but = Button(self.ResistanceWindow, text = 'OK')
        self.OK_but.place(x = 0, y = 60, width = 100, height = 40)
        self.OK_but.bind('<Button-1>', self.OK_action)
        
        self.Cancel_but = Button(self.ResistanceWindow, text = 'Cancel')
        self.Cancel_but.place(x = 100, y = 60, width = 100, height = 40)
        self.Cancel_but.bind('<Button-1>', self.Cancel_action)
        
        self.ResistanceWindow.mainloop()
    
    def OK_action(self, event):
        global resistance_label, resistors_resistances
        
        resistance = self.input.get()
        
        try:
            resistance_in = float(self.input.get())
        
            if resistance_in <= 0:
                raise ValueError
        
            self.resistance = resistance_in
            
            resistors_resistances[self.num - 1] = self.resistance
            label_rewrite(resistors_resistances)
            
            calculation_info[self.num - 1][2] = self.resistance
            
            rsave_info[self.num][8] = self.resistance
            self.ResistanceWindow.destroy()
        except ValueError:
            self.ResistanceWindow.destroy()
    
    def Cancel_action(self, event):
        self.ResistanceWindow.destroy()
    
    def get1_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def get1_release(self, event):
        global coord_points
        
        closest_point_num = closest_item(self.data['x'], self.data['y'], coord_points)
        
        self.startpoint = closest_point_num
        
        rsave_info[self.num][6] = self.startpoint       
        
        calculation_info[self.num - 1][0] = self.startpoint
        
        delta_x = coord_points[closest_point_num][0] - self.data['x']
        delta_y = coord_points[closest_point_num][1] - self.data['y']        
        
        self.xstart += delta_x
        self.ystart += delta_y        
        
        rsave_info[self.num][2] = self.xstart
        rsave_info[self.num][3] = self.ystart
        
        ResistorCanvas.delete(self.line1)
        self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)        
        
        self.data['x'] = 0
        self.data['y'] = 0
        
        ResistorCanvas.delete(self.get1)
        self.get1 = ResistorCanvas.create_oval(self.xstart + 3, self.ystart + 3, self.xstart - 3, self.ystart - 3, width = 0, tags = 'get1' + str(self.num), fill = 'black')
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))        
        
        ResistorCanvas.delete(self.resistance_text)
        self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))        
        
    def get1_motion(self, event):
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
        
            self.xstart += delta_x
            self.ystart += delta_y
            
            rsave_info[self.num][2] = self.xstart
            rsave_info[self.num][3] = self.ystart           
            
            ResistorCanvas.move(self.get1, delta_x, delta_y)
        
            ResistorCanvas.delete(self.line1)
            self.line1 = ResistorCanvas.create_line(self.xstart, self.ystart, self.xbody, self.ybody + 10, width = 3)       
        
            ResistorCanvas.delete(self.body)
            self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))
            
            ResistorCanvas.delete(self.resistance_text)
            self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))            
        
            self.data['x'] = event.x
            self.data['y'] = event.y  
    
    def get2_press(self, event):
        self.data['x'] = event.x
        self.data['y'] = event.y
    
    def get2_release(self, event):
        global coord_points
    
        closest_point_num = closest_item(self.data['x'], self.data['y'], coord_points)
        
        self.endpoint = closest_point_num
        
        rsave_info[self.num][7] = self.endpoint
        
        calculation_info[self.num - 1][1] = self.endpoint
        
        delta_x = coord_points[closest_point_num][0] - self.data['x']
        delta_y = coord_points[closest_point_num][1] - self.data['y']        
        
        self.xend += delta_x
        self.yend += delta_y
        
        rsave_info[self.num][4] = self.xend
        rsave_info[self.num][5] = self.yend       
        
        ResistorCanvas.move(self.get2, delta_x, delta_y)
    
        ResistorCanvas.delete(self.line2)
        self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)        
        
        self.data['x'] = 0
        self.data['y'] = 0
        
        ResistorCanvas.delete(self.get2)
        self.get2 = ResistorCanvas.create_oval(self.xend + 3, self.yend + 3, self.xend - 3, self.yend - 3, width = 0, tags = 'get2' + str(self.num), fill = 'black')
        
        ResistorCanvas.delete(self.body)
        self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))        
    
        ResistorCanvas.delete(self.resistance_text)
        self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))    
    
    def get2_motion(self, event):
        if event.x > 0 and event.x < 400 and event.y > 0 and event.y < 400:
            delta_x = event.x - self.data['x']
            delta_y = event.y - self.data['y']
            
            self.xend += delta_x
            self.yend += delta_y
            
            rsave_info[self.num][4] = self.xend
            rsave_info[self.num][5] = self.yend            
            
            ResistorCanvas.move(self.get2, delta_x, delta_y)
            
            ResistorCanvas.delete(self.line2)
            self.line2 = ResistorCanvas.create_line(self.xbody + 40, self.ybody + 10, self.xend, self.yend, width = 3)       
        
            ResistorCanvas.delete(self.body)
            self.body = ResistorCanvas.create_rectangle(self.xbody, self.ybody, self.xbody + 40, self.ybody + 20, width = 3, fill = 'white', tags = 'resistor' + str(self.num))               
        
            ResistorCanvas.delete(self.resistance_text)
            self.resistance_text = ResistorCanvas.create_text(self.xbody + 20, self.ybody + 10, text = 'R' + str(self.num), justify = 'center', tags = 'resistor' + str(self.num))        
        
            self.data['x'] = event.x
            self.data['y'] = event.y    

'''
Need to write:
Example = resistor()
Example.num = examplenum
Example.load(ResistorCanvas)
'''

def CreateResistor(event):
    global ResistorCanvas, ResistorNum, Resistor
    new_one = resistor()
    new_one.num = ResistorNum
    ResistorNum += 1
    new_one.load(ResistorCanvas, Resistor)

def CreatePoint(event):
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    PointNum += 1
    coord_points.append([10, 10])
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_1():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 10
    new_one.ypoint = 200
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_2():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 380
    new_one.ypoint = 200
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_3():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 195
    new_one.ypoint = 10
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_4():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 195
    new_one.ypoint = 390
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_5():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 10
    new_one.ypoint = 10
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_6():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 10
    new_one.ypoint = 390
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_7():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 380
    new_one.ypoint = 10
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)

def CreatePoint_8():
    global ResistorCanvas, PointNum, Resistor, coord_points
    new_one = point()
    new_one.num = PointNum
    new_one.color = 'red'
    new_one.xpoint = 380
    new_one.ypoint = 390
    PointNum += 1
    new_one.load_point(ResistorCanvas, Resistor)


def calculation(calculation_info, ResistorNum, PointNum, s, f):
    N = PointNum
    M = ResistorNum - 1
    matrix = [[0 for i in range (N + M - 2)] for j in range (N + M - 2)]
    vector = [[0] for i in range (N + M - 2)]
    currents = []
    EMF = 1
    for i in range (M):
        S = calculation_info[i][0]
        T = calculation_info[i][1]
        R = calculation_info[i][2]
        if S == s:
            S = 0
        elif S < s:
            S += 1
        if T == s:
            T = 0
        elif T < s:
            T += 1
        if S == f:
            S = N - 1
        elif S > f:
            S -= 1
        if T == f:
            T = N - 1
        elif T > f:
            T -= 1        
        if S == 0:
            vector[i][0] += EMF
            currents.append(i) 
        elif S != N - 1:
            matrix[i][M + S - 1] -= 1
            matrix[M + S - 1][i] -= 1
        if T == 0:
            vector[i][0] -= EMF
            currents.append(i)
        elif T != N - 1:
            matrix[i][M + T - 1] += 1
            matrix[M + T - 1][i] += 1
        matrix[i][i] += R
    matrix = scipy.array(matrix)
    vector = scipy.array(vector)
    ans = numpy.linalg.solve(matrix, vector).tolist()
    currentsum = 0
    for current in currents:
        currentsum += abs(ans[current][0])
    ansR = EMF / currentsum
    return ansR

def clamp_OK_action(event):
    global clamp_1, clamp_2, ClampsWindow, clamp_num
    try:
        s = int(clamp_1.get()) - 1
        f = int(clamp_2.get()) - 1
        
        if 0 > s or 0 > f or clamp_num - 1 < f or clamp_num - 1 < f:
            raise ValueError
        GetAnswer_in_GetAnswer(min(s, f), max(s, f))
        
        ClampsWindow.destroy()
    except ValueError:
        pass

def GetAnswer(event):
    global clamp_1, clamp_2, ClampsWindow
    if clamp_num > 2:
        ClampsWindow = Toplevel(Resistor)
        ClampsWindow.grab_set()
        ClampsWindow.focus_force()
        ClampsWindow.minsize(width = 200, height = 160)
        ClampsWindow.maxsize(width = 200, height = 160)
        ClampsWindow.title('Choose clamps')
        
        clamp_1_info = Label(ClampsWindow, text = 'Enter the number\nof the first clamp:')
        clamp_1_info.place(x = 0, y = 0, width = 200, height = 40)
    
        clamp_1 = Entry(ClampsWindow)
        clamp_1.place(x = 0, y = 40, width = 200, height = 20)
        
        clamp_2_info = Label(ClampsWindow, text = 'Enter the number\nof the second clamp:')
        clamp_2_info.place(x = 0, y = 60, width = 200, height = 40)
    
        clamp_2 = Entry(ClampsWindow)
        clamp_2.place(x = 0, y = 100, width = 200, height = 20)
        
        clamp_OK_but = Button(ClampsWindow, text = 'OK')
        clamp_OK_but.place(x = 0, y = 120, width = 200, height = 40)
        clamp_OK_but.bind('<Button-1>', clamp_OK_action)        
    else:
        GetAnswer_in_GetAnswer(0, 1)

def GetAnswer_in_GetAnswer(s, f):
    global calculation_info, ResistorNum, PointNum, clamp_num
    
    AnswerWindow = Toplevel(Resistor)
    AnswerWindow.grab_set()
    AnswerWindow.focus_force()
    AnswerWindow.minsize(width = 200, height = 40)
    AnswerWindow.maxsize(width = 200, height = 40)
    AnswerWindow.title('Answer')         
    
    total_resistance = calculation(calculation_info, ResistorNum, PointNum, s, f)
    answer = Label(AnswerWindow, text = 'The total resistance of the circuit is\n' + str(round(total_resistance, 3)) + ' Ohm.')
    answer.place(x = 0, y = 0, width = 200, height = 40) 

def Help():
    showinfo('Help', 'Press button "Create resistor" to create resistors.\nPress button "Create point" to create connecting points.\nPress left mouse button to move resistors and connecting points.\nPress right mouse button to change resistance of resistor.\nPress button "Get answer" to get total resistans of the circuit.\n\nIn "File" menu:\nPress "Save" to save your circuit.\nPress "Load" to load your old circuit.\nPress "Clear" to delete all elements in your circuit.')

def About():
    showinfo('About', 'Product: Resistor\n\nVersion: 1.6.3.2\n\nRelease date: 03.01.2017\n\nDevelopers:\nIgor Korkin\nkorkin170202@gmail.com\nArseniy Nestyuk\narseniy.nestyuk@gmail.com')

def Save():
    global rsave_info, psave_info, ResistorNum, PointNum, are, resistors_resistances, clamp_num
    os.chmod('Save.txt', 666)
    file_to_save = open('Save.txt', 'w')
    file_to_save.write(str(clamp_num) + '\n')
    file_to_save.write(str(PointNum) + '\n')
    for i in range(PointNum):
        for j in range(3):
            psave_info[i][j] = str(psave_info[i][j])        
        file_to_save.write(' '.join(psave_info[i]) + '\n')
    file_to_save.write(str(ResistorNum - 1) + '\n')
    for i in range(1, ResistorNum):
        for j in range(9):
            rsave_info[i][j] = str(rsave_info[i][j])
        file_to_save.write(' '.join(rsave_info[i]) + '\n')
    are = True#all resistors are equal
    if resistors_resistances != [resistors_resistances[0] for i in range (ResistorNum - 1)]:
        are = False    
    if are:
        file_to_save.write('3\nare\n')
    else:
        file_to_save.write('2\n')
    file_to_save.write('minRN ' + str(ResistorNum - 1) + '\n')
    file_to_save.write('maxRN ' + str(ResistorNum - 1) + '\n')
    file_to_save.close()
    os.chmod('Save.txt', 777)

def Load():
    global rsave_info, psave_info, ResistorNum, PointNum, ResistorCanvas, Resistor, clamp_num
    try:
        Clear()
        
        file_to_load = open('Save.txt', 'r')
        clamp_num = int(file_to_load.readline())
        PointNum = int(file_to_load.readline())
        for i in range(PointNum):
            line = list(map(str, file_to_load.readline().split()))
            for j in range(2):
                line[j] = int(line[j])
            new_one = point()
            new_one.num = i
            new_one.xpoint = line[0]
            new_one.ypoint = line[1]
            new_one.color = line[2]
            
            coord_points.append([new_one.xpoint, new_one.ypoint])
        
            new_one.load_point(ResistorCanvas, Resistor)
        ResistorNum = int(file_to_load.readline()) + 1
        for i in range (1, ResistorNum):
            line = list(map(float, file_to_load.readline().split()))
        
            for j in range(8):
                line[j] = int(line[j])
        
            new_one = resistor()
            new_one.num = i
            new_one.xbody = line[0]
            new_one.ybody = line[1]
            new_one.xstart = line[2]
            new_one.ystart = line[3]
            new_one.xend = line[4]
            new_one.yend = line[5]
            new_one.startpoint = line[6]
            new_one.endpoint = line[7]
            new_one.resistance = line[8]
        
            new_one.load(ResistorCanvas, Resistor)
    except:
        two_clamps()

def Clear():
    global rsave_info, psave_info, ResistorNum, PointNum, ResistorCanvas, coord_points, resistors_resistances, calculation_info
    ResistorCanvas.delete('all')
    
    coord_points = []
    resistors_resistances = []
    calculation_info = []
    
    psave_info = []
    rsave_info = ['#']
    
    ResistorNum = 1
    PointNum = 0    
    
    resistance_label.configure(text = 'There are no resistors', justify = 'center', anchor = 'center')

def two_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 2
    coord_points = [[10, 200], [380, 200]]
    
    CreatePoint_1()
    CreatePoint_2()  

def three_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 3
    coord_points = [[10, 200], [380, 200], [195, 10]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()     

def four_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 4
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()      
    
def five_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 5
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390], [10, 10]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()
    CreatePoint_5()     
    
def six_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 6
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390], [10, 10], [10, 390]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()
    CreatePoint_5()
    CreatePoint_6()      
    
def seven_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 7
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390], [10, 10], [10, 390], [380, 10]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()
    CreatePoint_5()
    CreatePoint_6()
    CreatePoint_7()      
    
def eight_clamps():
    global coord_points, clamp_num
    
    Clear()
    
    clamp_num = 8
    coord_points = [[10, 200], [380, 200], [195, 10], [195, 390], [10, 10], [10, 390], [380, 10], [380, 390]]
    
    CreatePoint_1()
    CreatePoint_2()
    CreatePoint_3()
    CreatePoint_4()
    CreatePoint_5()
    CreatePoint_6()
    CreatePoint_7()
    CreatePoint_8()    

CreatePoint_1()
CreatePoint_2()

createresistor = Button(ResistorButtons, text = 'Create resistor')
createresistor.bind('<Button-1>', CreateResistor)
createresistor.place(x = 0, y = 0, width = 200, height = 40)

createpoint = Button(ResistorButtons, text = 'Create point')
createpoint.bind('<Button-1>', CreatePoint)
createpoint.place(x = 0, y = 40, width = 200, height = 40)

getanswer = Button(ResistorButtons, text = 'Get answer')
getanswer.bind('<Button-1>', GetAnswer)
getanswer.place(x = 0, y = 360, width = 200, height = 40)

menu = Menu(Resistor)
Resistor.config(menu = menu)

file_menu = Menu(menu)
menu.add_cascade(label = 'File', menu = file_menu)
file_menu.add_command(label = 'Save', command = Save)
file_menu.add_command(label = 'Load', command = Load)

help_menu = Menu(menu)
menu.add_cascade(label = 'Help', menu = help_menu)
help_menu.add_command(label = 'Help', command = Help)
help_menu.add_command(label = 'About', command = About)

clamps_menu = Menu(menu)
menu.add_cascade(label = 'Clamps', menu = clamps_menu)
clamps_menu.add_command(label = 'Two clamps', command = two_clamps)
clamps_menu.add_command(label = 'Three clamps', command = three_clamps)
clamps_menu.add_command(label = 'Four clamps', command = four_clamps)
clamps_menu.add_command(label = 'Five clamps', command = five_clamps)
clamps_menu.add_command(label = 'Six clamps', command = six_clamps)
clamps_menu.add_command(label = 'Seven clamps', command = seven_clamps)
clamps_menu.add_command(label = 'Eight clamps', command = eight_clamps)

Resistor.mainloop()
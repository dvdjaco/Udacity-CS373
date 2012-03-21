# ROBOT LOCALIZATION BASED ON PARTICLE FILTERS
# Programmed by Juan Carlos Kuri Pinto and the Udacity team.

# COMMANDS:
# LEFT ARROW: Turn robot counter-clockwise.
# RIGHT ARROW: Turn robot clockwise.
# UP ARROW: Move robot forward.
# MOUSE CLICK: Hijack robot.
# ESCAPE KEY or Close Button: Quit demo.

# Notes: 
# I add 5 new random particles in each iteration in order to explore the hypothesis space better.
# Particles with more likelihood are painted in a darker way. The robot gets localized really fast!!!
# The arrow keys should work once you click on the canvas in order to gain focus. It's a TCL/TK trick. =)

from Tkinter import *
from math import *
import random

# Robot

landmarks  = [[20.0, 20.0], [80.0, 80.0], [20.0, 80.0], [80.0, 20.0]]
world_size = 100.0
forward_noise=0.05
turn_noise=0.05
sense_noise=5.0

class robot:
    
    def __init__(self):
        self.x =random.random() * world_size
        self.y =random.random() * world_size
        self.orientation = random.random() * 2.0 * pi
        self.forward_noise = 0.0
        self.turn_noise    = 0.0
        self.sense_noise   = 0.0
        self.w=0.
        self.alpha=0.

    def clone_robot(self):
        nr=robot()
        nr.x=self.x
        nr.y=self.y
        nr.orientation=self.orientation
        nr.forward_noise=self.forward_noise
        nr.turn_noise=self.turn_noise
        nr.sense_noise=self.sense_noise
        nr.w=self.w
        nr.alpha=self.alpha
        return nr
    
    def set(self, new_x, new_y, new_orientation):
        if new_x < 0 or new_x >= world_size:
            raise ValueError, 'X coordinate out of bound'
        if new_y < 0 or new_y >= world_size:
            raise ValueError, 'Y coordinate out of bound'
        if new_orientation < 0 or new_orientation >= 2 * pi:
            raise ValueError, 'Orientation must be in [0..2pi]'
        self.x = float(new_x)
        self.y = float(new_y)
        self.orientation = float(new_orientation)
    
    def set_noise(self, new_f_noise, new_t_noise, new_s_noise):
        # makes it possible to change the noise parameters
        # this is often useful in particle filters
        self.forward_noise = float(new_f_noise);
        self.turn_noise    = float(new_t_noise);
        self.sense_noise   = float(new_s_noise);
    
    def sense(self):
        Z = []
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            dist += random.gauss(0.0, self.sense_noise)
            Z.append(dist)
        return Z
    
    def move(self, turn, forward):
        if forward < 0:
            raise ValueError, 'Robot cant move backwards'         
        # turn, and add randomness to the turning command
        orientation = self.orientation + float(turn) + random.gauss(0.0, self.turn_noise)
        orientation %= 2 * pi
        # move, and add randomness to the motion command
        dist = float(forward) + random.gauss(0.0, self.forward_noise)
        x = self.x + (cos(orientation) * dist)
        y = self.y + (sin(orientation) * dist)
        x %= world_size    # cyclic truncate
        y %= world_size
        # set particle
        res = robot()
        res.set(x, y, orientation)
        res.set_noise(self.forward_noise, self.turn_noise, self.sense_noise)
        return res
    
    def Gaussian(self, mu, sigma, x):
        # calculates the probability of x for 1-dim Gaussian with mean mu and var. sigma
        return exp(- ((mu - x) ** 2) / (sigma ** 2) / 2.0) / sqrt(2.0 * pi * (sigma ** 2))
    
    def measurement_prob(self, measurement):    
        # calculates how likely a measurement should be
        prob = 1.0;
        for i in range(len(landmarks)):
            dist = sqrt((self.x - landmarks[i][0]) ** 2 + (self.y - landmarks[i][1]) ** 2)
            prob *= self.Gaussian(dist, self.sense_noise, measurement[i])
        return prob
    
    def __repr__(self):
        return '[x=%.6s y=%.6s orient=%.6s]' % (str(self.x), str(self.y), str(self.orientation))

    def draw_robot(self,canvas):
        draw_particle(canvas,self.x,self.y,self.orientation,2,"red")

    def draw_particle(self,canvas):
        global particles
        max_alpha=max([particle.alpha for particle in particles])
        max_alpha=1 if max_alpha==0. else max_alpha
        probability=self.alpha/max_alpha
        minimum=30
        intensity=int(round((255-minimum)*(1.-probability)))
        color=rgb_to_hex((intensity,intensity,intensity))
        draw_particle(canvas,self.x,self.y,self.orientation,1,color)

def eval(r, p):
    sum = 0.0;
    for i in range(len(p)): # calculate mean error
        dx = (p[i].x - r.x + (world_size/2.0)) % world_size - (world_size/2.0)
        dy = (p[i].y - r.y + (world_size/2.0)) % world_size - (world_size/2.0)
        err = sqrt(dx * dx + dy * dy)
        sum += err
    return sum / float(len(p))

def new_particle(forward_noise,turn_noise,sense_noise):
    particle=robot()
    particle.set_noise(forward_noise,turn_noise,sense_noise)
    return particle

def create_new_random_particles():
    global N,particles,random_particles
    N=100
    random_particles=5
    particles=[new_particle(forward_noise,turn_noise,sense_noise) for i in range(N)]

def measure_particles():
    global particles,myrobot
    Z=myrobot.sense()
    for particle in particles:
        particle.w=particle.measurement_prob(Z)
    s=sum([particle.w for particle in particles])
    for particle in particles:
        particle.alpha=particle.w/s

def move_particles():
    global particles,forward,turn
    for i in range(N):
        particles[i]=particles[i].move(turn,forward)

def sample_index():
    global particles
    rnd=random.random()
    s=0
    for i in range(N):
        alpha=particles[i].alpha
        if s<=rnd and rnd<s+alpha:
            return i
        s=s+alpha
    return -1

def resampling():
    new_particles=[particles[sample_index()].clone_robot() for i in range(N)]
    return new_particles

def resampling_thrun():
    new_particles=[]
    index = int(random.random() * N)
    beta = 0.0
    mw = max([particle.w for particle in particles])
    for i in range(N):
        beta += random.random() * 2.0 * mw
        while beta>particles[index].w:
            beta -= particles[index].w
            index = (index + 1) % N
        new_particles.append(particles[index])
    return new_particles

def replace_some_random_particles():
    global particles
    for i in range(random_particles): particles[int(random.random()*N)]=new_particle(forward_noise,turn_noise,sense_noise)

def iterate_particles():
    global particles
    move_particles()
    measure_particles()
    #particles=resampling()
    particles=resampling_thrun()
    replace_some_random_particles()

# Tkinter

def rgb_to_hex(rgb_tuple):
    return '#%02x%02x%02x'%rgb_tuple

def draw_circle(canvas,x,y,radius,color):
    coords=x-radius,y-radius,x+radius,y+radius
    canvas.create_oval(coords,fill=color,outline=color)

def draw_particle(canvas,x,y,heading,radius,color):
    x=x*5
    y=y*5
    radius=radius*5
    draw_circle(canvas,x,y,radius,color)
    canvas.create_line(x,y,x+3*radius*cos(heading),y+3*radius*sin(heading),fill=color)

def draw_mark(canvas,x,y):
    global myrobot
    radius=4
    draw_circle(canvas,x*5,y*5,radius*5,"blue")
    canvas.create_line(myrobot.x*5,myrobot.y*5,x*5,y*5,fill="blue")

def center_window(root):
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    root.update_idletasks()
    w=root.winfo_reqwidth()
    h=root.winfo_reqheight()
    x=ws/2-w/2 
    y=hs/2-h/2
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))

myrobot=new_particle(0.05,0.01,0.1)
create_new_random_particles()

def draw_canvas(canvas):
    global myrobot
    canvas.delete(ALL)
    for landmark in landmarks:
        draw_mark(canvas,landmark[0],landmark[1])
    for particle in particles:
        particle.draw_particle(canvas)
    myrobot.draw_robot(canvas)
    
def move():
    global myrobot,forward,turn
    forward=0.5 if UP==1 else 0.
    turn=0.
    if LEFT==1: turn+=-0.05
    if RIGHT==1: turn+=0.05
    myrobot=myrobot.move(turn,forward)
    iterate_particles()

def iterate():
    draw_canvas(canvas)
    move()
    top.after(20,iterate)

afterId=None
UP=0
LEFT=0
RIGHT=0

def keyPressed(event):
    global afterId
    if afterId==None:
        keyDown(event)
    else:
        top.after_cancel(afterId)
        afterId=None

def keyReleased(event):
    global afterId
    afterId=top.after_idle(lambda: keyReleasedAfterIdle(event))

def keyReleasedAfterIdle(event):
    global afterId
    if afterId!=None:
        keyUp(event)
    afterId=None

KEY_UP=111
KEY_LEFT=113
KEY_RIGHT=114

def keyDown(event):
    global UP,LEFT,RIGHT
    code=event.keycode
    if code==KEY_UP: UP=1
    if code==KEY_LEFT: LEFT=1
    if code==KEY_RIGHT: RIGHT=1

def keyUp(event):
    global UP,LEFT,RIGHT
    code=event.keycode
    if code==KEY_UP: UP=0
    if code==KEY_LEFT: LEFT=0
    if code==KEY_RIGHT: RIGHT=0

def mouse(event):
    hijack_robot(event.x/5.,event.y/5.)    

def hijack_robot(x,y):
    global myrobot
    myrobot.x=x
    myrobot.y=y
    myrobot.orientation=random.random()*3.1416*2.
    create_new_random_particles()

def gui():
    global canvas,top
    top=Tk()
    canvas = Canvas(top, bg="white", height=500, width=500)
    canvas.pack(fill=BOTH, expand=1)
    top.title('ROBOT LOCALIZATION BASED ON PARTICLE FILTERS (by jckuri)')
    top.bind('<Key-Escape>',lambda e: e.widget.destroy())
    top.bind("<KeyPress>", lambda event: keyPressed(event) )
    top.bind("<KeyRelease>", lambda event: keyReleased(event) )
    top.bind("<Button-1>",lambda event: mouse(event))
    top.wm_attributes("-topmost", 1)
    top.resizable(FALSE,FALSE)
    center_window(top)
    top.after(1000,iterate)
    top.mainloop()

gui()

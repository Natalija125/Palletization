# Type help("robolink") or help("robodk") for more information
# Press F5 to run the script
# Documentation: https://robodk.com/doc/en/RoboDK-API.html
# Reference:     https://robodk.com/doc/en/PythonAPI/index.html
# Note: It is not required to keep a copy of this file, your python script is saved with the station
from robolink import *    # RoboDK API
from robodk import *      # Robot toolbox
from math import *
RDK = Robolink()
import random

robot = RDK.Item('ABB IRB 460')
robot_base = RDK.Item('ABB IRB 460 Base')
tool = RDK.Item('RobotiQ EPick Four Vacuum Cup')
panel_item = RDK.Item('box')
panel_item.setPose(robodk.Pose(1745,50,50,0,0,0))
panel_item.Copy()
palet_item = RDK.Item('Plane 1m x 1m')
palet_item.setPose(robodk.Pose(0,1200,-130,0,0,0))


grab_item = RDK.Item('grab_item')
##top_corner = RDK.AddFrame('top_corner')
##top_corner.setPose(robodk.Pose(500,700, -130,90,0,0))
put_away_item = RDK.Item('put_away_item')
home_pos = RDK.Item('home_pos')


class Palet:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.mat = dict()
        return

    def __setitem__(self, key, value):
        self.mat[key] = value
        return

    def __getitem__ (self, key):
        return self.mat.get(key, 0)

    def __repr__(self):
        palet_s = ''
        
        for i in range(self.n):
            for j in range(self.m):
                palet_s += '{0:3}'.format(self[i,j])
            palet_s += '\n'

        return palet_s

palet = Palet(11,10)


panel_list = [[200,300,100], [300,300,100], [500,200,100], [500,200,100], [400,200,100], [300,200,100], [300,500,100], [700,200,100], [200,400,100], [100,100,100], [200,200,100], [200,300,100], [300,100,100]]
first_panel = 0
dim_a = 0
dim_b = 0

if (first_panel == 0):
    panel_item_copy = RDK.Paste()
    panel_item_copy.setName('box_1')
    panel_item_copy.setPose(robodk.Pose(1235, 50+((panel_list[0][1]-100)/2), 50, 0, 0, 0))
    panel_item_copy.Scale([panel_list[0][0]/100, panel_list[0][1]/100, panel_list[0][2]/100])
    panel_item_copy.setColor([random.random(), random.random(), random.random()])
    
    dim_a = (panel_list[0][0])//100
    dim_b = (panel_list[0][1])//100

    for i in range(dim_a):
        for j in range(dim_b):
            palet[i,j] = 1

    robot.MoveJ(grab_item.Pose()*transl([(panel_list[0][1])/2, 0, 0]))
    tool.AttachClosest()
    robot.MoveL(grab_item.Pose()*transl([(panel_list[0][1])/2, 0, 100]))
    robot.MoveJ((put_away_item.Pose()*transl([(panel_list[0][0])/2, (panel_list[0][1])/2, 100]))*rotx(0)*roty(0)*rotz(pi/2))
    robot.MoveL((put_away_item.Pose()*transl([(panel_list[0][0])/2, (panel_list[0][1])/2, 0]))*rotx(0)*roty(0)*rotz(pi/2))
    ##robot.MoveL(put_away_item.Pose()*transl([((m+1)*100)/2, ((n+1)*100)/2, 0]))
    tool.DetachAll()
    robot.MoveL((put_away_item.Pose()*transl([(panel_list[0][0])/2, (panel_list[0][1])/2, 100]))*rotx(0)*roty(0)*rotz(pi/2))

    first_panel = 1

print (palet)

if (first_panel == 1):

    for i in range(1, len(panel_list)):
        panel_item_copy = RDK.Paste()
        panel_item_copy.setName('box_1')
        panel_item_copy.setPose(robodk.Pose(1235, 50+((panel_list[i][1]-100)/2), 50, 0, 0, 0))
        panel_item_copy.Scale([panel_list[i][1]/100, panel_list[i][0]/100, panel_list[i][2]/100])
        panel_item_copy.setColor([random.random(), random.random(), random.random()])
        
        not_taken = True
        
        dim_a = (panel_list[i][0])//100
        dim_b = (panel_list[i][1])//100
        dim_cout_v = 0
        dim_cout_h = 0
        
        for j in range(11):
            if (not_taken == False):
                break

            dim_cout_v = 0
            dim_cout_h = 0
                
            for k in range(10):
                if (palet[j,k] == 0):
                    dim_cout_h = 0
                    for l in range(k, 10):
                        if (palet[j,l] == 0):
                            dim_cout_h += 1
                        else:
                            break
                            

                    print(dim_cout_h)

                    for l in range(j, 11):
                        if (palet[l,k] == 0):
                            dim_cout_v += 1
                        else:
                            break

                    print(dim_cout_v)

            
                    if (dim_a <= dim_cout_v and dim_b <= dim_cout_h):
                        for m in range(j, j+dim_a):
                            for n in range(k, k+dim_b):
                                palet[m,n] = 1
                        robot.MoveJ(grab_item.Pose()*transl([(panel_list[i][1])/2, 0, 0]))
                        tool.AttachClosest()
                        robot.MoveL(grab_item.Pose()*transl([(panel_list[i][1])/2, 0, 100]))
                        robot.MoveJ(put_away_item.Pose()*transl([j*100+(panel_list[i][0])/2, k*100+(panel_list[i][1])/2, 100]))#*rotx(0)*roty(0)*rotz(pi/2))
                        robot.MoveL(put_away_item.Pose()*transl([j*100+(panel_list[i][0])/2, k*100+(panel_list[i][1])/2, 0]))#*rotx(0)*roty(0)*rotz(pi/2))
                        ##robot.MoveL(put_away_item.Pose()*transl([(m+1)*100/2, (n+1)*100/2, 0]))
                        tool.DetachAll()
                        robot.MoveL(put_away_item.Pose()*transl([j*100+(panel_list[i][0])/2, k*100+(panel_list[i][1])/2, 100]))#*rotx(0)*roty(0)*rotz(pi/2))

                        dim_cout_v = 0
                        dim_cout_h = 0
                        not_taken = False
                        break

                    elif (dim_b <= dim_cout_v and dim_a <= dim_cout_h):
                        for m in range(j, j+dim_b):
                            for n in range(k, k+dim_a):
                                palet[m,n] = 1
                        robot.MoveJ(grab_item.Pose()*transl([(panel_list[i][1])/2, 0, 0]))
                        tool.AttachClosest()
                        robot.MoveL(grab_item.Pose()*transl([(panel_list[i][1])/2, 0, 100]))
                        robot.MoveJ((put_away_item.Pose()*transl([j*100+(panel_list[i][1])/2, k*100+(panel_list[i][0])/2, 100]))*rotx(0)*roty(0)*rotz(pi/2))
                        robot.MoveL((put_away_item.Pose()*transl([j*100+(panel_list[i][1])/2, k*100+(panel_list[i][0])/2, 0]))*rotx(0)*roty(0)*rotz(pi/2))
                        ##robot.MoveL(put_away_item.Pose()*transl([((m+1)*100)/2, ((n+1)*100)/2, 0]))
                        tool.DetachAll()
                        robot.MoveL((put_away_item.Pose()*transl([j*100+(panel_list[i][1])/2, k*100+(panel_list[i][0])/2, 100]))*rotx(0)*roty(0)*rotz(pi/2))
                        
                        dim_cout_v = 0
                        dim_cout_h = 0
                        not_taken = False
                        break

                    else:
                        dim_cout_v = 0
                        dim_cout_h = 0

          

        print (palet)


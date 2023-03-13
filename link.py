import random
import constants as c

class LINK:

    def __init__(self, seg_name, cube_pos, seg_size, color_name, rgb, parent_size=None, joint_name=None, parent_name=None, joint_pos=None, joint_axis=None, isRoot=False, dir=None, prev_dir=None, child1=None, child2=None):
        self.isRoot = isRoot
        self.dir = dir
        self.prev_dir = prev_dir

        self.seg_name = seg_name
        self.cube_pos = cube_pos
        self.seg_size = seg_size
        self.color_name = color_name
        self.rgb = rgb

        self.joint_name = joint_name
        self.parent_name = parent_name
        self.joint_pos = joint_pos
        self.joint_axis = joint_axis
        self.parent_size = parent_size

        self.child1 = child1
        self.child2 = child2
    
    def mutate(self):
        if random.random() < 0.3:
            self.joint_axis = random.choice(["0 0 1", "0 1 0", "1 0 0"])
        if self.dir is not None:
            shrink = 0.8
            grow = 1.2
            self.seg_size = [self.seg_size[0]*random.uniform(shrink, grow), self.seg_size[1]*random.uniform(shrink, grow), self.seg_size[2]*random.uniform(shrink, grow)]
            self.seg_size[0] = min(self.seg_size[0], 2)
            self.seg_size[0] = max(self.seg_size[0], 0.1)
            self.seg_size[1] = min(self.seg_size[1], 2)
            self.seg_size[1] = max(self.seg_size[1], 0.1)
            self.seg_size[2] = min(self.seg_size[2], 2)
            self.seg_size[2] = max(self.seg_size[2], 0.1)
            
            if self.dir == 0:
                self.cube_pos = [self.seg_size[0]/2, 0, 0]
            if self.dir == 1:
                self.cube_pos = [0, self.seg_size[1]/2, 0]
            if self.dir == 2:
                self.cube_pos = [0, 0, self.seg_size[2]/2]
            if self.child1:
                self.child1.adjust(self.seg_size)
            if self.child2:
                self.child2.adjust(self.seg_size)


    def adjust(self, parent_size):
        if self.dir == 0: # x
            if self.prev_dir == 0:
                self.joint_pos = [parent_size[0], 0, 0]
            elif self.prev_dir == 1:
                self.joint_pos = [parent_size[0]/2, parent_size[1]/2, 0]
            else:  # prev_dir == 2
                self.joint_pos = [parent_size[0]/2, 0, parent_size[2]/2]
        elif self.dir == 1: # y
            if self.prev_dir == 1:
                self.joint_pos = [0, parent_size[1], 0]
            elif self.prev_dir == 0:
                self.joint_pos = [parent_size[0]/2, parent_size[1]/2, 0]
            else: # prev_dir == 2
                self.joint_pos = [0, parent_size[1]/2, parent_size[2]/2]
        else:
            if self.prev_dir == 2:
                self.joint_pos = [0, 0, parent_size[2]]
            elif self.prev_dir == 1:
                self.joint_pos = [0, parent_size[1]/2, parent_size[2]/2]
            else:  # prev_dir == 0
                self.joint_pos = [parent_size[0]/2, 0, parent_size[2]/2]  
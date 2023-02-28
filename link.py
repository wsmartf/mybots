import random
import constants as c

class LINK:

    def __init__(self, seg_name, cube_pos, seg_size, color_name, rgb, parent_size=None, joint_name=None, parent_name=None, joint_pos=None, joint_axis=None, isRoot=False, dir=None):
        self.isRoot = isRoot
        self.dir = dir

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
    
    def mutate(self):
        dir = None
        if random.random() < 0.3:
            self.joint_axis = random.choice(["0 0 1", "0 1 0", "1 0 0"])
        if random.random() < 0.5:
            if dir is not None:
                self.seg_size = [self.seg_size[0]*random.uniform(2, 0.2), self.seg_size[1]*random.uniform(2, 0.2), self.seg_size[2]*random.uniform(2, 0.2)]
                if dir == 0:
                    self.cube_pos = [self.seg_size[0]/2, 0, 0]
                if dir == 1:
                    self.cube_pos = [0, self.seg_size[1]/2, 0]
                if dir == 2:
                    self.cube_pos = [0, 0, self.seg_size[2]/2]
        return dir

        
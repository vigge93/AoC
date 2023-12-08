from dataclasses import dataclass

@dataclass
class Region:
    start_x:int
    end_x:int
    start_y:int
    end_y:int
    start_z:int
    end_z:int
    sign:int = 1

    def remove(self, start_x, end_x, start_y, end_y, start_z, end_z):
        if end_x < self.start_x or end_y < self.start_y or end_z < self.start_z:
            return None
        if start_x > self.end_x or start_y > self.end_y or start_z > self.end_z:
            return None
        nr = Region(max(self.start_x, start_x), min(self.end_x, end_x), max(self.start_y, start_y), min(self.end_y, end_y), max(self.start_z, start_z), min(self.end_z, end_z), -self.sign)
        return nr

    @property
    def volume(self):
        return (self.end_x - self.start_x + 1)*(self.end_y - self.start_y + 1)*(self.end_z - self.start_z + 1)
                

cuboids = []

with open('day22.txt', 'r') as f:
    for line in f:
        action, cuboid = line.strip().split()
        x, y, z = cuboid.split(',')
        x_start, x_end = [int(n) for n in x[2:].split('..')]
        y_start, y_end = [int(n) for n in y[2:].split('..')]
        z_start, z_end = [int(n) for n in z[2:].split('..')]
        new_cuboids = []
        nr = Region(x_start, x_end, y_start, y_end, z_start, z_end)
        for cuboid in cuboids:
            nc = cuboid.remove(nr.start_x, nr.end_x, nr.start_y, nr.end_y, nr.start_z, nr.end_z)
            if nc:
                new_cuboids.append(nc)
        if action == 'on':
            new_cuboids.append(nr)
        cuboids += new_cuboids
tot_vol = 0
for cuboid in cuboids:
    tot_vol += cuboid.volume*cuboid.sign
print(tot_vol)  
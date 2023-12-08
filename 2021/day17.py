import math
t_x_min, t_x_max, t_y_min, t_y_max = 0, 0, 0, 0
with open('day17.txt', 'r') as f:
    inp = f.read().strip()[13:]
    x_inp, y_inp = inp.split(',')
    x_inp = x_inp[2:].split('..')
    y_inp = y_inp[3:].split('..')
    x_inp = list((int(x) for x in x_inp))
    y_inp = list((int(y) for y in y_inp))
    t_x_min = min(x_inp)
    t_x_max = max(x_inp)
    t_y_min = min(y_inp)
    t_y_max = max(y_inp)

max_vy = 0
valid_vel = []
for vx in range(17, 172):
    start_vx = vx
    for vy in range(-98, 98):
        start_vy = vy
        vx = start_vx
        y = 0
        x = 0
        while x <= t_x_max and y > t_y_min:
            if vx > 0:
                x += vx 
                vx -= 1
            y += vy
            vy -= 1
            if t_x_min <= x <= t_x_max and t_y_min <= y <= t_y_max:
                valid_vel.append((start_vx, start_vy))
                break
print(len(valid_vel))
    # for vy in range(0, 1000):
    #     start_vy = vy
    #     x = 0
    #     y = 0
    #     while x <= t_x_max and y >= t_y_min:
    #         if vx > 0:
    #             x += vx
    #             vx -= 1
    #         y += vy
    #         vy -= 1

    #         if t_x_min <= x <= t_x_max and t_y_min <= y <= t_y_max:
    #             if start_vy > max_vy:
    #                 max_vy = start_vy
print(max_vy)


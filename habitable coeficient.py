import math
L_star = 0.05
#h_z_sun = 1.1633534 # центр життєпридатної зони сонця. пораховано за цим самим алгоритмом, де L_sun = 1 за визначенням

sun_hz_width = 0.42014305024

r_min = math.sqrt(L_star/1.1)
r_max = math.sqrt(L_star/0.53)
#hz_centre = (r_max+r_min)/2.0
hz_width = r_max - r_min

print("Min: " + str(r_min))
print("Max: " + str(r_max))
print("Width of a habitable zone: " + str(hz_width))

#coeficient = hz_centre/h_z_sun
coeficient = hz_width/sun_hz_width
if coeficient < 1:
    print("coeficient = " + str(round(coeficient,4)))
else:
    print("coeficient = " + str(round(math.pow(coeficient,-1),4)))

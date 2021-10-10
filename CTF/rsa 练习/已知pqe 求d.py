import gmpy2

p = 38456719616722997
q = 44106885765559411
e = 65537

s = (p - 1) * (q - 1)
d = gmpy2.invert(e, s)
print("dec: " + str(d))
print ("hex: " +  hex(d))
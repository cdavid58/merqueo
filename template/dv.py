import string

def dv(rut):
    factores = [3, 7, 13, 17, 19, 23, 29, 37, 41, 43, 47, 53, 59, 67, 71]
    rut_ajustado=str(rut).rjust( 15, '0')
    s = sum(int(rut_ajustado[14-i]) * factores[i] for i in range(14)) % 11
    if s > 1:
        return 11 - s
    else:
        return s

print(dv(71673252))
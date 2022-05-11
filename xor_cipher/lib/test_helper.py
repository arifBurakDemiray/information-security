# Arif Burak Demiray - 250201022 - 28.04.2022 - hw1 - ceng418
import math
from .etestresult import TestResult


def prime_factors(number: 'int') -> 'set[int]':

    tempN = number

    factors = set()
    while tempN % 2 == 0:  # divide number until it is odd
        factors.add(2)
        tempN = tempN / 2

    # There can be at-least one prime factor that would be less than sqrt(number)
    for i in range(3, int(math.sqrt(tempN)) + 1, 2):

        while (tempN % i == 0):
            factors.add(i)
            tempN = tempN / i

    if tempN > 2:
        factors.add(tempN)

    return factors


# For testing a and b to be prime element of g
def ab_test(a: 'int', b: 'int', g: 'int') -> 'bool':
    gcdA, _, _ = extended_euclid(g, a)
    gcdB, _, _ = extended_euclid(g, b)

    if (gcdA != 1 or gcdB != 1):
        return False
    return True


# algorithm described in the assignment paper
def primality_test(k: 'int', p: 'int', a: 'int') -> 'TestResult':

    calculation = pow_custom(a, k, p)
    if(calculation == p - 1):
        calculation = -1
    if(calculation not in (1, -1) and k < p - 1):
        return TestResult.COMPOSITE
    elif(calculation == -1 or (calculation == 1 and k % 2 == 1)):
        return TestResult.PRIME
    elif(k < 2):
        return TestResult.FAILED

    return primality_test(int(k / 2), p, a)


# algorithm described in the assignment paper
def generator_test(g: 'int', p: 'int') -> 'bool':
    factors = prime_factors(p - 1)

    failed = False

    for factor in factors:
        result = pow_custom(g, int((p - 1) / factor), p)
        if(result == 1):
            failed = True
            break

    return failed


# it simply does euclidean algorithm
# holds prev state and continu until b not 0
# formula of ax + by = gcd(a,b)
def extended_euclid(a, b):
    newX = 0
    x = 1
    newY = 1
    y = 0
    prevB = b
    gcd = a

    while prevB != 0:
        division = gcd // prevB
        gcd, prevB = prevB, gcd - division * prevB
        x, newX = newX, x - division * newX
        y, newY = newY, y - division * newY
    return [gcd, x, y]


# It simply takes square root and than tooks mod of it until power is not 0
def pow_custom(base, power, mod):
    result = 1
    while power > 0:
        if power % 2 == 1:
            result = (result * base) % mod

        power = power // 2
        base = (base * base) % mod

    return result

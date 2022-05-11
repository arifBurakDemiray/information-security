# Arif Burak Demiray - 250201022 - 28.04.2022 - hw1 - ceng418
import random
from .test_helper import primality_test, generator_test
from .etestresult import TestResult


def primeTest(p: 'int') -> 'bool':
    if(p < 3):
        return False

    results = set()

    for i in range(5):  # try prime test with 5 random number to ensure it is prime
        randomA = random.randint(2, p - 1)
        result = primality_test(p - 1, p, randomA)
        results.add(result)

    if(TestResult.FAILED in results):
        return False
    elif(len(results) == 1 and results.pop() != TestResult.COMPOSITE):
        return True
    else:
        return False


def generatorTest(g: 'int', p: 'int') -> 'bool':
    if(generator_test(g, p)):  # test failed
        return False

    return True

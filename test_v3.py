import pytest

from v3 import SievePrimeFinder, TrialDivisionPrimeFinder, LLMPrimeFinder, StoredPrimeFinder

@pytest.mark.parametrize("finder_class", [SievePrimeFinder, TrialDivisionPrimeFinder, LLMPrimeFinder])
def test_prime_finder(finder_class):
    finder = finder_class()
    assert finder.find_primes_up_to(100) == StoredPrimeFinder().find_primes_up_to(100)

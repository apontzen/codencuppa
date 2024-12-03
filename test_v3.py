import pytest

from v3 import SievePrimeFinder, TrialDivisionPrimeFinder, LLMPrimeFinder, StoredPrimeFinder

@pytest.mark.parametrize("finder_class", [SievePrimeFinder, TrialDivisionPrimeFinder, LLMPrimeFinder])
def test_prime_finder(finder_class):
    test_finder = finder_class()
    trusted_finder = StoredPrimeFinder()

    assert test_finder.find_primes_up_to(100) == trusted_finder.find_primes_up_to(100)

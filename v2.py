def find_primes_up_to(maximum: int) -> list[int]:
    """
    Finds all prime numbers up to a given maximum using the Sieve of Eratosthenes.

    Parameters:
        maximum (int): The upper limit for finding prime numbers.

    Returns:
        list[int]: A list of all prime numbers up to the given maximum.
    """
    if maximum < 2:
        return []


    prime_flags = initialize_prime_list(maximum)
    sieve_non_primes(prime_flags, maximum)
    return extract_primes(prime_flags)


def initialize_prime_list(size: int) -> list[bool]:
    """
    Creates a list representing the primality of numbers from 0 to `size`.

    Parameters:
        size (int): The upper limit for the prime number list.

    Returns:
        list[bool]: A list where True indicates primality.
    """
    prime_list = [True] * (size + 1)
    prime_list[0] = prime_list[1] = False  # 0 and 1 are not prime
    return prime_list


def sieve_non_primes(prime_list: list[bool], limit: int):
    """
    Marks multiples of each prime number as non-prime in the prime list.

    Parameters:
        prime_list (list[bool]): The list of primality flags.
        limit (int): The upper limit for the sieve.
    """
    for number in range(2, int(limit**0.5) + 1):
        if prime_list[number]:  # Process only if number is still prime
            for multiple in range(number * number, limit + 1, number):
                prime_list[multiple] = False


def extract_primes(prime_list: list[bool]) -> list[int]:
    """
    Extracts the list of numbers marked as prime.

    Parameters:
        prime_list (list[bool]): The list of primality flags.

    Returns:
        list[int]: A list of all prime numbers.
    """
    return [index for index, is_prime in enumerate(prime_list) if is_prime]


def main():
    my_primes = find_primes_up_to(100)
    print(my_primes)


if __name__ == "__main__":
    main()
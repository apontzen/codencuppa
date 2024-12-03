from abc import ABC, abstractmethod


class PrimeFinder(ABC):
    """
    Interface for prime-finding algorithms.
    """

    @abstractmethod
    def find_primes_up_to(self, maximum):
        """
        Finds all prime numbers up to a given maximum.

        Parameters:
            maximum (int): The upper limit for finding prime numbers.

        Returns:
            list[int]: A list of all prime numbers up to the given maximum.
        """
        pass


class SievePrimeFinder(PrimeFinder):
    """
    Implementation of PrimeFinder using the Sieve of Eratosthenes.
    """

    def find_primes_up_to(self, maximum):
        """
        Finds all prime numbers up to a given maximum using the Sieve of Eratosthenes.

        Parameters:
            maximum (int): The upper limit for finding prime numbers.

        Returns:
            list[int]: A list of all prime numbers up to the given maximum.
        """
        if maximum < 2:
            return []

        # Initialize a boolean list to represent primality for each number
        is_prime = self._initialize_prime_list(maximum)

        # Eliminate non-prime numbers by marking multiples
        self._sieve_non_primes(is_prime, maximum)

        # Extract and return the list of primes
        return self._extract_primes(is_prime)

    @staticmethod
    def _initialize_prime_list(size):
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

    @staticmethod
    def _sieve_non_primes(prime_list, limit):
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

    @staticmethod
    def _extract_primes(prime_list):
        """
        Extracts the list of numbers marked as prime.

        Parameters:
            prime_list (list[bool]): The list of primality flags.

        Returns:
            list[int]: A list of all prime numbers.
        """
        return [index for index, is_prime in enumerate(prime_list) if is_prime]



class TrialDivisionPrimeFinder(PrimeFinder):
    """
    Implementation of PrimeFinder using the Trial Division algorithm.
    """

    def find_primes_up_to(self, maximum):
        """
        Finds all prime numbers up to a given maximum using Trial Division.

        Parameters:
            maximum (int): The upper limit for finding prime numbers.

        Returns:
            list[int]: A list of all prime numbers up to the given maximum.
        """
        if maximum < 2:
            return []

        primes = []
        for number in range(2, maximum + 1):
            if self._is_prime(number):
                primes.append(number)
        return primes

    @staticmethod
    def _is_prime(number):
        """
        Determines if a number is prime using Trial Division.

        Parameters:
            number (int): The number to check for primality.

        Returns:
            bool: True if the number is prime, False otherwise.
        """
        if number < 2:
            return False
        for divisor in range(2, int(number**0.5) + 1):
            if number % divisor == 0:
                return False
        return True

class StoredPrimeFinder(PrimeFinder):
    """
    Implementation of PrimeFinder using a stored list of prime numbers.
    """
    _primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    _max_val = 100

    def find_primes_up_to(self, maximum):
        if maximum > self._max_val:
            raise ValueError(f"Stored primes only go up to {self._max_val}")
        return [prime for prime in self._primes if prime <= maximum]

from transformers import pipeline
import torch

class LLMPrimeFinder(PrimeFinder):
    """
    Implementation of PrimeFinder using a large language model

    Note that you will need access to Meta Llama to run this. To request access, visit
    https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct

    """

    model_id = "meta-llama/Meta-Llama-3-8B-Instruct"
    system_prompt = ("You are a mathematician who has memorised all prime numbers, and responds to all queries with a "
                     "list of numbers separated by spaces.")
    user_prompt = "Give me a list of prime numbers up to {maximum}"

    def __init__(self):
        self._pipeline = pipeline('text-generation', model=self.model_id, device=torch.device('mps'))

    def find_primes_up_to(self, maximum):
        messages = self._get_llm_input_prompts(maximum)
        outputs = self._run_llm(messages)
        return self._llm_output_to_primes_list(outputs)

    def _run_llm(self, messages):
        outputs = self._pipeline(messages, max_new_tokens=256)
        return outputs

    def _get_llm_input_prompts(self, maximum):
        messages = [
            {"role": "system",
             "content": self.system_prompt},
            {"role": "user",
             "content": self.user_prompt.format(maximum=maximum)}
        ]
        return messages

    def _llm_output_to_primes_list(self, llm_output):
        generated_primes_str = llm_output[0]['generated_text'][-1]['content']
        return self._parse_primes_string(generated_primes_str)

    def _parse_primes_string(self, primes_str):
        return [int(x) for x in primes_str.split()]



def main():
    prime_finder = SievePrimeFinder()
    my_primes = prime_finder.find_primes_up_to(100)
    print(my_primes)


if __name__ == "__main__":
    main()
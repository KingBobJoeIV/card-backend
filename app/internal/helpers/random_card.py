import random


def card():
    # Visa card prefix
    prefix = "4"

    # Random number of digits
    digits = [str(random.randint(0, 9)) for _ in range(14)]

    # Compute Luhn check digit
    check_digit = luhn_checksum(prefix + "".join(digits))

    # Full credit card number
    cc_number = prefix + "".join(digits) + str(check_digit)

    return cc_number


def luhn_checksum(num):
    digits = [int(d) for d in str(num)][::-1]
    odd = True
    _sum = 0
    for digit in digits:
        if odd:
            digit *= 2
        if digit > 9:
            digit -= 9
        _sum += digit
        odd = not odd
    return _sum % 10

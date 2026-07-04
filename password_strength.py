"""
Q1: Password Strength Checker
------------------------------
A DevOps-focused utility to validate password strength against a set of
security criteria before it is accepted for use in system configurations,
service accounts, etc.

Criteria enforced:
    1. Minimum length of 8 characters
    2. Contains at least one uppercase letter
    3. Contains at least one lowercase letter
    4. Contains at least one digit
    5. Contains at least one special character
"""

import re
import getpass


# Centralised, easy-to-extend criteria definitions.
# Each entry maps a human-readable description to a validation function.
PASSWORD_CRITERIA = {
    "Minimum length of 8 characters": lambda pwd: len(pwd) >= 8,
    "Contains an uppercase letter": lambda pwd: bool(re.search(r"[A-Z]", pwd)),
    "Contains a lowercase letter": lambda pwd: bool(re.search(r"[a-z]", pwd)),
    "Contains a digit": lambda pwd: bool(re.search(r"\d", pwd)),
    "Contains a special character": lambda pwd: bool(
        re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=~`\[\]/;']", pwd)
    ),
}


def check_password_strength(password: str) -> bool:
    """
    Validate a password against the defined security criteria.

    Args:
        password (str): The password string to validate.

    Returns:
        bool: True if the password satisfies every criterion, False otherwise.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    return all(check(password) for check in PASSWORD_CRITERIA.values())


def get_failed_criteria(password: str) -> list:
    """
    Return a list of human-readable descriptions of criteria the password
    failed to satisfy. Useful for giving actionable feedback to the user.
    """
    return [desc for desc, check in PASSWORD_CRITERIA.items() if not check(password)]


def describe_strength(password: str) -> str:
    """
    Provide a short qualitative rating in addition to the pass/fail result,
    based on how many criteria were satisfied.
    """
    passed = sum(check(password) for check in PASSWORD_CRITERIA.values())
    total = len(PASSWORD_CRITERIA)

    if passed == total:
        return "Strong"
    if passed >= total - 1:
        return "Moderate"
    if passed >= total // 2:
        return "Weak"
    return "Very Weak"


def main():
    print("=== Password Strength Checker ===\n")

    # getpass hides the input on the terminal, which is good practice
    # when handling sensitive data like passwords.
    try:
        password = getpass.getpass("Enter a password to check: ")
    except Exception:
        # Fallback for environments where getpass is not supported (e.g. some IDEs)
        password = input("Enter a password to check: ")

    if not password:
        print("No password entered. Exiting.")
        return

    is_strong = check_password_strength(password)
    rating = describe_strength(password)

    print(f"\nStrength rating: {rating}")

    if is_strong:
        print("✅ Your password meets all security requirements.")
    else:
        print("❌ Your password does not meet the security requirements.")
        print("Missing requirements:")
        for issue in get_failed_criteria(password):
            print(f"  - {issue}")


if __name__ == "__main__":
    main()

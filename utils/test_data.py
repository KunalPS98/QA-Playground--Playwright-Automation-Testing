import uuid


def unique_suffix() -> str:
    # avoids 409 "email already exists" on repeat runs
    return uuid.uuid4().hex[:10]


def new_user_payload() -> dict:
    suffix = unique_suffix()
    return {
        "name": f"Test User {suffix}",
        "email": f"user_{suffix}@qa-playground-tests.test",
        "password": "Password123",
    }


# seeded accounts from the login page, for tests that need an existing account
SAMPLE_CUSTOMER = {"email": "charlie@qaplayground.test", "password": "Customer123!"}
SAMPLE_ADMIN = {"email": "admin@qaplayground.test", "password": "Admin123!"}

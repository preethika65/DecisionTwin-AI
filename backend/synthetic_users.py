import random


def generate_user():

    user = {

        "age": random.randint(18, 60),

        "income": random.randint(20000, 100000),

        "risk_level": random.choice(
            [
                "Low",
                "Medium",
                "High"
            ]
        ),

        "interest": random.choice(
            [
                "Technology",
                "Finance",
                "Healthcare",
                "Education"
            ]
        )

    }

    return user
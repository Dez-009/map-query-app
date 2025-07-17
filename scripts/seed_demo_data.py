"""Seed demo data for properties, units, residents and related models."""
import random
from datetime import date, timedelta
import psycopg2
from psycopg2.extras import DictCursor

PROPERTIES = [
    {"name": "Maple Apartments", "address": "100 Maple St"},
    {"name": "Oak Residences", "address": "200 Oak Ave"},
    {"name": "Pine Condos", "address": "300 Pine Rd"},
]

FIRST_NAMES = ["Alex", "Sam", "Jordan", "Taylor", "Casey", "Drew", "Morgan", "Jamie", "Robin", "Dez"]
LAST_NAMES = ["Smith", "Johnson", "Lee", "Brown", "Garcia", "Martinez", "Davis", "Lopez", "Clark", "Lewis"]
OCCUPATIONS = ["Engineer", "Teacher", "Designer", "Nurse", "Developer", "Manager", "Analyst"]
PET_TYPES = ["Dog", "Cat", "Bird", "Fish"]
VEHICLE_MAKES = ["Toyota", "Honda", "Ford", "Tesla"]
VEHICLE_MODELS = ["Sedan", "SUV", "Truck", "Coupe"]


def rand_name() -> str:
    return f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"


def main():
    conn = psycopg2.connect(
        host="db",
        database="mapquery",
        user="postgres",
        password="postgres",
        port=5432,
    )
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            # Clear existing data
            cur.execute(
                "TRUNCATE vehicles, pets, repairs, payments, residents, apartment_units, properties RESTART IDENTITY CASCADE"
            )

            # Insert properties
            for prop in PROPERTIES:
                cur.execute(
                    "INSERT INTO properties (name, address, unit_count) VALUES (%s, %s, %s) RETURNING id",
                    (prop["name"], prop["address"], 4),
                )
                prop["id"] = cur.fetchone()[0]

            # Insert units
            unit_sizes = ["STUDIO", "1BR", "2BR", "3BR"]
            unit_ids = []
            for prop in PROPERTIES:
                for i in range(1, 5):
                    unit_number = f"{prop['name'][0]}-{i}"
                    size = random.choice(unit_sizes)
                    rent = random.randint(800, 2500)
                    cur.execute(
                        """
                        INSERT INTO apartment_units (unit_number, size, rent, property_id)
                        VALUES (%s, %s, %s, %s) RETURNING id
                        """,
                        (unit_number, size, rent, prop["id"]),
                    )
                    unit_ids.append(cur.fetchone()[0])

            # Insert residents
            resident_ids = []
            for _ in range(30):
                name = rand_name()
                email = f"{name.replace(' ', '.').lower()}@example.com"
                phone = f"555-{random.randint(1000,9999)}"
                income = random.randint(30000, 120000)
                occupation = random.choice(OCCUPATIONS)
                num_occupants = random.randint(1, 4)
                unit_id = random.choice(unit_ids)
                cur.execute(
                    """
                    INSERT INTO residents (full_name, email, phone, income, occupation, num_occupants, unit_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                    """,
                    (name, email, phone, income, occupation, num_occupants, unit_id),
                )
                resident_ids.append(cur.fetchone()[0])

            # Insert pets
            for _ in range(15):
                resident_id = random.choice(resident_ids)
                pet_type = random.choice(PET_TYPES)
                breed = random.choice(["Mix", "Purebred", ""])
                weight = random.uniform(5, 80)
                cur.execute(
                    "INSERT INTO pets (type, breed, weight, resident_id) VALUES (%s, %s, %s, %s)",
                    (pet_type, breed, weight, resident_id),
                )

            # Insert vehicles
            for _ in range(20):
                resident_id = random.choice(resident_ids)
                make = random.choice(VEHICLE_MAKES)
                model = random.choice(VEHICLE_MODELS)
                plate = f"{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}{random.randint(1000,9999)}"
                cur.execute(
                    "INSERT INTO vehicles (make, model, plate, resident_id) VALUES (%s, %s, %s, %s)",
                    (make, model, plate, resident_id),
                )

            # Insert payments
            num_payments = random.randint(30, 50)
            statuses = ["ON_TIME", "LATE", "OUTSTANDING"]
            for _ in range(num_payments):
                resident_id = random.choice(resident_ids)
                amount = random.randint(800, 2500)
                days_ago = random.randint(0, 60)
                pay_date = date.today() - timedelta(days=days_ago)
                status = random.choices(statuses, weights=[0.7, 0.2, 0.1])[0]
                cur.execute(
                    """
                    INSERT INTO payments (amount, date, status, resident_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (amount, pay_date, status, resident_id),
                )

            # Insert repairs
            open_statuses = ["NEW", "IN_PROGRESS"]
            for _ in range(8):
                unit_id = random.choice(unit_ids)
                resident_id = random.choice(resident_ids)
                desc = random.choice(["Leaky faucet", "Broken heater", "Window crack", "Appliance issue"])
                status = random.choice(open_statuses)
                cur.execute(
                    """
                    INSERT INTO repairs (description, status, unit_id, resident_id)
                    VALUES (%s, %s, %s, %s)
                    """,
                    (desc, status, unit_id, resident_id),
                )

            conn.commit()
            print("Demo data inserted successfully!")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

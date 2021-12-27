from gateways.paypal import PayPalAPI
from django.conf import settings


# Create paypal plans from terminal

def create_paypal_plan(name, description, price):
    # TODO: Work on the data to use quantity
    product = PayPalAPI().create_billing_product({
        "name": name,
        "description": description,
        "type": "SERVICE",
        "category": "SOFTWARE",
    })

    product_id = product.json()['id']

    billing_plan = PayPalAPI().create_billing_plan({
        "product_id": product_id,
        "name": name,
        "description": price,
        "status": "ACTIVE",
        "billing_cycles": [
            {
            "frequency": {
                "interval_unit": "DAY" if settings.DEBUG else 'MONTH',
                "interval_count": 1
            },
            "tenure_type": "TRIAL",
            "sequence": 1,
            "total_cycles": 2,
            "pricing_scheme": {
                "fixed_price": {
                "value": "3",
                "currency_code": "USD"
                }
            }
            },
            {
            "frequency": {
                "interval_unit": "MONTH",
                "interval_count": 1
            },
            "tenure_type": "TRIAL",
            "sequence": 2,
            "total_cycles": 3,
            "pricing_scheme": {
                "fixed_price": {
                "value": "6",
                "currency_code": "USD"
                }
            }
            },
            {
            "frequency": {
                "interval_unit": "MONTH",
                "interval_count": 1
            },
            "tenure_type": "REGULAR",
            "sequence": 3,
            "total_cycles": 12,
            "pricing_scheme": {
                "fixed_price": {
                "value": price,
                "currency_code": "USD"
                }
            }
            }
        ],
        "payment_preferences": {
            "auto_bill_outstanding": True,
            "setup_fee": {
            "value": "10",
            "currency_code": "USD"
            },
            "setup_fee_failure_action": "CONTINUE",
            "payment_failure_threshold": 3
        },
        "taxes": {
            "percentage": "10",
            "inclusive": False
        }
    })
    
    price_id = billing_plan.json()['id']
    return price_id


def create_paypal_plans():
    id = create_paypal_plan("Doctor", "Doctor plan", 50)
    print("doctor", id)
    id = create_paypal_plan("Doctor", "Doctor with home service plan", 100)
    print("Doctor with home service", id)
    id = create_paypal_plan("Clinic", "Clinic", 50)
    print("Clinic", id)
    id = create_paypal_plan("Pharmacy", "Pharmacy", 100)
    print("Pharmacy", id)

# TODO: Do same thing for stripe

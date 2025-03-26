from zeep import Client, xsd
from app.core.config import settings
import logging


# NOTE: Real integration logic below is currently unused
# due to unresponsive external services. Mock version used during assessment.
def fetch_kyc(customer_number: str):
    try:
        wsdl_url = "https://kycapitest.credable.io/service/customerWsdl.wsdl"
        client = Client(wsdl_url)

        # Manually build the header block
        header = xsd.Element(
            "{http://credable.io/cbs/customer}Credentials",
            xsd.ComplexType(
                [
                    xsd.Element(
                        "{http://credable.io/cbs/customer}username", xsd.String()
                    ),
                    xsd.Element(
                        "{http://credable.io/cbs/customer}password", xsd.String()
                    ),
                ]
            ),
        )
        header_value = header(
            username=settings.CORE_BANKING_USERNAME,
            password=settings.CORE_BANKING_PASSWORD,
        )

        response = client.service.Customer(
            customerNumber=customer_number, _soapheaders=[header_value]
        )

        return dict(response)

    except Exception as e:
        logging.error(f"KYC fetch failed for customer {customer_number}: {e}")
        return None


def fetch_kyc_mock(customer_number: str):
    logging.warning(f"[MOCK] Returning fake KYC data for customer {customer_number}")

    return {
        "customerNumber": customer_number,
        "fullName": "Jane Doe",
        "idType": "National ID",
        "idNumber": "12345678",
        "dateOfBirth": "1990-01-01",
        "gender": "F",
        "riskRating": "LOW",
        "accountStatus": "ACTIVE",
    }


# NOTE: Real integration logic below is currently unused
# due to unresponsive external services. Mock version used during assessment.
def fetch_transactions(customer_number: str):
    try:
        wsdl_url = "https://trxapitest.credable.io/service/transactionWsdl.wsdl"
        client = Client(wsdl_url)
        print("\nAvailable Transaction operations:")
        for service in client.wsdl.services.values():
            for port in service.ports.values():
                operations = sorted(port.binding._operations.keys())
                for operation in operations:
                    print(f"- {operation}")
        response = client.service.getTransactions(
            customerNumber=customer_number,
            username=settings.CORE_BANKING_USERNAME,
            password=settings.CORE_BANKING_PASSWORD,
        )

        # Convert to list of dicts for JSON storage
        if isinstance(response, list):
            trx_data = [dict(trx) for trx in response]
        else:
            trx_data = [dict(response)]

        return trx_data

    except Exception as e:
        logging.error(f"Transaction fetch failed for customer {customer_number}: {e}")
        return None


def fetch_transactions_mock(customer_number: str):
    logging.warning(
        f"[MOCK] Returning fake transactions for customer {customer_number}"
    )

    return [
        {
            "accountNumber": "332216783322167555621628",
            "credittransactionsAmount": 6000.00,
            "debitcardpostransactionsAmount": 200.00,
            "monthlyBalance": 10500.50,
            "bouncedChequesDebitNumber": 0,
            "mobilemoneycredittransactionAmount": 1500.25,
            "mobilemoneydebittransactionAmount": 350.00,
            "overthecounterwithdrawalsAmount": 120.00,
            "lastTransactionDate": 1697809200000,
            "transactionValue": 1.0,
        }
    ]

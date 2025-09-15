"""BagelPay Python SDK

A Python client library for the BagelPay API.

Example usage:
    from src import BagelPayClient, CheckoutRequest, Customer

    # 1. Initialize the client
    client = BagelPayClient(
        base_url="https://test.bagelpay.io",
        api_key="your-test-api-key-here"
    )

    # 2. Create a payment session
    from datetime import datetime

    checkout_request = CheckoutRequest(
        product_id="prod_123456789",
        request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        units="1",
        customer=Customer(
            email="customer@example.com"
        ),
        success_url="https://yoursite.com/success",
        metadata={
            "order_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        }
    )

    # 3. Get payment URL
    response = client.create_checkout(checkout_request)
    print(f"Payment URL: {response.checkout_url}")
"""

__version__ = "1.0.1"
__author__ = "andrew@gettrust.ai"
__email__ = "support@bagelpayment.com"

# Import main classes and exceptions
from .client import BagelPayClient
from .models import (
    CheckoutRequest,
    CheckoutResponse,
    CreateProductRequest,
    Product,
    UpdateProductRequest,
    ProductListResponse,
    Customer,
    ApiError,
    Transaction,
    TransactionCustomer,
    TransactionListResponse,
    Subscription,
    SubscriptionCustomer,
    SubscriptionListResponse,
    CustomerData,
    CustomerListResponse
)
from .exceptions import (
    BagelPayError,
    BagelPayAPIError,
    BagelPayAuthenticationError,
    BagelPayValidationError,
    BagelPayNotFoundError,
    BagelPayRateLimitError,
    BagelPayServerError
)

__all__ = [
    # Client
    "BagelPayClient",
    
    # Models
    "CheckoutRequest",
    "CheckoutResponse",
    "CreateProductRequest",
    "Product",
    "UpdateProductRequest",
    "ProductListResponse",
    "Customer",
    "ApiError",
    "Transaction",
    "TransactionCustomer",
    "TransactionListResponse",
    "Subscription",
    "SubscriptionCustomer",
    "SubscriptionListResponse",
    "CustomerData",
    "CustomerListResponse",
    
    # Exceptions
    "BagelPayError",
    "BagelPayAPIError",
    "BagelPayAuthenticationError",
    "BagelPayValidationError",
    "BagelPayNotFoundError",
    "BagelPayRateLimitError",
    "BagelPayServerError",
]

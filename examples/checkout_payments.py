#!/usr/bin/env python3
"""
BagelPay SDK - Checkout and Payments Examples

This script demonstrates how to use the BagelPay SDK for various checkout and payment scenarios:
- Creating simple one-time payment checkouts
- Creating checkouts with customer information
- Creating subscription checkouts
- Handling different payment flows
- Error handling and validation

Before running this script:
1. Set your BagelPay API key as an environment variable:
   export BAGELPAY_API_KEY="your_api_key_here"
   
2. Install the required dependencies:
   pip install bagelpay
"""

import os
import sys
import random
from datetime import datetime
from typing import Optional

# Add the parent directory to the path to import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.bagelpay.client import BagelPayClient
from src.bagelpay.models import (
    CheckoutRequest,
    CheckoutResponse,
    Customer,
    CreateProductRequest
)
from src.bagelpay.exceptions import (
    BagelPayError,
    BagelPayAPIError,
    BagelPayAuthenticationError,
    BagelPayValidationError,
    BagelPayNotFoundError
)


def get_client(api_key: Optional[str] = None, base_url: Optional[str] = None) -> BagelPayClient:
    """
    Initialize and return a BagelPay client.
    
    Args:
        api_key (Optional[str]): Your BagelPay API key. If not provided, will read from BAGELPAY_API_KEY environment variable.
        base_url (Optional[str]): Custom base URL for the API. If not provided, will use the default URL based on test_mode.
    
    Environment variables:
    - BAGELPAY_API_KEY: Your BagelPay API key (required if api_key parameter is not provided)
    - BAGELPAY_TEST_MODE: Whether to use test mode (optional, defaults to true)
    
    Returns:
        BagelPayClient: Initialized BagelPay client instance
    
    Raises:
        ValueError: If no API key is provided via parameter or environment variable
    """
    # Get API key from parameter or environment variable
    if api_key is None:
        api_key = os.getenv('BAGELPAY_API_KEY')
    
    if not api_key:
        raise ValueError(
            "API key is required. Either pass it as a parameter or "
            "set BAGELPAY_API_KEY environment variable with: export BAGELPAY_API_KEY='your_api_key_here'"
        )
    
    # Use test mode by default for examples
    test_mode = os.getenv('BAGELPAY_TEST_MODE', 'true').lower() != 'false'
    
    # Initialize the client
    client_kwargs = {
        'api_key': api_key,
        'test_mode': test_mode,
        'timeout': 30  # 30 seconds timeout
    }
    
    # Add base_url if provided
    if base_url is not None:
        client_kwargs['base_url'] = base_url
    
    client = BagelPayClient(**client_kwargs)
    
    print(f"✅ BagelPay client initialized")
    print(f"   Mode: {'Test' if test_mode else 'Live'}")
    print(f"   Base URL: {client.base_url}")
    print(f"   API Key: {api_key[:8]}...{api_key[-4:]}")
    
    return client


def create_simple_checkout(client: BagelPayClient) -> str:
    """Create a simple one-time payment checkout session."""
    print("\n💳 Creating a simple checkout session...")
    
    try:
        # First create a product for checkout
        product_request = CreateProductRequest(
            name="Product_" + str(random.randint(1000, 9999)),
            description="One-time premium software license",
            price=99.99,
            currency="USD",
            billing_type="single_payment",
            tax_inclusive=True,
            tax_category="digital_products",
            recurring_interval="daily",
            trial_days=0
        )
        product = client.create_product(product_request)
        
        # Create customer
        customer = Customer(email="andrew@gettrust.ai")
        
        checkout_request = CheckoutRequest(
            product_id=product.product_id,
            request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            units=random.choice(["1", "2", "3", "4"]),
            customer=customer,
            success_url="https://yoursite.com/success",
            metadata={
                "order_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "campaign": "simple_checkout",
                "source": "website"
            }
        )
        
        checkout_response = client.create_checkout(checkout_request)
        
        print(f"✅ Checkout session created successfully!")
        print(f"   Payment ID: {checkout_response.payment_id}")
        print(f"   Checkout URL: {checkout_response.checkout_url}")
        print(f"   Product ID: {checkout_response.product_id}")
        print(f"   Status: {checkout_response.status}")
        
        return checkout_response.payment_id
        
    except BagelPayValidationError as e:
        print(f"❌ Validation error: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def create_checkout_with_customer(client: BagelPayClient) -> str:
    """Create a checkout session with customer information."""
    print("\n👤 Creating checkout session with customer info...")
    
    try:
        # Create customer object
        customer = Customer(
            email="customer@example.com"
        )
        
        # Create a product for checkout
        product_request = CreateProductRequest(
            name="Product_" + str(random.randint(1000, 9999)),
            description="Annual Pro Subscription with full features",
            price=149.99,
            currency="USD",
            billing_type="single_payment",
            tax_inclusive=True,
            tax_category="digital_products",
            recurring_interval="none",
            trial_days=0
        )
        product = client.create_product(product_request)
        
        checkout_request = CheckoutRequest(
            product_id=product.product_id,
            request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            units=random.choice(["1", "2", "3", "4"]),
            customer=customer,
            success_url="https://yoursite.com/success",
            metadata={
                "order_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "campaign": "customer_checkout",
                "source": "website"
            }
        )
        
        checkout_response = client.create_checkout(checkout_request)
        
        print(f"✅ Checkout session with customer created successfully!")
        print(f"   Payment ID: {checkout_response.payment_id}")
        print(f"   Checkout URL: {checkout_response.checkout_url}")
        print(f"   Customer: {customer.email}")
        print(f"   Product ID: {checkout_response.product_id}")
        print(f"   Status: {checkout_response.status}")
        
        return checkout_response.payment_id
        
    except BagelPayValidationError as e:
        print(f"❌ Validation error: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def create_subscription_checkout(client: BagelPayClient) -> str:
    """Create a checkout session for a subscription."""
    print("\n🔄 Creating subscription checkout session...")
    
    try:
        customer = Customer(
            email="subscriber@example.com"
        )
        
        # Create a subscription product
        product_request = CreateProductRequest(
            name="Product_" + str(random.randint(1000, 9999)),
            description="Monthly SaaS Subscription with premium features",
            price=29.99,
            currency="USD",
            billing_type="subscription",
            tax_inclusive=True,
            tax_category="digital_products",
            recurring_interval="monthly",
            trial_days=7
        )
        product = client.create_product(product_request)
        
        checkout_request = CheckoutRequest(
            product_id=product.product_id,
            request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            units=random.choice(["1", "2", "3", "4"]),
            customer=customer,
            success_url="https://yoursite.com/welcome",
            metadata={
                "order_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "campaign": "subscription_checkout",
                "source": "website"
            }
        )
        
        checkout_response = client.create_checkout(checkout_request)
        
        print(f"✅ Subscription checkout session created successfully!")
        print(f"   Payment ID: {checkout_response.payment_id}")
        print(f"   Checkout URL: {checkout_response.checkout_url}")
        print(f"   Customer: {customer.email}")
        print(f"   Product ID: {checkout_response.product_id}")
        print(f"   Status: {checkout_response.status}")
        
        return checkout_response.payment_id
        
    except BagelPayValidationError as e:
        print(f"❌ Validation error: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def list_recent_transactions(client: BagelPayClient) -> None:
    """List recent transactions."""
    print("\n📊 Listing recent transactions...")
    
    try:
        # This would typically use a list_transactions method
        # For demo purposes, we'll show how it might work
        print("✅ Recent transactions:")
        
    except Exception as e:
        print(f"❌ Error listing transactions: {str(e)}")


def demonstrate_payment_flows(client: BagelPayClient) -> None:
    """Demonstrate different payment flows."""
    print("\n🔄 Demonstrating payment flows...")
    
    try:
        # Simple one-time payment
        simple_payment_id = create_simple_checkout(client)
        print(f"   Simple payment created: {simple_payment_id}")
        
        # Payment with customer info
        customer_payment_id = create_checkout_with_customer(client)
        print(f"   Customer payment created: {customer_payment_id}")
        
        # Subscription payment
        subscription_payment_id = create_subscription_checkout(client)
        print(f"   Subscription payment created: {subscription_payment_id}")
        
        print("\n✅ All payment flows demonstrated successfully!")
        
    except Exception as e:
        print(f"❌ Error in payment flows: {str(e)}")


def demonstrate_error_handling(client: BagelPayClient) -> None:
    """Demonstrate error handling scenarios."""
    print("\n⚠️  Demonstrating error handling...")
    
    try:
        # Test with invalid data
        print("\n1. Testing with invalid product data...")
        try:
            invalid_product = CreateProductRequest(
                name="",  # Empty name should cause validation error
                description="Invalid product",
                price=-10.00,  # Negative price should cause validation error
                currency="INVALID",  # Invalid currency
                billing_type="invalid_type",
                tax_inclusive=True,
                tax_category="invalid",
                recurring_interval="invalid",
                trial_days=-1
            )
            client.create_product(invalid_product)
        except BagelPayValidationError as e:
            print(f"   ✅ Caught validation error as expected: {e.message}")
        except Exception as e:
            print(f"   ⚠️  Unexpected error type: {str(e)}")
        
        # Test with invalid customer data
        print("\n2. Testing with invalid customer data...")
        try:
            invalid_customer = Customer(
                email="invalid-email",  # Invalid email format
            )
            
            # Create a valid product first
            product_request = CreateProductRequest(
                name="Product_" + str(random.randint(1000, 9999)),
                description="Annual Pro Subscription with full features",
                price=149.99,
                currency="USD",
                billing_type="single_payment",
                tax_inclusive=True,
                tax_category="digital_products",
                recurring_interval="none",
                trial_days=0
            )
            product = client.create_product(product_request)
            
            checkout_request = CheckoutRequest(
                product_id=product.product_id,
                request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                units=random.choice(["1", "2", "3", "4"]),
                customer=invalid_customer,
                success_url="https://yoursite.com/success",
                metadata={
                    "order_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    "campaign": "error_handling_test",
                    "source": "website"
                }
            )
            client.create_checkout(checkout_request)
        except BagelPayValidationError as e:
            print(f"   ✅ Caught validation error as expected: {e.message}")
        except Exception as e:
            print(f"   ⚠️  Unexpected error type: {str(e)}")
        
        print("\n✅ Error handling demonstration completed!")
        
    except Exception as e:
        print(f"❌ Error in error handling demo: {str(e)}")


def main():
    """Main function to run all checkout and payment examples."""
    print("🚀 BagelPay SDK - Checkout and Payments Examples")
    print("=======================================================")
    
    try:
        # Initialize client
        client = get_client(
            api_key="bagel_test_64C70FE8526A48568D4EEA9D9164F508"
            )
        
        # Run examples
        create_simple_checkout(client)
        create_checkout_with_customer(client)
        create_subscription_checkout(client)
        list_recent_transactions(client)
        demonstrate_payment_flows(client)
        demonstrate_error_handling(client)
        
        print("\n🎉 All checkout and payment examples completed successfully!")
        
    except BagelPayAuthenticationError as e:
        print(f"❌ Authentication failed: {e.message}")
        print("   Please check your API key and try again.")
        sys.exit(1)
    except BagelPayError as e:
        print(f"❌ BagelPay error: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
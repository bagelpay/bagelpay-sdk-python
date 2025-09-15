#!/usr/bin/env python3
"""
BagelPay SDK - Basic Usage Examples

This example demonstrates the basic usage of the BagelPay SDK including:
- Client initialization
- Product management (create, list, get, update)
- Checkout session creation
- Transaction listing
- Error handling

Before running this example:
1. Install the SDK: pip install bagelpay
2. Set your API key as an environment variable: export BAGELPAY_API_KEY="your_api_key_here"
3. Optionally set test mode: export BAGELPAY_TEST_MODE="false" (defaults to true)
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
    Customer,
    CheckoutRequest,
    CreateProductRequest,
    UpdateProductRequest,
    ApiError,
    Subscription,
    SubscriptionListResponse,
    CustomerListResponse
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


def create_sample_product(client: BagelPayClient) -> str:
    """
    Create a sample product and return its product_id.
    """
    print("\n📦 Creating a sample product...")
    
    try:
        # Create a product request
        product_request = CreateProductRequest(
            name="Product_" + str(random.randint(1000, 9999)),
            description="Description_of_product_" + str(random.randint(1000, 9999)),
            price=random.uniform(50.5, 1024.5),
            currency="USD",
            billing_type=random.choice(["subscription", "subscription", "subscription", "single_payment"]),
            tax_inclusive=False,
            tax_category=random.choice(["digital_products", "saas_services", "ebooks"]),
            recurring_interval=random.choice(["daily", "weekly", "monthly", "3months", "6months"]),
            trial_days=random.choice([0, 1, 7])
        )
        
        # Create the product
        product = client.create_product(product_request)
        
        print(f"✅ Product created successfully!")
        print(f"   Product ID: {product.product_id}")
        print(f"   Billing Type: {product.billing_type}")
        print(f"   Name: {product.name}")
        if product.recurring_interval:
            print(f"   Price: ${product.price}/{product.recurring_interval} {product.currency}")
        else:
            print(f"   Price: ${product.price} {product.currency}")
        print(f"   URL: {product.product_url}")
        
        return product.product_id
        
    except BagelPayValidationError as e:
        print(f"❌ Validation error: {e}")
        print("   Please check your product data and try again.")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e}")
        print(f"   Status code: {e.status_code}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise


def list_products(client: BagelPayClient) -> None:
    """
    List all products with pagination.
    """
    print("\n📋 Listing products...")
    
    try:
        # List products with pagination
        products_response = client.list_products(pageNum=1, pageSize=10)
        
        print(f"✅ Found {products_response.total} total products")
        print(f"   Showing {len(products_response.items)} products on this page")
        
        for i, product in enumerate(products_response.items, 1):
            status = "🗄️ Archived" if product.is_archive else "✅ Active"
            if product.recurring_interval:
                print(f"   {i}. {product.name} ({product.product_id}) - ${product.price}/{product.recurring_interval} {product.currency} {status}")
            else:
                print(f"   {i}. {product.name} ({product.product_id}) - ${product.price} {product.currency} {status}")

        # If there are more pages, show pagination info
        if products_response.total > len(products_response.items):
            total_pages = (products_response.total + 9) // 10  # Ceiling division
            print(f"   📄 Page 1 of {total_pages} (use pagination to see more)")
            
    except BagelPayAPIError as e:
        print(f"❌ Failed to list products: {e}")
        raise


def get_product_details(client: BagelPayClient, product_id: str) -> None:
    """
    Get detailed information about a specific product.
    """
    print(f"\n🔍 Getting details for product {product_id}...")
    
    try:
        product = client.get_product(product_id)
        
        print(f"✅ Product details:")
        print(f"   Product ID: {product.product_id}")
        print(f"   Name: {product.name}")
        print(f"   Description: {product.description}")
        if product.recurring_interval:
            print(f"   Price: ${product.price} {product.currency}/{product.recurring_interval}")
        else:
            print(f"   Price: ${product.price} {product.currency}")
        print(f"   Billing: {product.billing_type}")
        print(f"   Tax Inclusive: {product.tax_inclusive}")
        print(f"   Tax Category: {product.tax_category}")
        print(f"   Status: {'Archived' if product.is_archive else 'Active'}")
        print(f"   Created: {product.created_at}")
        print(f"   Updated: {product.updated_at}")
        print(f"   Product URL: {product.product_url}")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Product not found: {e}")
        print(f"   The product {product_id} does not exist or has been deleted.")
        raise
    except BagelPayAPIError as e:
        print(f"❌ Failed to get product details: {e}")
        raise


def update_product(client: BagelPayClient, product_id: str) -> None:
    """
    Update a product's information.
    """
    print(f"\n✏️ Updating product {product_id}...")
    
    try:
        # Create update request
        update_request = UpdateProductRequest(
            product_id=product_id,
            name="New_Product_" + str(random.randint(1000, 9999)),
            description="New_Description_of_product_" + str(random.randint(1000, 9999)),
            price=random.uniform(50.5, 1024.5),
            currency="USD",
            billing_type=random.choice(["subscription", "subscription", "single_payment"]),
            tax_inclusive=False,
            tax_category=random.choice(["digital_products", "saas_services", "ebooks"]),
            recurring_interval=random.choice(["daily", "weekly", "monthly", "3months", "6months"]),
            trial_days=random.choice([0, 1, 7])
        )
        
        # Update the product
        updated_product = client.update_product(update_request)
        
        print(f"✅ Product updated successfully!")
        print(f"   New name: {updated_product.name}")
        print(f"   New price: ${updated_product.price} {updated_product.currency}")
        print(f"   Updated at: {updated_product.updated_at}")
        
    except BagelPayValidationError as e:
        print(f"❌ Validation error during update: {e}")
        raise
    except BagelPayNotFoundError as e:
        print(f"❌ Product not found for update: {e}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ Failed to update product: {e}")
        raise


def create_checkout_session(client: BagelPayClient, product_id: str) -> str:
    """
    Create a checkout session for a product.
    """
    print(f"\n💳 Creating checkout session for product {product_id}...")
    
    try:
        # Create customer information
        customer = Customer(email="andrew@gettrust.ai")
        
        # Create checkout request
        checkout_request = CheckoutRequest(
            product_id=product_id,
            request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            units=random.choice(["1", "2", "3", "4"]),
            customer=customer,
            success_url=random.choice([None, "https://yourapp.com/success"]),
            metadata={
                "order_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                "campaign": "summer_sale",
                "source": "website"
            }
        )
        
        # Create the checkout session
        checkout = client.create_checkout(checkout_request)
        
        print(f"✅ Checkout session created successfully!")
        print(f"   Payment ID: {checkout.payment_id}")
        print(f"   Status: {checkout.status}")
        print(f"   Checkout URL: {checkout.checkout_url}")
        print(f"   Expires on: {checkout.expires_on}")
        print(f"   Success URL: {checkout.success_url}")
        
        return checkout.payment_id
        
    except BagelPayValidationError as e:
        print(f"❌ Validation error during checkout creation: {e}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ Failed to create checkout session: {e}")
        raise


def list_transactions(client: BagelPayClient) -> None:
    """
    List recent transactions.
    """
    print("\n💰 Listing recent transactions...")
    
    try:
        # List transactions with pagination
        transactions_response = client.list_transactions(pageNum=1, pageSize=5)
        
        print(f"✅ Found {transactions_response.total} total transactions")
        print(f"   Showing {len(transactions_response.items)} transactions on this page")
        
        for i, transaction in enumerate(transactions_response.items, 1):
            print(f"   {i}. Transaction {transaction.transaction_id}")
            print(f"      Amount: ${transaction.amount / 100:.2f} {transaction.currency}")
            print(f"      Type: {transaction.type}")
            print(f"      Customer: {transaction.customer.email if transaction.customer else 'N/A'}")
            print(f"      Created: {transaction.created_at}")
            if transaction.remark:
                print(f"      Remark: {transaction.remark}")
            print()
        
    except BagelPayAPIError as e:
        print(f"❌ Failed to list transactions: {e}")
        raise


def archive_and_unarchive_product(client: BagelPayClient, product_id: str) -> None:
    """
    Demonstrate archiving and unarchiving a product.
    """
    print(f"\n🗄️ Archiving product {product_id}...")
    
    try:
        # Archive the product
        archive_result = client.archive_product(product_id)
        print(f"✅ Product archived successfully!")
        print(f"   Product ID: {archive_result.product_id}")
        print(f"   Status: {'Archived' if archive_result.is_archive else 'Active'}")
        
        # Unarchive the product
        print(f"\n📤 Unarchiving product {product_id}...")
        unarchive_result = client.unarchive_product(product_id)
        print(f"✅ Product unarchived successfully!")
        print(f"   Product ID: {unarchive_result.product_id}")
        print(f"   Status: {'Archived' if unarchive_result.is_archive else 'Active'}")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Product not found for archive/unarchive: {e}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ Failed to archive/unarchive product: {e}")
        raise


def list_subscriptions_basic(client: BagelPayClient) -> None:
    """
    Demonstrate basic subscription listing.
    """
    print("\n🔄 Subscription Management")
    print("=" * 30)
    
    try:
        print("\n📋 Listing subscriptions...")
        subscriptions_response = client.list_subscriptions(pageNum=1, pageSize=5)
        
        print(f"Total subscriptions: {subscriptions_response.total}")
        
        if subscriptions_response.items:
            print("\nRecent subscriptions:")
            for subscription in subscriptions_response.items[:3]:  # Show first 3
                print(f"  📦 {subscription.subscription_id}")
                print(f"     Status: {subscription.status}")
                print(f"     Product: {subscription.product_name}")
                print(f"     Customer: {subscription.customer.email}")
                print(f"     Amount: ${subscription.next_billing_amount}/{subscription.recurring_interval}")
                print(f"     Payment method: {subscription.payment_method}")
                print(f"     Subscription Started: {subscription.created_at}")
                if subscription.trial_end:
                    print(f"     Trial Start: {subscription.trial_start}")
                    print(f"     Trial End: {subscription.trial_end}")
                    print(f"     Next Billing Amount: {subscription.next_billing_amount}/{subscription.recurring_interval}")
                    print(f"     Next Billing Date: {subscription.trial_end}")
                else:
                    print(f"     Next Billing Amount: {subscription.next_billing_amount}/{subscription.recurring_interval}")
                    print(f"     Next Billing Date: {subscription.billing_period_end}")
                print()
        else:
            print("   No subscriptions found.")
            print("   💡 Create subscription products and checkout sessions to see subscriptions here.")
    
    except BagelPayAPIError as e:
        print(f"❌ API Error: {e.message} (Code: {e.error_code})")
    except Exception as e:
        print(f"❌ Error: {e}")


def list_customers_basic(client: BagelPayClient) -> None:
    """
    Demonstrate basic customer listing.
    """
    print("\n👥 Customer Management")
    print("=" * 30)
    
    try:
        print("\n📋 Listing customers...")
        customers_response = client.list_customers(pageNum=1, pageSize=5)
        
        print(f"Total customers: {customers_response.total}")
        
        if customers_response.items:
            print("\nRecent customers:")
            total_revenue = 0
            for customer in customers_response.items[:3]:  # Show first 3
                print(f"  👤 {customer.name} ({customer.email})")
                print(f"     Subscriptions: {customer.subscriptions}")
                print(f"     Total Spend: ${customer.total_spend / 100:.2f}")
                total_revenue += customer.total_spend
                print()
            
            print(f"Revenue from shown customers: ${total_revenue / 100:.2f}")
        else:
            print("   No customers found.")
            print("   💡 Create checkout sessions to see customers here.")
    
    except BagelPayAPIError as e:
        print(f"❌ API Error: {e.message} (Code: {e.error_code})")
    except Exception as e:
        print(f"❌ Error: {e}")


def get_subscription_details(client: BagelPayClient) -> None:
    """
    Demonstrate getting detailed information about a specific subscription.
    """
    print("\n🔍 Getting subscription details example...")
    
    try:
        # Get subscription details example
        subscriptions_response = client.list_subscriptions()
        active_subscriptions = [sub for sub in subscriptions_response.items if sub.status in ['active', 'trialing']]
        
        if not active_subscriptions:
            print("   No active subscriptions found to demonstrate details.")
            return
            
        subscription_id = active_subscriptions[0].subscription_id
        print(f"   Using subscription {subscription_id} for demonstration...")
        
        subscription = client.get_subscription(subscription_id)
        
        print(f"✅ Subscription details:")
        print(f"   Subscription ID: {subscription.subscription_id}")
        print(f"   Status: {subscription.status}")
        print(f"   Product: {subscription.product_name} (ID: {subscription.product_id})")
        print(f"   Customer: {subscription.customer.email}")
        print(f"   Payment Method: {subscription.payment_method}")
        print(f"   Amount: ${subscription.next_billing_amount}/{subscription.recurring_interval}")
        print(f"   Created: {subscription.created_at}")
        print(f"   Updated: {subscription.updated_at}")
        
        if subscription.trial_start and subscription.trial_end:
            print(f"   Trial Period: {subscription.trial_start} to {subscription.trial_end}")
        
        if subscription.billing_period_start and subscription.billing_period_end:
            print(f"   Current Billing Period: {subscription.billing_period_start} to {subscription.billing_period_end}")
        
        if subscription.cancel_at:
            print(f"   Scheduled Cancellation: {subscription.cancel_at}")
        
        if subscription.remark:
            print(f"   Remark: {subscription.remark}")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Subscription not found: {e}")
        print(f"   The subscription does not exist or has been deleted.")
        raise
    except BagelPayAPIError as e:
        print(f"❌ Failed to get subscription details: {e}")
        raise


def cancel_subscription_example(client: BagelPayClient) -> None:
    """
    Demonstrate canceling a subscription.
    """
    print("\n❌ Cancel subscription example...")
    
    try:
        # Cancel subscription example
        subscriptions_response = client.list_subscriptions()
        active_subscriptions = [sub for sub in subscriptions_response.items if sub.status in ['active', 'trialing']]
        
        if not active_subscriptions:
            print("   No active subscriptions found to demonstrate cancellation.")
            print("   💡 Skipping cancellation example for safety.")
            return
            
        subscription_id = active_subscriptions[0].subscription_id
        
        canceled_subscription = client.cancel_subscription(subscription_id)
        print(f"✅ Subscription canceled successfully!")
        print(f"   Subscription ID: {canceled_subscription.subscription_id}")
        print(f"   Status: {canceled_subscription.status}")
        print(f"   Product: {canceled_subscription.product_name}")
        print(f"   Customer: {canceled_subscription.customer.email}")
        if canceled_subscription.cancel_at:
             print(f"   Cancellation Date: {canceled_subscription.cancel_at}")
        print(f"   💡 The subscription will remain active until the end of the current billing period.")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Subscription not found for cancellation: {e}")
        print(f"   The subscription does not exist or has already been canceled.")
        raise
    except BagelPayAPIError as e:
        print(f"❌ Failed to cancel subscription: {e}")
        if e.error_code:
            print(f"   Error code: {e.error_code}")
        raise


def demonstrate_error_handling(client: BagelPayClient) -> None:
    """
    Demonstrate various error handling scenarios.
    
    The SDK supports the API error format: {"msg": "Validation failed", "code": 500}
    """
    print("\n🚨 Demonstrating error handling...")
    print("   📝 Note: SDK handles API error format {msg, code}")
    
    # Try to get a non-existent product
    try:
        print("   Trying to get non-existent product...")
        client.get_product("nonexistent_product_id")
    except BagelPayNotFoundError as e:
        print(f"   ✅ Caught expected NotFoundError: {e}")
    except BagelPayAPIError as e:
        print(f"   ✅ Caught API error: {e} (status: {e.status_code})")
        if e.error_code:
            print(f"      Error code: {e.error_code}")
        if hasattr(e, 'api_error') and e.api_error:
            print(f"      API Error details: {e.api_error.message} (code: {e.api_error.code})")
    except Exception as e:
        print(f"   ✅ Caught error: {e}")
    
    # Try to create a product with invalid data
    try:
        print("   Trying to create product with invalid price...")
        invalid_request = CreateProductRequest(
            name="Invalid Product",
            description="This product has invalid data",
            price=-100,  # Invalid negative price
            currency="INVALID",  # Invalid currency
            billing_type="invalid_type",  # Invalid billing type
            tax_inclusive=True,
            tax_category="digital_products",
            recurring_interval="monthly",
            trial_days=7
        )
        client.create_product(invalid_request)
    except BagelPayValidationError as e:
        print(f"   ✅ Caught expected ValidationError: {e}")
        if e.error_code:
            print(f"      Error code: {e.error_code}")
    except BagelPayAPIError as e:
        print(f"   ✅ Caught API error: {e} (status: {e.status_code})")
        if e.error_code:
            print(f"      Error code: {e.error_code}")
    except Exception as e:
        print(f"   ✅ Caught error: {e}")


def main():
    """
    Main function demonstrating the complete BagelPay SDK usage.
    """
    print("🥯 BagelPay SDK - Basic Usage Example")
    print("=" * 50)
    
    try:
        # Initialize the client
        client = get_client(
            api_key="bagel_test_64C70FE8526A48568D4EEA9D9164F508"
            )
        
        # Use the client as a context manager for automatic cleanup
        with client:
            # Create a sample product
            product_id = create_sample_product(client)
            
            # List all products
            list_products(client)
            
            # Get product details
            get_product_details(client, product_id)
            
            # Update the product
            update_product(client, product_id)

            # Archive and unarchive the product
            archive_and_unarchive_product(client, product_id)
            
            # Create a checkout session
            payment_id = create_checkout_session(client, product_id)
            
            # List transactions
            list_transactions(client)
            
            # List subscriptions
            list_subscriptions_basic(client)
            
            # Get subscription details example
            get_subscription_details(client)
            
            # Cancel subscription example
            # cancel_subscription_example(client)
            
            # List customers
            list_customers_basic(client)
            
            # Demonstrate error handling
            demonstrate_error_handling(client)
        
        print("\n✅ All operations completed successfully!")
        print("\n💡 Tips:")
        print("   - Always use the client as a context manager for proper cleanup")
        print("   - Handle specific exceptions for better error management")
        print("   - Use pagination for large datasets")
        print("   - Store product IDs and payment IDs for future reference")
        print("   - Check the API documentation for more advanced features")
        
    except BagelPayAuthenticationError as e:
        print(f"\n❌ Authentication failed: {e}")
        print("   Please check your API key and try again.")
        sys.exit(1)
    except BagelPayError as e:
        print(f"\n❌ BagelPay SDK error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
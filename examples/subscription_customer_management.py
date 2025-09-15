#!/usr/bin/env python3
"""
BagelPay SDK - Subscription and Customer Management Examples

This example demonstrates subscription and customer management operations including:
- Listing subscriptions with pagination
- Getting subscription details
- Canceling subscriptions
- Listing customers with pagination
- Error handling for subscription and customer operations

Before running this example:
1. Install the SDK: pip install bagelpay
2. Set your API key as an environment variable: export BAGELPAY_API_KEY="your_api_key_here"
3. Optionally set test mode: export BAGELPAY_TEST_MODE="false" (defaults to true)
"""

import os
import sys
from datetime import datetime
from typing import Optional

# Add the parent directory to the path to import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.bagelpay.client import BagelPayClient
from src.bagelpay.models import (
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
    
    print(f"✅ BagelPay client initialized in {'Test' if test_mode else 'Live'} mode")
    return client


def list_all_subscriptions(client: BagelPayClient) -> Optional[str]:
    """List all subscriptions with pagination."""
    print("\n🔄 Listing all subscriptions...")
    
    try:
        page_num = 1
        page_size = 5
        total_subscriptions = 0
        first_subscription_id = None
        
        while True:
            response = client.list_subscriptions(pageNum=page_num, pageSize=page_size)
            
            if page_num == 1:
                print(f"📊 Total subscriptions found: {response.total}")
                # Calculate pages from total and page_size
                total_pages = (response.total + page_size - 1) // page_size
                print(f"📄 Total pages: {total_pages}")
            
            if not response.items:
                break
            
            print(f"\n--- Page {page_num} ---")
            for subscription in response.items:
                total_subscriptions += 1
                if first_subscription_id is None:
                    first_subscription_id = subscription.subscription_id
                
                print(f"  {total_subscriptions}. Subscription ID: {subscription.subscription_id}")
                print(f"     Customer: {subscription.customer.email if subscription.customer else 'N/A'}")
                print(f"     Status: {subscription.status}")
                print(f"     Product: {subscription.product_name or 'N/A'}")
                print(f"     Created: {subscription.created_at}")
                if hasattr(subscription, 'current_period_start'):
                    print(f"     Current Period: {subscription.current_period_start} - {getattr(subscription, 'current_period_end', 'N/A')}")
                print()
            
            # Calculate if we've reached the last page
            total_pages = (response.total + page_size - 1) // page_size
            if page_num >= total_pages:
                break
            
            page_num += 1
        
        if total_subscriptions == 0:
            print("📭 No subscriptions found.")
            print("💡 Tip: Create some subscription checkout sessions first to see subscriptions here.")
        else:
            print(f"✅ Listed {total_subscriptions} subscriptions across {page_num} pages")
        
        return first_subscription_id
        
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def get_subscription_details(client: BagelPayClient, subscription_id: str) -> None:
    """Get detailed information about a specific subscription."""
    print(f"\n🔍 Getting details for subscription {subscription_id}...")
    
    try:
        subscription = client.get_subscription(subscription_id)
        
        print(f"✅ Subscription details retrieved successfully!")
        print(f"   ID: {subscription.subscription_id}")
        print(f"   Status: {subscription.status}")
        print(f"   Customer: {subscription.customer.email if subscription.customer else 'N/A'}")
        print(f"   Product: {subscription.product_name or 'N/A'}")
        print(f"   Created: {subscription.created_at}")
        print(f"   Updated: {getattr(subscription, 'updated_at', 'N/A')}")
        
        if hasattr(subscription, 'billing_period_start'):
            print(f"   Billing Period Start: {subscription.billing_period_start}")
        if hasattr(subscription, 'billing_period_end'):
            print(f"   Billing Period End: {subscription.billing_period_end}")
        if hasattr(subscription, 'trial_end'):
            print(f"   Trial End: {subscription.trial_end}")
        if hasattr(subscription, 'cancel_at_period_end'):
            print(f"   Cancel at Period End: {subscription.cancel_at}")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Subscription not found: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def cancel_subscription_example(client: BagelPayClient, subscription_id: str) -> None:
    """Demonstrate canceling a subscription."""
    print(f"\n❌ Canceling subscription {subscription_id}...")
    
    try:
        # Get subscription details before canceling
        print("📋 Getting subscription details before canceling...")
        subscription_before = client.get_subscription(subscription_id)
        print(f"   Status before: {subscription_before.status}")
        
        # Cancel the subscription
        canceled_subscription = client.cancel_subscription(subscription_id)
        
        print(f"✅ Subscription canceled successfully!")
        print(f"   ID: {canceled_subscription.subscription_id}")
        print(f"   Status after: {canceled_subscription.status}")
        print(f"   Updated: {getattr(canceled_subscription, 'updated_at', 'N/A')}")
        
        if hasattr(canceled_subscription, 'canceled_at'):
            print(f"   Canceled at: {canceled_subscription.cancel_at}")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Subscription not found: {e.message}")
        print("💡 This might happen if the subscription ID doesn't exist or has already been canceled.")
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        if "already canceled" in e.message.lower():
            print("💡 This subscription might already be canceled.")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


def list_all_customers(client: BagelPayClient) -> None:
    """List all customers with pagination."""
    print("\n👥 Listing all customers...")
    
    try:
        page_num = 1
        page_size = 5
        total_customers = 0
        
        while True:
            response = client.list_customers(pageNum=page_num, pageSize=page_size)
            
            if page_num == 1:
                print(f"📊 Total customers found: {response.total}")
                total_pages = (response.total + page_size - 1) // page_size
                print(f"📄 Total pages: {total_pages}")
            
            if not response.items:
                break
            
            print(f"\n--- Page {page_num} ---")
            for customer in response.items:
                total_customers += 1
                print(f"  {total_customers}. Customer ID: {customer.id}")
                print(f"     Name: {getattr(customer, 'name', 'N/A')}")
                print(f"     Email: {customer.email}")
                print(f"     Phone: {getattr(customer, 'phone', 'N/A')}")
                print(f"     Created: {customer.created_at}")
                if hasattr(customer, 'total_spent'):
                    print(f"     Total Spent: ${customer.total_spend}")
                if hasattr(customer, 'subscription_count'):
                    print(f"     Subscriptions: {customer.subscriptions}")
                print()
            
            total_pages = (response.total + page_size - 1) // page_size
            if page_num >= total_pages:
                break
            
            page_num += 1
        
        if total_customers == 0:
            print("📭 No customers found.")
            print("💡 Tip: Create some checkout sessions with customer info to see customers here.")
        else:
            print(f"✅ Listed {total_customers} customers across {page_num} pages")
        
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def analyze_subscription_metrics(client: BagelPayClient) -> None:
    """Analyze subscription metrics and provide insights."""
    print("\n📈 Analyzing subscription metrics...")
    
    try:
        # Get all subscriptions for analysis
        all_subscriptions = []
        page_num = 1
        page_size = 50  # Larger page size for analysis
        
        while True:
            response = client.list_subscriptions(pageNum=page_num, pageSize=page_size)
            
            if not response.items:
                break
            
            all_subscriptions.extend(response.items)
            
            total_pages = (response.total + page_size - 1) // page_size
            if page_num >= total_pages:
                break
            
            page_num += 1
        
        if not all_subscriptions:
            print("📭 No subscriptions available for analysis.")
            return
        
        # Analyze subscription statuses
        status_counts = {}
        
        for subscription in all_subscriptions:
            status = subscription.status
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"📊 Subscription Analysis:")
        print(f"   Total Subscriptions: {len(all_subscriptions)}")
        print(f"   Status Breakdown:")
        for status, count in status_counts.items():
            percentage = (count / len(all_subscriptions)) * 100
            print(f"     {status.title()}: {count} ({percentage:.1f}%)")
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")


def demonstrate_error_handling(client: BagelPayClient) -> None:
    """Demonstrate various error handling scenarios for subscriptions and customers."""
    print("\n🚨 Demonstrating subscription/customer error handling...")
    
    # Try to get a non-existent subscription
    print("\n1. Trying to get a non-existent subscription...")
    try:
        client.get_subscription("non-existent-subscription-id")
    except BagelPayNotFoundError as e:
        print(f"✅ Correctly caught NotFoundError: {e.message}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    
    # Try to cancel a non-existent subscription
    print("\n2. Trying to cancel a non-existent subscription...")
    try:
        client.cancel_subscription("non-existent-subscription-id")
    except BagelPayNotFoundError as e:
        print(f"✅ Correctly caught NotFoundError: {e.message}")
    except BagelPayAPIError as e:
        print(f"✅ Correctly caught API error: {e.message}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    
    # Try to list with invalid pagination parameters
    print("\n3. Trying to list subscriptions with invalid page size...")
    try:
        client.list_subscriptions(pageNum=1, pageSize=0)  # Invalid page size
    except BagelPayValidationError as e:
        print(f"✅ Correctly caught ValidationError: {e.message}")
    except BagelPayAPIError as e:
        print(f"✅ Correctly caught API error: {e.message}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


def main():
    """Main function to run all subscription and customer management examples."""
    print("🚀 BagelPay SDK - Subscription and Customer Management Examples")
    print("=" * 70)
    
    try:
        # Initialize client
        client = get_client()
        
        # List all subscriptions
        first_subscription_id = list_all_subscriptions(client)
        
        # Get subscription details if we have any subscriptions
        if first_subscription_id:
            get_subscription_details(client, first_subscription_id)
            
            # Note: We'll demonstrate cancellation but won't actually cancel
            # to avoid affecting real subscriptions
            print("\n💡 Subscription cancellation example:")
            print("   (Skipping actual cancellation to preserve test data)")
            print(f"   To cancel subscription {first_subscription_id}, you would call:")
            print(f"   client.cancel_subscription('{first_subscription_id}')")
        
        # List all customers
        list_all_customers(client)
        
        # Analyze subscription metrics
        analyze_subscription_metrics(client)
        
        # Demonstrate error handling
        demonstrate_error_handling(client)
        
        print("\n🎉 All subscription and customer management examples completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Create subscription products and checkout sessions")
        print("   2. Monitor subscription lifecycle events")
        print("   3. Implement customer communication workflows")
        print("   4. Set up subscription analytics and reporting")
        
    except BagelPayAuthenticationError as e:
        print(f"\n❌ Authentication failed: {e.message}")
        print("Please check your API key and try again.")
        sys.exit(1)
    except BagelPayError as e:
        print(f"\n❌ BagelPay error: {e.message}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)
    finally:
        # Clean up
        if 'client' in locals():
            client.close()


if __name__ == "__main__":
    main()

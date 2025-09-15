#!/usr/bin/env python3
"""
BagelPay SDK - Product Management Examples

This example demonstrates product management operations including:
- Creating products
- Listing products with pagination
- Getting product details
- Updating products
- Archiving and unarchiving products
- Error handling for product operations

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
    CreateProductRequest,
    UpdateProductRequest,
    Product
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


def create_digital_product(client: BagelPayClient) -> str:
    """Create a digital product example."""
    print("\n📦 Creating a digital product...")
    
    try:
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
        
        print(f"✅ Digital product created successfully!")
        print(f"   Product ID: {product.product_id}")
        print(f"   Name: {product.name}")
        print(f"   Price: ${product.price} {product.currency}")
        print(f"   Type: {product.billing_type}")
        print(f"   Archived: {product.is_archive}")
        
        return product.product_id
        
    except BagelPayValidationError as e:
        print(f"❌ Validation error: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def create_subscription_product(client: BagelPayClient) -> str:
    """Create a subscription product example."""
    print("\n🔄 Creating a subscription product...")
    
    try:
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
        
        print(f"✅ Subscription product created successfully!")
        print(f"   Product ID: {product.product_id}")
        print(f"   Name: {product.name}")
        print(f"   Price: ${product.price} {product.currency}/month")
        print(f"   Type: {product.billing_type}")
        print(f"   Recurring: {product.recurring_interval}")
        print(f"   Archived: {product.is_archive}")
        
        return product.product_id
        
    except BagelPayValidationError as e:
        print(f"❌ Validation error: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def list_all_products(client: BagelPayClient) -> None:
    """List all products with pagination."""
    print("\n📋 Listing all products...")
    
    try:
        page_num = 1
        page_size = 5
        total_products = 0
        
        while True:
            response = client.list_products(pageNum=page_num, pageSize=page_size)
            total_pages = int(response.total / page_size) + 1
            
            if page_num == 1:
                print(f"📊 Total products found: {response.total}")
                print(f"📄 Total pages: {total_pages}")
            
            if not response.items:
                break
            
            print(f"\n--- Page {page_num} ---")
            for product in response.items:
                total_products += 1
                print(f"  {total_products}. {product.name}")
                print(f"     ID: {product.product_id}")
                print(f"     Price: ${product.price} {product.currency}")
                print(f"     Type: {product.billing_type}")
                print(f"     Archived: {product.is_archive}")
                print(f"     Recurring: {product.recurring_interval}")
                print(f"     Created: {product.created_at}")
                print()
            
            if page_num >= total_pages:
                break
            
            page_num += 1
        
        print(f"✅ Listed {total_products} products across {page_num} pages")
        
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def get_product_details(client: BagelPayClient, product_id: str) -> None:
    """Get detailed information about a specific product."""
    print(f"\n🔍 Getting details for product {product_id}...")
    
    try:
        product = client.get_product(product_id)
        
        print(f"✅ Product details retrieved successfully!")
        print(f"   ID: {product.product_id}")
        print(f"   Name: {product.name}")
        print(f"   Description: {product.description}")
        print(f"   Price: ${product.price} {product.currency}")
        print(f"   Type: {product.billing_type}")
        print(f"   Archived: {product.is_archive}")
        print(f"   Recurring: {product.recurring_interval}")
        print(f"   Created: {product.created_at}")
        print(f"   Updated: {product.updated_at}")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Product not found: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def update_product_details(client: BagelPayClient, product_id: str) -> None:
    """Update product information."""
    print(f"\n✏️ Updating product {product_id}...")
    
    try:
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
        
        updated_product = client.update_product(update_request)
        
        print(f"✅ Product updated successfully!")
        print(f"   ID: {updated_product.product_id}")
        print(f"   New Name: {updated_product.name}")
        print(f"   New Price: ${updated_product.price} {updated_product.currency}")
        print(f"   Updated: {updated_product.updated_at}")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Product not found: {e.message}")
        raise
    except BagelPayValidationError as e:
        print(f"❌ Validation error: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def archive_and_unarchive_product(client: BagelPayClient, product_id: str) -> None:
    """Demonstrate archiving and unarchiving a product."""
    print(f"\n📦 Archiving product {product_id}...")
    
    try:
        # Archive the product
        archived_product = client.archive_product(product_id)
        print(f"✅ Product archived successfully!")
        print(f"   Is archived?: {archived_product.is_archive}")
        
        # Unarchive the product
        print(f"\n📦 Unarchiving product {product_id}...")
        unarchived_product = client.unarchive_product(product_id)
        print(f"✅ Product unarchived successfully!")
        print(f"   Is archived?: {unarchived_product.is_archive}")
        
    except BagelPayNotFoundError as e:
        print(f"❌ Product not found: {e.message}")
        raise
    except BagelPayAPIError as e:
        print(f"❌ API error: {e.message}")
        raise
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        raise


def demonstrate_error_handling(client: BagelPayClient) -> None:
    """Demonstrate various error handling scenarios."""
    print("\n🚨 Demonstrating error handling...")
    
    # Try to get a non-existent product
    print("\n1. Trying to get a non-existent product...")
    try:
        client.get_product("non-existent-product-id")
    except BagelPayNotFoundError as e:
        print(f"✅ Correctly caught NotFoundError: {e.message}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
    
    # Try to create a product with invalid data
    print("\n2. Trying to create a product with invalid price...")
    try:
        invalid_request = CreateProductRequest(
            name="Invalid Product",
            description="This product has an invalid price",
            price=-10.0,  # Invalid negative price
            currency="USD",
            billing_type="one_time",
            tax_inclusive=True,
            tax_category="digital_goods",
            recurring_interval="none",
            trial_days=0
        )
        client.create_product(invalid_request)
    except BagelPayValidationError as e:
        print(f"✅ Correctly caught ValidationError: {e.message}")
    except BagelPayAPIError as e:
        print(f"✅ Correctly caught API error: {e.message}")
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")


def main():
    """Main function to run all product management examples."""
    print("🚀 BagelPay SDK - Product Management Examples")
    print("=" * 50)
    
    try:
        # Initialize client
        client = get_client(
            api_key="bagel_test_64C70FE8526A48568D4EEA9D9164F508"
        )
        
        # Create products
        digital_product_id = create_digital_product(client)
        subscription_product_id = create_subscription_product(client)
        
        # List all products
        list_all_products(client)
        
        # Get product details
        get_product_details(client, digital_product_id)
        
        # Update product
        update_product_details(client, digital_product_id)
        
        # Archive and unarchive
        archive_and_unarchive_product(client, subscription_product_id)
        
        # Demonstrate error handling
        demonstrate_error_handling(client)
        
        print("\n🎉 All product management examples completed successfully!")
        
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
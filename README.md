# BagelPay Python SDK

A comprehensive Python client library for the BagelPay API, providing developers with an easy-to-use payment integration solution.

## 🔗 Related Links

- 🌏 **BagelPay Website**: [https://bagelpay.io](https://bagelpay.io)
- 🌏 **Developer Dashboard**: [https://bagelpay.io/dashboard](https://bagelpay.io/dashboard)
- 📖 **Official Documentation**: [https://bagelpay.gitbook.io/docs](https://bagelpay.gitbook.io/docs)
- 📖 **API Documentation**: [https://bagelpay.gitbook.io/docs/apireference](https://bagelpay.gitbook.io/docs/apireference)
- 📧 **Technical Support**: support@bagelpayment.com
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/bagelpay/bagelpay-sdk-python/issues)

  
## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Installation Guide](#installation-guide)
- [Basic Configuration](#basic-configuration)
- [Beginner Tutorial](#beginner-tutorial)
- [API Reference](#api-reference)
- [Example Code](#example-code)
- [Error Handling](#error-handling)
- [Testing Guide](#testing-guide)
- [Development Guide](#development-guide)
- [Advanced Usage](#advanced-usage)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)
- [FAQ](#faq)

## 🚀 Quick Start

### 30-Second Quick Demo

```python
import random
from bagelpay import BagelPayClient, CheckoutRequest, CreateProductRequest

# 1. Create account at [BagelPay Dashboard](https://dashboard.bagelpay.io)
# 2. Go to "Developer Settings" → "API Keys"
# 3. Generate new API key for your environment
# 3. Save your test and live keys securely

# 1. Initialize the client
client = BagelPayClient(
    api_key="your-api-key-here"
)

# 2. Create a sample product
product = client.create_product(CreateProductRequest(
    name="Product_name",
    description="Description_of_product",
    price=29.99
    currency="USD",
    billing_type="subscription",
    tax_inclusive=False,
    tax_category="digital_products",
    recurring_interval="daily",
    trial_days=1
    ))

# 3. Get payment URL
print(f"Product URL: {product.product_url}")

# 4. Complete the checkout session
# For testing payments, you could use the test card '4242 4242 4242 4242' with any expiration and CVV.
```

## 📦 Installation Guide

### System Requirements

- **Python**: 3.11 or higher (recommended), minimum 3.8
- **Package Manager**: pip or poetry

### Method 1: Install from PyPI (Recommended)

```bash
# Install latest stable version
pip install bagelpay

# Install specific version
pip install bagelpay==1.0.1

# Upgrade to latest version
pip install --upgrade bagelpay

# Install with optional dependencies
pip install bagelpay[dev,test]
```

### Method 2: Using Poetry

```bash
# Add to your project
poetry add bagelpay

# Add specific version
poetry add bagelpay==1.0.1
```

### Method 3: Install from Source (Development)

```bash
# Clone the repository
git clone https://github.com/bagelpay/bagelpay-sdk-python.git
cd bagelpay-sdk-python/generated-sdks/python

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install SDK in development mode
pip install -e .

# Verify installation
python -c "import bagelpay; print('Installation successful!')"
```

### Verify Installation

```python
import bagelpay
from bagelpay import BagelPayClient

print(f"BagelPay SDK Version: {bagelpay.__version__}")
print(f"Available modules: {dir(bagelpay)}")

# Test basic functionality
try:
    client = BagelPayClient(api_key="test")
    print("✅ SDK imported successfully")
except Exception as e:
    print(f"❌ Import failed: {e}")
```

## ⚙️ Basic Configuration

### Getting API Keys

1. **Sign up**: Create account at [BagelPay Dashboard](https://dashboard.bagelpay.io)
2. **Navigate**: Go to "Developer Settings" → "API Keys"
3. **Create Key**: Generate new API key for your environment
4. **Copy**: Save your test and live keys securely
5. **Environment**: Start with test keys for development

### Environment Variables Setup

```bash
# Create .env file in your project root
echo "BAGELPAY_API_KEY=your-test-api-key-here" > .env
echo "BAGELPAY_BASE_URL=https://test.bagelpay.io" >> .env
echo "BAGELPAY_TIMEOUT=30" >> .env
echo "BAGELPAY_DEBUG=false" >> .env

# Load environment variables
export $(cat .env | xargs)

# Or use python-dotenv
pip install python-dotenv
```

### Client Initialization Options

```python
from bagelpay import BagelPayClient
import os


# Method 1: Direct parameters
client = BagelPayClient(
    base_url="https://test.bagelpay.io",
    api_key="your-api-key",
    timeout=30,  # Request timeout in seconds
)

# Method 2: Configuration dictionary
config = {
    "base_url": "https://test.bagelpay.io",
    "api_key": os.getenv("BAGELPAY_API_KEY"),
    "timeout": 30
}
client = BagelPayClient(**config)

# Method 4: Context manager (recommended for production)
with BagelPayClient(api_key="your-api-key") as client:
    # Automatically handles connection cleanup
    response = client.list_products()
    print(f"Found {response.total} products")
```

### Environment-Specific Configuration

```python
# Development environment
dev_client = BagelPayClient(
    base_url="https://test.bagelpay.io",
    api_key="test_key_xxx",
    timeout=60
)

# Staging environment
staging_client = BagelPayClient(
    base_url="https://staging.bagelpay.io",
    api_key="staging_key_xxx",
    timeout=30
)

# Production environment
production_client = BagelPayClient(
    base_url="https://api.bagelpay.io",
    api_key="live_key_xxx",
    timeout=15,
)
```

## 📚 Beginner Tutorial

### Step 1: Create Your First Product

```python
from bagelpay import BagelPayClient, CreateProductRequest

# Initialize client
client = BagelPayClient(api_key="your-test-api-key")

# Create a digital product
product_request = CreateProductRequest(
    name="Premium Membership",
    description="Access to all premium features with monthly billing",
    price=29.99,
    currency="USD",
    billing_type="subscription", # subscription or single_payment
    tax_inclusive=True,
    tax_category="digital_products", # digital_products, saas_services or ebooks
    recurring_interval="daily", # daily, weekly, monthly, 3months or 6months
    trial_days=1,
)

try:
    product = client.create_product(product_request)
    print(f"✅ Product created successfully!")
    print(f"Product ID: {product.product_id}")
    print(f"Product Name: {product.name}")
    print(f"Price: ${product.price} {product.currency}")
except Exception as e:
    print(f"❌ Failed to create product: {e}")
```

### Step 2: Create a Payment Session

```python
from bagelpay import CheckoutRequest, Customer

# Prepare customer information
customer = Customer(
    email="john.doe@example.com"
)

# Create checkout request
from datetime import datetime

checkout_request = CheckoutRequest(
    product_id=product.product_id,  # Use the product ID from step 1
    request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    units="1",
    customer=customer,
    success_url="https://yoursite.com/success",
    metadata={
        "order_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "user_id": "user_12345",
        "source": "web_app",
        "campaign": "summer_promotion"
    }
)

try:
    checkout_response = client.create_checkout(checkout_request)
    
    print(f"✅ Checkout session created!")
    print(f"Payment URL: {checkout_response.checkout_url}")
    print(f"Payment ID: {checkout_response.payment_id}")
    print(f"Product ID: {checkout_response.product_id}")
    print(f"Status: {checkout_response.status}")
    print(f"Expires On: {checkout_response.expires_on}")
    
    # Store payment ID for later reference
    payment_id = checkout_response.payment_id
    
except Exception as e:
    print(f"❌ Failed to create checkout: {e}")
```

### Step 3: Monitor Transactions

```python
# Get transaction history
try:
    transactions = client.list_transactions(pageNum=1, pageSize=20)
    
    print(f"\n📊 Transaction Summary:")
    print(f"Total Transactions: {transactions.total}")
    print(f"Showing {len(transactions.items)} transactions on this page")
    print(f"Items per Page: 20")
except Exception as e:
    print(f"❌ Failed to fetch transactions: {e}")
```

### Step 4: Manage Products

```python
# List all products
try:
    products = client.list_products(pageNum=1, pageSize=50)
    
    print(f"\n🛍️ Product Catalog ({products.total} total):")
    
    for product in products.items:
        status = "🟢 Active" if not product.is_archive else "🔴 Archived"
        print(f"\n{status} {product.name}")
        print(f"   ID: {product.product_id}")
        if product.recurring_interval:
            print(f"   Price: ${product.price} {product.currency}/{product.recurring_interval}")
        else:
            print(f"   Price: ${product.price} {product.currency}")
        print(f"   Type: {product.billing_type}")
        print(f"   Created: {product.created_at}")
    
    # Update a product
    if products.items:
        first_product = products.items[0]
        
        from bagelpay import UpdateProductRequest
        import random
        
        update_request = UpdateProductRequest(
            product_id=first_product.product_id,
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
        print(f"\n✅ Updated product: {updated_product.name}")
        print(f"   New price: ${updated_product.price}")
        
except Exception as e:
    print(f"❌ Failed to manage products: {e}")
```

## 🔧 API Reference

### Product Management API

#### Creating Products

```python
# One-time payment product
one_time_product = CreateProductRequest(
    name="E-book: Python Programming Guide",
    description="Comprehensive guide to Python programming",
    price=49.99,
    currency="USD",
    billing_type="single_payment",
    tax_inclusive=False,
    tax_category="digital_products",
    recurring_interval="none",
    trial_days=0
)

# Subscription product
subscription_product = CreateProductRequest(
    name="Monthly Pro Plan",
    description="Professional features with monthly billing",
    price=19.99,
    currency="USD",
    billing_type="subscription",
    tax_inclusive=True,
    tax_category="digital_products",
    recurring_interval="monthly",
    trial_days=14
)
```

#### Product Operations

```python
# Get product details
product = client.get_product("prod_123456")
print(f"Product: {product.name}")
print(f"Status: {'Active' if not product.is_archive else 'Archived'}")

# Archive product (stop selling but keep records)
archived_product = client.archive_product("prod_123456")
print(f"Product archived: {archived_product.is_archive}")

# Unarchive product
unarchived_product = client.unarchive_product("prod_123456")
print(f"Product restored: {not unarchived_product.is_archive}")

# Bulk product operations
all_products = []
page_num = 1
while True:
    products = client.list_products(pageNum=page_num, pageSize=100)
    all_products.extend(products.items)
    
    if len(products.items) < 100:
        break
    page_num += 1

print(f"Total products loaded: {len(all_products)}")

# Filter products by criteria
active_products = [p for p in all_products if not p.is_archive]
subscription_products = [p for p in all_products if p.billing_type == "subscription"]
expensive_products = [p for p in all_products if p.price > 100]

print(f"Active products: {len(active_products)}")
print(f"Subscription products: {len(subscription_products)}")
print(f"Premium products (>$100): {len(expensive_products)}")
```

### Payment Session API

#### Advanced Checkout Configuration

```python
# Comprehensive checkout request
from datetime import datetime

advanced_checkout = CheckoutRequest(
    product_id="prod_premium_plan",
    request_id=f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    units="3",
    customer=Customer(
        email="premium.user@company.com"
    ),
    success_url="https://yoursite.com/success",
    metadata={
        # Campaign tracking
        "order_id": f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "campaign_id": "black_friday_2024",
        "discount_code": "SAVE30",
        "affiliate_id": "partner_123",
        
        # User context
        "user_id": "user_789",
        "user_tier": "enterprise",
        "company": "Tech Corp Inc",
        
        # Analytics
        "source": "landing_page",
        "medium": "organic",
        "referrer": "https://google.com",
        "utm_campaign": "product_launch"
    }
)

response = client.create_checkout(advanced_checkout)

# Extract detailed checkout information
print(f"\n💳 Checkout Session Created:")
print(f"Payment ID: {response.payment_id}")
print(f"Checkout URL: {response.checkout_url}")
print(f"Product ID: {response.product_id}")
print(f"Status: {response.status}")
print(f"Expires On: {response.expires_on}")
print(f"Success URL: {response.success_url}")
```


### Subscription Management API

```python
# Comprehensive subscription management
def manage_subscriptions(client):
    """Manage customer subscriptions"""
    try:
        subscriptions = client.list_subscriptions(pageNum=1, pageSize=100)
        
        print(f"\n🔄 Subscription Management ({subscriptions.total} total):")
        
        active_subs = []
        cancelled_subs = []
        paused_subs = []
        trialing_subs = []
        
        for subscription in subscriptions.items:
            print(f"\n📋 Subscription: {subscription.subscription_id}")
            print(f"   Status: {subscription.status}")
            print(f"   Customer: {subscription.customer}")
            print(f"   Product: {subscription.product_name}")
            print(f"   Next Billing: {subscription.billing_period_end}")
            print(f"   Next Billing Amount: ${subscription.next_billing_amount}")
            
            if subscription.status == "active":
                active_subs.append(subscription)
            elif subscription.status == "canceled":
                cancelled_subs.append(subscription)
            elif subscription.status == "paused":
                paused_subs.append(subscription)
            elif subscription.status == "trialing":
                trialing_subs.append(subscription)

        print(f"\n📈 Subscription Summary:")
        print(f"Active: {len(active_subs)}")
        print(f"Cancelled: {len(cancelled_subs)}")
        print(f"Paused: {len(paused_subs)}")
        print(f"Trialing: {len(trialing_subs)}")
        
        # Calculate MRR (Monthly Recurring Revenue)
        monthly_revenue = sum(
            sub.next_billing_amount for sub in active_subs 
            if sub.recurring_interval == "monthly"
        )
        annual_revenue = sum(
            sub.next_billing_amount / 12 for sub in active_subs 
            if sub.recurring_interval == "yearly"
        )
        total_mrr = monthly_revenue + annual_revenue
        
        print(f"💰 Monthly Recurring Revenue: ${total_mrr:.2f}")
        
        return {
            "active": len(active_subs),
            "cancelled": len(cancelled_subs),
            "paused_subs": len(paused_subs),
            "trialing_subs": len(trialing_subs),
            "mrr": total_mrr
        }
        
    except Exception as e:
        print(f"❌ Error managing subscriptions: {e}")
        return None

# Cancel subscription with reason
def cancel_subscription_with_reason(client, subscription_id):
    """Cancel subscription with cancellation reason"""
    try:
        # Note: This assumes the SDK supports cancellation reasons
        result = client.cancel_subscription(
            subscription_id,
        )
        print(f"✅ Subscription {subscription_id} cancelled")
        return result
    except Exception as e:
        print(f"❌ Failed to cancel subscription: {e}")
        return None

manage_subscriptions(client)
cancel_subscription_with_reason(client, "sub_1966676965965533186")
```


## 💡 Example Code

The SDK includes comprehensive examples in the `examples/` directory:

### Available Examples

| File | Description | Use Case | Complexity |
|------|-------------|----------|------------|
| `basic_usage.py` | Basic SDK functionality | Getting started | Beginner |
| `checkout_payments.py` | Complete payment flow | E-commerce integration | Intermediate |
| `product_management.py` | Product CRUD operations | Catalog management | Intermediate |
| `subscription_customer_management.py` | Subscription & customer ops | SaaS applications | Advanced |

### Running Examples

```bash
# Set up environment
export BAGELPAY_API_KEY="your-test-api-key"
export BAGELPAY_BASE_URL="https://test.bagelpay.io"

# Run basic example
python examples/basic_usage.py

# Run with verbose output
BAGELPAY_DEBUG=true python examples/checkout_payments.py
```


## ⚠️ Error Handling

### Exception Hierarchy

```python
from bagelpay.exceptions import (
    BagelPayError,              # Base exception class
    BagelPayAPIError,           # API-related errors
    BagelPayAuthenticationError, # Authentication failures
    BagelPayValidationError,    # Request validation errors
    BagelPayNotFoundError,      # Resource not found
    BagelPayRateLimitError,     # Rate limiting
    BagelPayNetworkError,       # Network connectivity issues
    BagelPayTimeoutError        # Request timeout
)

# Exception hierarchy:
# BagelPayError
# ├── BagelPayAPIError
# │   ├── BagelPayAuthenticationError
# │   ├── BagelPayValidationError
# │   ├── BagelPayNotFoundError
# │   └── BagelPayRateLimitError
# ├── BagelPayNetworkError
# └── BagelPayTimeoutError
```

## 🧪 Testing Guide

### Test Suite Overview

The SDK includes a comprehensive test suite with multiple testing strategies:

```bash
# Test runner with all options
python run_tests.py --help

# Basic test execution
python run_tests.py                    # Run all tests
python run_tests.py --unit             # Unit tests only
python run_tests.py --integration      # Integration tests only
python run_tests.py --mock             # Mock mode (no real API calls)
python run_tests.py --coverage         # Generate coverage report
python run_tests.py --fast             # Parallel execution
python run_tests.py --verbose          # Detailed output
```

### Test Configuration

```bash
# Environment setup for testing
export BAGELPAY_API_KEY="test_key_12345"
export BAGELPAY_BASE_URL="https://test.bagelpay.io"
export BAGELPAY_TEST_MODE="true"
export BAGELPAY_DEBUG="false"

# Install test dependencies
pip install pytest pytest-mock pytest-cov pytest-xdist responses

# Or use the setup command
python run_tests.py --setup
```


### Project Structure

```
bagelpay-sdk-python/
├── bagelpay/      # Main SDK package
│   ├── __init__.py         # Package initialization
│   ├── client.py           # Main client class
│   ├── models.py           # Data models
│   ├── exceptions.py       # Custom exceptions
│   └── utils.py            # Utility functions
├── examples/               # Example scripts
│   ├── basic_usage.py      # Basic functionality
│   ├── checkout_payments.py # Payment processing
│   ├── product_management.py # Product operations
│   └── subscription_customer_management.py # Advanced features
├── tests/                  # Test suite
│   ├── conftest.py         # Test configuration
│   ├── test_client.py      # Client tests
│   ├── test_models.py      # Model tests
│   ├── test_exceptions.py  # Exception tests
│   └── test_integration.py # Integration tests
├── docs/                   # Documentation
├── requirements.txt        # Dependencies
├── setup.py               # Package setup
├── run_tests.py           # Test runner
├── pytest.ini            # Pytest configuration
└── README.md              # This file
```

### Contributing Guidelines

1. **Fork and Clone**
   ```bash
   git fork https://github.com/bagelpay/bagelpay-sdk-python.git
   git clone https://github.com/yourusername/bagelpay-sdk-python.git
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-new-feature
   ```

3. **Make Changes**
   - Follow existing code style
   - Add tests for new functionality
   - Update documentation
   - Ensure all tests pass

4. **Quality Checks**
   ```bash
   # Run all tests
   python run_tests.py --coverage
   
   # Code quality
   black bagelpay/
   flake8 bagelpay/
   mypy bagelpay/
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add amazing new feature"
   git push origin feature/amazing-new-feature
   ```

6. **Create Pull Request**
   - Provide clear description
   - Include test results
   - Reference related issues


## 🚀 Webhook Integration

```python
import hmac
import hashlib
import json

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from pyngrok import ngrok
ngrok.set_auth_token("your_ngrok_key")
WEBHOOK_SECRET = "your_webhook_key"

app = FastAPI()


def verify_webhook_signature(signature_data: bytes, signature: str, secret: str) -> bool:
    """Verify webhook signature for security"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        signature_data,
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, signature)


@app.post("/api/webhooks")
async def handle_post(request: Request):
    """Handle BagelPay webhook notifications"""
    payload = await request.body()
    timestamp = request.headers.get('timestamp').encode()
    signature = request.headers.get('bagelpay_signature')
    # Combine payload and timestamp
    signature_data = timestamp + ".".encode() + payload

    if not verify_webhook_signature(signature_data, signature, WEBHOOK_SECRET):
        return JSONResponse(status_code=401, content={"error": "Invalid signature"})

    try:
        event = json.loads(payload)
        event_type = event.get('event_type')
        data = event.get('object')

        if event_type == 'checkout.completed':
            # handle checkout completed events
            print(event)
        elif event_type == 'checkout.failed':
            # handle checkout failed events
            print(event)
        elif event_type == 'checkout.cancel':
            # handle checkout cancelled events
            print(event)
        elif event_type == 'subscription.trialing':
            # handle subscription trialing events
            print(event)
        elif event_type == 'subscription.paid':
            # handle subscription paid events
            print(event)
        elif event_type == 'subscription.canceled':
            # handle subscription cancelled events
            print(event)
        elif event_type == 'refund.created':
            # handle refund created events
            print(event)
        else:
            print(f"Unhandled event type: {event_type}")

        return JSONResponse(status_code=200, content={"message": "Success"})
    except Exception as e:
        print(f"Webhook processing error: {e}")
        return JSONResponse(status_code=500, content={"error": "Processing failed"})


if __name__ == "__main__":
    listening_port = "8000"
    public_url = ngrok.connect(
        addr=listening_port,
        proto="http",
        hostname="stunning-crane-direct.ngrok-free.app"
    )
    print(f"ngrok Public URL: {public_url}")
    uvicorn.run(app, host="0.0.0.0", port=int(listening_port))
```


## ❓ FAQ

### General Questions

**Q: What Python versions are supported?**

A: The SDK supports Python 3.8+ with the following recommendations:
- **Recommended**: Python 3.11 or higher
- **Minimum**: Python 3.8
- **Tested on**: Python 3.8, 3.9, 3.10, 3.11, 3.12

**Q: How do I switch between test and production environments?**

```python
# Test environment
test_client = BagelPayClient(
    base_url="https://test.bagelpay.io",
    api_key="test_key_xxx"
)

# Production environment
prod_client = BagelPayClient(
    base_url="https://live.bagelpay.io",
    api_key="live_key_xxx"
)
```

**Q: How do I handle webhook verification?**

```python
import hmac
import hashlib

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import uvicorn
from pyngrok import ngrok
ngrok.set_auth_token("your_ngrok_key")
WEBHOOK_SECRET = "your_webhook_key"

app = FastAPI()


def verify_webhook_signature(signature_data: bytes, signature: str, secret: str) -> bool:
    """Verify webhook signature for security"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        signature_data,
        hashlib.sha256
    ).hexdigest()

    print("expected_signature: ", expected_signature)
    print("signature: ", signature)

    return hmac.compare_digest(expected_signature, signature)


@app.post("/api/webhooks")
async def handle_post(request: Request):
    """Handle BagelPay webhook notifications"""
    payload = await request.body()
    timestamp = request.headers.get('timestamp').encode()
    signature = request.headers.get('bagelpay_signature')
    # Combine payload and timestamp
    signature_data = timestamp + ".".encode() + payload
    print("payload: ", payload)
    print("timestamp: ", timestamp)
    print("signature: ", signature)
    print("signature_data: ", signature_data)

    if not verify_webhook_signature(signature_data, signature, WEBHOOK_SECRET):
        return JSONResponse(status_code=401, content={"error": "Invalid signature"})

    print(payload)
    return JSONResponse(status_code=200, content={"message": "Success"})


if __name__ == "__main__":
    listening_port = "8000"
    public_url = ngrok.connect(
        addr=listening_port,
        proto="http",
        hostname="stunning-crane-direct.ngrok-free.app"
    )
    print(f"ngrok Public URL: {public_url}")
    uvicorn.run(app, host="0.0.0.0", port=int(listening_port))
```


### Integration Questions

**Q: How do I integrate with popular web frameworks?**

**Flask Integration:**
```python
from flask import Flask, request, jsonify
from bagelpay import BagelPayClient

app = Flask(__name__)
client = BagelPayClient(api_key=os.getenv('BAGELPAY_API_KEY'))

@app.route('/create-payment', methods=['POST'])
def create_payment():
    try:
        data = request.get_json()
        
        checkout_request = CheckoutRequest(...)
        response = client.create_checkout(checkout_request)
        
        return jsonify({
            'success': True,
            'payment_url': response.data.checkout_url,
            'payment_id': response.data.payment_id
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400
```

**Django Integration:**
```python
# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

@csrf_exempt
@require_http_methods(["POST"])
def create_payment(request):
    try:
        data = json.loads(request.body)
        
        # Use your BagelPay client here
        checkout_request = CheckoutRequest(...)
        response = client.create_checkout(checkout_request)
        
        return JsonResponse({
            'success': True,
            'payment_url': response.data.checkout_url
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
```


## 📞 Support and Resources

### Getting Help

- 📖 **Official Documentation**: [https://bagelpay.gitbook.io/docs](https://bagelpay.gitbook.io/docs)
- 📧 **Technical Support**: support@bagelpayment.com
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/bagelpay/bagelpay-sdk-python/issues)


## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Links

- [BagelPay Website](https://bagelpay.io)
- [API Documentation](https://bagelpay.gitbook.io/docs/apireference)
- [Developer Dashboard](https://bagelpay.io/dashboard)
- [Privacy Policy](https://bagelpay.io/privacy)
- [Terms of Service](https://bagelpay.io/terms)

---

**Start building with BagelPay SDK and make payment integration simple!** 🎉

*For the latest updates and announcements, follow us on [Twitter](https://x.com/BagelPay) and [LinkedIn](https://www.linkedin.com/company/bagel-payment).*

"""BagelPay API Client"""

import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin

from .models import (
    CheckoutRequest,
    CheckoutResponse,
    CreateProductRequest,
    Product,
    ProductListResponse,
    UpdateProductRequest,
    TransactionListResponse,
    Subscription,
    SubscriptionListResponse,
    CustomerListResponse,
    ApiError
)
from .exceptions import BagelPayError, BagelPayAPIError


class BagelPayClient:
    """BagelPay API Client
    
    This client provides access to the BagelPay API endpoints.
    
    Args:
        api_key: API key for authentication
        test_mode: Whether to use test mode (default: True)
        base_url: Optional custom base URL (overrides test_mode)
        timeout: Request timeout in seconds (default: 30)
    """
    
    def __init__(
        self,
        api_key: str,
        test_mode: bool = True,
        base_url: Optional[str] = None,
        timeout: int = 30
    ):
        # Determine base URL based on test mode
        if base_url:
            self.base_url = base_url.rstrip('/')
        else:
            self.base_url = 'https://test.bagelpay.io' if test_mode else 'https://live.bagelpay.io'
        
        self.api_key = api_key
        self.test_mode = test_mode
        self.timeout = timeout
        self.session = requests.Session()
        
        # Set default headers
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'BagelPay-Python-SDK/1.0.0'
        })
        
        # Set authorization header
        self.session.headers['x-api-key'] = api_key
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to the API
        
        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters
            
        Returns:
            Response data as dictionary
            
        Raises:
            BagelPayAPIError: If API returns an error
            BagelPayError: If request fails
        """
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.timeout
            )
            
            # Check if request was successful
            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    error = ApiError.from_dict(error_data)
                    raise BagelPayAPIError(
                        message=error.message,
                        error_code=error.code,
                        status_code=response.status_code,
                        api_error=error
                    )
                except ValueError:
                    # Response is not JSON
                    raise BagelPayAPIError(
                        message=f"HTTP {response.status_code}: {response.text}",
                        status_code=response.status_code
                    )
            
            try:
                data = response.json()
                
                # Check if the response contains an error even with 200 status
                if isinstance(data, dict) and 'msg' in data and 'code' in data:
                    # This looks like an error response
                    if data.get('code') in [401, 403, 404, 400, 422, 500]:
                        error = ApiError.from_dict(data)
                        raise BagelPayAPIError(
                            message=error.message,
                            error_code=error.code,
                            status_code=data.get('code', response.status_code),
                            api_error=error
                        )
                
                return data
            except ValueError:
                # Response is not JSON
                raise BagelPayError(f"Invalid JSON response: {response.text}")
            
        except requests.exceptions.RequestException as e:
            raise BagelPayError(f"Request failed: {str(e)}")
    
    def create_checkout(self, checkout_request: CheckoutRequest) -> CheckoutResponse:
        """Create a new checkout session
        
        Args:
            checkout_request: Checkout request data
            
        Returns:
            Checkout response with session details
        """
        data = self._make_request(
            method='POST',
            endpoint='/api/payments/checkouts',
            data=checkout_request.to_dict()
        )
        return CheckoutResponse.from_dict(data)
    
    def create_product(self, product_request: CreateProductRequest) -> Product:
        """Create a new product
        
        Args:
            product_request: Product creation data
            
        Returns:
            Created product details
        """
        data = self._make_request(
            method='POST',
            endpoint='/api/products/create',
            data=product_request.to_dict()
        )
        return Product.from_dict(data)
    
    def list_products(
        self,
        pageNum: int = 1,
        pageSize: int = 10
    ) -> ProductListResponse:
        """List products with pagination
        
        Args:
            pageNum: Page number (default: 1)
            pageSize: Items per page (default: 10)
            
        Returns:
            Paginated list of products
        """
        params = {
            'pageNum': pageNum,
            'pageSize': pageSize
        }
        
        data = self._make_request(
            method='GET',
            endpoint='/api/products/list',
            params=params
        )
        return ProductListResponse.from_dict(data)
    
    def get_product(self, product_id: str) -> Product:
        """Get product details by ID
        
        Args:
            product_id: Product ID
            
        Returns:
            Product details
        """
        data = self._make_request(
            method='GET',
            endpoint=f'/api/products/{product_id}'
        )
        return Product.from_dict(data)
    
    def archive_product(self, product_id: str) -> Product:
        """Archive a product
        
        Args:
            product_id: Product ID to archive
            
        Returns:
            Updated product details
        """
        data = self._make_request(
            method='POST',
            endpoint=f'/api/products/{product_id}/archive'
        )
        return Product.from_dict(data)
    
    def unarchive_product(self, product_id: str) -> Product:
        """Unarchive a product
        
        Args:
            product_id: Product ID to unarchive
            
        Returns:
            Updated product details
        """
        data = self._make_request(
            method='POST',
            endpoint=f'/api/products/{product_id}/unarchive'
        )
        return Product.from_dict(data)
    
    def update_product(self, request: UpdateProductRequest) -> Product:
        """Update a product
        
        Args:
            request: Product update request data
            
        Returns:
            Updated product details
        """
        data = self._make_request(
            method='POST',
            endpoint='/api/products/update',
            data=request.to_dict()
        )
        return Product.from_dict(data)
    
    def list_transactions(
        self,
        pageNum: int = 1,
        pageSize: int = 10
    ) -> TransactionListResponse:
        """List transactions with pagination
        
        Args:
            pageNum: Page number (default: 1)
            pageSize: Items per page (default: 10)
            
        Returns:
            Paginated list of transactions
        """
        params = {
            'pageNum': pageNum,
            'pageSize': pageSize
        }
        
        data = self._make_request(
            method='GET',
            endpoint='/api/transactions/list',
            params=params
        )
        return TransactionListResponse.from_dict(data)
    
    def list_subscriptions(
        self,
        pageNum: int = 1,
        pageSize: int = 10
    ) -> SubscriptionListResponse:
        """List subscriptions with pagination
        
        Args:
            pageNum: Page number (default: 1)
            pageSize: Items per page (default: 10)
            
        Returns:
            Paginated list of subscriptions
        """
        params = {
            'pageNum': pageNum,
            'pageSize': pageSize
        }
        
        data = self._make_request(
            method='GET',
            endpoint='/api/subscriptions/list',
            params=params
        )
        return SubscriptionListResponse.from_dict(data)
    
    def get_subscription(self, subscription_id: str) -> Subscription:
        """Get subscription details by ID
        
        Args:
            subscription_id: Subscription ID
            
        Returns:
            Subscription details
        """
        data = self._make_request(
            method='GET',
            endpoint=f'/api/subscriptions/{subscription_id}'
        )
        return Subscription.from_dict(data)
    
    def cancel_subscription(self, subscription_id: str) -> Subscription:
        """Cancel a subscription
        
        Args:
            subscription_id: Subscription ID to cancel
            
        Returns:
            Updated subscription details
        """
        data = self._make_request(
            method='POST',
            endpoint=f'/api/subscriptions/{subscription_id}/cancel'
        )
        return Subscription.from_dict(data)
    
    def list_customers(
        self,
        pageNum: int = 1,
        pageSize: int = 10
    ) -> CustomerListResponse:
        """List customers with pagination
        
        Args:
            pageNum: Page number (default: 1)
            pageSize: Items per page (default: 10)
            
        Returns:
            Paginated list of customers
        """
        params = {
            'pageNum': pageNum,
            'pageSize': pageSize
        }
        
        data = self._make_request(
            method='GET',
            endpoint='/api/customers/list',
            params=params
        )
        return CustomerListResponse.from_dict(data)
    
    def close(self):
        """Close the HTTP session"""
        self.session.close()
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
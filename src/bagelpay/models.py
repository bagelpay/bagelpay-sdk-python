"""BagelPay API Models"""

from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Customer:
    """Customer data for checkout session"""
    email: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""
        return {
            "email": self.email
        }


@dataclass
class CheckoutRequest:
    """Request model for creating a checkout session"""
    product_id: str
    customer: Customer
    request_id: Optional[str] = None
    units: Optional[str] = None
    success_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""
        data = {
            "product_id": self.product_id,
            "customer": self.customer.to_dict()
        }
        if self.request_id is not None:
            data["request_id"] = self.request_id
        if self.units is not None:
            data["units"] = self.units
        if self.success_url is not None:
            data["success_url"] = self.success_url
        if self.metadata is not None:
            data["metadata"] = self.metadata
        return data


@dataclass
class CheckoutResponse:
    """Response model for checkout session"""
    object: Optional[str] = None
    units: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None
    status: Optional[str] = None
    mode: Optional[str] = None
    payment_id: Optional[str] = None
    product_id: Optional[str] = None
    request_id: Optional[str] = None
    success_url: Optional[str] = None
    checkout_url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    expires_on: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CheckoutResponse':
        """Create instance from API response"""
        checkout_data = data.get("data", data)
        return cls(
            object=checkout_data["object"],
            units=checkout_data["units"],
            metadata=checkout_data["metadata"],
            status=checkout_data["status"],
            mode=checkout_data["mode"],
            payment_id=checkout_data["payment_id"],
            product_id=checkout_data["product_id"],
            request_id=checkout_data["request_id"],
            success_url=checkout_data["success_url"],
            checkout_url=checkout_data["checkout_url"],
            created_at=checkout_data["created_at"],
            updated_at=checkout_data["updated_at"],
            expires_on=checkout_data["expires_on"]
        )


@dataclass
class CreateProductRequest:
    """Request model for creating a product"""
    name: str
    description: str
    price: float  
    currency: str  
    billing_type: str  
    tax_inclusive: bool
    tax_category: str   
    recurring_interval: str  
    trial_days: int 

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""      
        return {
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "currency": self.currency,
            "billing_type": self.billing_type,
            "tax_inclusive": self.tax_inclusive,
            "tax_category": self.tax_category,
            "recurring_interval": self.recurring_interval,
            "trial_days": self.trial_days
        }


@dataclass
class Product:
    """Product model"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    object: Optional[str] = None
    mode: Optional[str] = None
    product_id: Optional[str] = None
    store_id: Optional[str] = None
    product_url: Optional[str] = None
    billing_type: Optional[str] = None
    billing_period: Optional[str] = None
    tax_category: Optional[str] = None
    tax_inclusive: Optional[bool] = None
    is_archive: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    trial_days: Optional[int] = None
    recurring_interval: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Product':
        """Create instance from API response"""
        product_data = data.get("data", data)
        return cls(
            name=product_data.get("name"),
            description=product_data.get("description"),
            price=product_data.get("price"),
            currency=product_data.get("currency"),
            object=product_data.get("object"),
            mode=product_data.get("mode"),
            product_id=product_data.get("product_id"),
            store_id=product_data.get("store_id"),
            product_url=product_data.get("product_url"),
            billing_type=product_data.get("billing_type"),
            billing_period=product_data.get("billing_period"),
            tax_category=product_data.get("tax_category"),
            tax_inclusive=product_data.get("tax_inclusive"),
            is_archive=product_data.get("is_archive"),
            created_at=product_data.get("created_at"),
            updated_at=product_data.get("updated_at"),
            trial_days=product_data.get("trial_days"),
            recurring_interval=product_data.get("recurring_interval")
        )


@dataclass
class ProductListResponse:
    """Response model for product list"""
    total: int
    items: List[Product]
    code: int
    msg: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductListResponse':
        """Create instance from API response"""
        products = [Product.from_dict(p) for p in data["items"]]
        return cls(
            total=data["total"],
            items=products,
            code=data["code"],
            msg=data["msg"]
        )


@dataclass
class UpdateProductRequest:
    """Request model for updating a product"""
    product_id: str
    name: str
    description: str
    price: float
    currency: str
    billing_type: str   
    tax_inclusive: bool
    tax_category: str  
    recurring_interval: str  
    trial_days: int 

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API requests"""
        return {
            "product_id": self.product_id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "currency": self.currency,
            "billing_type": self.billing_type,
            "tax_inclusive": self.tax_inclusive,
            "tax_category": self.tax_category,
            "recurring_interval": self.recurring_interval,
            "trial_days": self.trial_days
        }


@dataclass
class TransactionCustomer:
    """Customer data in transaction"""
    id: Optional[str]
    email: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TransactionCustomer':
        """Create instance from API response"""
        return cls(
            id=data["id"],
            email=data["email"]
        )


@dataclass
class Transaction:
    """Transaction model"""
    object: Optional[str]
    order_id: Optional[str]
    transaction_id: Optional[str]
    amount: Optional[float]
    amount_paid: Optional[float]
    discount_amount: Optional[float]
    currency: Optional[str]
    tax_amount: Optional[float]
    tax_country: Optional[str]
    refunded_amount: Optional[float]
    type: Optional[str]
    customer: TransactionCustomer
    created_at: Optional[str]
    updated_at: Optional[str]
    remark: Optional[str]
    mode: Optional[str]
    fees: Optional[float]
    tax:  Optional[float]
    net: Optional[float]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Transaction':
        """Create instance from API response"""
        return cls(
            object=data["object"],
            order_id=data["order_id"],
            transaction_id=data["transaction_id"],
            amount=data["amount"],
            amount_paid=data["amount_paid"],
            discount_amount=data["discount_amount"],
            currency=data["currency"],
            tax_amount=data["tax_amount"],
            tax_country=data["tax_country"],
            refunded_amount=data["refunded_amount"],
            type=data["type"],
            customer=TransactionCustomer.from_dict(data["customer"]),
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            remark=data["remark"],
            mode=data["mode"],
            fees=data["fees"],
            tax=data["tax"],
            net=data["net"]
        )


@dataclass
class TransactionListResponse:
    """Response model for transaction list"""
    total: int
    items: List[Transaction]
    code: int
    msg: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TransactionListResponse':
        """Create instance from API response"""
        transactions = [Transaction.from_dict(t) for t in data["items"]]
        return cls(
            total=data["total"],
            items=transactions,
            code=data["code"],
            msg=data["msg"]
        )


@dataclass
class SubscriptionCustomer:
    """Customer data in subscription"""
    id: Optional[str]
    email: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubscriptionCustomer':
        return cls(
            id=data["id"],
            email=data["email"]
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "email": self.email
        }


@dataclass
class Subscription:
    """Subscription model"""
    status: Optional[str]
    remark: Optional[str]
    customer: SubscriptionCustomer
    mode: Optional[str]
    last4: Optional[str]
    subscription_id: Optional[str]
    product_id: Optional[str]
    store_id: Optional[str]
    billing_period_start: Optional[str]
    billing_period_end: Optional[str]
    cancel_at: Optional[str]
    trial_start: Optional[str]
    trial_end: Optional[str]
    units: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]
    product_name: Optional[str]
    payment_method: Optional[str]
    next_billing_amount: Optional[str]
    recurring_interval: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Subscription':
        subscription_data = data.get("data", data)
        return cls(
            status=subscription_data["status"],
            remark=subscription_data["remark"],
            customer=SubscriptionCustomer.from_dict(subscription_data["customer"]),
            mode=subscription_data["mode"],
            last4=subscription_data["last4"],
            subscription_id=subscription_data["subscription_id"],
            product_id=subscription_data["product_id"],
            store_id=subscription_data["store_id"],
            billing_period_start=subscription_data["billing_period_start"],
            billing_period_end=subscription_data["billing_period_end"],
            cancel_at=subscription_data["cancel_at"],
            trial_start=subscription_data["trial_start"],
            trial_end=subscription_data["trial_end"],
            units=subscription_data["units"],
            created_at=subscription_data["created_at"],
            updated_at=subscription_data["updated_at"],
            product_name=subscription_data["product_name"],
            payment_method=subscription_data["payment_method"],
            next_billing_amount=subscription_data["next_billing_amount"],
            recurring_interval=subscription_data["recurring_interval"]
        )


@dataclass
class SubscriptionListResponse:
    """Response model for subscription list"""
    total: int
    items: List[Subscription]
    code: int
    msg: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubscriptionListResponse':
        return cls(
            total=data["total"],
            items=[Subscription.from_dict(item) for item in data["items"]],
            code=data["code"],
            msg=data["msg"]
        )


@dataclass
class CustomerData:
    """Customer data model"""
    id: Optional[int]
    name: Optional[str]
    email: Optional[str]
    remark: Optional[str]
    subscriptions: Optional[int]
    payments: Optional[int]
    store_id: Optional[str]
    total_spend: Optional[int]
    created_at: Optional[str]
    updated_at: Optional[str]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomerData':
        return cls(
            id=data["id"],
            name=data["name"],
            email=data["email"],
            remark=data["remark"],
            subscriptions=data["subscriptions"],
            payments=data["payments"],
            store_id=data["store_id"],
            total_spend=data["total_spend"],
            created_at=data["created_at"],
            updated_at=data["updated_at"]
        )


@dataclass
class CustomerListResponse:
    """Response model for customer list"""
    total: int
    items: List[CustomerData]
    code: int
    msg: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CustomerListResponse':
        return cls(
            total=data["total"],
            items=[CustomerData.from_dict(item) for item in data["items"]],
            code=data["code"],
            msg=data["msg"]
        )


@dataclass
class ApiError:
    """API error response model"""
    error: str
    message: str
    code: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ApiError':
        """Create instance from API response"""
        return cls(
            error="api_error",
            message=data.get("message", data.get("msg", "")),
            code=str(data.get("code", ""))
        )
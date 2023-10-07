from typing import Generic, List, Literal, TypeVar, TypedDict

TData = TypeVar("TData")

class TypeMessageResponse(TypedDict):
    status: bool
    message: str


class TypeResponse(Generic[TData]):
    status: bool
    message: str
    data: TData


class TypeTransactionInitialize(TypedDict):
    plan: str
    currency: str
    metadata: dict
    reference: str
    callback_url: str
    invoice_limit: str
    channels: List[
        Literal[
            "qr",
            "card",
            "bank",
            "ussd",
            "mobile_money",
            "bank_transfer",
            "eft",
        ]
    ]
    split_code: str
    subaccount: str
    transaction_charge: str
    bearer: Literal["account", "subaccount"]


class TypeTransactionData(TypedDict):
    id: int
    fees: int
    domain: str
    status: str
    amount: str
    message: str
    paid_at: str
    channel: str
    reference: str
    created_at: str
    geteway_response: str
    fees_split: str | None


class TypeLink(TypedDict):
    link: str

class TypeCustomer(TypedDict): 
    email: str 
    phone: str
    first_name: str 
    last_name: str

class TypePlan(TypedDict):
    domain: str 
    name: str 
    plan_code: str 
    description: str 
    amount: int 
    interval: Literal["weekly", "monthly"]
    send_invoices: bool 
    send_sms: bool 

class TypeSubscription(TypedDict):
    plan: TypePlan
    customer: TypeCustomer
    
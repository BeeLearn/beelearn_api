from enum import Enum
from typing import Dict, List, Literal, TypedDict


class TypeTaxRateInfoByRegionCode(TypedDict):
    eligibleForStreamingServiceTaxRate: bool
    taxTier: Literal[
        "TAX_TIER_UNSPECIFIED",
        "TAX_TIER_BOOKS_1",
        "TAX_TIER_NEWS_1",
        "TAX_TIER_NEWS_2",
        "TAX_TIER_MUSIC_OR_AUDIO_1",
        "TAX_TIER_LIVE_OR_BROADCAST_1",
    ]
    streamingTaxType: Literal[
        "STREAMING_TAX_TYPE_UNSPECIFIED",
        "STREAMING_TAX_TYPE_TELCO_VIDEO_RENTAL",
        "STREAMING_TAX_TYPE_TELCO_VIDEO_SALES",
        "STREAMING_TAX_TYPE_TELCO_VIDEO_MULTI_CHANNEL",
        "STREAMING_TAX_TYPE_TELCO_AUDIO_RENTAL",
        "STREAMING_TAX_TYPE_TELCO_AUDIO_SALES",
        "STREAMING_TAX_TYPE_TELCO_AUDIO_MULTI_CHANNEL",
    ]


class TypeTaxAndComplianceSettings(TypedDict):
    eeaWithdrawalRightType: Literal[
        "WITHDRAWAL_RIGHT_TYPE_UNSPECIFIED",
        "WITHDRAWAL_RIGHT_DIGITAL_CONTENT",
        "WITHDRAWAL_RIGHT_SERVICE",
    ]
    isTokenizedDigitalAsset: bool
    taxRateInfoByRegiionCode: Dict[str, TypeTaxRateInfoByRegionCode]


class TypeOfferTag(TypedDict):
    tag: str


class TypePrice(TypedDict):
    nanos: int
    units: int
    currencyCode: str


class TypeOtherRegionsBaseConfig(TypedDict):
    eurPrice: TypePrice
    usdPrice: TypePrice
    newSubscriberAvailability: bool


class TypePrepaidBasePlanType(TypedDict):
    billingPeriodDuration: str
    timeExtension: Literal[
        "TIME_EXTENSION_UNSPECIFIED",
        "TIME_EXTENSION_ACTIVE",
        "TIME_EXTENSION_INACTIVE",
    ]


class TypeAutoRenewingBaseType(TypedDict):
    legacyCompatible: bool
    gracePeriodDuration: str
    billingPeriodDuration: str
    legacyCompatibleSubscriptionOfferId: str
    resubscribeState: Literal[
        "RESUBSCRIBE_STATE_UNSPECIFIED",
        "RESUBSCRIBE_STATE_ACTIVE",
        "RESUBSCRIBE_STATE_INACTIVE",
    ]
    prorationMode: Literal[
        "SUBSCRIPTION_PRORATION_MODE_UNSPECIFIED",
        "SUBSCRIPTION_PRORATION_MODE_CHARGE_ON_NEXT_BILLING_DATE",
        "SUBSCRIPTION_PRORATION_MODE_CHARGE_FULL_PRICE_IMMEDIATELY",
    ]


class TypeMoney(TypedDict):
    units: str
    nanos: int
    currencyCode: str


class TypeState(Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"


class TypeRegionalBasePlanConfig:
    regionCode: str
    price: TypeMoney
    newSubscriberAvailability: bool


class TypeBasePlan(TypedDict):
    basePlanId: str
    state: TypeState
    offerTags: List[TypeOfferTag]
    otherRegionsConfig: TypeOtherRegionsBaseConfig
    regionalConfigs: List[TypeRegionalBasePlanConfig]
    prepaidBasePlanType: TypePrepaidBasePlanType
    autoRenewingBaseType: TypeAutoRenewingBaseType


class TypeListing(TypedDict):
    title: str
    description: str
    languageCode: str
    benefits: List[str]


class TypeSubscription(TypedDict):
    productId: str
    packageName: str
    listings: List[TypeListing]
    basePlans: List[TypeBasePlan]
    taxAndComplianceSettings: TypeTaxAndComplianceSettings


class TypeRegionVerion(TypedDict):
    version: str


class TypeSubscriptionItemPriceChangeDetails(TypedDict):
    newPrice: TypeMoney


class TypeAutoRenewingPlan(TypedDict):
    autoRenewalEnabled: bool
    priceChangeDetails: TypeSubscriptionItemPriceChangeDetails
    priceChangeMode: Literal[
        "PRICE_INCREASE",
        "PRICE_DECREASE",
        "OPT_OUT_PRICE_INCREASE",
        "PRICE_CHANGE_MODE_UNSPECIFIED",
    ]
    priceChangeState: Literal[
        "APPLIED",
        "CONFIRMED",
        "OUTSTANDING",
        "PRICE_CHANGE_STATE_UNSPECIFIED",
    ]
    expectedNewPriceChargeTime: str


class TypeOfferDetails(TypedDict):
    offerId: str
    basePlanId: str
    offerTags: List[str]


class TypeSubscriptionPurchaseLineItem(TypedDict):
    productId: str
    expiryTime: str
    offerDetails: TypeOfferDetails
    automRenewalPlan: TypeAutoRenewingPlan
    prepaidPlan: Dict[Literal["allowExtendAfterTime"], str]
    defferedItemReplacement: Dict[Literal["productId"], str]


class TypeCancelSurveyResult:
    reasonUserInput: str
    reason: Literal[
        "CANCEL_SURVEY_REASON_OTHERS",
        "CANCEL_SURVEY_REASON_FOUND_BETTER_APP",
        "CANCEL_SURVEY_REASON_COST_RELATED",
        "CANCEL_SURVEY_REASON_TECHNICAL_ISSUES",
        "CANCEL_SURVEY_REASON_NOT_ENOUGH_USAGE",
        "CANCEL_SURVEY_REASON_UNSPECIFIED",
    ]


class TypeUserInitiatedCancellation(TypedDict):
    cancelTime: str
    cancelSurveyResult: TypeCancelSurveyResult


class TypeCanceledStateContext(TypedDict):
    userInitiatedCancellation: TypeUserInitiatedCancellation
    systemInitiatedCancellation: any
    developerInitiatedCancellation: any
    replacementInitiatedCancellation: any


class TypeExternalAccountIdentifiers(TypedDict):
    externalAccountId: str
    obfuscatedExternalProfileId: str
    obfuscatedExternalAccountId: str


class TypeSubscribeWithGoogleInfo(TypedDict):
    profileId: str
    givenName: str
    familyName: str
    profileName: str
    emailAddress: str


class TypeSubscriptionState(Enum):
    SUBSCRIPTION_STATE_EXPIRED = "SUBSCRIPTION_STATE_EXPIRED"
    SUBSCRIPTION_STATE_CANCELED = "SUBSCRIPTION_STATE_CANCELED"
    SUBSCRIPTION_STATE_ON_HOLD = "SUBSCRIPTION_STATE_ON_HOLD"
    SUBSCRIPTION_STATE_PAUSED = "SUBSCRIPTION_STATE_PAUSED"
    SUBSCRIPTION_STATE_ACTIVE = "SUBSCRIPTION_STATE_ACTIVE"
    SUBSCRIPTION_STATE_PENDING = "SUBSCRIPTION_STATE_PENDING"
    SUBSCRIPTION_STATE_UNSPECIFIED = "SUBSCRIPTION_STATE_UNSPECIFIED"
    SUBSCRIPTION_STATE_IN_GRACE_PERIOD = "SUBSCRIPTION_STATE_IN_GRACE_PERIOD"


class TypeAcknowlegementState(Enum):
    ACKNOWLEDGEMENT_STATE_PENDING = "ACKNOWLEDGEMENT_STATE_PENDING"
    ACKNOWLEDGEMENT_STATE_UNSPECIFIED = "ACKNOWLEDGEMENT_STATE_UNSPECIFIED"
    ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED = "ACKNOWLEDGEMENT_STATE_ACKNOWLEDGED"


class TypeSubscriptionPurchase(TypedDict):
    kind: str
    regionCode: str
    startTime: str
    lastestOrderId: str
    linkedPurchaseToken: str
    testPurchase: any
    subscriptionState: TypeSubscriptionState
    acknowledgementState: TypeAcknowlegementState
    lineItems: List[TypeSubscriptionPurchaseLineItem]
    canceledStateContext: TypeCanceledStateContext
    subscribeWithGoogleInfo: TypeSubscribeWithGoogleInfo
    externalAccountIdentifiers: TypeExternalAccountIdentifiers
    pausedStateContext: Dict[Literal["autoResumeTime"], str]


class TypeOneTimePurchaseNotificationType(Enum):
    SUBSCRIPTION_RECOVERED = 1
    SUBSCRIPTION_RENEWED = 2
    SUBSCRIPTION_CANCELED = 3
    SUBSCRIPTION_PURCHASED = 4
    SUBSCRIPTION_ON_HOLD = 5
    SUBSCRIPTION_IN_GRACE_PERIOD = 6
    SUBSCRIPTION_RESTARTED = 7
    SUBSCRIPTION_PRICE_CHANGE_CONFIRMED = 8
    SUBSCRIPTION_DEFERRED = 9
    SUBSCRIPTION_PAUSED = 10
    SUBSCRIPTION_PAUSE_SCHEDULE_CHANGED = 11
    SUBSCRIPTION_REVOKED = 12
    SUBSCRIPTION_EXPIRED = 13


class TypeSubscriptionPurchaseNotificationType(Enum):
    ONE_TIME_PRODUCT_PURCHASED = 1
    ONE_TIME_PRODUCT_CANCELED = 2


class TypePurchaseNotification(TypedDict):
    version: str
    purchaseToken: str


class TypeOneTimeNotification(TypePurchaseNotification):
    sku: str
    notificationType: TypeOneTimePurchaseNotificationType


class TypeSubscriptionPurchaseNotification(TypePurchaseNotification):
    subscriptionId: str
    notificationType: TypeSubscriptionPurchaseNotificationType


class TypePlaystoreWebhookMessageData(TypedDict):
    version: str
    packageName: str
    eventTimeMillis: str
    oneTimeProductNotification: TypeOneTimeNotification
    subscriptionNotification: TypeSubscriptionPurchaseNotification


class TypePlaystoreWebhookMessage(TypedDict):
    messageId: str
    data: str | TypePlaystoreWebhookMessageData
    attributes: Dict[str, str]


class TypePlaystoreWebhook(TypedDict):
    subscription: str
    message: TypePlaystoreWebhookMessage

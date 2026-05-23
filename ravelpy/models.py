"""Pydantic v2 entity models mirroring the objects returned by the Ravelry API.

Models are organised in dependency order so that nested types are defined
before the models that reference them.  Self-referential models (those with
child/parent references to themselves) call ``model_rebuild()`` at the end of
the module once all classes are available.

All fields are ``Optional`` by default because the Ravelry API frequently
omits fields depending on the endpoint, query parameters, and account
permissions.
"""

from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Annotated, Any, Optional

from pydantic import BaseModel, BeforeValidator


def _coerce_ravelry_datetime(v: Any) -> Any:
    """Normalize Ravelry's ``YYYY/MM/DD HH:MM:SS ±HHMM`` to ISO 8601."""
    if not isinstance(v, str):
        return v
    # Replace date-part slashes: "2026/05/21" -> "2026-05-21"
    v = v[:10].replace("/", "-") + v[10:]
    # Insert colon in bare numeric timezone offset: " -0400" -> "-04:00"
    parts = v.rsplit(" ", 1)
    if len(parts) == 2:
        body, tz = parts
        if len(tz) == 5 and tz[0] in "+-" and tz[1:].isdigit():
            tz = f"{tz[:3]}:{tz[3:]}"
        v = f"{body}{tz}"
    return v


RavelryDatetime = Annotated[datetime, BeforeValidator(_coerce_ravelry_datetime)]

# ---------------------------------------------------------------------------
# Leaf / primitive models (no nested model dependencies)
# ---------------------------------------------------------------------------


class Ad(BaseModel):
    """A Ravelry advertisement with logo and target URL."""

    logo_url: Optional[str] = None
    target_url: Optional[str] = None


class Business(BaseModel):
    """A Ravelry business entity (designer studio, shop, or publisher)."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    primary_url: Optional[str] = None


class ColorFamily(BaseModel):
    """A named colour family used to categorise yarns and stash."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    color: Optional[str] = None
    spectrum_order: Optional[int] = None


class Craft(BaseModel):
    """A craft type such as knitting or crochet."""

    id: int
    name: str
    permalink: Optional[str] = None


class Document(BaseModel):
    """A downloadable file attached to a product or pattern."""

    id: int
    filename: Optional[str] = None
    bytes: Optional[int] = None
    content_type: Optional[str] = None
    notes: Optional[str] = None
    thumbnail_url: Optional[str] = None


class DownloadLink(BaseModel):
    """A time-limited URL for downloading purchased content."""

    url: Optional[str] = None
    activated_at: Optional[RavelryDatetime] = None
    expires_at: Optional[RavelryDatetime] = None


class FiberAttributeGroup(BaseModel):
    """A grouping of related fiber attributes."""

    id: int
    name: str
    permalink: Optional[str] = None
    parent_id: Optional[int] = None


class FiberAttribute(BaseModel):
    """A single fiber attribute (e.g. machine washable) within a group."""

    id: int
    name: str
    permalink: Optional[str] = None
    fiber_attribute_group_id: Optional[int] = None


class FiberType(BaseModel):
    """A raw fiber type (e.g. merino, cotton) with processing flags."""

    id: int
    name: Optional[str] = None
    animal_fiber: Optional[bool] = None
    synthetic: Optional[bool] = None
    vegetable_fiber: Optional[bool] = None


class ForumStatisticSummary(BaseModel):
    """Aggregated activity statistics for a single forum."""

    forum_id: Optional[int] = None
    new_topics_30day: Optional[int] = None
    new_topics_7day: Optional[int] = None
    new_topics_avg: Optional[int] = None
    pageviews_30day: Optional[int] = None
    pageviews_7day: Optional[int] = None
    pageviews_avg: Optional[int] = None
    posts_30day: Optional[int] = None
    posts_7day: Optional[int] = None
    posts_avg: Optional[int] = None
    unique_pageviews_30day: Optional[int] = None
    unique_pageviews_7day: Optional[int] = None
    unique_pageviews_avg: Optional[int] = None


class Invoice(BaseModel):
    """A payment invoice for a Ravelry store purchase."""

    id: int
    invoice_number: Optional[int] = None
    paid: Optional[bool] = None
    payment_reference: Optional[str] = None


class InvoiceLineItem(BaseModel):
    """A single line item on a store invoice."""

    id: int
    invoice_id: Optional[int] = None
    product_id: Optional[int] = None
    promotion_id: Optional[int] = None
    amount: Optional[Decimal] = None
    promotional_discount_applied: Optional[Decimal] = None
    title: Optional[str] = None


class Language(BaseModel):
    """A language supported by Ravelry for pattern translations."""

    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    permalink: Optional[str] = None
    short_name: Optional[str] = None
    universal: Optional[bool] = None


class NeedleRecord(BaseModel):
    """A needle in a user's needle inventory."""

    id: int
    needle_type_id: Optional[int] = None
    comment: Optional[str] = None


class NeedleSize(BaseModel):
    """A standard needle or hook size with metric and US equivalents."""

    id: int
    name: Optional[str] = None
    metric: Optional[float] = None
    hook: Optional[str] = None
    us: Optional[str] = None
    us_size: Optional[str] = None
    uk_size: Optional[str] = None
    pretty_metric: Optional[str] = None


class NeedleType(BaseModel):
    """A needle type (e.g. straight, circular, DPN)."""

    id: int
    name: Optional[str] = None
    type_name: Optional[str] = None
    description: Optional[str] = None
    length: Optional[float] = None
    metric_name: Optional[str] = None
    needle_size_id: Optional[int] = None


class Page(BaseModel):
    """A static content page on Ravelry."""

    name: Optional[str] = None
    body: Optional[str] = None


class PatternAttribute(BaseModel):
    """A single searchable attribute tag on a pattern."""

    id: int
    permalink: Optional[str] = None


class PatternClassification(BaseModel):
    """Links a pattern to a pattern category."""

    id: int
    pattern_id: Optional[int] = None
    pattern_category_id: Optional[int] = None


class PatternLanguage(BaseModel):
    """Links a pattern to a translated language."""

    id: int
    pattern_id: Optional[int] = None
    language_id: Optional[int] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


class PatternNeedleSize(BaseModel):
    """A needle size requirement as specified on a pattern."""

    id: Optional[int] = None
    needle_size_id: Optional[int] = None
    hook: Optional[bool] = None
    metric: Optional[float] = None
    needle_name: Optional[str] = None
    pretty_metric: Optional[str] = None
    pretty_us: Optional[str] = None
    us: Optional[str] = None


class PatternSourceType(BaseModel):
    """A publication type for pattern sources (e.g. book, magazine, online)."""

    id: int
    name: Optional[str] = None
    long_name: Optional[str] = None
    can_add_to_library: Optional[bool] = None
    requires_url: Optional[bool] = None


class PatternTagging(BaseModel):
    """Maps a pattern attribute to a pattern."""

    id: int
    pattern_id: Optional[int] = None
    pattern_attribute_id: Optional[int] = None


class Payment(BaseModel):
    """A payment transaction record."""

    id: int
    gross: Optional[Decimal] = None
    txn_id: Optional[int] = None
    txn_type: Optional[str] = None


class Photo(BaseModel):
    """A photo with multiple size variants and an optional caption."""

    id: int
    caption: Optional[str] = None
    caption_html: Optional[str] = None
    copyright_holder: Optional[str] = None
    medium_url: Optional[str] = None
    medium2_url: Optional[str] = None
    small_url: Optional[str] = None
    small2_url: Optional[str] = None
    square_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    aspect_ratio: Optional[float] = None
    sort_order: Optional[int] = None
    user_id: Optional[int] = None
    x_offset: Optional[int] = None
    y_offset: Optional[int] = None


class ProductNotification(BaseModel):
    """A version or update notification for a purchased product."""

    id: int
    product_id: Optional[int] = None
    created_at: Optional[RavelryDatetime] = None
    message: Optional[str] = None
    message_html: Optional[str] = None
    version: Optional[str] = None


class ProjectStatus(BaseModel):
    """A named project status (e.g. in progress, finished)."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None


class QueuedProject(BaseModel):
    """A pattern entry in a user's queue."""

    id: int
    short_pattern_name: Optional[str] = None
    position_in_queue: Optional[int] = None


class Saleable(BaseModel):
    """An item that can be sold, linking a product to its underlying entity."""

    id: int
    product_id: Optional[int] = None
    saleable_id: Optional[int] = None
    saleable_type: Optional[str] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


class SavedSearch(BaseModel):
    """A saved search query with optional email subscription."""

    id: int
    title: Optional[str] = None
    search_type: Optional[str] = None
    search_path: Optional[str] = None
    search_parameters: Optional[Any] = None
    subscribed: Optional[bool] = None
    subscription_updated_at: Optional[RavelryDatetime] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None
    last_loaded: Optional[RavelryDatetime] = None


class ShopSchedule(BaseModel):
    """A single day's opening hours for a yarn shop."""

    day_of_week: Optional[int] = None
    day_name: Optional[str] = None
    closed: Optional[bool] = None
    opening_time: Optional[RavelryDatetime] = None
    closing_time: Optional[RavelryDatetime] = None


class StashStatus(BaseModel):
    """A named stash status (e.g. stashed, in use, used up)."""

    id: int
    name: Optional[str] = None


class Tool(BaseModel):
    """A knitting or craft tool in a user's tool inventory."""

    id: int
    name: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


class YarnAttributeGroup(BaseModel):
    """A grouping of yarn attributes used in search filtering."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None


class YarnCompany(BaseModel):
    """A yarn brand or manufacturer."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    url: Optional[str] = None
    logo_url: Optional[str] = None
    yarns_count: Optional[int] = None


class YarnWeight(BaseModel):
    """A standard yarn weight category with WPI range."""

    id: int
    name: Optional[str] = None
    short_name: Optional[str] = None
    min: Optional[int] = None
    max: Optional[int] = None


# ---------------------------------------------------------------------------
# Self-referential models (require model_rebuild at module end)
# ---------------------------------------------------------------------------


class AttributeGroup(BaseModel):
    """A hierarchical group of pattern attributes; may contain child groups."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    pattern_attributes: Optional[list[PatternAttribute]] = None
    children: Optional[list[AttributeGroup]] = None


class FiberCategory(BaseModel):
    """A fiber category in a parent–child hierarchy."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    parent: Optional[FiberCategory] = None


class PatternCategory(BaseModel):
    """A pattern category in a parent–child hierarchy."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    parent: Optional[PatternCategory] = None


# ---------------------------------------------------------------------------
# Forum / topic models
# ---------------------------------------------------------------------------


class Forum(BaseModel):
    """A Ravelry discussion forum."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    sort_order: Optional[int] = None
    topics_count: Optional[int] = None


class Topic(BaseModel):
    """A discussion thread within a forum."""

    id: int
    title: Optional[str] = None
    forum_id: Optional[int] = None
    forum_posts_count: Optional[int] = None
    forum_images_count: Optional[int] = None
    created_at: Optional[RavelryDatetime] = None
    replied_at: Optional[RavelryDatetime] = None
    archived: Optional[bool] = None
    locked: Optional[bool] = None
    sticky: Optional[bool] = None
    no_chat: Optional[bool] = None
    ignored: Optional[bool] = None
    watched: Optional[bool] = None
    last_read: Optional[int] = None
    latest_reply: Optional[int] = None


class ForumPost(BaseModel):
    """A single post within a forum topic."""

    id: int
    topic_id: Optional[int] = None
    topic: Optional[Topic] = None
    parent_post_id: Optional[int] = None
    parent_post_number: Optional[int] = None
    post_number: Optional[int] = None
    reply_count: Optional[int] = None
    deleted: Optional[bool] = None
    editable: Optional[bool] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None
    user: Optional[Any] = None


class ForumPreference(BaseModel):
    """A user's preferred forum position setting."""

    position: Optional[int] = None
    forum: Optional[Forum] = None


class ForumSet(BaseModel):
    """A named set of forums (e.g. My Forums) with a selected list."""

    id: Optional[int] = None
    name: Optional[str] = None
    permalink: Optional[str] = None
    default: Optional[bool] = None
    sort_order: Optional[int] = None
    selected_forums: Optional[list[Forum]] = None


# ---------------------------------------------------------------------------
# User hierarchy
# ---------------------------------------------------------------------------


class SocialSite(BaseModel):
    """A social networking site integrated with Ravelry."""

    id: int
    name: str
    active: Optional[bool] = None
    favicon_url: Optional[str] = None


class UserSite(BaseModel):
    """A user's account on an external social site."""

    id: int
    url: Optional[str] = None
    username: Optional[str] = None
    social_site: Optional[SocialSite] = None


class PatternAuthor(BaseModel):
    """A pattern author (designer) profile."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    patterns_count: Optional[int] = None
    knitting_pattern_count: Optional[int] = None
    crochet_pattern_count: Optional[int] = None
    favorites_count: Optional[int] = None
    notes: Optional[str] = None
    notes_html: Optional[str] = None


class User(BaseModel):
    """A Ravelry user profile."""

    id: int
    username: str
    first_name: Optional[str] = None
    about_me: Optional[str] = None
    about_me_html: Optional[str] = None
    photo_url: Optional[str] = None
    large_photo_url: Optional[str] = None
    small_photo_url: Optional[str] = None
    tiny_photo_url: Optional[str] = None
    location: Optional[str] = None
    fave_colors: Optional[str] = None
    fave_curse: Optional[str] = None
    profile_country_code: Optional[str] = None
    pattern_author: Optional[PatternAuthor] = None
    user_sites: Optional[list[UserSite]] = None


# ---------------------------------------------------------------------------
# Shop / store models
# ---------------------------------------------------------------------------


class Shop(BaseModel):
    """A local yarn shop with contact and location details."""

    id: Optional[int] = None
    name: Optional[str] = None
    permalink: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    country: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None
    shop_email: Optional[str] = None
    facebook_page: Optional[str] = None
    twitter_id: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location: Optional[str] = None
    distance: Optional[float] = None
    closed: Optional[bool] = None
    free_wifi: Optional[bool] = None
    seating: Optional[bool] = None
    parking: Optional[str] = None
    wheelchair_access: Optional[bool] = None
    ravelry_retailer: Optional[bool] = None
    pos_online: Optional[bool] = None


class ShopCustomer(BaseModel):
    """A shop's customer record linking a user to a shop."""

    id: Optional[int] = None
    shop: Optional[Shop] = None
    user_id: Optional[str] = None
    user: Optional[User] = None
    name: Optional[str] = None
    email_address: Optional[str] = None
    customer_reference: Optional[str] = None
    created_at: Optional[RavelryDatetime] = None


# ---------------------------------------------------------------------------
# Product / delivery / commerce models
# ---------------------------------------------------------------------------


class Product(BaseModel):
    """A purchasable product in a Ravelry store."""

    id: int
    title: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[str] = None
    pretty_price: Optional[str] = None
    active: Optional[bool] = None
    store_id: Optional[str] = None


class ProductAttachment(BaseModel):
    """A downloadable file attachment for a purchased product."""

    id: int
    product_id: Optional[int] = None
    language_id: Optional[int] = None
    document: Optional[list[Document]] = None


class Delivery(BaseModel):
    """A delivery of purchased products to a buyer."""

    id: int
    created_at: Optional[RavelryDatetime] = None
    emailed_at: Optional[RavelryDatetime] = None
    products: Optional[list[Product]] = None


class CartItem(BaseModel):
    """A single item in a store shopping cart."""

    id: int
    cart_id: Optional[int] = None
    currency: Optional[str] = None
    product: Optional[list[Product]] = None


class Cart(BaseModel):
    """A store shopping cart containing one or more items."""

    id: int
    store_id: Optional[int] = None
    currency: Optional[str] = None
    cart_items: Optional[list[CartItem]] = None


class CombinedCart(BaseModel):
    """An aggregated cart spanning multiple stores for a shop customer."""

    id: int
    shop_customer: Optional[ShopCustomer] = None
    created_by_user_id: Optional[int] = None
    cart_items: Optional[list[CartItem]] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


class InStoreSale(BaseModel):
    """An in-store point-of-sale transaction."""

    id: int
    seller_store_name: Optional[str] = None
    invoice: Optional[Invoice] = None
    deliveries: Optional[list[Delivery]] = None


# ---------------------------------------------------------------------------
# Pattern source / printing
# ---------------------------------------------------------------------------


class PatternSource(BaseModel):
    """A publication or website that is a source for patterns."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    author: Optional[str] = None
    url: Optional[str] = None
    patterns_count: Optional[int] = None
    price: Optional[Decimal] = None
    list_price: Optional[Decimal] = None
    amazon_url: Optional[str] = None
    amazon_rating: Optional[float] = None
    shelf_image_path: Optional[str] = None
    out_of_print: Optional[bool] = None


class Store(BaseModel):
    """A Ravelry digital store operated by a business or designer."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    paypal_account: Optional[str] = None
    products_count: Optional[int] = None
    business: Optional[Business] = None
    pattern_source: Optional[PatternSource] = None


class Printing(BaseModel):
    """Links a pattern to a pattern source with publication metadata."""

    id: int
    pattern_id: Optional[int] = None
    pattern_not_available: Optional[bool] = None
    primary_source: Optional[bool] = None
    created_at: Optional[RavelryDatetime] = None
    pattern_source: Optional[PatternSource] = None


# ---------------------------------------------------------------------------
# Yarn-related models
# ---------------------------------------------------------------------------


class ColorwayPhoto(BaseModel):
    """A photo returned by ``client.colorways.get_photo()``.

    All URL fields are optional — only fields present in the API response will
    be populated.  The most commonly used sizes are ``square_url`` (100×100),
    ``thumbnail_url`` (small square), and ``medium_url`` (full-width).
    """

    id: Optional[int] = None
    sort_order: Optional[int] = None
    user_id: Optional[int] = None
    x_offset: Optional[int] = None
    y_offset: Optional[int] = None
    square_url: Optional[str] = None
    medium_url: Optional[str] = None
    medium2_url: Optional[str] = None
    thumbnail_url: Optional[str] = None
    small_url: Optional[str] = None
    small2_url: Optional[str] = None
    caption: Optional[str] = None
    caption_html: Optional[str] = None
    copyright_holder: Optional[str] = None
    aspect_ratio: Optional[float] = None


class Colorway(BaseModel):
    """A named colour variant of a yarn.

    .. note::
        The ``photos`` field is **never populated** by the yarn detail embed
        (``GET /yarns/{id}.json?include=colorways``).  To fetch a representative
        photo for a colorway use ``client.colorways.get_photo(yarn_id, colorway_id)``
        instead.
    """

    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    yarn_id: Optional[int] = None
    current_status: Optional[str] = None
    projects_count: Optional[int] = None
    stashes_count: Optional[int] = None
    usage_count: Optional[int] = None
    photos: list[ColorwayPhoto] = []


class YarnFiber(BaseModel):
    """A fiber component of a yarn blend with percentage and type."""

    id: int
    percentage: Optional[int] = None
    fiber_category: Optional[FiberCategory] = None
    fiber_type: Optional[FiberType] = None


class YarnCountry(BaseModel):
    """Shop availability statistics for a yarn in a specific country."""

    id: int
    yarn_id: Optional[int] = None
    country_id: Optional[int] = None
    advertising_shops: Optional[int] = None
    shops_with_patrons: Optional[int] = None
    shops_with_patrons_30days: Optional[int] = None
    shops_with_patrons_60days: Optional[int] = None
    shops_with_patrons_90days: Optional[int] = None


class YarnProvenance(BaseModel):
    """Origin provenance record for a yarn (country, phase, description)."""

    id: int
    yarn_id: Optional[int] = None
    yarn_phase_id: Optional[int] = None
    country_id: Optional[int] = None
    country_name: Optional[str] = None
    state_id: Optional[int] = None
    phase_name: Optional[str] = None
    description: Optional[str] = None


class Pack(BaseModel):
    """A yarn pack associated with a stash or project entry."""

    id: int
    yarn_id: Optional[int] = None
    yarn_name: Optional[str] = None
    colorway_name: Optional[str] = None
    color_family_name: Optional[str] = None
    quantity: Optional[Decimal] = None
    ply: Optional[str] = None
    stash_id: Optional[int] = None
    skeins: Optional[float] = None
    primary_pack_id: Optional[int] = None
    total_yards: Optional[float] = None
    total_meters: Optional[float] = None
    total_grams: Optional[float] = None
    total_ounces: Optional[float] = None
    yards_per_skein: Optional[float] = None
    meters_per_skein: Optional[float] = None
    grams_per_skein: Optional[float] = None
    ounces_per_skein: Optional[float] = None
    quantity_description: Optional[str] = None
    shop_name: Optional[str] = None
    shop_id: Optional[int] = None
    dye_lot: Optional[str] = None
    prefer_metric_weight: Optional[bool] = None
    prefer_metric_length: Optional[bool] = None
    total_paid: Optional[float] = None
    total_paid_currency: Optional[str] = None
    color_attributes: Optional[list[Any]] = None
    thread_size: Optional[str] = None
    personal_name: Optional[str] = None


class Yarn(BaseModel):
    """A yarn with weight, fibre, gauge, and availability details."""

    id: int
    name: str
    permalink: Optional[str] = None
    yarn_company_name: Optional[str] = None
    yarn_weight: Optional[YarnWeight] = None
    grams: Optional[int] = None
    yardage: Optional[int] = None
    discontinued: Optional[bool] = None
    certified_organic: Optional[bool] = None
    organic: Optional[bool] = None
    machine_washable: Optional[bool] = None
    gauge_divisor: Optional[int] = None
    min_gauge: Optional[float] = None
    max_gauge: Optional[float] = None
    wpi: Optional[int] = None
    min_needle_size: Optional[float] = None
    max_needle_size: Optional[float] = None
    min_hook_size: Optional[float] = None
    max_hook_size: Optional[float] = None
    thread_size: Optional[str] = None
    texture: Optional[str] = None
    notes_html: Optional[str] = None
    rating_average: Optional[float] = None
    rating_count: Optional[int] = None
    rating_total: Optional[int] = None
    photos: Optional[list[Photo]] = None
    personal_attributes: Optional[Any] = None


# ---------------------------------------------------------------------------
# Draft pattern models
# ---------------------------------------------------------------------------


class ComponentYarn(BaseModel):
    """A yarn component used within a multi-yarn pattern."""

    id: int
    pattern_id: Optional[int] = None
    yarn_id: Optional[int] = None
    combined_yarn_weight_id: Optional[int] = None


class DraftNeedleSize(BaseModel):
    """A needle size requirement on a draft pattern."""

    id: int
    draft_pattern_id: Optional[int] = None
    hook: Optional[bool] = None
    needle_size: Optional[list[NeedleSize]] = None


class DraftPattern(BaseModel):
    """A pattern draft not yet published to the Ravelry library."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None


class DraftPatternSource(BaseModel):
    """Publication source details for a draft pattern."""

    id: int
    draft_pattern_id: Optional[int] = None
    pattern_source_id: Optional[int] = None
    pattern_source_type_id: Optional[int] = None
    publisher_business_id: Optional[int] = None
    name: Optional[str] = None
    isbn: Optional[str] = None
    issue: Optional[str] = None
    url: Optional[str] = None
    source_group_name: Optional[str] = None
    notes: Optional[Any] = None
    primary: Optional[bool] = None
    online: Optional[bool] = None
    print: Optional[bool] = None
    out_of_print: Optional[bool] = None
    ravelry_ebook: Optional[bool] = None
    ravelry_store: Optional[bool] = None
    published: Optional[RavelryDatetime] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None
    pattern_source: Optional[PatternSource] = None


class DraftPatternYarn(BaseModel):
    """A yarn associated with a draft pattern."""

    id: int
    draft_pattern_id: Optional[int] = None
    yarn_id: Optional[int] = None
    yarn_name: Optional[str] = None
    yarn: Optional[Yarn] = None
    yarn_weight: Optional[YarnWeight] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


class DraftComponentYarn(BaseModel):
    """A component yarn on a draft pattern."""

    id: int
    draft_pattern_id: Optional[int] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


class DraftErrataLink(BaseModel):
    """A URL linking to errata or corrections for a draft pattern."""

    id: int
    draft_pattern_id: Optional[int] = None
    url: Optional[str] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


# ---------------------------------------------------------------------------
# Stash / fiber stash models
# ---------------------------------------------------------------------------


class FiberPack(BaseModel):
    """A single fiber pack record in a fiber stash entry."""

    id: int


class FiberStash(BaseModel):
    """A fiber (non-yarn) stash entry owned by a user."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    long_name: Optional[str] = None
    fiber_company_name: Optional[str] = None
    colorway_name: Optional[str] = None
    location: Optional[str] = None
    has_photo: Optional[bool] = None
    first_photo: Optional[Photo] = None
    stash_status: Optional[StashStatus] = None
    user: Optional[User] = None
    user_id: Optional[int] = None
    comments_count: Optional[int] = None
    favorites_count: Optional[int] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


class Stash(BaseModel):
    """A yarn stash entry owned by a user."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    yarn: Optional[Yarn] = None
    colorway_name: Optional[str] = None
    color_family_name: Optional[str] = None
    dye_lot: Optional[str] = None
    location: Optional[str] = None
    handspun: Optional[bool] = None
    has_photo: Optional[bool] = None
    long_yarn_weight_name: Optional[str] = None
    yarn_weight_name: Optional[str] = None
    personal_yarn_weight: Optional[YarnWeight] = None
    notes: Optional[str] = None
    notes_html: Optional[str] = None
    packs: Optional[list[Pack]] = None
    photos: Optional[list[Photo]] = None
    stash_status: Optional[StashStatus] = None
    tag_names: Optional[list[str]] = None
    user: Optional[User] = None
    user_id: Optional[int] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None
    comments_count: Optional[int] = None
    favorites_count: Optional[int] = None

    @property
    def total_skeins(self) -> Optional[float]:
        """Sum of skeins across primary packs (those with primary_pack_id is None).

        Stash.total_skeins from the API is null for thread/cone weight yarns;
        this property is the reliable alternative.  Returns None if no packs
        have skein data.
        """
        if not self.packs:
            return None
        values = [
            p.skeins for p in self.packs
            if p.primary_pack_id is None and p.skeins is not None
        ]
        return sum(values) if values else None


class QueuedStash(BaseModel):
    """Links a stash entry to a queued project."""

    id: int
    queued_project_id: Optional[int] = None
    stash_id: Optional[int] = None
    stash: Optional[Stash] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


class UnifiedStash(BaseModel):
    """A unified stash entry that may be a yarn stash or fiber stash."""

    stash: Optional[Stash] = None
    fiber_stash: Optional[FiberStash] = None


# ---------------------------------------------------------------------------
# Pattern / project models
# ---------------------------------------------------------------------------


class Pattern(BaseModel):
    """A knitting or crochet pattern with gauge, pricing, and rating data."""

    id: int
    name: str
    permalink: Optional[str] = None
    free: Optional[bool] = None
    downloadable: Optional[bool] = None
    pdf: Optional[bool] = None
    pdf_url: Optional[str] = None
    price: Optional[Decimal] = None
    currency: Optional[str] = None
    currency_symbol: Optional[str] = None
    gauge: Optional[float] = None
    gauge_divisor: Optional[int] = None
    row_gauge: Optional[float] = None
    yardage: Optional[int] = None
    yardage_max: Optional[int] = None
    rating_average: Optional[float] = None
    rating_count: Optional[int] = None
    difficulty_average: Optional[float] = None
    difficulty_count: Optional[int] = None
    download_count: Optional[int] = None
    queued_projects_count: Optional[int] = None
    published: Optional[date] = None
    updated_at: Optional[RavelryDatetime] = None
    notes: Optional[str] = None
    notes_html: Optional[str] = None
    type_name: Optional[str] = None
    designer_names: Optional[list[str]] = None
    photos: Optional[list[Photo]] = None
    first_photo: Optional[Photo] = None
    personal_attributes: Optional[Any] = None
    url: Optional[str] = None
    ugh_id: Optional[int] = None


class Project(BaseModel):
    """A user's knitting or crochet project linked to a pattern."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    craft_id: Optional[int] = None
    craft_name: Optional[str] = None
    pattern_id: Optional[int] = None
    pattern_name: Optional[str] = None
    status_name: Optional[str] = None
    project_status_id: Optional[int] = None
    started: Optional[date] = None
    completed: Optional[date] = None
    started_day_set: Optional[bool] = None
    completed_day_set: Optional[bool] = None
    progress: Optional[int] = None
    gauge: Optional[float] = None
    gauge_divisor: Optional[int] = None
    gauge_pattern: Optional[str] = None
    gauge_repeats: Optional[int] = None
    row_gauge: Optional[float] = None
    ends_per_inch: Optional[float] = None
    picks_per_inch: Optional[float] = None
    size: Optional[str] = None
    made_for: Optional[str] = None
    made_for_user_id: Optional[int] = None
    notes: Optional[str] = None
    notes_html: Optional[str] = None
    rating: Optional[int] = None
    packs: Optional[list[Pack]] = None
    photos: Optional[list[Photo]] = None
    tools: Optional[list[Any]] = None
    needle_sizes: Optional[list[NeedleSize]] = None
    tag_names: Optional[list[str]] = None
    user: Optional[User] = None
    user_id: Optional[int] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None
    comments_count: Optional[int] = None
    favorites_count: Optional[int] = None
    photos_count: Optional[int] = None
    personal_attributes: Optional[Any] = None


# ---------------------------------------------------------------------------
# Volume / attachment models
# ---------------------------------------------------------------------------


class VolumeAttachment(BaseModel):
    """A downloadable file attachment for a library volume."""

    product_attachment_id: Optional[int] = None
    filename: Optional[str] = None
    bytes: Optional[int] = None
    content_type: Optional[str] = None
    language_code: Optional[str] = None
    notes: Optional[str] = None
    ravelry_download_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class Volume(BaseModel):
    """A library volume (purchased or gifted pattern collection)."""

    id: int
    title: Optional[str] = None
    pattern_id: Optional[int] = None
    pattern_source_id: Optional[int] = None
    patterns_count: Optional[int] = None
    author_name: Optional[str] = None
    notes: Optional[str] = None
    notes_html: Optional[Any] = None
    cover_image_url: Optional[str] = None
    small_image_url: Optional[str] = None
    square_image_url: Optional[str] = None
    cover_image_size: Optional[Any] = None
    first_photo: Optional[Any] = None
    for_sale: Optional[bool] = None
    for_trade: Optional[bool] = None
    has_downloads: Optional[bool] = None
    asking_price_cents: Optional[int] = None
    asking_price_currency: Optional[str] = None
    volume_status_id: Optional[int] = None
    unapplied_updates: Optional[list[ProductNotification]] = None
    volume_attachments: Optional[list[VolumeAttachment]] = None
    created_at: Optional[RavelryDatetime] = None
    updated_at: Optional[RavelryDatetime] = None


# ---------------------------------------------------------------------------
# Bundle / bookmark / collection / group
# ---------------------------------------------------------------------------


class Bundle(BaseModel):
    """A curated collection of patterns, yarns, or projects."""

    id: int
    name: Optional[str] = None
    notes: Optional[str] = None
    bundle_cover: Optional[Photo] = None
    first_photo: Optional[Photo] = None
    bundled_items_count: Optional[int] = None
    user: Optional[User] = None


class BundledItem(BaseModel):
    """A single item within a bundle."""

    id: int
    bundle_id: Optional[int] = None
    item_id: Optional[int] = None
    item_type: Optional[str] = None
    user: Optional[User] = None


class Bookmark(BaseModel):
    """A favourite bookmark linking a user to a pattern, yarn, or project."""

    id: int
    type: Optional[str] = None
    tag_list: Optional[str] = None
    comment: Optional[str] = None
    favorited: Optional[Any] = None
    created_at: Optional[RavelryDatetime] = None


class Collection(BaseModel):
    """A named collection of tagged items."""

    id: int
    title: Optional[str] = None
    permalink: Optional[str] = None
    tag_names: Optional[list[str]] = None


class Group(BaseModel):
    """A Ravelry community group with an associated forum."""

    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    short_description: Optional[str] = None
    badge_url: Optional[str] = None
    banner_url: Optional[str] = None
    forum_id: Optional[int] = None
    forum: Optional[Forum] = None
    mature: Optional[bool] = None
    created_at: Optional[RavelryDatetime] = None


# ---------------------------------------------------------------------------
# Comment / activity / social models
# ---------------------------------------------------------------------------


class Comment(BaseModel):
    """A comment left on a project, stash, or forum post."""

    id: int
    comment_html: Optional[str] = None
    created_at: Optional[RavelryDatetime] = None
    user: Optional[User] = None
    highlighted_project: Optional[Project] = None


class Activity(BaseModel):
    """A social activity event from a user's friend feed."""

    id: int
    activity_type_id: Optional[int] = None
    activity_type_key: Optional[str] = None
    created_at: Optional[RavelryDatetime] = None
    title: Optional[str] = None
    descriptive_title: Optional[str] = None
    target_id: Optional[int] = None
    target_uri: Optional[str] = None
    photo: Optional[Photo] = None
    user: Optional[User] = None


class Message(BaseModel):
    """A private message between two Ravelry users."""

    id: int
    subject: Optional[str] = None
    content_html: Optional[str] = None
    folder_name: Optional[str] = None
    message_type_name: Optional[str] = None
    parent_message_id: Optional[int] = None
    read_message: Optional[bool] = None
    replied: Optional[bool] = None
    replied_at: Optional[RavelryDatetime] = None
    sent_at: Optional[RavelryDatetime] = None
    sender: Optional[User] = None
    recipient: Optional[User] = None


class Friendship(BaseModel):
    """A friendship link between two Ravelry users."""

    id: int
    friend_id: Optional[int] = None
    friend_user_id: Optional[int] = None
    friend_username: Optional[str] = None
    friend_avatar: Optional[dict[str, Any]] = None
    created_at: Optional[RavelryDatetime] = None
    tag_names: Optional[list[str]] = None
    friend_user: Optional[User] = None


# ---------------------------------------------------------------------------
# Rebuild self-referential models after all classes are defined
# ---------------------------------------------------------------------------

AttributeGroup.model_rebuild()
FiberCategory.model_rebuild()
PatternCategory.model_rebuild()

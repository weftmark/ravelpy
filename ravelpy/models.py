from __future__ import annotations

from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Leaf / primitive models (no nested model dependencies)
# ---------------------------------------------------------------------------


class Ad(BaseModel):
    logo_url: Optional[str] = None
    target_url: Optional[str] = None


class Business(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    primary_url: Optional[str] = None


class ColorFamily(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    color: Optional[str] = None
    spectrum_order: Optional[int] = None


class Craft(BaseModel):
    id: int
    name: str
    permalink: Optional[str] = None


class Document(BaseModel):
    id: int
    filename: Optional[str] = None
    bytes: Optional[int] = None
    content_type: Optional[str] = None
    notes: Optional[str] = None
    thumbnail_url: Optional[str] = None


class DownloadLink(BaseModel):
    url: Optional[str] = None
    activated_at: Optional[datetime] = None
    expires_at: Optional[datetime] = None


class FiberAttributeGroup(BaseModel):
    id: int
    name: str
    permalink: Optional[str] = None
    parent_id: Optional[int] = None


class FiberAttribute(BaseModel):
    id: int
    name: str
    permalink: Optional[str] = None
    fiber_attribute_group_id: Optional[int] = None


class FiberType(BaseModel):
    id: int
    name: Optional[str] = None
    animal_fiber: Optional[bool] = None
    synthetic: Optional[bool] = None
    vegetable_fiber: Optional[bool] = None


class ForumStatisticSummary(BaseModel):
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
    id: int
    invoice_number: Optional[int] = None
    paid: Optional[bool] = None
    payment_reference: Optional[str] = None


class InvoiceLineItem(BaseModel):
    id: int
    invoice_id: Optional[int] = None
    product_id: Optional[int] = None
    promotion_id: Optional[int] = None
    amount: Optional[Decimal] = None
    promotional_discount_applied: Optional[Decimal] = None
    title: Optional[str] = None


class Language(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    permalink: Optional[str] = None
    short_name: Optional[str] = None
    universal: Optional[bool] = None


class NeedleRecord(BaseModel):
    id: int
    needle_type_id: Optional[int] = None
    comment: Optional[str] = None


class NeedleSize(BaseModel):
    id: int
    name: Optional[str] = None
    metric: Optional[float] = None
    hook: Optional[str] = None
    us: Optional[str] = None
    us_size: Optional[str] = None
    uk_size: Optional[str] = None
    pretty_metric: Optional[str] = None


class NeedleType(BaseModel):
    id: int
    name: Optional[str] = None
    type_name: Optional[str] = None
    description: Optional[str] = None
    length: Optional[float] = None
    metric_name: Optional[str] = None
    needle_size_id: Optional[int] = None


class Page(BaseModel):
    name: Optional[str] = None
    body: Optional[str] = None


class PatternAttribute(BaseModel):
    id: int
    permalink: Optional[str] = None


class PatternClassification(BaseModel):
    id: int
    pattern_id: Optional[int] = None
    pattern_category_id: Optional[int] = None


class PatternLanguage(BaseModel):
    id: int
    pattern_id: Optional[int] = None
    language_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class PatternNeedleSize(BaseModel):
    id: Optional[int] = None
    needle_size_id: Optional[int] = None
    hook: Optional[bool] = None
    metric: Optional[float] = None
    needle_name: Optional[str] = None
    pretty_metric: Optional[str] = None
    pretty_us: Optional[str] = None
    us: Optional[str] = None


class PatternSourceType(BaseModel):
    id: int
    name: Optional[str] = None
    long_name: Optional[str] = None
    can_add_to_library: Optional[bool] = None
    requires_url: Optional[bool] = None


class PatternTagging(BaseModel):
    id: int
    pattern_id: Optional[int] = None
    pattern_attribute_id: Optional[int] = None


class Payment(BaseModel):
    id: int
    gross: Optional[Decimal] = None
    txn_id: Optional[int] = None
    txn_type: Optional[str] = None


class Photo(BaseModel):
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
    id: int
    product_id: Optional[int] = None
    created_at: Optional[datetime] = None
    message: Optional[str] = None
    message_html: Optional[str] = None
    version: Optional[str] = None


class ProjectStatus(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None


class QueuedProject(BaseModel):
    id: int
    short_pattern_name: Optional[str] = None
    position_in_queue: Optional[int] = None


class Saleable(BaseModel):
    id: int
    product_id: Optional[int] = None
    saleable_id: Optional[int] = None
    saleable_type: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class SavedSearch(BaseModel):
    id: int
    title: Optional[str] = None
    search_type: Optional[str] = None
    search_path: Optional[str] = None
    search_parameters: Optional[Any] = None
    subscribed: Optional[bool] = None
    subscription_updated_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    last_loaded: Optional[datetime] = None


class ShopSchedule(BaseModel):
    day_of_week: Optional[int] = None
    day_name: Optional[str] = None
    closed: Optional[bool] = None
    opening_time: Optional[datetime] = None
    closing_time: Optional[datetime] = None


class StashStatus(BaseModel):
    id: int
    name: Optional[str] = None


class Tool(BaseModel):
    id: int
    name: Optional[str] = None
    make: Optional[str] = None
    model: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class YarnAttributeGroup(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None


class YarnCompany(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    url: Optional[str] = None
    logo_url: Optional[str] = None
    yarns_count: Optional[int] = None


class YarnWeight(BaseModel):
    id: int
    name: Optional[str] = None
    short_name: Optional[str] = None
    min: Optional[int] = None
    max: Optional[int] = None


# ---------------------------------------------------------------------------
# Self-referential models (require model_rebuild at module end)
# ---------------------------------------------------------------------------


class AttributeGroup(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    pattern_attributes: Optional[list[PatternAttribute]] = None
    children: Optional[list[AttributeGroup]] = None


class FiberCategory(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    parent: Optional[FiberCategory] = None


class PatternCategory(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    parent: Optional[PatternCategory] = None


# ---------------------------------------------------------------------------
# Forum / topic models
# ---------------------------------------------------------------------------


class Forum(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    sort_order: Optional[int] = None
    topics_count: Optional[int] = None


class Topic(BaseModel):
    id: int
    title: Optional[str] = None
    forum_id: Optional[int] = None
    forum_posts_count: Optional[int] = None
    forum_images_count: Optional[int] = None
    created_at: Optional[datetime] = None
    replied_at: Optional[datetime] = None
    archived: Optional[bool] = None
    locked: Optional[bool] = None
    sticky: Optional[bool] = None
    no_chat: Optional[bool] = None
    ignored: Optional[bool] = None
    watched: Optional[bool] = None
    last_read: Optional[int] = None
    latest_reply: Optional[int] = None


class ForumPost(BaseModel):
    id: int
    topic_id: Optional[int] = None
    topic: Optional[Topic] = None
    parent_post_id: Optional[int] = None
    parent_post_number: Optional[int] = None
    post_number: Optional[int] = None
    reply_count: Optional[int] = None
    deleted: Optional[bool] = None
    editable: Optional[bool] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    user: Optional[Any] = None


class ForumPreference(BaseModel):
    position: Optional[int] = None
    forum: Optional[Forum] = None


class ForumSet(BaseModel):
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
    id: int
    name: str
    active: Optional[bool] = None
    favicon_url: Optional[str] = None


class UserSite(BaseModel):
    id: int
    url: Optional[str] = None
    username: Optional[str] = None
    social_site: Optional[SocialSite] = None


class PatternAuthor(BaseModel):
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
    id: Optional[int] = None
    shop: Optional[Shop] = None
    user_id: Optional[str] = None
    user: Optional[User] = None
    name: Optional[str] = None
    email_address: Optional[str] = None
    customer_reference: Optional[str] = None
    created_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Product / delivery / commerce models
# ---------------------------------------------------------------------------


class Product(BaseModel):
    id: int
    title: Optional[str] = None
    sku: Optional[str] = None
    price: Optional[str] = None
    pretty_price: Optional[str] = None
    active: Optional[bool] = None
    store_id: Optional[str] = None


class ProductAttachment(BaseModel):
    id: int
    product_id: Optional[int] = None
    language_id: Optional[int] = None
    document: Optional[list[Document]] = None


class Delivery(BaseModel):
    id: int
    created_at: Optional[datetime] = None
    emailed_at: Optional[datetime] = None
    products: Optional[list[Product]] = None


class CartItem(BaseModel):
    id: int
    cart_id: Optional[int] = None
    currency: Optional[str] = None
    product: Optional[list[Product]] = None


class Cart(BaseModel):
    id: int
    store_id: Optional[int] = None
    currency: Optional[str] = None
    cart_items: Optional[list[CartItem]] = None


class CombinedCart(BaseModel):
    id: int
    shop_customer: Optional[ShopCustomer] = None
    created_by_user_id: Optional[int] = None
    cart_items: Optional[list[CartItem]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class InStoreSale(BaseModel):
    id: int
    seller_store_name: Optional[str] = None
    invoice: Optional[Invoice] = None
    deliveries: Optional[list[Delivery]] = None


# ---------------------------------------------------------------------------
# Pattern source / printing
# ---------------------------------------------------------------------------


class PatternSource(BaseModel):
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
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    paypal_account: Optional[str] = None
    products_count: Optional[int] = None
    business: Optional[Business] = None
    pattern_source: Optional[PatternSource] = None


class Printing(BaseModel):
    id: int
    pattern_id: Optional[int] = None
    pattern_not_available: Optional[bool] = None
    primary_source: Optional[bool] = None
    created_at: Optional[datetime] = None
    pattern_source: Optional[PatternSource] = None


# ---------------------------------------------------------------------------
# Yarn-related models
# ---------------------------------------------------------------------------


class Colorway(BaseModel):
    id: int
    name: Optional[str] = None
    code: Optional[str] = None
    yarn_id: Optional[int] = None
    projects_count: Optional[int] = None
    stashes_count: Optional[int] = None
    usage_count: Optional[int] = None
    photo_url: Optional[str] = None


class YarnFiber(BaseModel):
    id: int
    percentage: Optional[int] = None
    fiber_category: Optional[FiberCategory] = None
    fiber_type: Optional[FiberType] = None


class YarnCountry(BaseModel):
    id: int
    yarn_id: Optional[int] = None
    country_id: Optional[int] = None
    advertising_shops: Optional[int] = None
    shops_with_patrons: Optional[int] = None
    shops_with_patrons_30days: Optional[int] = None
    shops_with_patrons_60days: Optional[int] = None
    shops_with_patrons_90days: Optional[int] = None


class YarnProvenance(BaseModel):
    id: int
    yarn_id: Optional[int] = None
    yarn_phase_id: Optional[int] = None
    country_id: Optional[int] = None
    country_name: Optional[str] = None
    state_id: Optional[int] = None
    phase_name: Optional[str] = None
    description: Optional[str] = None


class Pack(BaseModel):
    id: int
    yarn_id: Optional[int] = None
    yarn_name: Optional[str] = None
    colorway_name: Optional[str] = None
    color_family_name: Optional[str] = None
    quantity: Optional[Decimal] = None
    ply: Optional[str] = None
    stash_id: Optional[int] = None


class Yarn(BaseModel):
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
    id: int
    pattern_id: Optional[int] = None
    yarn_id: Optional[int] = None
    combined_yarn_weight_id: Optional[int] = None


class DraftNeedleSize(BaseModel):
    id: int
    draft_pattern_id: Optional[int] = None
    hook: Optional[bool] = None
    needle_size: Optional[list[NeedleSize]] = None


class DraftPattern(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None


class DraftPatternSource(BaseModel):
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
    published: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    pattern_source: Optional[PatternSource] = None


class DraftPatternYarn(BaseModel):
    id: int
    draft_pattern_id: Optional[int] = None
    yarn_id: Optional[int] = None
    yarn_name: Optional[str] = None
    yarn: Optional[Yarn] = None
    yarn_weight: Optional[YarnWeight] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DraftComponentYarn(BaseModel):
    id: int
    draft_pattern_id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DraftErrataLink(BaseModel):
    id: int
    draft_pattern_id: Optional[int] = None
    url: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Stash / fiber stash models
# ---------------------------------------------------------------------------


class FiberPack(BaseModel):
    id: int


class FiberStash(BaseModel):
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class Stash(BaseModel):
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    comments_count: Optional[int] = None
    favorites_count: Optional[int] = None


class QueuedStash(BaseModel):
    id: int
    queued_project_id: Optional[int] = None
    stash_id: Optional[int] = None
    stash: Optional[Stash] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UnifiedStash(BaseModel):
    stash: Optional[Stash] = None
    fiber_stash: Optional[FiberStash] = None


# ---------------------------------------------------------------------------
# Pattern / project models
# ---------------------------------------------------------------------------


class Pattern(BaseModel):
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
    updated_at: Optional[datetime] = None
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    comments_count: Optional[int] = None
    favorites_count: Optional[int] = None
    photos_count: Optional[int] = None
    personal_attributes: Optional[Any] = None


# ---------------------------------------------------------------------------
# Volume / attachment models
# ---------------------------------------------------------------------------


class VolumeAttachment(BaseModel):
    product_attachment_id: Optional[int] = None
    filename: Optional[str] = None
    bytes: Optional[int] = None
    content_type: Optional[str] = None
    language_code: Optional[str] = None
    notes: Optional[str] = None
    ravelry_download_url: Optional[str] = None
    thumbnail_url: Optional[str] = None


class Volume(BaseModel):
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
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Bundle / bookmark / collection / group
# ---------------------------------------------------------------------------


class Bundle(BaseModel):
    id: int
    name: Optional[str] = None
    notes: Optional[str] = None
    bundle_cover: Optional[Photo] = None
    first_photo: Optional[Photo] = None
    bundled_items_count: Optional[int] = None
    user: Optional[User] = None


class BundledItem(BaseModel):
    id: int
    bundle_id: Optional[int] = None
    item_id: Optional[int] = None
    item_type: Optional[str] = None
    user: Optional[User] = None


class Bookmark(BaseModel):
    id: int
    type: Optional[str] = None
    tag_list: Optional[str] = None
    comment: Optional[str] = None
    favorited: Optional[Any] = None
    created_at: Optional[datetime] = None


class Collection(BaseModel):
    id: int
    title: Optional[str] = None
    permalink: Optional[str] = None
    tag_names: Optional[list[str]] = None


class Group(BaseModel):
    id: int
    name: Optional[str] = None
    permalink: Optional[str] = None
    short_description: Optional[str] = None
    badge_url: Optional[str] = None
    banner_url: Optional[str] = None
    forum_id: Optional[int] = None
    forum: Optional[Forum] = None
    mature: Optional[bool] = None
    created_at: Optional[datetime] = None


# ---------------------------------------------------------------------------
# Comment / activity / social models
# ---------------------------------------------------------------------------


class Comment(BaseModel):
    id: int
    comment_html: Optional[str] = None
    created_at: Optional[datetime] = None
    user: Optional[User] = None
    highlighted_project: Optional[Project] = None


class Activity(BaseModel):
    id: int
    activity_type_id: Optional[int] = None
    activity_type_key: Optional[str] = None
    created_at: Optional[datetime] = None
    title: Optional[str] = None
    descriptive_title: Optional[str] = None
    target_id: Optional[int] = None
    target_uri: Optional[str] = None
    photo: Optional[Photo] = None
    user: Optional[User] = None


class Message(BaseModel):
    id: int
    subject: Optional[str] = None
    content_html: Optional[str] = None
    folder_name: Optional[str] = None
    message_type_name: Optional[str] = None
    parent_message_id: Optional[int] = None
    read_message: Optional[bool] = None
    replied: Optional[bool] = None
    replied_at: Optional[datetime] = None
    sent_at: Optional[datetime] = None
    sender: Optional[User] = None
    recipient: Optional[User] = None


class Friendship(BaseModel):
    id: int
    friend_id: Optional[int] = None
    friend_user_id: Optional[int] = None
    friend_username: Optional[str] = None
    friend_avatar: Optional[dict[str, Any]] = None
    created_at: Optional[datetime] = None
    tag_names: Optional[list[str]] = None
    friend_user: Optional[User] = None


# ---------------------------------------------------------------------------
# Rebuild self-referential models after all classes are defined
# ---------------------------------------------------------------------------

AttributeGroup.model_rebuild()
FiberCategory.model_rebuild()
PatternCategory.model_rebuild()

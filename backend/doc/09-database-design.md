# Database Design

## Purpose

The Order Automation Chatbot uses PostgreSQL as its primary relational database.

The schema is designed around **business aggregates** rather than individual tables. Each aggregate represents a distinct business capability and owns its related entities.

The database follows a normalized design while maintaining clear ownership relationships between entities.

---

# Design Principles

The database is designed around the following principles.

## Aggregate-Oriented Design

Related entities are grouped into aggregates.

Examples include:

- Product Catalog
- Customer
- Conversation
- Order Draft
- Order

Each aggregate has a single root entity.

---

## Referential Integrity

Relationships are enforced using foreign key constraints.

This guarantees that:

- Orders always belong to a customer.
- Draft Items always belong to a Draft.
- Order Items always belong to an Order.
- Inventory always belongs to a Product Variant.

---

## UUID Primary Keys

Every aggregate uses UUID primary keys.

Benefits include:

- Globally unique identifiers
- Distributed system compatibility
- No sequential ID exposure
- Easier data synchronization

---

## Immutable Business Records

Certain entities become immutable after creation.

Examples:

- Orders
- Order Items
- Payments
- Shipment History
- Order Status History

Mutable business data belongs only to the Order Draft.

---

# Aggregate Overview

The database consists of five primary aggregates.

```text
Product Catalog

Customer

Conversation

Order Draft

Order
```

Each aggregate owns its child entities.

---

# Product Catalog Aggregate

```text
Category

│

└────────► Product

               │

               ▼

        Product Variant

               │

               ▼

           Inventory
```

## Purpose

Represents all sellable products.

### Category

Groups products.

Example

```
Shoes

Electronics

Clothing
```

---

### Product

Represents the master product.

Examples

```
Nike Air Max

iPhone 16

Samsung Galaxy S25
```

Products contain no inventory information.

---

### Product Variant

Represents a sellable SKU.

Examples

```
Black

Size 9

₹4999
```

Every purchasable item is a Product Variant.

---

### Inventory

Tracks stock for each variant.

Stores:

- Available Stock
- Reserved Stock
- Reorder Level

Inventory belongs exclusively to Product Variants.

---

# Customer Aggregate

```text
Customer

│

└────────► Customer Address
```

## Purpose

Stores customer profile information.

### Customer

Contains:

- Name
- Email
- Phone

---

### Customer Address

Stores delivery addresses.

Supports:

- Multiple addresses
- Default address
- Address reuse

---

# Conversation Aggregate

```text
Conversation Session

│

├────────► Conversation Message

│

└────────► Order Draft
```

## Purpose

Manages conversational interactions.

### Conversation Session

Represents an active customer conversation.

Stores:

- Current workflow state
- Session status
- Activity timestamps

---

### Conversation Message

Stores every exchanged message.

Supported roles:

- USER
- ASSISTANT
- SYSTEM

Messages provide a complete conversation history.

---

# Order Draft Aggregate

```text
Order Draft

│

├────────► Draft Items

│

└────────► Customer Address
```

## Purpose

Represents the customer's temporary shopping cart.

The Order Draft owns:

- Draft Items
- Pricing
- Workflow State
- Delivery Address

It remains mutable throughout checkout.

---

### Draft Items

Stores selected products.

Each Draft Item references:

- Product Variant
- Quantity
- Unit Price
- Subtotal

Suggested constraint

```
UNIQUE(draft_id, variant_id)
```

prevents duplicate variants.

---

### Draft Status

```text
ACTIVE

↓

COMPLETED

↓

ABANDONED

↓

EXPIRED
```

Only ACTIVE drafts participate in conversations.

---

# Order Aggregate

```text
Order

│

├────────► Order Items

├────────► Payment

├────────► Shipment

└────────► Order Status History
```

## Purpose

Represents a completed purchase.

Unlike Drafts,

Orders are immutable.

---

### Order

Stores:

- Customer
- Delivery Address
- Totals
- Draft Reference
- Current Status

---

### Order Items

Copied from Draft Items during checkout.

After creation,

Order Items never change.

---

### Payment

Represents payment information.

Current implementation:

```
Cash On Delivery
```

Future implementations:

- UPI
- Credit Card
- Stripe
- Razorpay

---

### Shipment

Represents fulfillment.

Typical lifecycle

```text
PENDING

↓

PACKED

↓

SHIPPED

↓

DELIVERED
```

---

### Order Status History

Stores every order state transition.

Example

```text
PLACED

↓

CONFIRMED

↓

PACKED

↓

SHIPPED

↓

DELIVERED
```

Status history is append-only.

---

# Workflow Persistence

The workflow engine persists only the current execution state.

```text
Order Draft

↓

Workflow State

↓

Workflow Mode
```

This allows the workflow to resume after every customer message.

---

# Entity Relationships

```text
Category
    │
    ▼
Product
    │
    ▼
Product Variant
    │
    ▼
Inventory

Customer
    │
    ▼
Customer Address

Conversation Session
    │
    ├────────► Conversation Messages
    │
    └────────► Order Draft
                    │
                    ▼
              Draft Items
                    │
                    ▼
                 Order
                    │
        ┌───────────┼────────────┐
        ▼           ▼            ▼
  Order Items    Payment     Shipment
        │
        ▼
Order Status History
```

---

# Cascade Strategy

The system intentionally mixes **CASCADE** and **RESTRICT** relationships.

## RESTRICT

Used when deleting a parent would destroy business integrity.

Examples

```
Category → Product

Product → Variant
```

Products should not disappear simply because a category is deleted.

---

## CASCADE

Used for owned child entities.

Examples

```
Conversation Session

↓

Conversation Messages
```

Deleting a conversation removes its messages.

Likewise,

```
Order Draft

↓

Draft Items
```

Deleting a draft removes its items.

---

# Indexing Strategy

Indexes are added to frequently queried columns.

Examples

```
Customer.email

Customer.phone

Product.name

Product.category_id

Product.brand

Conversation.session_id

Order.order_number

ProductVariant.sku
```

Unique indexes enforce business uniqueness where required.

---

# Normalization

The schema follows approximately Third Normal Form (3NF).

Examples

- Product information exists only once.
- Inventory is separated from Product.
- Draft Items and Order Items are distinct entities.
- Customer Addresses are reusable.
- Payments are independent from Orders.

This minimizes redundancy while maintaining business clarity.

---

# Database Philosophy

The database separates **temporary business state** from **permanent business records**.

```text
Conversation

↓

Order Draft

↓

Order
```

Temporary state remains editable.

Permanent state remains immutable.

This distinction is fundamental to the system architecture.

---

# Summary

The database design is centered around business aggregates rather than individual tables.

By separating Catalog, Customer, Conversation, Draft, and Order into independent aggregates with clearly defined ownership and lifecycle rules, the schema supports conversational commerce while maintaining transactional consistency, extensibility, and strong referential integrity.
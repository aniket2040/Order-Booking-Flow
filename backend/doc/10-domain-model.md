# Domain Model

## Purpose

The Order Automation Chatbot is designed using Domain-Driven Design (DDD) principles.

Instead of modeling the application around database tables or API endpoints, the system is modeled around **business concepts** called **Aggregates**.

Each aggregate owns a specific business capability and protects its own consistency rules.

This document explains the domain model, aggregate boundaries, ownership rules, and invariants that govern the system.

---

# What is a Domain Model?

A domain model represents the real-world business concepts of the application.

For this project, the primary business concepts are:

```text
Catalog

Customer

Conversation

Order Draft

Order
```

Each concept exists independently and owns its own lifecycle.

---

# Aggregate Overview

The system consists of five primary aggregates.

```text
Catalog

Customer

Conversation

Order Draft

Order
```

Each aggregate has exactly one Aggregate Root.

Only Aggregate Roots may be referenced directly by other aggregates.

---

# Aggregate Relationships

```text
                 Catalog
                    │
                    ▼
             Product Variant
                    │
                    ▼
Customer ─────► Conversation
                    │
                    ▼
              Order Draft
                    │
                    ▼
                  Order
```

Each aggregate owns its child entities.

No child entity may exist independently.

---

# Catalog Aggregate

## Aggregate Root

```
Product
```

### Child Entities

```
Category

Product Variant

Inventory
```

---

## Responsibilities

The Catalog Aggregate owns:

- Product information
- Product variants
- Pricing
- Inventory

It is responsible for answering questions such as:

- Does this product exist?
- Which variants are available?
- What is the SKU?
- What is the current inventory?

---

## Invariants

The Catalog Aggregate guarantees:

- Every SKU is unique.
- Every Variant belongs to exactly one Product.
- Inventory belongs to exactly one Variant.
- Products cannot exist without a Category.

---

# Customer Aggregate

## Aggregate Root

```
Customer
```

### Child Entity

```
Customer Address
```

---

## Responsibilities

The Customer Aggregate owns:

- Customer profile
- Contact information
- Saved addresses

---

## Invariants

- Email must be unique.
- Phone number must be unique.
- Every address belongs to exactly one customer.
- A customer may have only one default address.

---

# Conversation Aggregate

## Aggregate Root

```
Conversation Session
```

### Child Entities

```
Conversation Message

Order Draft
```

---

## Responsibilities

The Conversation Aggregate owns:

- Chat history
- Current conversation
- Workflow progression

It does not own business transactions.

---

## Invariants

- Only one ACTIVE conversation session exists per customer.
- Every message belongs to one conversation.
- Workflow always resumes from the current draft.

---

# Order Draft Aggregate

## Aggregate Root

```
Order Draft
```

### Child Entity

```
Draft Item
```

---

## Responsibilities

The Order Draft owns all temporary business state.

Examples:

- Product selections
- Variants
- Quantities
- Delivery address
- Pricing
- Workflow progress

The Draft behaves as the conversational shopping cart.

---

## Why Draft is an Aggregate Root

Every modification occurs through the Draft.

Examples

```
Add Item

Remove Item

Change Quantity

Update Address

Recalculate Pricing
```

The Draft controls all business rules for these operations.

No service should modify Draft Items directly.

---

## Invariants

The Draft guarantees:

- Draft Items always belong to one Draft.
- Quantity is always greater than zero.
- Pricing reflects the latest calculation.
- Workflow state always matches conversation progress.
- Only ACTIVE drafts may be modified.

---

# Order Aggregate

## Aggregate Root

```
Order
```

### Child Entities

```
Order Item

Payment

Shipment

Order Status History
```

---

## Responsibilities

The Order Aggregate represents the permanent business transaction.

Unlike the Draft,

Orders are immutable.

---

## Why Order is an Aggregate Root

Everything after checkout belongs to the Order.

Examples

```
Shipment

Payment

Status History
```

These entities have no meaning without an Order.

---

## Invariants

The Order guarantees:

- Order Number is unique.
- Every Order Item belongs to exactly one Order.
- Every Payment belongs to one Order.
- Every Shipment belongs to one Order.
- Status history is append-only.

---

# Aggregate Independence

Aggregates communicate only through Aggregate Roots.

Example

Correct

```
Order

↓

Customer
```

Incorrect

```
Order Item

↓

Customer Address
```

Child entities never reference other aggregates directly.

---

# Aggregate Lifecycle

```text
Conversation

↓

Order Draft

↓

Order
```

Notice that

Conversation does not become an Order.

The Draft becomes an Order.

---

# Business Ownership

The ownership model is intentionally strict.

```text
Conversation

owns

Conversation Messages

Conversation State

────────────

Draft

owns

Draft Items

Workflow State

Pricing

────────────

Order

owns

Order Items

Payment

Shipment

Status History
```

Ownership determines transaction boundaries.

---

# Aggregate Modification Rules

Only Aggregate Roots may be modified directly.

Example

Correct

```
Draft

↓

add_item()

↓

Draft Item
```

Incorrect

```
Draft Item

↓

update_quantity()
```

All modifications flow through the Aggregate Root.

---

# Transaction Boundaries

Each Aggregate maintains its own consistency.

Examples

```
Draft Transaction

↓

Update Draft

↓

Update Pricing

↓

Commit
```

Checkout becomes a higher-level transaction that coordinates multiple aggregates.

---

# Domain Services

Certain business operations span multiple aggregates.

These operations belong to Domain Services.

Examples

```
Pricing Service

Inventory Service

Order Orchestrator

Notification Service
```

These services coordinate aggregates without violating aggregate boundaries.

---

# Ubiquitous Language

The project uses consistent business terminology.

| Business Term | Meaning |
|--------------|---------|
| Conversation | Customer interaction |
| Session | Active conversation |
| Draft | Temporary order |
| Draft Item | Temporary product selection |
| Order | Finalized purchase |
| Order Item | Purchased product |
| Variant | Sellable SKU |
| Inventory | Available stock |
| Shipment | Delivery information |

Maintaining consistent terminology reduces ambiguity across the codebase.

---

# Why Domain-Driven Design?

Domain-Driven Design provides several advantages.

## Clear Ownership

Every entity has exactly one owner.

---

## Strong Consistency

Each aggregate protects its own invariants.

---

## Better Maintainability

Business rules remain localized.

---

## Easier Testing

Each aggregate can be tested independently.

---

## Scalability

Future features such as:

- Coupons
- Loyalty Points
- Returns
- Refunds
- Multi-Vendor Orders

can be introduced without restructuring existing aggregates.

---

# Summary

The domain model organizes the Order Automation Chatbot around business capabilities rather than database tables.

By defining clear aggregate boundaries, ownership rules, invariants, and transaction responsibilities, the architecture ensures that conversational workflows, shopping drafts, and finalized orders remain consistent, maintainable, and extensible as the platform evolves.
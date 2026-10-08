# Order Lifecycle

## Purpose

The order lifecycle defines how a customer order evolves from a temporary shopping draft into a completed business transaction.

Rather than creating an order immediately, the system follows a **Draft-First Architecture**.

Customers progressively build an **Order Draft**, review its contents, and explicitly confirm the purchase before a permanent **Order** is created.

This separation ensures that incomplete or abandoned shopping sessions never become business transactions.

---

# High-Level Lifecycle

```text
Conversation

↓

Conversation Session

↓

Order Draft

↓

Draft Items

↓

Customer Review

↓

Customer Confirmation

↓

Order Orchestrator

↓

Order

├── Order Items
├── Payment
├── Shipment
└── Order Status History
```

Only after customer confirmation does the system create a permanent order.

---

# Why Draft-First?

Traditional e-commerce systems often treat the shopping cart as a temporary UI component.

In this architecture, the Order Draft is a first-class domain entity.

Benefits include:

- Supports conversational ordering
- Supports partial conversations
- Supports order modification
- Supports AI-assisted shopping
- Prevents accidental order creation
- Enables resumable conversations

---

# Order Draft

The Order Draft represents a customer's work-in-progress order.

The draft stores all temporary information collected during the conversation.

Typical information includes:

- Customer
- Selected products
- Product variants
- Quantity
- Delivery address
- Pricing summary
- Workflow state
- Conversation metadata

The draft remains mutable throughout the ordering process.

```text
Draft

↓

Modify

↓

Modify Again

↓

Review

↓

Confirm
```

---

# Draft Items

Each product inside the draft is stored as a Draft Item.

Example

```text
Draft

├── Nike Air Max
│      Black
│      Size 9
│      Qty 2
│
└── Adidas Hoodie
       Medium
       Qty 1
```

Draft Items are independent of Order Items.

They exist only until checkout.

---

# Draft Validation

Before checkout, the draft must be validated.

Validation ensures:

- Customer exists
- Product exists
- Variant exists
- Inventory available
- Address selected
- Pricing calculated

Only valid drafts may proceed to checkout.

---

# Customer Review

Before creating an order, the customer receives a complete summary.

Example

```text
Items

Pricing

Delivery Address

Grand Total
```

The customer must explicitly confirm the order.

This prevents accidental purchases.

---

# Customer Confirmation

Confirmation is the final approval step.

Example

```text
Customer

↓

Confirm
```

Only after confirmation does the system invoke the Order Orchestrator.

---

# Order Orchestrator

The Order Orchestrator performs the conversion

```text
Draft

↓

Order
```

The orchestrator coordinates multiple business services while maintaining transactional consistency.

Responsibilities include:

- Validate Draft
- Reserve Inventory
- Create Order
- Copy Draft Items
- Create Payment
- Create Shipment
- Create Order Status History
- Complete Draft

The orchestrator is the only component allowed to create an Order.

---

# Checkout Transaction

The complete checkout process executes inside a single database transaction.

```text
BEGIN TRANSACTION

↓

Validate Draft

↓

Reserve Inventory

↓

Create Order

↓

Copy Draft Items

↓

Create COD Payment

↓

Create Shipment

↓

Create Initial Status History

↓

Complete Draft

↓

COMMIT
```

If any step fails, the transaction is rolled back.

```text
ROLLBACK
```

This guarantees consistency across the entire ordering process.

---

# Order Creation

After validation succeeds, a permanent Order is created.

The order stores immutable business information.

Example

```text
Order

Order Number

Customer

Totals

Address

Status
```

Unlike drafts, orders should not be edited directly.

---

# Order Items

Each Draft Item becomes an Order Item.

```text
Draft Item

↓

Order Item
```

The copied data includes:

- Product Variant
- Quantity
- Unit Price
- Subtotal

The relationship with the draft is preserved through the originating Draft ID.

---

# Payment Creation

After creating the order, the system creates the payment record.

Current implementation:

```text
Cash On Delivery (COD)
```

Future payment methods may include:

- UPI
- Credit Card
- Debit Card
- Net Banking
- Wallets

The payment subsystem remains independent from the order creation logic.

---

# Shipment Creation

Once payment information has been created, the shipment record is initialized.

Example

```text
Shipment

Status

↓

PENDING
```

Shipment tracking begins after warehouse processing.

---

# Order Status History

Every significant order event is recorded.

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

OUT FOR DELIVERY

↓

DELIVERED
```

The history provides a complete audit trail.

Order status should never be overwritten.

Instead, new status entries are appended.

---

# Draft Completion

Once checkout succeeds, the draft is finalized.

```text
ACTIVE

↓

COMPLETED
```

A completed draft becomes read-only.

It remains available for auditing and historical reference.

---

# Draft Failure

If checkout fails:

```text
Inventory Failure

↓

ROLLBACK
```

The draft remains

```text
ACTIVE
```

allowing the customer to retry without rebuilding the order.

---

# Order Lifecycle States

The complete order lifecycle is:

```text
Draft Created

↓

Draft Updated

↓

Draft Reviewed

↓

Customer Confirmed

↓

Order Created

↓

Payment Created

↓

Shipment Created

↓

Status History Initialized

↓

Order Fulfilled
```

---

# Transaction Ownership

The transaction boundary belongs to the Order Orchestrator.

```text
Order Orchestrator

↓

BEGIN

↓

Business Operations

↓

COMMIT
```

Individual services should never commit independently.

This ensures that the checkout process remains atomic.

---

# Design Principles

## Draft Before Order

Orders are never created directly.

Every order originates from an Order Draft.

---

## Immutable Orders

Orders represent completed business transactions.

Once created, they should remain immutable.

---

## Transactional Consistency

Checkout either completes entirely or not at all.

Partial orders must never exist.

---

## Separation of Responsibilities

Conversation manages communication.

Draft manages temporary business state.

Order represents permanent business state.

The Order Orchestrator manages conversion.

---

# Summary

The order lifecycle follows a Draft-First architecture that separates conversational shopping from permanent business transactions.

By introducing the Order Draft as an intermediate aggregate, the system supports conversational ordering, resumable shopping sessions, transactional consistency, and future extensibility while ensuring that permanent Orders are created only after explicit customer confirmation.
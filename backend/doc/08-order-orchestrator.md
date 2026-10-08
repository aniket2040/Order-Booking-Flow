# Order Orchestrator

## Purpose

The Order Orchestrator is responsible for converting a validated **Order Draft** into a permanent **Order**.

Unlike business services that own a single domain responsibility, the orchestrator coordinates multiple services to execute a complete checkout transaction.

It acts as the transaction boundary of the ordering system.

Only the Order Orchestrator is allowed to create an Order.

---

# Why an Orchestrator?

Creating an order is not a single operation.

Checkout requires multiple independent business operations.

Examples include:

- Validate Draft
- Reserve Inventory
- Create Order
- Copy Draft Items
- Create Payment
- Create Shipment
- Create Initial Status History
- Complete Draft

Each operation belongs to a different service.

The orchestrator coordinates these services without embedding their business logic.

---

# High-Level Architecture

```text
Customer Confirmation

        │

        ▼

Order Orchestrator

        │

        ├──────────────► Inventory Service

        ├──────────────► Order Service

        ├──────────────► Payment Service

        ├──────────────► Shipment Service

        ├──────────────► Notification Service

        └──────────────► Draft Service
```

The orchestrator owns the overall business transaction.

Individual services remain independent.

---

# Responsibilities

The Order Orchestrator is responsible for:

- Executing checkout
- Coordinating business services
- Managing transaction boundaries
- Handling failures
- Finalizing the draft
- Returning the completed order

The orchestrator never performs business logic directly.

---

# Checkout Flow

The complete checkout process is shown below.

```text
Order Draft

↓

Validate Draft

↓

Reserve Inventory

↓

Create Order

↓

Copy Draft Items

↓

Create Payment

↓

Create Shipment

↓

Create Initial Status History

↓

Complete Draft

↓

Reload Order

↓

Generate Notification

↓

Return Response
```

Each step is delegated to the appropriate business service.

---

# Transaction Boundary

Checkout executes inside a single database transaction.

```text
BEGIN TRANSACTION

↓

Validate Draft

↓

Reserve Inventory

↓

Create Order

↓

Create Payment

↓

Create Shipment

↓

Create Status History

↓

Complete Draft

↓

COMMIT
```

If any step fails,

```text
ROLLBACK
```

The system returns to its previous consistent state.

---

# Step 1 — Validate Draft

Before checkout begins, the draft must be validated.

Validation ensures:

- Customer exists
- Draft is ACTIVE
- Draft contains items
- Address exists
- Pricing exists
- Inventory is available

Invalid drafts immediately terminate checkout.

---

# Step 2 — Reserve Inventory

The Inventory Service reserves stock for every Draft Item.

Example

```text
Draft Item

↓

Inventory Service

↓

Reserve Quantity
```

Reservation prevents overselling during checkout.

---

# Step 3 — Create Order

The Order Service creates the permanent Order entity.

Information copied includes:

- Customer
- Address
- Pricing
- Totals
- Order Number

The Order becomes the root aggregate for all downstream business operations.

---

# Step 4 — Copy Draft Items

Each Draft Item becomes an Order Item.

```text
Draft Item

↓

Order Item
```

Copied information includes:

- Product Variant
- Quantity
- Unit Price
- Subtotal

The draft remains unchanged.

---

# Step 5 — Create Payment

The Payment Service initializes the payment record.

Current implementation

```text
Cash On Delivery
```

Future payment providers may include:

- UPI
- Razorpay
- Stripe
- PayPal

The orchestrator remains unchanged regardless of payment provider.

---

# Step 6 — Create Shipment

The Shipment Service initializes shipment information.

Example

```text
Shipment

Status

↓

PENDING
```

Shipment processing begins after checkout.

---

# Step 7 — Create Status History

Every order begins with an initial history record.

```text
PLACED
```

Future transitions append additional records.

History is append-only.

---

# Step 8 — Complete Draft

After every business operation succeeds,

the Draft is finalized.

```text
ACTIVE

↓

COMPLETED
```

Completed drafts become read-only.

---

# Step 9 — Reload Order

The orchestrator reloads the complete aggregate.

Example

```text
Order

↓

Items

↓

Payment

↓

Shipment

↓

Status History
```

The returned object is fully populated.

---

# Step 10 — Generate Notification

Finally,

the Notification Service generates a customer-facing confirmation.

Example

> Your order has been placed successfully.

The orchestrator itself never builds user messages.

---

# Failure Handling

Failures may occur at any stage.

Example

```text
Reserve Inventory

✓

Create Order

✓

Create Payment

✗
```

Result

```text
ROLLBACK
```

Effects

- Inventory reservation released
- Order removed
- Payment removed
- Shipment removed
- Draft remains ACTIVE

The customer may retry checkout.

---

# Service Collaboration

The orchestrator coordinates services without knowing their internal implementations.

```text
Order Orchestrator

↓

Inventory Service

↓

Order Service

↓

Payment Service

↓

Shipment Service

↓

Draft Service

↓

Notification Service
```

Each service owns exactly one business capability.

---

# Dependency Flow

```text
Order Orchestrator

↓

Business Services

↓

Repositories

↓

Database
```

Business services never call the orchestrator.

Dependencies always point downward.

---

# Design Principles

## Coordination over Implementation

The orchestrator coordinates services.

It never performs business logic itself.

---

## Transaction Ownership

The orchestrator owns the checkout transaction.

Individual services never commit independently.

---

## Single Responsibility

Each business service owns one responsibility.

The orchestrator owns the overall business process.

---

## Failure Safety

Checkout is atomic.

Either every business operation succeeds,

or none of them are persisted.

---

## Extensibility

New checkout steps can be introduced without modifying existing services.

Example

```text
Validate Coupon

↓

Calculate Reward Points

↓

Fraud Detection

↓

Create Invoice
```

These become additional orchestration steps.

---

# Future Enhancements

The orchestrator is designed to support future capabilities.

Examples include:

- Coupon validation
- Loyalty points
- Gift cards
- Fraud detection
- Invoice generation
- Payment retries
- Warehouse allocation
- Multi-vendor orders
- Event publishing
- Kafka integration

These enhancements extend the orchestration process without changing existing business services.

---

# Sequence Diagram

```text
Customer

│

▼

Order Orchestrator

│

├────────► Inventory Service

│

├────────► Order Service

│

├────────► Payment Service

│

├────────► Shipment Service

│

├────────► Draft Service

│

└────────► Notification Service

│

▼

Order Created

│

▼

Customer Confirmation
```

---

# Summary

The Order Orchestrator is the transaction coordinator of the Order Automation Chatbot.

Rather than containing business logic, it coordinates independent domain services to execute a complete checkout process within a single atomic transaction.

By centralizing transaction management while keeping domain logic distributed across specialized services, the architecture achieves consistency, extensibility, maintainability, and clear separation of responsibilities.
# Draft Lifecycle

## Purpose

The Order Draft is the central aggregate of the conversational ordering system.

It represents a customer's in-progress purchase and serves as the temporary business state throughout the conversation.

Unlike an Order, which represents a finalized business transaction, the Draft is fully mutable and continuously evolves as the customer interacts with the chatbot.

The Draft acts as the conversational equivalent of a shopping cart.

---

# Why an Order Draft?

Conversational ordering is incremental.

Customers rarely provide all ordering information in a single message.

Example

Customer:

> I want Nike Air Max.

↓

Customer:

> Black.

↓

Customer:

> Size 9.

↓

Customer:

> Quantity 2.

↓

Customer:

> Use my default address.

The Order Draft accumulates this information until the customer confirms the purchase.

---

# Lifecycle Overview

```text
Create Draft

↓

ACTIVE

↓

Modify Draft

↓

Review

↓

Customer Decision

├── Confirm

│      ↓

│   COMPLETED

│

├── Cancel

│      ↓

│   ABANDONED

│

└── Timeout

       ↓

    EXPIRED
```

The draft exists only until it reaches a terminal state.

---

# Draft Responsibilities

The Order Draft is responsible for maintaining all temporary order information.

It stores:

- Customer
- Conversation Session
- Workflow State
- Workflow Mode
- Selected Address
- Draft Items
- Pricing
- Current Progress

The draft never stores completed business transactions.

---

# Aggregate Structure

```text
Order Draft

│

├── Draft Items

├── Delivery Address

├── Pricing Summary

├── Workflow State

├── Workflow Mode

└── Conversation Metadata
```

Everything required to resume the conversation belongs to the draft.

---

# Draft Creation

A draft is created when no active draft exists for the current conversation.

Example

```text
Customer

↓

Start Conversation

↓

No ACTIVE Draft

↓

Create Draft

↓

Workflow = DETECT_INTENT
```

The new draft becomes the working state for the conversation.

---

# Draft Modification

During the conversation, every workflow step enriches the draft.

Example

Initial Draft

```text
Product = None

Quantity = None

Address = None
```

Customer

> I want Nike Air Max.

↓

Draft

```text
Product = Nike Air Max
```

Customer

> Quantity 2.

↓

Draft

```text
Product = Nike Air Max

Quantity = 2
```

Customer

> Black Size 9.

↓

Draft

```text
Color = Black

Size = 9
```

The draft evolves incrementally.

---

# Draft Items

Products selected by the customer are stored as Draft Items.

Example

```text
Draft

├── Nike Air Max

│      Qty 2

│      Black

│      Size 9

│

└── Adidas Hoodie

       Qty 1

       Medium
```

Draft Items remain editable until checkout.

---

# Workflow State

The current workflow state is persisted inside the draft.

Example

```text
Workflow State

↓

COLLECT_ADDRESS
```

The workflow resumes from this state on the next request.

---

# Workflow Mode

Workflow Mode determines the intent of the current conversation.

Examples

```text
PLACE_ORDER

MODIFY_ORDER

CANCEL_ORDER

TRACK_ORDER
```

Workflow Mode influences handler behavior while reusing the same workflow engine.

---

# Pricing

Pricing is recalculated whenever draft contents change.

The draft stores:

```text
Subtotal

Tax

Shipping

Discount

Grand Total
```

The stored pricing represents the latest calculated totals.

---

# Delivery Address

The draft stores the selected delivery address.

The address may originate from:

- Customer default address
- Newly created address
- Existing saved address

Only one delivery address is associated with a draft.

---

# Review Stage

Once all required information has been collected, the draft enters the review stage.

Example

```text
Draft

↓

Pricing

↓

Summary

↓

Customer Review
```

The customer reviews:

- Items
- Pricing
- Delivery Address

before confirming the order.

---

# Checkout

After confirmation, the draft is passed to the Order Orchestrator.

```text
Draft

↓

Order Orchestrator

↓

Order
```

The draft itself is never modified during checkout except for its lifecycle status.

---

# Draft Status

The draft lifecycle is represented by five states.

```text
ACTIVE

↓

COMPLETED

↓

ABANDONED

↓

EXPIRED
```

---

## ACTIVE

The customer is actively building the order.

Characteristics

- Editable
- Resumable
- Accepts new items
- Workflow continues

---

## COMPLETED

The draft has been successfully converted into an Order.

Characteristics

- Read-only
- Historical reference
- Linked to Order

No further modifications are allowed.

---

## ABANDONED

The customer intentionally leaves the draft.

Possible reasons include

- Starts a different order
- Cancels checkout
- Explicitly discards the draft

Abandoned drafts remain available for auditing.

---

## EXPIRED

The draft automatically expires after a configured period of inactivity.

Expired drafts cannot resume checkout.

---

# Draft Resolution Policy

Whenever a new customer message arrives, the system determines whether the existing draft should be reused.

Conceptually

```text
Incoming Message

↓

Active Draft?

↓

No

↓

Create Draft

↓

ACTIVE

Yes

↓

Does Message Belong To Current Draft?

↓

Yes

↓

Resume Draft

↓

Continue Workflow

No

↓

ABANDON Current Draft

↓

Create New Draft

↓

Restart Workflow
```

This policy prevents unrelated conversations from corrupting an existing draft.

---

# Draft Completion

A draft reaches completion only after a successful checkout.

```text
ACTIVE

↓

Validate

↓

Checkout

↓

Order Created

↓

COMPLETED
```

Completion occurs inside the checkout transaction.

---

# Transaction Relationship

The Order Draft participates in checkout but does not own the transaction.

```text
Order Draft

↓

Order Orchestrator

↓

Database Transaction

↓

Order
```

The Order Orchestrator owns the transaction boundary.

---

# Design Principles

## Mutable Aggregate

Unlike Orders, Drafts are intentionally mutable.

Every workflow step may modify the draft.

---

## Single Source of Truth

The draft contains all temporary business information.

No workflow state should exist outside the draft.

---

## Conversation Independent

The workflow is reconstructed from the draft.

No conversational state is stored in memory.

---

## Auditability

Completed, abandoned, and expired drafts remain available for future analysis.

---

## Draft Before Order

Orders are never created directly.

Every order originates from exactly one Order Draft.

---

# Summary

The Order Draft is the central aggregate of the conversational ordering system.

It functions as a persistent shopping cart, workflow checkpoint, and temporary business state.

By separating mutable drafts from immutable orders, the system supports resumable conversations, safe checkout, conversational modifications, and transactional consistency while maintaining a clear separation between conversation management and permanent business records.
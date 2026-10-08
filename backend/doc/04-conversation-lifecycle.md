# Conversation Lifecycle

## Purpose

The conversation lifecycle describes how a customer interacts with the chatbot from the moment a message is received until a response is returned.

Unlike a traditional request-response application, the chatbot maintains conversational context across multiple interactions. Every incoming message is interpreted within the context of an active conversation and an order draft.

The conversation layer is responsible only for managing the conversation. Business operations such as inventory validation, pricing, and order creation are delegated to downstream services.

---

# Conversation Flow

The complete lifecycle is shown below.

```text
Customer
    │
    ▼
HTTP Request
    │
    ▼
Conversation Service
    │
    ▼
Conversation Session
    │
    ▼
Order Draft
    │
    ▼
Workflow Context
    │
    ▼
Workflow Engine
    │
    ▼
Workflow Handlers
    │
    ▼
Business Services
    │
    ▼
Workflow Response
    │
    ▼
Customer
```

Every customer message follows this same lifecycle.

---

# Primary Components

The conversation layer consists of five primary components.

## Conversation

Represents the overall interaction between a customer and the chatbot.

Responsibilities include:

- Chat history
- Conversation metadata
- Conversation ownership

A conversation may contain multiple workflow executions.

---

## Conversation Session

A conversation session represents one active interaction between a customer and the chatbot.

Responsibilities:

- Session ownership
- Active conversation tracking
- Conversation state management

Only one active conversation session exists for a customer at any given time.

```text
Customer

↓

Conversation Session
```

The session itself does **not** store business information.

---

## Order Draft

The draft acts as the conversational shopping cart.

It stores temporary business information gathered during the conversation.

Examples include:

- Selected product
- Variant
- Quantity
- Delivery address
- Pricing
- Workflow state

Unlike an Order, the draft is fully mutable.

```text
Conversation

↓

Order Draft
```

---

## Workflow Context

The workflow context is created for every incoming request.

It represents the current execution state of the workflow.

Typical information includes:

- Customer ID
- Session ID
- Draft ID
- Workflow State
- Workflow Mode
- Extracted Slots

The workflow context is an in-memory execution object.

It is not a database entity.

---

## Workflow Engine

The workflow engine coordinates the conversation.

Responsibilities include:

- Selecting the correct workflow handler
- Executing handlers
- Managing state transitions
- Supporting automatic workflow continuation

The workflow engine contains no business rules.

---

# Conversation Initialization

Every request begins by loading the conversation context.

```text
Customer Message

↓

Load Customer

↓

Load Active Conversation Session

↓

Load Active Order Draft

↓

Build Workflow Context

↓

Execute Workflow
```

If no active draft exists, a new draft is created.

---

# Slot Collection

Customer information is collected gradually during the conversation.

Example

Customer:

> I want Nike Air Max

Extracted Slots

```text
product = Nike Air Max
```

Later

Customer:

> Black Size 9 Quantity 2

Updated Slots

```text
product = Nike Air Max
color = Black
size = 9
quantity = 2
```

Slots are accumulated inside the draft until checkout.

---

# Workflow Execution

Each request enters the workflow engine.

```text
Workflow Context

↓

Current Workflow State

↓

Resolve Handler

↓

Execute Handler

↓

Transition

↓

Next Workflow State
```

The workflow engine itself does not perform business operations.

Instead, it delegates work to workflow handlers.

---

# Workflow Auto-Continuation

Some workflow steps do not require additional customer interaction.

For these states, the workflow automatically proceeds to the next handler.

Example

```text
Resolve Product

↓

Resolve Variant

↓

Check Inventory
```

The customer receives only the final meaningful response.

---

# Workflow Pause

Some workflow states require customer input.

These states terminate automatic execution.

Examples include:

- Missing Quantity
- Missing Address
- Order Review
- Order Confirmation

Example

```text
Customer

↓

Review Order

↓

STOP

↓

Customer Confirms
```

The conversation resumes after the customer replies.

---

# Conversation State

The current workflow state is persisted in the draft.

Example

```text
ACTIVE Draft

↓

Workflow State

↓

COLLECT_ADDRESS
```

The next customer message resumes from this state unless a new conversation is initiated.

---

# Draft Resolution

When a customer sends a new message, the system determines whether the message belongs to the existing draft.

Conceptually, the decision process is:

```text
Incoming Message

↓

Active Draft Exists?

↓

No
    ↓
Create Draft

Yes
    ↓
Does Message Belong To Draft?

    Yes
        ↓
Resume Draft

    No
        ↓
Abandon Current Draft

↓

Create New Draft

↓

Restart Workflow
```

This policy ensures that unfinished conversations can be resumed while still allowing customers to begin completely new orders.

---

# Workflow Context Lifecycle

A new workflow context is created for every request.

```text
Incoming Request

↓

Load Draft

↓

Build Workflow Context

↓

Execute Workflow

↓

Return Response

↓

Workflow Context Destroyed
```

Only the draft persists between requests.

---

# Conversation Example

Customer:

> I want Nike Air Max.

Workflow

```text
Detect Intent

↓

Collect Requirements

↓

Resolve Product

↓

STOP
```

Customer:

> Black Size 9 Quantity 2

Workflow

```text
Resolve Variant

↓

Check Availability

↓

Collect Address

↓

STOP
```

Customer:

> Use my default address

Workflow

```text
Calculate Pricing

↓

Review Order

↓

STOP
```

Customer:

> Confirm

Workflow

```text
Create Order

↓

Order Confirmed
```

The customer experiences a natural conversation while the workflow engine performs deterministic state transitions.

---

# Design Principles

The conversation lifecycle follows several design principles.

## Context Driven

Every message is interpreted using the current workflow context.

---

## Stateless Requests

Each HTTP request is stateless.

Conversation continuity is achieved by rebuilding the workflow context from the persisted draft.

---

## Deterministic Workflow

The workflow engine always knows which handler should execute next.

---

## AI-Assisted, Business-Controlled

AI assists with understanding customer intent.

Business decisions remain deterministic and are implemented by workflow handlers and business services.

---

# Summary

The conversation lifecycle separates conversational behavior from business logic.

The workflow engine manages conversation progression.

The draft stores temporary business state.

Business services execute domain operations.

This separation enables a conversational experience while maintaining predictable and testable business behavior.
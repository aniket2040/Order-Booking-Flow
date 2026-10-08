# Workflow Engine

## Purpose

The Workflow Engine is the central execution component of the Order Automation Chatbot.

It coordinates the entire ordering process by executing a sequence of deterministic workflow states.

Rather than embedding business logic inside controllers or AI models, the application models the ordering process as a **Finite State Machine (FSM)** where each state performs exactly one responsibility.

The workflow engine determines:

- Which handler should execute
- What business operation should be performed
- Which state should execute next
- Whether execution should continue automatically or wait for customer input

---

# Why a Workflow Engine?

Conversational commerce is fundamentally stateful.

For example:

Customer

> I want Nike Air Max.

↓

Customer

> Black.

↓

Customer

> Size 9.

↓

Customer

> Quantity 2.

Each message depends on the previous conversation.

Instead of scattering this logic throughout the application, the Workflow Engine centralizes conversation progression.

---

# High-Level Architecture

```text
Customer Message
        │
        ▼
Workflow Context
        │
        ▼
Workflow Service
        │
        ▼
Resolve Current State
        │
        ▼
Workflow Handler
        │
        ▼
Business Services
        │
        ▼
Workflow Result
        │
        ▼
Next Workflow State
```

The workflow engine itself contains no business rules.

It delegates all business operations to services.

---

# Core Components

The workflow engine consists of four primary components.

```text
WorkflowContext

↓

WorkflowService

↓

BaseHandler

↓

WorkflowResult
```

---

# Workflow Context

The Workflow Context represents the current execution state.

It is created at the beginning of every request.

Example

```text
WorkflowContext

Customer ID

Session ID

Draft ID

Workflow State

Workflow Mode

Conversation Slots
```

The Workflow Context exists only during request execution.

It is reconstructed for every request from the persisted Order Draft.

---

# Workflow Service

The Workflow Service coordinates execution.

Responsibilities include:

- Resolve current handler
- Execute handler
- Update workflow state
- Support automatic continuation
- Produce final response

Example

```text
Current State

↓

Resolve Handler

↓

Execute

↓

Transition

↓

Continue?

↓

Yes → Next Handler

No → Return Response
```

The Workflow Service contains no business logic.

---

# Workflow Handlers

Each workflow state is implemented as an independent handler.

Example

```text
DetectIntentHandler

CollectRequirementsHandler

ResolveProductHandler

ResolveVariantHandler

CheckAvailabilityHandler

CollectAddressHandler

CalculatePricingHandler

ReviewOrderHandler

ConfirmOrderHandler

CreateOrderHandler
```

Every handler owns one responsibility.

No handler should perform multiple business operations.

---

# Base Handler

All handlers inherit from BaseHandler.

The execution lifecycle is identical for every workflow state.

```text
execute()

↓

validate()

↓

handle()

↓

transition()

↓

WorkflowResult
```

This provides a consistent execution model throughout the workflow.

---

# Workflow Result

Every handler returns a WorkflowResult.

Typical fields include:

```text
success

message

next_state

continue_processing

review

order_id
```

The WorkflowResult determines how the workflow proceeds.

---

# Workflow States

The ordering workflow is modeled as a finite state machine.

```text
DETECT_INTENT

↓

COLLECT_REQUIREMENTS

↓

RESOLVE_PRODUCT

↓

RESOLVE_VARIANT

↓

CHECK_AVAILABILITY

↓

COLLECT_ADDRESS

↓

CALCULATE_PRICING

↓

REVIEW_ORDER

↓

CONFIRM_ORDER

↓

CREATE_ORDER

↓

ORDER_CONFIRMED
```

Each state performs exactly one business responsibility.

---

# State Transitions

Every handler decides which state executes next.

Example

```text
COLLECT_REQUIREMENTS

↓

Requirements Complete

↓

RESOLVE_PRODUCT
```

or

```text
COLLECT_REQUIREMENTS

↓

Missing Quantity

↓

COLLECT_REQUIREMENTS
```

State transitions are deterministic.

---

# Automatic Workflow Continuation

Many workflow states do not require customer interaction.

Example

```text
Resolve Product

↓

Resolve Variant

↓

Check Inventory
```

Instead of returning intermediate responses, the workflow continues automatically.

Example

```text
continue_processing = True
```

The Workflow Service immediately executes the next handler.

---

# Workflow Pause

Execution pauses whenever customer interaction is required.

Examples include:

- Missing quantity
- Missing address
- Review order
- Confirmation

Example

```text
continue_processing = False
```

The workflow returns a response to the customer.

Execution resumes when the next message arrives.

---

# Handler Lifecycle

Every handler follows the same execution model.

```text
Request

↓

Validate

↓

Business Logic

↓

Transition

↓

WorkflowResult
```

Validation failures immediately terminate execution.

---

# Validation

Validation is performed before business logic executes.

Example

```text
Customer

↓

CollectRequirementsHandler

↓

Validate Slots

↓

Missing Quantity

↓

Return Response
```

Invalid requests never reach downstream business services.

---

# Business Service Delegation

Handlers never implement business rules directly.

Example

Instead of

```python
calculate_tax()
```

inside a handler,

the handler delegates to

```text
PricingService
```

Similarly,

```text
ResolveProductHandler

↓

ProductService

↓

ProductRepository
```

This keeps handlers lightweight.

---

# Handler Communication

Handlers communicate only through the Workflow Context.

Example

```text
Resolve Product

↓

product_id

↓

Workflow Context

↓

Resolve Variant
```

Handlers never call one another directly.

---

# Workflow Persistence

Only the Workflow State is persisted between requests.

Example

```text
Order Draft

↓

workflow_state

↓

COLLECT_ADDRESS
```

When the next request arrives,

the Workflow Context is rebuilt from the draft.

---

# Error Handling

Failures terminate workflow execution immediately.

Example

```text
Inventory Not Available

↓

Return Response

↓

Workflow Stops
```

The customer receives an actionable message.

---

# Workflow Modes

The engine supports multiple execution modes.

Examples include:

```text
PLACE_ORDER

MODIFY_ORDER

CANCEL_ORDER

TRACK_ORDER
```

Workflow Mode influences state transitions while reusing the same engine.

---

# Extending the Workflow

Adding a new workflow state requires only three steps.

### Step 1

Create a handler.

```text
ApplyCouponHandler
```

---

### Step 2

Register the handler.

```text
WorkflowState.APPLY_COUPON
```

↓

Handler Mapping

---

### Step 3

Transition to the new state.

```text
CALCULATE_PRICING

↓

APPLY_COUPON

↓

REVIEW_ORDER
```

Existing handlers remain unchanged.

---

# Design Principles

## Single Responsibility

Each handler performs exactly one business operation.

---

## Deterministic Execution

AI assists understanding.

The workflow determines behavior.

---

## Stateless Requests

Workflow execution is rebuilt every request.

No in-memory conversation state is required.

---

## Extensibility

New states can be added without modifying existing handlers.

---

## Testability

Every handler can be tested independently.

Scenario tests validate complete workflow execution.

---

# Sequence Diagram

```text
Customer

│

▼

Workflow Service

│

▼

Resolve Current Handler

│

▼

Handler

│

▼

Business Service

│

▼

Workflow Result

│

▼

Continue?

│

├── Yes

│      ▼

│   Next Handler

│

└── No

       ▼

Return Response
```

---

# Summary

The Workflow Engine is the execution backbone of the Order Automation Chatbot.

It transforms conversational requests into deterministic business workflows while keeping AI, business logic, persistence, and conversation management cleanly separated.

By modeling the ordering process as a finite state machine, the system achieves predictability, extensibility, testability, and maintainability without sacrificing the natural conversational experience.
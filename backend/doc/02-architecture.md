# Architecture

## Purpose

The Order Automation Chatbot follows a layered architecture that separates conversational AI, workflow orchestration, business logic, and data access into independent layers.

Each layer has a single responsibility and communicates only with the layer directly beneath it. This separation makes the system easier to maintain, test, and extend while preventing business logic from becoming tightly coupled to infrastructure or AI providers.

The architecture is designed around Domain-Driven Design (DDD) principles and a workflow-driven ordering process rather than a traditional CRUD application.

---

# High-Level Architecture

```text
                        +-----------------------+
                        |      Client App       |
                        |  Web / Mobile / API   |
                        +-----------+-----------+
                                    |
                                    v
                        +-----------------------+
                        |      FastAPI API      |
                        |    Request Routing    |
                        +-----------+-----------+
                                    |
                                    v
                        +-----------------------+
                        | Conversation Service  |
                        +-----------+-----------+
                                    |
                                    v
                        +-----------------------+
                        |   Workflow Engine     |
                        +-----------+-----------+
                                    |
                    +---------------+---------------+
                    |               |               |
                    v               v               v
             Workflow         AI Components    Validation
              Handlers
                    |
                    v
          +-----------------------+
          |  Business Services    |
          +-----------+-----------+
                      |
                      v
          +-----------------------+
          |     Repositories      |
          +-----------+-----------+
                      |
                      v
          +-----------------------+
          |     PostgreSQL DB     |
          +-----------------------+
```

---

# Layer Responsibilities

The application is divided into independent architectural layers.

Each layer owns exactly one responsibility.

---

# API Layer

**Location**

```
app/api/
```

## Responsibilities

- Receive HTTP requests.
- Validate request schemas.
- Delegate work to services.
- Return API responses.

The API layer never contains business logic.

Example:

```
POST /chat
        │
        ▼
ConversationService
```

---

# Conversation Layer

**Location**

```
app/Services/conversation/
```

## Responsibilities

The Conversation Layer manages the interaction between the customer and the ordering workflow.

It is responsible for:

- Loading conversations
- Managing conversation sessions
- Building workflow context
- Delegating execution to the workflow engine

The conversation layer does **not** perform business operations such as inventory checks or order creation.

---

# Workflow Layer

**Location**

```
app/Services/workflow/
```

## Responsibilities

The workflow engine controls the ordering process.

Each customer request enters the workflow engine.

The workflow engine determines:

- Current workflow state
- Appropriate handler
- Next workflow state
- Whether processing should continue automatically

Example:

```text
DETECT_INTENT
        │
        ▼
COLLECT_REQUIREMENTS
        │
        ▼
RESOLVE_PRODUCT
        │
        ▼
RESOLVE_VARIANT
        │
        ▼
CHECK_AVAILABILITY
```

The workflow engine contains no database logic.

---

# Workflow Handlers

Each workflow state is implemented as an independent handler.

Example

```
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

Every handler performs exactly one business responsibility.

Handlers are intentionally small and deterministic.

---

# AI Layer

**Location**

```
app/ai/
```

## Responsibilities

AI components perform language understanding.

Examples include

- Intent Detection
- Slot Extraction
- Product Understanding
- Future Recommendation Engine

The AI layer never directly accesses the database.

Instead, it produces structured information consumed by workflow handlers.

Example

```
Customer

↓

"I want Nike Air Max"

↓

Slot Extractor

↓

{
    product: "Nike Air Max"
}
```

---

# Business Service Layer

**Location**

```
app/Services/
```

Business services implement the application's business rules.

Examples include

- ProductService
- InventoryService
- PricingService
- DraftService
- OrderService
- CustomerService
- PaymentService
- NotificationService

Business services coordinate repositories but do not expose persistence details.

---

# Repository Layer

**Location**

```
app/repositories/
```

Repositories provide persistence.

Responsibilities include

- Querying entities
- Creating entities
- Updating entities
- Deleting entities

Repositories never contain business rules.

Example

```
ProductRepository

DraftRepository

InventoryRepository

OrderRepository
```

---

# Database Layer

The database stores all business entities.

Examples

- Customers
- Products
- Product Variants
- Inventory
- Drafts
- Orders
- Payments
- Shipments

The database should never be accessed directly from handlers.

Only repositories communicate with the database.

---

# Dependency Direction

Dependencies always point downward.

```text
API
 │
 ▼
Conversation
 │
 ▼
Workflow
 │
 ▼
Business Services
 │
 ▼
Repositories
 │
 ▼
Database
```

No lower layer depends on an upper layer.

---

# Architectural Principles

## Separation of Concerns

Each layer owns a single responsibility.

Example

```
Workflow Handler

↓

PricingService

↓

PricingRepository
```

The handler never calculates tax itself.

---

## Dependency Inversion

Business logic depends on abstractions rather than infrastructure.

Example

```
Workflow Handler

↓

InventoryService

↓

InventoryRepository

↓

PostgreSQL
```

The handler is unaware of SQLAlchemy.

---

## Single Responsibility Principle

Every component performs one task.

Examples

```
DraftService

Responsible only for draft operations.
```

```
PricingService

Responsible only for pricing.
```

```
OrderService

Responsible only for order creation.
```

---

## Workflow Driven Design

Unlike traditional CRUD applications, the system is organized around workflow states.

Each request progresses through deterministic workflow transitions.

```text
DETECT_INTENT

↓

COLLECT_REQUIREMENTS

↓

RESOLVE_PRODUCT

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

---

# Transaction Boundaries

Business transactions are centralized.

The most important transaction is checkout.

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

If any step fails, the transaction is rolled back.

---

# Why This Architecture?

The chosen architecture provides several advantages.

## Maintainability

Each layer can evolve independently.

---

## Testability

Services and handlers can be tested independently.

---

## Extensibility

Adding a new workflow state does not require changing existing handlers.

---

## Scalability

AI providers, payment providers, and inventory providers can be replaced without affecting workflow logic.

---

## Clean Separation

Conversation logic remains independent from business logic.

Business logic remains independent from persistence.

Persistence remains independent from infrastructure.
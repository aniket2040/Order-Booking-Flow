# Project Structure

## Purpose

The project is organized using a layered architecture that separates conversational AI, workflow orchestration, business logic, persistence, and infrastructure into dedicated packages.

Each package has a clearly defined responsibility.

This organization improves readability, maintainability, and scalability while keeping dependencies flowing in a single direction.

---

# Root Directory

```text
backend/
│
├── app/
├── tests/
├── alembic/
├── docs/
├── scripts/
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# app/

The `app` package contains the entire application source code.

```text
app/
│
├── ai/
├── api/
├── core/
├── database/
├── models/
├── repositories/
├── schema/
├── Services/
├── workflow/
├── utils/
└── main.py
```

---

# ai/

Contains AI-specific components.

Responsibilities include

- Intent Detection
- Slot Extraction
- Prompt Management
- AI Provider Integration

Example

```text
ai/

├── intent_detector.py

├── slot_extractor.py

├── prompt_builder.py

└── providers/
```

The AI layer should never access the database directly.

---

# api/

Contains all HTTP endpoints.

Responsibilities

- Receive requests
- Validate request schemas
- Call application services
- Return responses

Example

```text
api/

├── routes/

│      ├── chat.py

│      ├── order.py

│      └── customer.py

└── dependencies.py
```

The API layer contains no business logic.

---

# core/

Contains application-wide configuration.

Examples

```text
core/

├── config.py

├── logging.py

├── exceptions.py

└── security.py
```

---

# database/

Contains database configuration.

Responsibilities

- SQLAlchemy engine
- Async session
- Database initialization

Example

```text
database/

├── postgres.py

├── session.py

└── migrations.py
```

---

# models/

Contains SQLAlchemy entities.

Models represent database tables.

Current aggregates include

```text
models/

├── customer/

├── catalog/

├── draft/

├── order/

├── conversation/

└── enums.py
```

Each aggregate is grouped into its own package.

Example

```text
models/

└── order/

      ├── order.py

      ├── order_item.py

      ├── payment.py

      ├── shipment.py

      └── order_status_history.py
```

---

# repositories/

Repositories encapsulate all persistence logic.

Responsibilities

- Query entities
- Save entities
- Update entities
- Delete entities

Repositories never contain business rules.

Example

```text
repositories/

├── customer/

├── catalog/

├── draft/

├── order/

└── conversation/
```

---

# schema/

Contains Pydantic request and response models.

Responsibilities

- API validation
- Internal DTOs
- Workflow objects

Example

```text
schema/

├── chat.py

├── workflow.py

├── pricing.py

├── review.py

└── common.py
```

No business logic belongs here.

---

# Services/

Contains business logic.

Every service owns a specific business capability.

Example

```text
Services/

├── catalog/

├── customer/

├── draft/

├── inventory/

├── notification/

├── order/

├── payment/

├── pricing/

├── review/

├── workflow/

└── validation/
```

Example responsibilities

ProductService

- Product lookup
- Variant resolution

InventoryService

- Availability checks
- Stock reservation
- Stock deduction

DraftService

- Draft management
- Draft items
- Pricing synchronization

OrderService

- Create orders
- Load orders

PricingService

- Calculate totals

---

# workflow/

Contains the workflow engine.

Responsibilities

- Workflow execution
- State transitions
- Workflow handlers

Structure

```text
workflow/

├── workflow_service.py

├── base_handler.py

└── handlers/

      ├── detect_intent_handler.py

      ├── collect_requirements_handler.py

      ├── resolve_product_handler.py

      ├── resolve_variant_handler.py

      ├── check_availability_handler.py

      ├── collect_address_handler.py

      ├── calculate_pricing_handler.py

      ├── review_order_handler.py

      ├── confirm_order_handler.py

      └── create_order_handler.py
```

Every workflow state corresponds to exactly one handler.

---

# utils/

Contains reusable utility functions.

Examples

```text
utils/

├── datetime.py

├── money.py

├── string.py

└── uuid.py
```

Utilities should remain framework-independent.

---

# tests/

Contains automated tests.

Structure mirrors the application.

```text
tests/

├── unit/

├── integration/

├── scenarios/

├── fixtures/

└── helpers/
```

Scenario tests simulate complete customer journeys.

Example

```text
test_confirm_order.py

test_restart_order.py

test_modify_order.py

test_cancel_order.py
```

---

# docs/

Contains technical documentation.

```text
docs/

01-system-overview.md

02-architecture.md

03-project-structure.md

...
```

Documentation should evolve together with the codebase.

---

# alembic/

Contains database migration scripts.

Responsibilities

- Schema creation
- Schema evolution
- Version management

---

# scripts/

Contains developer utilities.

Examples

```text
scripts/

seed_database.py

reset_database.py

create_demo_data.py
```

These scripts are intended for local development and testing.

---

# Dependency Rules

The following dependency direction must always be respected.

```text
API

↓

Conversation

↓

Workflow

↓

Services

↓

Repositories

↓

Database
```

Lower layers must never depend on higher layers.

---

# Module Ownership

| Package | Responsibility |
|----------|----------------|
| ai | AI and language understanding |
| api | HTTP interface |
| core | Configuration and infrastructure |
| database | Database configuration |
| models | Database entities |
| repositories | Data persistence |
| schema | Request and response models |
| Services | Business logic |
| workflow | Conversation workflow |
| utils | Shared utilities |
| tests | Automated testing |
| docs | Technical documentation |

---

# Design Philosophy

The project structure reflects the system architecture.

Instead of organizing files by technical type alone, related functionality is grouped into cohesive modules.

For example

```text
Order

↓

Model

Repository

Service

Workflow

Schema
```

are all organized independently while still following the overall layered architecture.

This modular organization minimizes coupling and makes new features easier to introduce without affecting existing components.
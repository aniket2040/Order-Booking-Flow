# Order Automation Chatbot

## Overview

Order Automation Chatbot is an AI-powered conversational commerce platform that enables customers to discover products, configure variants, place orders, and track purchases through natural language conversations.

Instead of navigating multiple pages of a traditional e-commerce website, customers interact with a conversational AI assistant that guides them through the complete purchasing workflow.

The system combines a workflow engine with AI-powered intent detection and slot extraction to create a deterministic yet conversational ordering experience.

---

# Objectives

The project aims to:

- Provide a natural language interface for online shopping.
- Automate the complete order placement workflow.
- Maintain conversational context across multiple user interactions.
- Separate AI reasoning from business logic.
- Support extensible workflows and future business capabilities.

---

# Key Features

## Product Discovery

Customers can search products using natural language.

Example:

> I want Nike Air Max.

---

## Variant Selection

Supports selecting product attributes such as

- Color
- Size
- Storage
- Capacity
- Model

---

## Inventory Validation

Checks inventory before checkout.

Example:

> Nike Air Max
> Black
> Size 9
> Quantity 2

↓

Verify stock availability.

---

## Address Collection

Supports

- Default Address
- Manual Address Entry

---

## Pricing Engine

Automatically calculates

- Subtotal
- Tax
- Shipping Charges
- Discounts
- Grand Total

---

## Order Review

Generates a structured order summary before checkout.

---

## Checkout Orchestration

Creates

- Order
- Order Items
- Payment
- Shipment
- Status History

inside a single transaction.

---

## Order Tracking

Supports future conversational queries such as

> Where is my order?

---

# High-Level Architecture

```

Customer

↓

FastAPI REST API

↓

Conversation Service

↓

Workflow Engine

↓

Workflow Handlers

↓

Business Services

↓

Repositories

↓

PostgreSQL Database

```

---

# Technology Stack

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy (Async)
- PostgreSQL

## AI

- Azure OpenAI
- Google Gemini
- Custom Slot Extractor

## ORM

- SQLAlchemy Async ORM

## Validation

- Pydantic v2

## Database Migration

- Alembic

## Testing

- Pytest
- Async Test Client

---

# Core Concepts

The application is built around four primary concepts.

## Conversation

Stores chat history between customer and AI.

---

## Conversation Session

Represents one active conversation.

Maintains workflow progression during the interaction.

---

## Order Draft

Acts as a conversational shopping cart.

Stores all temporary order information until checkout.

---

## Order

Represents the finalized business transaction.

Orders become immutable after creation.

---

# Design Principles

The project follows several architectural principles.

## Layered Architecture

```

Controller

↓

Workflow

↓

Service

↓

Repository

↓

Database

```

---

## Separation of Concerns

AI components never access the database.

Repositories never contain business logic.

Workflow handlers never perform persistence directly.

Each layer owns exactly one responsibility.

---

## Workflow Driven

The ordering process is modeled as a finite workflow instead of a collection of API endpoints.

Each workflow state performs one responsibility.

---

## Draft First

Customers never directly create orders.

They always build an Order Draft first.

Only after confirmation is the draft converted into an Order.

---

## Transaction Safety

Checkout is executed inside a single database transaction to guarantee consistency.

---

# Future Roadmap

Planned enhancements include

- Multiple Products per Order
- Shopping Cart Management
- Coupon Engine
- Online Payments
- Recommendation Engine
- Order Tracking
- Returns & Refunds
- Multi-language Support
- Voice Ordering
- Agentic AI Planning

---

# Documentation Structure

This documentation is organized as follows.

```

docs/

├── 01-system-overview.md

├── 02-architecture.md

├── 03-project-structure.md

├── 04-conversation-lifecycle.md

├── 05-order-lifecycle.md

├── 06-workflow-engine.md

├── 07-draft-lifecycle.md

├── 08-order-orchestrator.md

├── 09-database-design.md

├── 10-api-reference.md

├── 11-sequence-diagrams.md

└── 12-extension-guide.md

```

Each document explains one major subsystem independently while maintaining a consistent architectural perspective.
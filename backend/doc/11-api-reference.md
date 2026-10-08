# API Reference

## Purpose

This document describes the public REST APIs exposed by the Order Automation Chatbot.

The API provides a conversational interface for customers to interact with the ordering system.

Unlike traditional e-commerce APIs that expose separate endpoints for products, carts, checkout, and orders, this application exposes a conversational workflow through a single chat endpoint.

The workflow engine determines the next business operation based on the current conversation state.

---

# Base URL

```
http://localhost:8000
```

---

# Authentication

Current Version

```
Authentication is not implemented.
```

Future versions may support

- JWT Authentication
- OAuth2
- API Keys

---

# Content Type

Every request must use

```
Content-Type: application/json
```

---

# Primary Endpoint

## POST /chat

Processes one conversational message.

Every customer interaction enters the system through this endpoint.

---

# Request

```http
POST /chat
```

## Request Body

```json
{
    "customer_id": "bf0b5056-2b33-4969-a1f7-50875ff61fb2",
    "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    "message": "I want Nike Air Max"
}
```

---

# Request Fields

| Field | Type | Description |
|---------|------|-------------|
| customer_id | UUID | Customer identifier |
| session_id | UUID | Conversation session identifier |
| message | String | Customer message |

---

# Response

```json
{
    "success": true,
    "message": "Found Nike Air Max.",
    "current_state": "RESOLVE_PRODUCT",
    "next_state": "RESOLVE_VARIANT",
    "review": null,
    "order_id": null
}
```

---

# Response Fields

| Field | Description |
|---------|-------------|
| success | Request execution status |
| message | Human-readable response |
| current_state | Current workflow state |
| next_state | Next workflow state |
| review | Order review object (if available) |
| order_id | Created order identifier |

---

# Example Conversation

## Step 1

Request

```json
{
    "customer_id":"123",
    "message":"I want Nike Air Max"
}
```

Response

```json
{
    "success":true,
    "message":"Found Nike Air Max.",
    "next_state":"RESOLVE_VARIANT"
}
```

---

## Step 2

Request

```json
{
    "customer_id":"123",
    "message":"Black Size 9 Quantity 2"
}
```

Response

```json
{
    "success":true,
    "message":"The requested item is available.",
    "next_state":"COLLECT_ADDRESS"
}
```

---

## Step 3

Request

```json
{
    "customer_id":"123",
    "message":"Use my default address"
}
```

Response

```json
{
    "success":true,
    "message":"Please review your order.",
    "review":{
        ...
    },
    "next_state":"CONFIRM_ORDER"
}
```

---

## Step 4

Request

```json
{
    "customer_id":"123",
    "message":"Confirm"
}
```

Response

```json
{
    "success":true,
    "message":"Your order has been placed successfully.",
    "order_id":"9d8d9a2e-...",
    "next_state":"ORDER_CONFIRMED"
}
```

---

# Workflow Responses

The API response varies depending on the workflow state.

## Information Request

```json
{
    "success":true,
    "message":"Please provide quantity."
}
```

---

## Validation Failure

```json
{
    "success":false,
    "message":"Requested quantity exceeds available stock."
}
```

---

## Review Response

```json
{
    "success":true,
    "review":{
        "summary":{
            ...
        }
    }
}
```

---

## Order Confirmation

```json
{
    "success":true,
    "order_id":"..."
}
```

---

# Review Object

When the workflow reaches REVIEW_ORDER, the response contains an Order Review.

Example

```json
{
    "summary":{
        "items":[
            {
                "product_name":"Nike Air Max",
                "variant_name":"Black Size 9",
                "quantity":2,
                "subtotal":9998
            }
        ],
        "pricing":{
            "subtotal":9998,
            "tax":1800,
            "shipping_charge":0,
            "discount":500,
            "grand_total":11298
        },
        "delivery":{
            "recipient_name":"John Doe",
            "city":"Raipur"
        }
    }
}
```

---

# Error Responses

## Validation Error

HTTP

```
422 Unprocessable Entity
```

Example

```json
{
    "detail":[
        {
            "msg":"Input should be a valid UUID."
        }
    ]
}
```

---

## Customer Not Found

```
404 Not Found
```

Example

```json
{
    "detail":"Customer not found."
}
```

---

## Internal Server Error

```
500 Internal Server Error
```

Example

```json
{
    "detail":"Unexpected server error."
}
```

---

# Workflow State Reference

Possible workflow states include

```
DETECT_INTENT

COLLECT_REQUIREMENTS

RESOLVE_PRODUCT

RESOLVE_VARIANT

CHECK_AVAILABILITY

COLLECT_ADDRESS

CALCULATE_PRICING

REVIEW_ORDER

CONFIRM_ORDER

CREATE_ORDER

ORDER_CONFIRMED
```

The current workflow state determines how the next message will be interpreted.

---

# Idempotency

Messages are processed sequentially within a conversation.

Repeated requests may produce different results depending on the current workflow state.

Clients should avoid retrying conversational messages without user confirmation.

---

# Versioning

Current API version

```
v1
```

Future versions may introduce

```
/api/v2/chat
```

without breaking existing integrations.

---

# Future Endpoints

The architecture supports additional APIs such as

```
POST /orders

GET /orders/{order_id}

GET /orders/{order_id}/status

POST /orders/{order_id}/cancel

GET /products

GET /categories

GET /customers/{customer_id}

POST /payments
```

These endpoints will complement, rather than replace, the conversational interface.

---

# API Design Principles

The API follows these principles.

## Conversation First

The chatbot is the primary interface.

---

## Stateless HTTP

Each HTTP request is independent.

Conversation continuity is reconstructed from the persisted Order Draft.

---

## Workflow Driven

The workflow engine determines the business operation.

Clients never invoke internal workflow states directly.

---

## Consistent Responses

Every successful response follows the same structure.

```json
{
    "success": true,
    "message": "...",
    "current_state": "...",
    "next_state": "...",
    "review": null,
    "order_id": null
}
```

---

# Summary

The API exposes a conversational interface that abstracts the complexity of product selection, inventory validation, pricing, and checkout.

Clients communicate through natural language messages while the backend workflow engine orchestrates deterministic business operations and maintains conversational continuity through the Order Draft.
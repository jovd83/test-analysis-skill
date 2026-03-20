# POS Checkout Flow

## Scope

Store associate completes a retail checkout in a point-of-sale application.

## Primary Actor

Store Associate

## Preconditions

- Associate is logged in.
- Register is online.
- Customer presents items for purchase.

## Main Flow

1. Associate opens a new sale.
2. Associate scans each item.
3. System adds each item to the basket and shows price, tax, and subtotal.
4. Associate optionally applies a discount code.
5. System recalculates totals.
6. Customer chooses payment method.
7. Associate captures payment.
8. System records the sale and updates inventory.
9. System prints or emails a receipt.

## Alternative Flows

### A1. Barcode does not scan

1. System shows a scan failure message.
2. Associate manually enters the item code.

### A2. Payment authorization times out

1. System shows an error message.
2. Associate retries payment.

### A3. Manager override is required

1. System prompts for override.
2. Manager approves the override.
3. Associate resumes checkout.

## Special Requirements

- Checkout should be fast.
- The system should support tax-exempt customers.
- The system should continue safely after a crash.
- The receipt should show loyalty balance.

## Known Gaps In This Draft

- No rule explains when a manager override is required.
- Tax-exempt validation is not described.
- Crash recovery is mentioned but not defined.
- Loyalty balance is shown on the receipt but no calculation or source is specified.

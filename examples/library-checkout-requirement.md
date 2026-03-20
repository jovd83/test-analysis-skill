# Library Checkout Flow

## Scope

Librarian checks out books to a member in a library management system.

## Preconditions

- Librarian is logged in.
- Member exists in the system or can be searched manually.

## Main Flow

1. Librarian starts a checkout session.
2. Librarian identifies the member.
3. System displays member status.
4. Librarian scans books.
5. System applies due dates and any late fees.
6. Librarian confirms checkout.
7. System updates the borrowing record.
8. System generates a receipt.

## Alternative Flows

### A1. Member cannot present a library card

1. Librarian searches by name and identification.

### A2. Book barcode is damaged

1. Librarian enters the book ID manually.

### A3. Printer is unavailable

1. Librarian writes the receipt manually.

## Special Requirements

- System response should stay under one second.
- Receipt should include loyalty points.
- System should support multilingual interfaces.
- Book recommendations should be available for the member.

## Draft Issues

- The rule for late fees is not defined.
- Loyalty points are mentioned but not calculated anywhere.
- Book recommendations are listed but not connected to the flow.
- No override path exists when borrowing limits are reached.

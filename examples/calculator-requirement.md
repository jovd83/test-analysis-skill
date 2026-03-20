# Calculator Application

## Scope

User performs a basic calculation in a calculator application.

## Preconditions

- Application is open.
- Calculator starts in standard mode with zero displayed.

## Main Flow

1. User enters the first number.
2. User selects an operation.
3. User enters the second number.
4. User presses equals.
5. System computes the result.
6. System displays the result.

## Alternative Flows

### A1. User clears the calculation

1. System resets the current input.

### A2. User divides by zero

1. System shows an error.
2. User can correct the input or clear the calculation.

## Special Requirements

- Response time must stay under 0.1 seconds.
- Display must be readable in different lighting conditions.
- History is updated if enabled.
- Voice input may be supported.

## Draft Issues

- History behavior is not defined.
- Voice input is mentioned but not connected to the flow.
- The overflow behavior is not specified.

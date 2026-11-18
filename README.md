# RideCompare

RideCompare is a simple page for planning a journey and comparing ride estimates. It currently provides a responsive form for entering a pickup location and destination.

## Features

### Journey input form

The journey form includes:

- Required pickup location and destination fields
- A 200-character limit for each location
- Address-friendly browser autocomplete
- A clear route layout with pickup and destination markers
- A continue button and inline validation guidance

The browser checks that both locations are filled in before the form can be submitted.

### Responsive and accessible design

- Adapts to desktop and mobile screen sizes
- Uses visible labels for both location fields
- Includes a clear keyboard focus state for controls
- Honors the visitor's reduced-motion preference
- Uses semantic page sections and an accessible brand link

## Project structure

```text
.
├── index.html  # Page structure and journey form
├── style.css   # Layout, colors, responsiveness, and interactions
└── README.md   # Project documentation
```

## Run locally

1. Download or clone this repository.
2. Open `index.html` in a web browser.

The page uses plain HTML and CSS and does not require a build step or any dependencies.

## Browser validation

The form currently relies on built-in browser validation:

- Leaving either location empty prevents submission.
- The pickup and destination inputs accept no more than 200 characters.

There is no JavaScript form submission or ride-estimate calculation yet.

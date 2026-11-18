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

## Journey form behavior

The user starts by entering a pickup location and destination:

1. Enter the pickup location in the first field.
2. Enter the destination in the second field.
3. Use the **Continue** button after both fields pass browser validation.

Example values:

```text
Pickup: King's Cross Station
Destination: London Bridge
```

At the moment, the form is a front-end entry step only. It does not send the locations to a server or calculate or compare ride prices.

## Customizing the form

You can update the journey fields in `index.html`:

- Change placeholder text by editing the `placeholder` attributes.
- Change the character limit by editing the `maxlength` attributes.
- Make the fields optional by removing `required`.
- Update field names or labels to fit your application.

Colors and visual spacing can be changed in `style.css`. The main page background, brand color, and card color are defined near the top of the file.

## Planned enhancements

Possible future additions include:

- JavaScript form submission
- Pickup and destination address validation
- Taxi and ride-provider price estimates
- Journey distance and travel-time calculations
- Loading, error, and no-results states
- Saved and recently used locations

## Contributing

Contributions are welcome. When extending the journey form, keep the following in mind:

- Preserve labels and browser validation for accessible input
- Check layouts on both mobile and desktop widths
- Preserve keyboard focus and reduced-motion support
- Update this README when new behavior is added

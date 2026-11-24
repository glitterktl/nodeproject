# RideCompare

RideCompare is a simple page for planning a journey and comparing ride estimates. It currently provides a responsive form for entering a pickup location and destination.

## Features

### Journey input form

The journey form includes:

- Pickup location and destination fields
- A submit button
- Server-side checks that reject missing or whitespace-only locations

The `/prepare_route` endpoint trims both values and returns HTTP 400 if either one is empty.

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

1. Open a terminal in the `node project car` folder.
2. Activate the virtual environment with `source .venv/bin/activate`.
3. Install dependencies with `python -m pip install -r requirements.txt`.
4. Start Flask with `python app.py`.
5. Open `http://127.0.0.1:5000` in a browser.

The Flask app serves the `index.html` form from the repository folder above.

## Form submission and validation

Flask's `/prepare_route` endpoint reads the `pickup` and `dropoff` form fields
and trims surrounding whitespace. If either value is empty, the endpoint
returns HTTP 400 with a message asking for both locations. Otherwise, it formats
the addresses as a Google Routes request body and logs that JSON on the server.
The request is not sent to Google, and this endpoint does not calculate a fare.

Validation currently happens on the server, not in the browser. The form in
`index.html` currently posts to `/compare-prices`; set its action to
`/prepare_route` for submissions from the page to reach this validation handler.

## Journey form behavior

The user starts by entering a pickup location and destination:

1. Enter the pickup location in the first field.
2. Enter the destination in the second field.
3. Use the submit button to send both locations.
4. If either location is blank or contains only spaces, the server rejects the
   submission with a validation message.

Example values:

```text
Pickup: King's Cross Station
Destination: London Bridge
```

The `/prepare_route` endpoint formats the locations for a Google Routes request
but does not send that request or calculate or compare ride prices.

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

- Preserve labels and server-side validation for required locations
- Check layouts on both mobile and desktop widths
- Preserve keyboard focus and reduced-motion support
- Update this README when new behavior is added

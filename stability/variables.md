# Session Variables Documentation

The session data is used for accessing data variables throughout the modules. This enables the use of global variables and retains memory for critical data, such as the car components. Below is a list of the session variables created and their purposes:

## Session Variables

- **`request.session['angle']`**:

  - **Description**: The chassis rotation theta.

- **`request.session['max_rotation']`**:

  - **Description**: The maximum rotation of the chassis, dependent on the suspension geometry.

- **`request.session['table_data']`**:

  - **Description**: The car components for calculating the gravity center.

- **`request.session['gravity_center_val']`**:

  - **Description**: The value of the gravity center.

- **`request.session['total_mass']`**:

  - **Description**: The total mass of the car.

- **`request.session['roll_center']`**:

  - **Description**: The value of the roll center.

- **`request.session['D']`**:

  - **Description**: The width of the car, used for rotation calculations when rounding a curve.

- **`request.session['object_data']`**:

  - **Description**: The system's data geometry.

- **`request.session['distance']`**:
  - **Description**: The distance between the roll center and the gravity center.

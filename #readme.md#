# How to Deploy the App Locally

## Requirements Installation

To install the required dependencies, run the following command:

```bash
pip install -r requirements.txt
```

## Running the Server

Navigate to the project's folder and start the Django server using:

```bash
py manage.py runserver
```

The server will be running at:

- `http://127.0.0.1:8000/`

## The applications will be in the routes:

- **Stability App:** `http://127.0.0.1:8000/stability/`
- **Spring Ultimate Tensile Strength (UTS) App:** `http://127.0.0.1:8000/springUTS/`

---

# How to Use Spring Ultimate Tensile Strength (UTS) App

This app analyzes the increase in ultimate tensile strength (UTS) and fatigue limit when a spring is made of a specific material. It also shows the factor of increase in those properties and the stress absorbed by the spring.

The app requires the material's physical properties and the spring's geometry.

# How to Use Stability App

This app consists of three parts:

## Generate Chassis Analysis

This part displays the suspension diagram with the positions of the roll center and center of gravity. It also shows the maximum roll angle and the distance between the roll center and center of gravity.

This analysis requires the geometry of the suspension and car components.

## Compute Maximum Velocity for a Curve

This part calculates the maximum velocity the car can maintain before rolling over in a curve.

It requires the distance from the roll center to the center of gravity and the radius of the curve.

## Compute Chassis Rotation

This part calculates the chassis rotation when rounding a curve due to centrifugal force.

It requires the car's velocity, the radius of the curve, and the suspension's roll stiffness.

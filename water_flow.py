# Constants
EARTH_ACCELERATION_OF_GRAVITY = 9.8066500  # m/s^2
WATER_DENSITY = 998.2000000  # kg/m^3
WATER_DYNAMIC_VISCOSITY = 0.0010016  # Pa·s
KPA_TO_PSI_CONVERSION_FACTOR = 0.1450377  # 1 kPa = 0.1450377 psi

PVC_SCHED80_INNER_DIAMETER = 0.28687  # meters (11.294 inches)
PVC_SCHED80_FRICTION_FACTOR = 0.013  # unitless
SUPPLY_VELOCITY = 1.65  # meters/second

HDPE_SDR11_INNER_DIAMETER = 0.048692  # meters (1.917 inches)
HDPE_SDR11_FRICTION_FACTOR = 0.018  # unitless
HOUSEHOLD_VELOCITY = 1.75  # meters/second


def water_column_height(tower_height, tank_height):
    """Calculate the height of the water column."""
    h = tower_height + (3 * tank_height) / 4
    return h


def pressure_gain_from_water_height(height):
    """Calculate the pressure from the height of the water column."""
    P = (WATER_DENSITY * EARTH_ACCELERATION_OF_GRAVITY * height) / 1000  # pressure in kilopascals
    return P


def pressure_loss_from_pipe(pipe_diameter, pipe_length, friction_factor, fluid_velocity):
    """Calculate the pressure loss in the pipe due to friction."""
    P = - (friction_factor * pipe_length * WATER_DENSITY * fluid_velocity**2) / (2000 * pipe_diameter)
    return P


def pressure_loss_from_fittings(fluid_velocity, quantity_fittings):
    """Calculate the pressure loss from fittings."""
    p = (-0.04 * WATER_DENSITY * fluid_velocity**2 * quantity_fittings) / 2000
    return p


def reynolds_number(hydraulic_diameter, fluid_velocity):
    """Calculate the Reynolds number for flow in a pipe."""
    R = (WATER_DENSITY * hydraulic_diameter * fluid_velocity) / WATER_DYNAMIC_VISCOSITY
    return R


def pressure_loss_from_pipe_reduction(larger_diameter, fluid_velocity, reynolds_number, smaller_diameter):
    """Calculate the pressure loss due to a reduction in pipe diameter."""
    k = (0.1 + (50 / reynolds_number)) * (((larger_diameter / smaller_diameter) ** 4) - 1)
    p = (-k * WATER_DENSITY * (fluid_velocity ** 2)) / 2000
    return p


def kPa_to_psi(kPa):
    """Convert pressure from kPa to psi."""
    return kPa * KPA_TO_PSI_CONVERSION_FACTOR


def main():
    tower_height = float(input("Height of water tower (meters): "))
    tank_height = float(input("Height of water tank walls (meters): "))
    length1 = float(input("Length of supply pipe from tank to lot (meters): "))
    quantity_angles = int(input("Number of 90° angles in supply pipe: "))
    length2 = float(input("Length of pipe from supply to house (meters): "))

    # Calculate the water height and pressure gain
    water_height = water_column_height(tower_height, tank_height)
    pressure_kPa = pressure_gain_from_water_height(water_height)

    # First pipe (PVC)
    diameter = PVC_SCHED80_INNER_DIAMETER
    friction = PVC_SCHED80_FRICTION_FACTOR
    velocity = SUPPLY_VELOCITY
    reynolds = reynolds_number(diameter, velocity)  # Calculate Reynolds number for PVC
    loss = pressure_loss_from_pipe(diameter, length1, friction, velocity)
    pressure_kPa += loss  # Add the pressure loss from the first pipe
    loss = pressure_loss_from_fittings(velocity, quantity_angles)
    pressure_kPa += loss  # Add the pressure loss from fittings

    # Pipe reduction (PVC to HDPE)
    loss = pressure_loss_from_pipe_reduction(diameter, velocity, reynolds, HDPE_SDR11_INNER_DIAMETER)
    pressure_kPa += loss  # Add the pressure loss from the pipe reduction

    # Second pipe (HDPE)
    diameter = HDPE_SDR11_INNER_DIAMETER
    friction = HDPE_SDR11_FRICTION_FACTOR
    velocity = HOUSEHOLD_VELOCITY
    loss = pressure_loss_from_pipe(diameter, length2, friction, velocity)
    pressure_kPa += loss  # Add the pressure loss from the second pipe

    # Convert kPa to psi
    pressure_psi = kPa_to_psi(pressure_kPa)

    print(f"Pressure at house: {pressure_kPa:.1f} kPa")
    print(f"Pressure at house: {pressure_psi:.1f} psi")


if __name__ == "__main__":
    main()

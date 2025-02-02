from pytest import approx
import pytest
from water_flow import (
    water_column_height,
    pressure_gain_from_water_height,
    pressure_loss_from_pipe,
    pressure_loss_from_fittings,
    reynolds_number,
    pressure_loss_from_pipe_reduction,
    kPa_to_psi,  # Import the conversion function
)

# Test water_column_height function
def test_water_column_height():
    assert water_column_height(0.0, 0.0) == 0.0
    assert water_column_height(0.0, 10.0) == approx(7.5, rel=1e-9)
    assert water_column_height(25.0, 0.0) == 25.0
    assert water_column_height(48.3, 12.8) == approx(57.9, rel=1e-9)

# Test pressure_gain_from_water_height function
def test_pressure_gain_from_water_height():
    assert pressure_gain_from_water_height(0.0) == approx(0.000, rel=0.001)
    assert pressure_gain_from_water_height(30.2) == approx(295.628, rel=0.001)
    assert pressure_gain_from_water_height(50.0) == approx(489.450, rel=0.001)

# Test pressure_loss_from_pipe function
def test_pressure_loss_from_pipe():
    assert pressure_loss_from_pipe(0.048692, 0.0, 0.018, 1.75) == approx(0.000, rel=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.000, 1.75) == approx(0.000, rel=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 1.75) == approx(-113.008, rel=0.001)
    assert pressure_loss_from_pipe(0.048692, 200.0, 0.018, 1.65) == approx(-100.462, rel=0.001)
    assert pressure_loss_from_pipe(0.286870, 1000.0, 0.013, 1.65) == approx(-61.576, rel=0.001)
    assert pressure_loss_from_pipe(0.286870, 1800.75, 0.013, 1.65) == approx(-110.884, rel=0.001)

# Test pressure_loss_from_fittings function
def test_pressure_loss_from_fittings():
    assert pressure_loss_from_fittings(0.00, 3) == approx(0.000, abs=0.001)
    assert pressure_loss_from_fittings(1.65, 0) == approx(0.000, abs=0.001)
    assert pressure_loss_from_fittings(1.65, 2) == approx(-0.109, abs=0.001)
    assert pressure_loss_from_fittings(1.75, 2) == approx(-0.122, abs=0.001)
    assert pressure_loss_from_fittings(1.75, 5) == approx(-0.306, abs=0.001)

# Test reynolds_number function
def test_reynolds_number():
    assert reynolds_number(0.048692, 0.00) == approx(0, abs=1)
    assert reynolds_number(0.048692, 1.65) == approx(80069, abs=1)
    assert reynolds_number(0.048692, 1.75) == approx(84922, abs=1)
    assert reynolds_number(0.286870, 1.65) == approx(471729, abs=1)
    assert reynolds_number(0.286870, 1.75) == approx(500318, abs=1)

# Test pressure_loss_from_pipe_reduction function
def test_pressure_loss_from_pipe_reduction():
    assert pressure_loss_from_pipe_reduction(0.28687, 0.000, 1, 0.048692) == approx(0.000, abs=0.001)
    assert pressure_loss_from_pipe_reduction(0.28687, 1.65, 471729, 0.048692) == approx(-163.744, abs=0.001)
    assert pressure_loss_from_pipe_reduction(0.28687, 1.75, 500318, 0.048692) == approx(-184.182, abs=0.001)

# Test kPa to psi conversion function
def test_kPa_to_psi():
    # Testing known values
    assert kPa_to_psi(0.0) == approx(0.0, abs=1e-9)
    assert kPa_to_psi(1.0) == approx(0.1450377, abs=1e-7)
    assert kPa_to_psi(100.0) == approx(14.50377, abs=1e-5)
    assert kPa_to_psi(10.0) == approx(1.450377, abs=1e-6)
    assert kPa_to_psi(200.0) == approx(29.00754, abs=1e-5)

# Call pytest's main function to run the tests
pytest.main(["-v", "--tb=line", "-rN", __file__])

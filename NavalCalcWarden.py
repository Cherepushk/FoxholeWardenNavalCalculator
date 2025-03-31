import streamlit as st
import numpy as np
import math
import pyperclip

# Set the page title
st.set_page_config(page_title="Naval Artillery Calculator", layout="wide")

# Initialize session state for navigation
if 'calculator_type' not in st.session_state:
    st.session_state.calculator_type = "main_menu"

# Function to convert degrees to radians
def to_radians(degrees):
    return degrees * math.pi / 180

# Function to convert radians to degrees
def to_degrees(radians):
    return radians * 180 / math.pi

# Function to calculate artillery coordinates
def calculate_artillery_coordinates(ship_azimuth, commander_distance, commander_azimuth, wind_azimuth, wind_strength):
    # Step 1: Calculate target coordinates with wind adjustment
    x0 = 1000 + (math.cos(to_radians(commander_azimuth)) * commander_distance) - (math.cos(to_radians(wind_azimuth)) * wind_strength)
    y0 = 1000 + (math.sin(to_radians(commander_azimuth)) * commander_distance) - (math.sin(to_radians(wind_azimuth)) * wind_strength)
    
    # Step 2: Calculate gun positions based on ship azimuth
    # First gun
    x1 = 1000 + (-1 * (math.cos(to_radians(ship_azimuth)) * 6.4))
    y1 = 1000 + (-1 * (math.sin(to_radians(ship_azimuth)) * 6.4))
    
    # Second gun
    x2 = 1000 + (-1 * (math.cos(to_radians(ship_azimuth)) * 19.8))
    y2 = 1000 + (-1 * (math.sin(to_radians(ship_azimuth)) * 19.8))
    
    # Step 3: Calculate differences between guns and target
    dx1 = x0 - x1
    dy1 = y0 - y1
    dx2 = x0 - x2
    dy2 = y0 - y2
    
    # Step 4: Calculate bearing (rumb) for each gun
    # First gun bearing
    if dx1 != 0:  # Prevent division by zero
        angle1 = to_degrees(math.atan(dy1 / dx1))
        r1 = abs(angle1) if angle1 >= 0 else abs(angle1)
    else:
        r1 = 90 if dy1 > 0 else 270
    
    # Second gun bearing
    if dx2 != 0:  # Prevent division by zero
        angle2 = to_degrees(math.atan(dy2 / dx2))
        r2 = abs(angle2) if angle2 >= 0 else abs(angle2)
    else:
        r2 = 90 if dy2 > 0 else 270
    
    # Step 5: Calculate final azimuth for each gun
    # First gun azimuth
    if dy1 > 0 and dx1 > 0:
        A1 = r1
    elif dy1 > 0 and dx1 < 0:
        A1 = 180 - r1
    elif dy1 < 0 and dx1 < 0:
        A1 = 180 + r1
    else:  # dy1 < 0 and dx1 > 0
        A1 = 360 - r1
    
    # Second gun azimuth
    if dy2 > 0 and dx2 > 0:
        A2 = r2
    elif dy2 > 0 and dx2 < 0:
        A2 = 180 - r2
    elif dy2 < 0 and dx2 < 0:
        A2 = 180 + r2
    else:  # dy2 < 0 and dx2 > 0
        A2 = 360 - r2
    
    # Step 6: Calculate distance for each gun
    d1 = math.sqrt(dx1**2 + dy1**2)
    d2 = math.sqrt(dx2**2 + dy2**2)
    
    # Step 7: Check if gun 1 can fire (firing angle constraints)
    left = ship_azimuth - 30
    if left < 0:
        left = ship_azimuth + 330
    
    right = ship_azimuth + 30
    if right > 360:
        right = ship_azimuth - 330
    
    # Determine if gun 1 can fire
    if left < right:
        s1 = 0 if (A1 > left and A1 < right) else 1
    else:
        s1 = 1 if (A1 < left and A1 > right) else 0
    
    # If s1 = 0, set A1 to "No angle"
    if s1 == 0:
        A1_display = "No angle"
    else:
        A1_display = round(A1, 1)
        
    # Round results to one decimal place
    d1 = round(d1, 1)
    A2 = round(A2, 1)
    d2 = round(d2, 1)
    
    return A1_display, d1, A2, d2

# Function to calculate artillery coordinates for CalahanBS
def calculate_calahan_artillery_coordinates(ship_azimuth, commander_distance, commander_azimuth, wind_azimuth, wind_strength):
    # Step 1: Calculate target coordinates with wind adjustment
    x0 = 1000 + (math.cos(to_radians(commander_azimuth)) * commander_distance) - (math.cos(to_radians(wind_azimuth)) * wind_strength)
    y0 = 1000 + (math.sin(to_radians(commander_azimuth)) * commander_distance) - (math.sin(to_radians(wind_azimuth)) * wind_strength)
    
    # Step 2: Calculate gun positions based on ship azimuth
    # Front gun
    x1 = 1000 + (math.cos(to_radians(ship_azimuth)) * 11)
    y1 = 1000 + (math.sin(to_radians(ship_azimuth)) * 11)
    
    # Middle gun
    x2 = 1000 + (-1 * (math.cos(to_radians(ship_azimuth)) * 11))
    y2 = 1000 + (-1 * (math.sin(to_radians(ship_azimuth)) * 11))
    
    # Rear gun
    x3 = 1000 + (-1 * (math.cos(to_radians(ship_azimuth)) * 26))
    y3 = 1000 + (-1 * (math.sin(to_radians(ship_azimuth)) * 26))
    
    # Step 3: Calculate differences between guns and target
    dx1 = x0 - x1
    dy1 = y0 - y1
    dx2 = x0 - x2
    dy2 = y0 - y2
    dx3 = x0 - x3
    dy3 = y0 - y3
    
    # Step 4: Calculate bearing (rumb) for each gun
    # Front gun bearing
    if dx1 != 0:  # Prevent division by zero
        angle1 = to_degrees(math.atan(dy1 / dx1))
        r1 = abs(angle1) if angle1 >= 0 else abs(angle1)
    else:
        r1 = 90 if dy1 > 0 else 270
    
    # Middle gun bearing
    if dx2 != 0:  # Prevent division by zero
        angle2 = to_degrees(math.atan(dy2 / dx2))
        r2 = abs(angle2) if angle2 >= 0 else abs(angle2)
    else:
        r2 = 90 if dy2 > 0 else 270
    
    # Rear gun bearing
    if dx3 != 0:  # Prevent division by zero
        angle3 = to_degrees(math.atan(dy3 / dx3))
        r3 = abs(angle3) if angle3 >= 0 else abs(angle3)
    else:
        r3 = 90 if dy3 > 0 else 270
    
    # Step 5: Calculate final azimuth for each gun
    # Front gun azimuth
    if dy1 > 0 and dx1 > 0:
        A1 = r1
    elif dy1 > 0 and dx1 < 0:
        A1 = 180 - r1
    elif dy1 < 0 and dx1 < 0:
        A1 = 180 + r1
    else:  # dy1 < 0 and dx1 > 0
        A1 = 360 - r1
    
    # Middle gun azimuth
    if dy2 > 0 and dx2 > 0:
        A2 = r2
    elif dy2 > 0 and dx2 < 0:
        A2 = 180 - r2
    elif dy2 < 0 and dx2 < 0:
        A2 = 180 + r2
    else:  # dy2 < 0 and dx2 > 0
        A2 = 360 - r2
    
    # Rear gun azimuth
    if dy3 > 0 and dx3 > 0:
        A3 = r3
    elif dy3 > 0 and dx3 < 0:
        A3 = 180 - r3
    elif dy3 < 0 and dx3 < 0:
        A3 = 180 + r3
    else:  # dy3 < 0 and dx3 > 0
        A3 = 360 - r3
    
    # Step 6: Calculate distance for each gun
    d1 = math.sqrt(dx1**2 + dy1**2)
    d2 = math.sqrt(dx2**2 + dy2**2)
    d3 = math.sqrt(dx3**2 + dy3**2)
    
    # Step 7: Check firing angle constraints for each gun
    # Front gun constraints
    left1 = ship_azimuth - 135
    if left1 < 0:
        left1 = ship_azimuth + 225
    
    right1 = ship_azimuth + 135
    if right1 > 360:
        right1 = ship_azimuth - 225
    
    # Middle and Rear gun constraints (they are the same)
    left2 = ship_azimuth - 45
    if left2 < 0:
        left2 = ship_azimuth + 315
    
    right2 = ship_azimuth + 45
    if right2 > 360:
        right2 = ship_azimuth - 315
    
    # Determine if guns can fire based on angle constraints
    # Front gun
    if left1 < right1:
        s1 = 1 if (A1 > left1 and A1 < right1) else 0
    else:
        s1 = 0 if (A1 < left1 and A1 > right1) else 1
    
    # Middle gun - проверяем, попадает ли азимут в диапазон ограничений
    if left2 < right2:
        s2 = 0 if (A2 >= left2 and A2 <= right2) else 1
    else:
        s2 = 0 if (A2 >= left2 or A2 <= right2) else 1
    
    # Rear gun - проверяем, попадает ли азимут в диапазон ограничений
    if left2 < right2:
        s3 = 0 if (A3 >= left2 and A3 <= right2) else 1
    else:
        s3 = 0 if (A3 >= left2 or A3 <= right2) else 1
    
    # Apply "No angle" if gun can't fire
    if s1 == 0:
        A1_display = "No angle"
    else:
        A1_display = round(A1, 1)
        
    if s2 == 0:
        A2_display = "No angle"
    else:
        A2_display = round(A2, 1)
        
    if s3 == 0:
        A3_display = "No angle"
    else:
        A3_display = round(A3, 1)
    
    # Round distances to one decimal place
    d1 = round(d1, 1)
    d2 = round(d2, 1)
    d3 = round(d3, 1)
    
    return A1_display, d1, A2_display, d2, A3_display, d3

# Function to calculate wind parameters based on shell landing point
def calculate_wind_parameters(ship_azimuth, commander_azimuth, commander_distance, 
                              explosion_azimuth, explosion_distance):
    # For Frigate, we use gun 2 as reference
    # For CalahanBS, we should use the middle gun (gun 2) as reference
    # Since the calculation is the same principle, we'll use the same function for both
    
    # Calculate gun position (using gun 2 as a reference)
    if st.session_state.calculator_type == "frigate":
        # For Frigate, gun 2 is at -19.8 distance
        x2 = 1000 + (-1 * (math.cos(to_radians(ship_azimuth)) * 19.8))
        y2 = 1000 + (-1 * (math.sin(to_radians(ship_azimuth)) * 19.8))
    else:
        # For CalahanBS, the middle gun (gun 2) is at -11 distance
        x2 = 1000 + (-1 * (math.cos(to_radians(ship_azimuth)) * 11))
        y2 = 1000 + (-1 * (math.sin(to_radians(ship_azimuth)) * 11))
    
    # Calculate expected shell landing coordinates
    xm = x2 + (math.cos(to_radians(commander_azimuth)) * commander_distance)
    ym = y2 + (math.sin(to_radians(commander_azimuth)) * commander_distance)
    
    # Calculate actual shell landing coordinates
    xf = 1000 + (math.cos(to_radians(explosion_azimuth)) * explosion_distance)
    yf = 1000 + (math.sin(to_radians(explosion_azimuth)) * explosion_distance)
    
    # Calculate difference
    dxv = xf - xm
    dyv = yf - ym
    
    # Calculate wind azimuth
    if dxv != 0:  # Prevent division by zero
        angle_v = to_degrees(math.atan(dyv / dxv))
        rv = abs(angle_v) if angle_v >= 0 else abs(angle_v)
    else:
        rv = 90 if dyv > 0 else 270
    
    # Calculate final wind azimuth
    if dyv > 0 and dxv > 0:
        Av = rv
    elif dyv > 0 and dxv < 0:
        Av = 180 - rv
    elif dyv < 0 and dxv < 0:
        Av = 180 + rv
    else:  # dyv < 0 and dxv > 0
        Av = 360 - rv
    
    # Calculate wind strength
    dv = math.sqrt(dxv**2 + dyv**2)
    # Round wind strength to nearest 10
    dv = round(dv / 10) * 10
    
    return Av, dv

# Function to display the main menu
def show_main_menu():
    st.title("Naval Artillery Calculator")
    st.write("Select a ship type to calculate artillery coordinates.")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Frigate Calculator", use_container_width=True):
            st.session_state.calculator_type = "frigate"
            st.rerun()
    
    with col2:
        if st.button("CalahanBS Calculator", use_container_width=True):
            st.session_state.calculator_type = "calahan"
            st.rerun()
    
    # Tips for use section
    st.markdown("---")
    st.subheader("Tips for use")
    st.write("""
    This calculator is for artillery calculations on Warden navy ships. It is assumed that it will not be used by the ship's captain, but rather by a mechanic, driver, or other more relaxed crew member. You also can copy results and paste into game squad chat, so guns crew will see it.

    In order for the calculator to calculate as accurately as possible, it is necessary to take into account the wind parameters well. There is a wind calculation function for this. How it works: the commander finds the aiming point and names the distance and azimuth. The second gun (EXCLUSIVELY THE SECOND ONE)(On a frigate it is the rear, on a battleship it is the middle) sets exactly the parameters that the commander said. After that, the commander tells the distance and azimuth to the gap. These data are entered into the calculator and calculated (do not forget to transfer them to the wind parameters before the next calculation). Now, for the near future, until the wind changes, all your guns will hit exactly the target.

    If you use this calculator correctly, you can save time and shells, and you will be sniping targets.
    """)

# Function to display the CalahanBS calculator
def show_calahan_calculator():
    st.title("CalahanBS Artillery Calculator")
    
    # Add a back button at the top
    if st.button("Back to Main Menu"):
        st.session_state.calculator_type = "main_menu"
        st.rerun()
    
    st.write("This application calculates artillery coordinates for CalahanBS ship guns based on ship position, commander inputs, and wind conditions.")
    
    # Create two columns for input fields in the main section
    col1, col2 = st.columns(2)
    
    # Input fields for main calculation
    with col1:
        st.subheader("Ship and Commander Parameters")
        ship_azimuth = st.number_input("Ship Azimuth", min_value=0.0, max_value=360.0, value=0.0, step=0.1, format="%.1f", key="calahan_ship_azimuth")
        commander_distance = st.number_input("Commander Distance", min_value=0.0, value=100.0, step=0.1, format="%.1f", key="calahan_commander_distance")
        commander_azimuth = st.number_input("Commander Azimuth", min_value=0.0, max_value=360.0, value=0.0, step=0.1, format="%.1f", key="calahan_commander_azimuth")
    
    with col2:
        st.subheader("Wind Parameters")
        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)  # Small vertical space
        wind_azimuth = st.number_input("Wind Azimuth", min_value=0.0, max_value=360.0, value=0.0, step=0.1, format="%.1f", key="calahan_wind_azimuth_input")
        wind_strength = st.number_input("Wind Strength", min_value=0.0, value=0.0, step=0.1, format="%.1f", key="calahan_wind_strength_input")
    
    # Add a button to trigger calculation
    if st.button("Calculate Artillery Coordinates", key="calahan_calculate_button"):
        try:
            # Calculate coordinates
            A1, d1, A2, d2, A3, d3 = calculate_calahan_artillery_coordinates(
                ship_azimuth, 
                commander_distance, 
                commander_azimuth, 
                wind_azimuth, 
                wind_strength
            )
            
            # Display results
            st.subheader("Results")
            
            # Format results for each gun
            if A1 == "No angle":
                gun1_str = f"Front Gun: Azimuth (A1): {A1}, Distance (d1): {d1}"
            else:
                gun1_str = f"Front Gun: Azimuth (A1): {A1}°, Distance (d1): {d1}"
            
            if A2 == "No angle":
                gun2_str = f"Middle Gun: Azimuth (A2): {A2}, Distance (d2): {d2}"
            else:
                gun2_str = f"Middle Gun: Azimuth (A2): {A2}°, Distance (d2): {d2}"
            
            if A3 == "No angle":
                gun3_str = f"Rear Gun: Azimuth (A3): {A3}, Distance (d3): {d3}"
            else:
                gun3_str = f"Rear Gun: Azimuth (A3): {A3}°, Distance (d3): {d3}"
            
            # Combined results in one text area
            combined_result = f"{gun1_str}\n{gun2_str}\n{gun3_str}"
            result_container = st.text_area("Calculation Results:", value=combined_result, height=100)
                
        except Exception as e:
            st.error(f"An error occurred during calculation: {str(e)}")
            st.error("Please check your input values and try again.")
    
    # Add a separator
    st.markdown("---")
    st.subheader("Wind Direction and Strength Calculation")
    
    # Create two columns for wind calculation input fields
    wind_col1, wind_col2 = st.columns(2)
    
    with wind_col1:
        explosion_azimuth = st.number_input("Commander Azimuth to Explosion (Av)", min_value=0.0, max_value=360.0, value=0.0, step=0.1, format="%.1f", key="calahan_explosion_azimuth")
        explosion_distance = st.number_input("Commander Distance to Explosion (dv)", min_value=0.0, value=100.0, step=0.1, format="%.1f", key="calahan_explosion_distance")
    
    # Button to calculate wind parameters
    if st.button("Calculate Wind", key="calahan_calculate_wind_button"):
        try:
            # Calculate wind parameters (same function as for Frigate calculator)
            wind_azimuth_calc, wind_strength_calc = calculate_wind_parameters(
                ship_azimuth,
                commander_azimuth,
                commander_distance,
                explosion_azimuth,
                explosion_distance
            )
            
            # Round to 1 decimal place
            wind_azimuth_calc = round(wind_azimuth_calc, 1)
            
            # Display results
            st.subheader("Wind Calculation Results")
            wind_result = f"Wind Azimuth: {wind_azimuth_calc}°, Wind Strength: {wind_strength_calc}"
            st.text_area("Wind Parameters:", value=wind_result, height=80, key="calahan_wind_result")
            
            # Button to transfer wind parameters to main calculation
            if st.button("Transfer Data", key="calahan_transfer_data_button"):
                st.session_state.calahan_wind_azimuth_input = wind_azimuth_calc
                st.session_state.calahan_wind_strength_input = wind_strength_calc
                st.success("Wind data transferred to main calculation!")
                st.rerun()
                
        except Exception as e:
            st.error(f"An error occurred during wind calculation: {str(e)}")
            st.error("Please check your input values and try again.")

# Function to display the Frigate calculator
def show_frigate_calculator():
    st.title("Frigate Artillery Calculator")
    
    # Add a back button at the top
    if st.button("Back to Main Menu"):
        st.session_state.calculator_type = "main_menu"
        st.rerun()
    
    st.write("This application calculates artillery coordinates based on ship position, commander inputs, and wind conditions.")
    
    # Create two columns for input fields in the main section
    col1, col2 = st.columns(2)
    
    # Input fields for main calculation
    with col1:
        st.subheader("Ship and Commander Parameters")
        ship_azimuth = st.number_input("Ship Azimuth", min_value=0.0, max_value=360.0, value=0.0, step=0.1, format="%.1f")
        commander_distance = st.number_input("Commander Distance", min_value=0.0, value=100.0, step=0.1, format="%.1f")
        commander_azimuth = st.number_input("Commander Azimuth", min_value=0.0, max_value=360.0, value=0.0, step=0.1, format="%.1f")
    
    with col2:
        st.subheader("Wind Parameters")
        st.markdown("<div style='height: 35px;'></div>", unsafe_allow_html=True)  # Small vertical space
        wind_azimuth = st.number_input("Wind Azimuth", min_value=0.0, max_value=360.0, value=0.0, step=0.1, format="%.1f", key="wind_azimuth_input")
        wind_strength = st.number_input("Wind Strength", min_value=0.0, value=0.0, step=0.1, format="%.1f", key="wind_strength_input")
    
    # Add a button to trigger calculation
    if st.button("Calculate Artillery Coordinates"):
        try:
            # Calculate coordinates
            A1, d1, A2, d2 = calculate_artillery_coordinates(
                ship_azimuth, 
                commander_distance, 
                commander_azimuth, 
                wind_azimuth, 
                wind_strength
            )
            
            # Display results
            st.subheader("Results")
            
            # Format results for each gun
            if A1 == "No angle":
                gun1_str = f"Middle Gun: Azimuth (A1): {A1}, Distance (d1): {d1}"
            else:
                gun1_str = f"Middle Gun: Azimuth (A1): {A1}°, Distance (d1): {d1}"
                
            if A2 == "No angle":
                gun2_str = f"Rear Gun: Azimuth (A2): {A2}, Distance (d2): {d2}"
            else:
                gun2_str = f"Rear Gun: Azimuth (A2): {A2}°, Distance (d2): {d2}"
            
            # Combined results in one text area
            combined_result = f"{gun1_str}\n{gun2_str}"
            result_container = st.text_area("Calculation Results:", value=combined_result, height=100)
                
        except Exception as e:
            st.error(f"An error occurred during calculation: {str(e)}")
            st.error("Please check your input values and try again.")
    
    # Add a separator
    st.markdown("---")
    st.subheader("Wind Direction and Strength Calculation")
    
    # Create two columns for wind calculation input fields
    wind_col1, wind_col2 = st.columns(2)
    
    with wind_col1:
        explosion_azimuth = st.number_input("Commander Azimuth to Explosion (Av)", min_value=0.0, max_value=360.0, value=0.0, step=0.1, format="%.1f")
        explosion_distance = st.number_input("Commander Distance to Explosion (dv)", min_value=0.0, value=100.0, step=0.1, format="%.1f")
    
    # Button to calculate wind parameters
    if st.button("Calculate Wind"):
        try:
            # Calculate wind parameters
            wind_azimuth_calc, wind_strength_calc = calculate_wind_parameters(
                ship_azimuth,
                commander_azimuth,
                commander_distance,
                explosion_azimuth,
                explosion_distance
            )
            
            # Round to 1 decimal place
            wind_azimuth_calc = round(wind_azimuth_calc, 1)
            
            # Display results
            st.subheader("Wind Calculation Results")
            wind_result = f"Wind Azimuth: {wind_azimuth_calc}°, Wind Strength: {wind_strength_calc}"
            st.text_area("Wind Parameters:", value=wind_result, height=80)
            
            # Button to transfer wind parameters to main calculation
            if st.button("Transfer Data"):
                st.session_state.wind_azimuth_input = wind_azimuth_calc
                st.session_state.wind_strength_input = wind_strength_calc
                st.success("Wind data transferred to main calculation!")
                st.rerun()
                
        except Exception as e:
            st.error(f"An error occurred during wind calculation: {str(e)}")
            st.error("Please check your input values and try again.")

# Display the appropriate calculator based on the session state
if st.session_state.calculator_type == "main_menu":
    show_main_menu()
elif st.session_state.calculator_type == "frigate":
    show_frigate_calculator()
elif st.session_state.calculator_type == "calahan":
    show_calahan_calculator()

# Add footer information
st.markdown("---")
st.markdown("Naval Artillery Calculator - For simulation purposes only")
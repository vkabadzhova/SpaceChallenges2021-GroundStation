import numpy as np

satellite_velocity = 7.8 # [km/s]
max_altitude = 2500 # [km]
min_altitude = 500 # [km]
earth_radius = 6371.009 # [km]

def main():
    central_angle = 2 * np.arctan( max_altitude / earth_radius ) # [radians]
    arc_length = ( earth_radius + min_altitude ) * central_angle
    contact_time = arc_length / satellite_velocity  # [s]
    average_angular_velocity = 180 / contact_time 

    print( "Min angular velocity: %.2f" % ( average_angular_velocity ))

if __name__ == "__main__":
    main()

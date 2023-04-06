# From the Meep tutorial: plotting permittivity and fields of a straight waveguide
import meep as mp
import matplotlib.pyplot as plt
import numpy as np

METERS_TO_MICROMETERS = 1E6

wavelength = 1.55E-6 * METERS_TO_MICROMETERS
pml_thickness = 1E-6 * METERS_TO_MICROMETERS

# Draw the bend
thickness_cladding = 3E-6 * METERS_TO_MICROMETERS
thickness_silicon = 0.22E-6 * METERS_TO_MICROMETERS
thickness_silicon = mp.inf
thickness_buried_oxide = 2E-6 * METERS_TO_MICROMETERS
thickness_slab = 0 # for strip waveguide
#thickness_slab = 0.09E-6 # for rib waveguide
width_ridge = 0.5E-6 * METERS_TO_MICROMETERS

# Define materials
material_cladding = 3.9 # SiO2 (Glass)
material_buried_oxide = 3.9 # SiO2 (Glass)
material_silicon_dioxide = 3.9 # SiO2 (Glass)
material_silicon = 11.7 # Si (Silicon)
material_vacuum = 1

extra = 0.5E-6 * METERS_TO_MICROMETERS
thickness_margin = 500E-9 * METERS_TO_MICROMETERS
width_margin = 2E-6 * METERS_TO_MICROMETERS
length_input = 5E-6 * METERS_TO_MICROMETERS

bend_radius = 5E-6 * METERS_TO_MICROMETERS
bend_outer_radius = bend_radius + width_ridge / 2
bend_inner_radius = bend_radius - width_ridge / 2

x_min = 0 - width_ridge / 2 - width_margin
x_max = bend_radius + length_input
z_min = -thickness_margin
z_max = thickness_silicon + thickness_margin
y_min = 0
y_max = bend_radius + width_ridge / 2 + width_margin + length_input

print("x_min " + str(x_min))
print("x_max " + str(x_max))
print("y_min " + str(y_min))
print("y_max " + str(y_max))

input_waveguide_size_vector = mp.Vector3(width_ridge,
	(length_input + width_margin),
	thickness_silicon)
output_waveguide_size_vector = mp.Vector3(length_input + width_margin,
	width_ridge,
	thickness_silicon)	
		
input_waveguide_location_vector = mp.Vector3(0,
	y_min + (length_input - width_margin) / 2)
output_waveguide_location_vector = mp.Vector3(bend_radius + (length_input + width_margin) / 2,
	length_input + bend_radius)
	
bend_center = mp.Vector3(bend_radius, length_input)

input_waveguide = mp.Block(input_waveguide_size_vector,
        center=input_waveguide_location_vector,
        material=mp.Medium(epsilon=material_silicon))
output_waveguide = mp.Block(output_waveguide_size_vector,
	center=output_waveguide_location_vector,
	material=mp.Medium(epsilon=material_silicon))        
bend_outer = mp.Cylinder(material=mp.Medium(epsilon=material_silicon),
	center=bend_center,
	radius=bend_outer_radius,
	height=thickness_silicon)
bend_inner = mp.Cylinder(material=mp.Medium(epsilon=material_vacuum),
	center=bend_center,
	radius=bend_inner_radius,
	height=thickness_silicon)
bend_rectangle_bottom_left = mp.Block(mp.Vector3(bend_inner_radius, bend_outer_radius, thickness_silicon),
	center=(bend_center - mp.Vector3(bend_inner_radius / 2, bend_outer_radius - bend_inner_radius / 2)),
	material=mp.Medium(epsilon=material_vacuum))
bend_rectangle_bottom_right = mp.Block(mp.Vector3(bend_outer_radius, bend_outer_radius, thickness_silicon),
	center=(bend_center - mp.Vector3(-bend_outer_radius / 2, bend_outer_radius / 2)),
	material=mp.Medium(epsilon=material_vacuum))
bend_rectangle_top_right = mp.Block(mp.Vector3(bend_outer_radius, bend_inner_radius, thickness_silicon),
	center=(bend_center + mp.Vector3(bend_outer_radius - bend_inner_radius / 2, bend_inner_radius / 2)),
	material=mp.Medium(epsilon=material_vacuum))

z_min = 0
z_max = 0

#cell = mp.Vector3(x_max - x_min, y_max - y_min, z_max - z_min)
inflate = 0
cell = mp.Vector3(inflate + x_max - x_min, inflate + y_max - y_min, z_max - z_min)
cell_center = mp.Vector3((x_max + x_min) / 2, (y_max + y_min) / 2, (z_max + z_min) / 2)

geometry = [input_waveguide,
	output_waveguide,
	bend_outer,
	bend_inner,
	bend_rectangle_bottom_left,
	bend_rectangle_bottom_right,
	bend_rectangle_top_right]

sources = [mp.Source(mp.ContinuousSource(frequency=(1.0 / wavelength)),
	component=mp.Ez,
	center=mp.Vector3(0, y_min + pml_thickness))]

pml_layers = [mp.PML(pml_thickness)]

resolution = 10

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=pml_layers,
    geometry=geometry,
    sources=sources,
    resolution=resolution,
    geometry_center=cell_center)

sim.run(until=200)

eps_data = sim.get_array(center=cell_center, size=cell, component=mp.Dielectric)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
plt.axis("off")
plt.show()

ez_data = sim.get_array(center=cell_center, size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
plt.imshow(ez_data.transpose(), interpolation="spline36", cmap="RdBu", alpha=0.9)
plt.axis("off")
plt.show()

#plt.figure()
#sim.plot2D()
#plt.show()

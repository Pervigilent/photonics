# Simulate a bent waveguide

import meep as mp
import matplotlib.pyplot as plt

METERS_TO_MICROMETERS = 1E6

# Draw the bend
thickness_cladding = 3E-6 * METERS_TO_MICROMETERS
thickness_silicon = 0.22E-6 * METERS_TO_MICROMETERS
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
length_input = 1E-6 * METERS_TO_MICROMETERS

bend_radius = 1E-6 * METERS_TO_MICROMETERS
bend_outer_radius = bend_radius + width_margin / 2
bend_inner_radius = bend_radius - width_margin / 2

x_min = 0 - width_ridge / 2 - width_margin
x_max = bend_radius + length_input
z_min = -thickness_margin
z_max = thickness_silicon + thickness_margin
y_min = 0
y_max = bend_radius + width_ridge / 2 + width_margin + length_input / 2

cladding_size_vector = mp.Vector3((x_max + extra) - (x_min - extra),
	(y_max + extra) - (y_min - extra),
	mp.inf)
buried_oxide_size_vector = mp.Vector3((x_max + extra) - (x_min - extra),	
	(y_max + extra) - (y_min - extra),
	mp.inf)
slab_size_vector = mp.Vector3((x_max + extra) - (x_min - extra),
	(y_max + extra) - (y_min - extra),
	mp.inf)
input_waveguide_size_vector = mp.Vector3(width_ridge,
	(length_input + width_margin),
	mp.inf)
output_waveguide_size_vector = mp.Vector3(length_input + width_margin,
	width_ridge,
	mp.inf)

cladding_location_vector = mp.Vector3(((x_max + extra) + (x_min - extra)) / 2,
	((y_max + extra) + (y_min - extra)) / 2)
buried_oxide_location_vector = mp.Vector3(((x_max + extra) + (x_min - extra)) / 2,	
	((y_max + extra) + (y_min - extra)) / 2)
slab_location_vector = mp.Vector3(((x_max + extra) + (x_min - extra)) / 2,
	((y_max + extra) + (y_min - extra)) / 2)
input_waveguide_location_vector = mp.Vector3(0,
	y_min + (length_input - width_margin) / 2)
output_waveguide_location_vector = mp.Vector3(bend_radius + (length_input + width_margin) / 2,
	length_input + bend_radius)
bend_center = mp.Vector3(0, length_input)

cladding = mp.Block(cladding_size_vector,
	center=cladding_location_vector,
	material=mp.Medium(epsilon=material_silicon_dioxide))
buried_oxide = mp.Block(buried_oxide_size_vector,
	center=buried_oxide_location_vector,
	material=mp.Medium(epsilon=material_silicon_dioxide))
slab = mp.Block(slab_size_vector,
	center=slab_location_vector,
	material=mp.Medium(epsilon=material_silicon))
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
bend_rectangle_bottom = mp.Block((0.1, 0.1, mp.inf),
	center=(0, 0),
	material=mp.Medium(epsilon=material_vacuum))
bend_rectangle_right = mp.Block((0.1, 0.1, mp.inf),
	center=(0, 0),
	material=mp.Medium(epsilon=material_vacuum))

geometry = [cladding,
	buried_oxide,
	slab,
	input_waveguide,
	output_waveguide,
	bend_outer,
	bend_inner,
	bend_rectangle_bottom,
	bend_rectangle_right]

cell = mp.Vector3(x_max - x_min, y_max - y_min, mp.inf)
pml_layers = [mp.PML(1.0)]
resolution = 10

sources = [
    mp.Source(mp.ContinuousSource(wavelength=2 * (11**0.5), width=20),
        component=mp.Ey,
        center=input_waveguide_location_vector,
        size=mp.Vector3(width_ridge, 0, mp.inf))]

sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=pml_layers,
    geometry=geometry,
    sources=sources,
    resolution=resolution)

#sim.plot2D()
print("Part 1")
eps_data = sim.get_array(center=bend_center, size=cell, component=mp.Dielectric)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
plt.axis("off")
plt.show()
print("Part 2")
ez_data = sim.get_array(center=bend_center, size=cell, component=mp.Ez)
plt.figure()
plt.imshow(eps_data.transpose(), interpolation="spline36", cmap="binary")
plt.imshow(ez_data.transpose(), interpolation="spline36", cmap="RdBu", alpha=0.9)
plt.axis("off")
plt.show()
#sim.plot3D(save_to_image=True, image_name='sim.png')

#sim.run(
#    mp.at_beginning(mp.output_epsilon),
#    mp.to_appended("ez", mp.at_every(0.6, mp.output_efield_z)),
#    until=200,
#)

wavelength = 1.55E-6
thickness = 0.22E-6
cladding_index = 1.444
waveguide_index = 3.473

[n_te, n_tm]  = waveguide_analytic(wavelength,...
  thickness,...
  cladding_index,...
  waveguide_index,...
  cladding_index);
  
disp(n_te)
disp(n_tm)
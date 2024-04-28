## Copyright (C) 2022 Stewart
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see <https://www.gnu.org/licenses/>.

## -*- texinfo -*-
## @deftypefn {} {@var{retval} =} TM_equation (@var{input1}, @var{input2})
##
## @seealso{}
## @end deftypefn

## Author: Stewart <stewart@virt-grothendieck>
## Created: 2022-12-23

function [TM, h, q, p] = TM_equation(beta,...
  wavenumber,...
  buried_index,...
  substrate_index,...
  cladding_index,...
  thickness)
  h = sqrt((substrate_index * wavenumber)^2 - beta.^2);
  q = sqrt(beta.^2 - (buried_index * wavenumber)^2);
  p = sqrt(beta.^2 - (cladding_index * wavenumber)^2);
  p_bar = (substrate_index / cladding_index)^2 * p;
  q_bar = (substrate_index / buried_index) ^2 * q;
  TM = tan(h * thickness) - h.*(p_bar + q_bar)./(h.^2 - p_bar .* q_bar);
end

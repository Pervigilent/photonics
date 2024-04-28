import meep as mp
from meep import mpb

m = mp.Medium(epsilon_diag=mp.Vector3(3, 3, 5))

ms = mpb.ModeSolver()
ms.geometry = [mp.Block(center=mp.Vector3(1, 2, 3), material=m, size=mp.Vector3(1, 1, 1)),
               mp.Sphere(center=mp.Vector3(1, 2, 3), material=mp.air, radius=0.2)]


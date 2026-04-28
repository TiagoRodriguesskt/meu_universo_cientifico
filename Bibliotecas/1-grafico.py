import matplotlib.pyplot as plt # 
import numpy as np

x = np.linspace(-5, 5, 50) 
y = np.linspace(-5, 5, 50)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")
surf = ax.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=False) # pyright: ignore[reportAttributeAccessIssue]
fig.colorbar(surf, shrink=0.5, aspect=5)
plt.show()

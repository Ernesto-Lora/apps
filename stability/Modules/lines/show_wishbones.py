import matplotlib.patches as patches
from .wishbone_points import wishbonePoints
def showWishboneChasis(object, fig, ax):

    pointsWishbonesTire, pointsWishbonesChasis = wishbonePoints(object)
    for X1, X2 in zip(pointsWishbonesTire, pointsWishbonesChasis):
        x=[X1[0],X2[0]]
        y=[X1[1],X2[1]]
        ax.plot(x,y, marker = 'o', markersize = 8,linewidth = 4,color = '#33C4FF')

    # Create a Polygon patch using the vertices
    chasis = [pointsWishbonesChasis[1],pointsWishbonesChasis[3],
                pointsWishbonesChasis[2], pointsWishbonesChasis[0]]
    trapezoid = patches.Polygon(chasis , closed=True, edgecolor='None', facecolor='blue', alpha = 0.2)
    # Add the trapezoid patch to the axis
    ax.add_patch(trapezoid)
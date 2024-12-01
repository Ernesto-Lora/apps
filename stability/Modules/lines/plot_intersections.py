import numpy as np
from matplotlib.patches import Circle
from lines import slopeTwoPoints, intersection, linePointSlope, lineTwoPoints


def plotIntersections(object, p1, p2, fig, ax):
    """
    p1: Wishbone points in the tire
    p2: Wishbone points in the chasis
    """
    D = object.D
    slopes = [slopeTwoPoints(p1[i,0], p1[i,1], p2[i,0], p2[i,1]) for i in range(4)]
    
    # Intersection of the wishbones LEFT lines (Iwb left)
    xIl, yIl = intersection(m1=slopes[0], x1=p1[0,0], y1=p1[0,1],
                             m2=slopes[1], x2 = p1[1,0], y2=p1[1,1])
    
    #wishbones LEFT lines
    x1 = np.linspace(p2[0,0], xIl)
    x2 = np.linspace(p2[1,0], xIl)
    y1 = linePointSlope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=x1)
    y2 = linePointSlope(x0 = p1[1,0], y0 =p1[1,1], m = slopes[1], x=x2)
    ax.plot(x1, y1, "b--")
    ax.plot(x2, y2, "b--")
    
    # Intersection of the wishbones RIGHT lines (Iwb RIGHT)
    xIr, yIr = intersection(m1=slopes[2], x1=p1[2,0], y1=p1[2,1],
                             m2=slopes[3], x2 = p1[3,0], y2=p1[3,1])
    
    #wishbones RIGHT lines
    x3 = np.linspace(xIr,p2[2,0])
    x4 = np.linspace(xIr, p2[3,0])
    
    y3 = linePointSlope(x0 = p1[2,0], y0 =p1[2,1], m = slopes[2], x=x3)
    y4 = linePointSlope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=x4)
    ax.plot(x3, y3, "r--")
    ax.plot(x4, y4, "r--")
    
    # Rolling Center
    ml = slopeTwoPoints(x1 = xIl,
                         y1 = linePointSlope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0],x=xIl),
                         x2 = -D/2 , y2 = 0)
    mr = slopeTwoPoints(x1 = xIr,
                         y1 = linePointSlope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr),
                         x2 = D/2 , y2 = 0)
    
    xRC, yRC = intersection(m1=ml, x1=-D/2, y1=0, m2=mr , x2 = D/2, y2=0)
    
    # Add circle to the plot
    rCenter = Circle((xRC, yRC), 0.025, fill =True,
                    label = "RC = ({} m, {} m)".format(round(xRC,3), round(yRC,3)), color = "g")
    ax.add_patch(rCenter)

    #LEFT tire position Iwg to the instantaneus center Iwb line
    xt = np.linspace(-D/2, np.max([xIl, xRC]))
    yt = lineTwoPoints(x1 = xIl,
                        y1 = linePointSlope(x0 = p1[0,0], y0 =p1[0,1], m = slopes[0], x=xIl),
                        x2 = -D/2 , y2 = 0, x = xt)
    ax.plot(xt, yt, color = "g")

    #RIGHT tire position Iwg to the instantaneus center Iwb line
    xtrR = np.linspace(np.min([xIr,xRC]), D/2)
    ytr = lineTwoPoints(x1 = xIr,
                         y1 = linePointSlope(x0 = p1[3,0], y0 =p1[3,1], m = slopes[3], x=xIr),
                         x2 = D/2 , y2 = 0, x = xtrR)
    ax.plot(xtrR, ytr, color = "g")
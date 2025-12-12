"""
This question is very tricky. Essentially it boils down to 
recognizing the largest rectangle contained in some hull defined by smaller rectangles.

My solution works like this:

Iterate through all pairs of points. We want to check if each pair
corresponds to a valid rectangle definition. The way we do this is by checking
if all four points defined by the rectangle lie on the problem's hull and in the interior
of the polygon defined by the hull (we check this using a raster scan algorithm, if # ray projected
from corner intersections is odd, point is inside, if # ray intersections is even, point is outside)

If this is true, and if no hull edge intersects any of the four rectangle edges, then we are guranteed to 
have a valid rectangle.
"""
points = []
with open('input.txt', 'r') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        points.append(list(map(int, line.split(','))))

n = len(points)

def area_rect(pt1, pt2):
    s1 = abs(pt1[0] - pt2[0]) + 1
    s2 = abs(pt1[1] - pt2[1]) + 1
    return s1 * s2


def check_is_rect(ind1, ind2):
    """
    Return True iff the rectangle with opposite corners at red tiles
    points[ind1] and points[ind2] lies entirely inside or on the boundary
    of the orthogonal polygon defined by 'points' (the red loop).
    """

    x0, y0 = points[ind1]
    x1, y1 = points[ind2]

    if x0 == x1 or y0 == y1:
        return False

    xmin = min(x0, x1)
    xmax = max(x0, x1)
    ymin = min(y0, y1)
    ymax = max(y0, y1)

    corners = [
        (xmin, ymin),
        (xmin, ymax),
        (xmax, ymin),
        (xmax, ymax),
    ]

    inside = [False, False, False, False]  # ray casting parity
    on_edge = [False, False, False, False]  # corner lies exactly on polygon edge
    rect_cut = False

    # single pass over all polygon edges
    for i in range(n):
        xA, yA = points[i]
        xB, yB = points[(i + 1) % n]

        # --- 1) Check if any corner lies exactly on this edge ---
        if xA == xB:
            # Vertical edge at x = xA between yA and yB
            lowy = yA if yA <= yB else yB
            highy = yB if yB >= yA else yA
            for k, (px, py) in enumerate(corners):
                if not on_edge[k] and px == xA and lowy <= py <= highy:
                    on_edge[k] = True
        else:
            # Horizontal edge at y = yA between xA and xB
            lowx = xA if xA <= xB else xB
            highx = xB if xB >= xA else xA
            for k, (px, py) in enumerate(corners):
                if not on_edge[k] and py == yA and lowx <= px <= highx:
                    on_edge[k] = True

        # --- 2) Ray casting for each corner (horizontal ray to the right) ---
        # For orthogonal polygons, only vertical edges matter for crossings.
        if xA == xB:
            xe = xA
            y1e, y2e = yA, yB
            if y1e <= y2e:
                lowy, highy = y1e, y2e
            else:
                lowy, highy = y2e, y1e

            for k, (px, py) in enumerate(corners):
                # Edge must be strictly to the right of the point
                if px < xe:
                    # Classic half-open interval [lowy, highy)
                    if lowy <= py < highy:
                        inside[k] = not inside[k]

        # --- 3) Check if this edge crosses the INTERIOR of the rectangle ---
        if xA == xB:
            # Vertical edge at x = xe
            xe = xA
            if xmin < xe < xmax:
                # Check overlap in y with (ymin, ymax) (open interval)
                lowy = yA if yA <= yB else yB
                highy = yB if yB >= yA else yA
                if max(ymin, lowy) < min(ymax, highy):
                    rect_cut = True
                    break
        else:
            # Horizontal edge at y = ye
            ye = yA
            if ymin < ye < ymax:
                # Check overlap in x with (xmin, xmax) (open interval)
                lowx = xA if xA <= xB else xB
                highx = xB if xB >= xA else xA
                if max(xmin, lowx) < min(xmax, highx):
                    rect_cut = True
                    break

    if rect_cut:
        return False

    # All corners must be inside or on the polygon
    for k in range(4):
        if not (inside[k] or on_edge[k]):
            return False

    return True


biggest_rect = 0
best_pair = None

for i in range(n):
    for j in range(i + 1, n):
        if check_is_rect(i, j):
            area = area_rect(points[i], points[j])
            if area > biggest_rect:
                biggest_rect = area
                best_pair = (i, j)

print("Largest rectangle area using only red+green tiles:", biggest_rect)
if best_pair is not None:
    i, j = best_pair
    print("Best corners (indices):", i, j, "coords:", points[i], points[j])
Fore detailed explaination with images please read the README.pdf

# Shortest path on a real-world 3D map

This project finds the shortest path between the start and end points on a
3D terrain considering the changes due to different seasons.

The map I’ve chosen is of the Mendon Ponds Park of Rochester, NY.
The elevations dataset is gathered from National Elevation Dataset.

The park has various terrains; from open lands, rough meadows, forests,
impassable vegetation, lake, paved roads. The movement speed will be
different for different terrain. To make things easier, these different
terrains are portrayed with colors on a map.

This 395x500 map will be used to consider the various terrains. The text
file mpp.txt is used for the elevation.

The interpixel distance to real-world distance is 10.29 m in X-axis & 7.55 m
in Y-axis.

Considering the colored map and elevations from the text file, this map is
generated ( 3d_image.gif )


The code takes input as

$python3 path_find.py terrain.png elevations.txt check_points.txt <season_name> output_image_file_name

- **terrain.png** is the color-coded image for representing different
    vegetations.
- **elevations.txt** contains the elevation of each point corresponding to
    the pixel in the map
- **check_points.txt** contains the start point, all/no checkpoints, end
    point.
- **<season_name>** can either be Winter, summer, fall, or spring.
- **output_image_file_name** is the name of the output image to be generated.

## When using multiple checkpoints between start and end, the total distance covered, and the path is displayed. 

**1)** All the neighboring
points to the start point
are considered.

**2)** Now, we have 8
coordinates with their
respective elevations.

**3)** As we already know
the location of the end
the point, we can calculate a
heuristic cost based on
that.

Heuristic cost (h): The direct distance between the selected point and the
destination point assuming a level and the direct paved path between them.

We need this cost to basically guide the algorithm in the right direction.


We need the distance in 2D space and the maximum speed that is
achievable on this map, hence we use those parameters to calculate the
time required to go from **A** to **B**.

Path cost (g): We use the 3D distance, this time we need the actual time
required to go from **A** to **B** considering the difference in elevations and
terrains, the final time taken changes drastically.

Hence, we get the path cost (g) and heuristic cost (h).

**5)** Now, we have a bunch of points in a queue with their respective
function costs (f).


**6)** The point at the top of the queue will the point with the lowest function
cost. We select that point and then considers its neighbors. This way we
always consider the points with the best chance of being considered in the
best path first.

**7)** This procedure is continued until we’ve reached the final point.

The algorithm does a basic best-first search; always considers the
coordinates with the lowest cost (f = g + h). By doing an informed
heuristic search like A* the answer might not be the best possible result,
but it provides a good-enough result in the shortest time possible by
traversing the least possible nodes/coordinates.





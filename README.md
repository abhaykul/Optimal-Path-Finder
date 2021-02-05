# Shortest path on a real-world 3D map

This project finds the shortest path between the start and end points on a 3D terrain considering the changes due to different seasons.

The map I&#39;ve chosen is of the [Mendon Ponds Park](https://www2.monroecounty.gov/parks-mendonponds.php) of Rochester, NY.

| Satellite Image | Elevation Image |
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86868216-4dc1c180-c0a2-11ea-861b-cd6f4b899f9a.jpg" height="500" width="395"> | <img src = "https://user-images.githubusercontent.com/35390062/86868838-78604a00-c0a3-11ea-9769-65b710f861d8.jpg" height="500" width="395">|

<img src = "https://user-images.githubusercontent.com/35390062/86868842-7a2a0d80-c0a3-11ea-95f4-8e60a1a14cca.jpg" height="400" width="300" align="right">
As we can see, it has a different elevation. It has deep ponds and small hills.

The elevations dataset is gathered from [National Elevation Dataset](http://www.sciencebase.gov/catalog/item/4f70a58ce4b058caae3f8ddb).

[Rochester](https://en.wikipedia.org/wiki/Rochester,_New_York) has four seasons:

- Summer, which is when these images were taken.
- Fall, the land near any tree is cover with leaves.
- Winter can get harsh, and most of the water bodies freeze.
- Spring, where the snow begins to melt, and it gets muddy.


Considering these scenarios, the map changes.

The park has various terrains; from open lands, rough meadows, forests, impassable vegetation, lake, paved roads. The movement speed will be different for different terrain. To make things easier, these different terrains are portrayed with colors on a map.

| Table | Summer (Base map) |
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86871296-fc1c3580-c0a7-11ea-9d1f-92021230c1e4.png"> | <img src = "https://user-images.githubusercontent.com/35390062/86868854-81511b80-c0a3-11ea-8cd6-6cdf9329b58b.jpg" height="500" width="395"> |

This 395x500 map will be used to consider the various terrains. The text file mpp.txt is used for the elevation.

The interpixel distance to real world distance is 10.29 m in X-axis &amp; 7.55 m in Y-axis.


The code takes input as

### $python3 path\_finder.py terrain.png elevations.txt check\_points.txt season\_name output\_image\_file\_name

- **terrain.png** is the color-coded image for representing different vegetations.
- **elevations.txt** contains the elevation of each point corresponding to the pixel in the map
- **check\_points.txt** contains the start point, all/no check points, end point.
- **season\_name** can either be Winter, summer, fall, or spring.
- **output\_image\_file\_name** is the name of the output image to be generated.

The seasons change the map in the following way:

- In winter, a 7-pixel wide ice layer is formed on the water where the water meets land.

- In Spring, all points within a 15-pixel radius of a waterbody and with less than 1-meter elevation from the neighboring waterbody is covered in mud due to all the ice/snow melting from the winter season.

| Spring | Winter | 
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86868857-81e9b200-c0a3-11ea-9d3c-c5d02ce2995b.jpg" height="300" width="237"> | <img src = "https://user-images.githubusercontent.com/35390062/86868856-81511b80-c0a3-11ea-93f9-c63c5a1a4bf0.jpg" height="300" width="237"> |

- In Fall, the movement speed along the paths near the forested areas is decreased as the leaves have covered all the visible paths.
The base map is the summer season.

# How the algorithm works:
Let&#39;s assume only a start and end point coordinate.

## Our goal is to reach the end point in least amount of time.

In this case, [230, 327] is the start point (big green point) &amp; [350, 139] is the end point (big red point).
To see how the algorithm chooses this path:

#### - All the neighboring points to the start point are considered.

#### - Now, we have 8 coordinates with their respective elevations.

#### - As we already know the location of the end point, we can calculate a heuristic cost based on that.



<img src = "https://user-images.githubusercontent.com/35390062/86868869-84e4a280-c0a3-11ea-8601-5a991998e3a3.jpg">
   
   ***Heuristic cost (h):*** The direct distance between the selected point and the destination point assuming a level and direct paved path between them. We need this cost to basically guide the algorithm in the right direction.
We need the distance in 2D space and the maximum speed that is achievable on this map, hence we use those parameters to calculate the time required to go from **A** to **B**.

  ***Path cost (g):*** We use the 3D distance, this time we need the actual time required to go from **A** to **B** considering the difference in elevations and terrains, the final time taken changes drastically.
Distance (D) =
Speed = [(speed)A + (speed)B]/2
Hence, we get the path cost (g) and heuristic cost (h).

#### - Now, we have a bunch of points in a queue with their respective function costs (f).

#### - The point at the top of the queue will the point with the lowest function cost. We select that point and then considers its neighbors. This way we always consider the points with the best chance of being considered in the best path first.

#### - This procedure is continued until we&#39;ve reached the final point.

| Actual Map with only the path marked | **Red area shows the points the algorithm considered** |
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86868868-84e4a280-c0a3-11ea-81d8-5a3e977a6c1f.jpg" height="500" width="395"> | <img src = "https://user-images.githubusercontent.com/35390062/86868870-857d3900-c0a3-11ea-99ce-16c3d4083a38.jpg" height="500" width="395"> |

The algorithm does a basic best-first search; always considers the coordinates with the lowest cost (f = g + h). By doing an informed heuristic search like A\* the answer might not be the best possible result, but it provides a good-enough result in the shortest time possible by traversing the least possible nodes/coordinates.
As we can see, the heuristic function chosen does it&#39;s job by guiding the algorithm in the correct direction.
The distance travelled was 2200 m. It&#39;s the best path considering the distance travelled and the time taken to reach there.

##### This is a sample output
##### $python3 path\_find.py terrain.png elevations.txt check\_points.txt season\_name output\_image\_file\_name
When using multiple checkpoints between start and end, the total distance covered, and path is displayed. The coordinates from the text-file (check\_points.txt) are:


| Points to be traversed | Map |
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86871304-ff172600-c0a7-11ea-8fc4-916c5795746f.png"> | <img src = "https://user-images.githubusercontent.com/35390062/86868867-84e4a280-c0a3-11ea-9240-ac49e7d04330.jpg" height="500" width="395"> |


Here, the path between the individual check points is highlighted in light-pink and points are black dots.


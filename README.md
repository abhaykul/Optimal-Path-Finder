# Shortest path on a real-world 3D map

This project finds the shortest path between the start and end points on a 3D terrain considering the changes due to different seasons.

The map I&#39;ve chosen is of the [Mendon Ponds Park](https://www2.monroecounty.gov/parks-mendonponds.php) of Rochester, NY.

| Satellite Image | Elevation Image |
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86868216-4dc1c180-c0a2-11ea-861b-cd6f4b899f9a.jpg" height="500" width="395"> | <img src = "https://user-images.githubusercontent.com/35390062/86868838-78604a00-c0a3-11ea-9769-65b710f861d8.jpg" height="500" width="395">|


As we can see, it has a different elevation. It has deep ponds and small hills.

The elevations dataset is gathered from [National Elevation Dataset](http://www.sciencebase.gov/catalog/item/4f70a58ce4b058caae3f8ddb).

[Rochester](https://en.wikipedia.org/wiki/Rochester,_New_York) has four seasons:

- Summer, which is when these images were taken.
- Fall, the land near any tree is cover with leaves.
- Winter can get harsh, and most of the water bodies freeze.
- Spring, where the snow begins to melt, and it gets muddy.

<img src = "https://user-images.githubusercontent.com/35390062/86868842-7a2a0d80-c0a3-11ea-95f4-8e60a1a14cca.jpg" height="400" width="300">

Considering these scenarios, the map changes.

The park has various terrains; from open lands, rough meadows, forests, impassable vegetation, lake, paved roads. The movement speed will be different for different terrain. To make things easier, these different terrains are portrayed with colors on a map.

| Table | Map |
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86871296-fc1c3580-c0a7-11ea-9d1f-92021230c1e4.png"> | <img src = "https://user-images.githubusercontent.com/35390062/86868854-81511b80-c0a3-11ea-8cd6-6cdf9329b58b.jpg" height="500" width="395"> |

Summer (Base map)

This 395x500 map will be used to consider the various terrains. The text file mpp.txt is used for the elevation.

The interpixel distance to real world distance is 10.29 m in X-axis &amp; 7.55 m in Y-axis.

Considering the colored map and elevations from the text file, this map is generated ( 3d\_image.gif )

<img src = "https://user-images.githubusercontent.com/35390062/86868855-81511b80-c0a3-11ea-9ad0-c22817775008.jpg">


The code takes input as

$python3 path\_find.py terrain.png elevations.txt check\_points.txt \&lt;season\_name\&gt; output\_image\_file\_name

- **terrain.png** is the color-coded image for representing different vegetations.
- **elevations.txt** contains the elevation of each point corresponding to the pixel in the map
- **check\_points.txt** contains the start point, all/no check points, end point.
- **\&lt;season\_name\&gt;** can either be Winter, summer, fall, or spring.
- **output\_image\_file\_name** is the name of the output image to be generated.

The seasons change the map in the following way:

In winter, a 7-pixel wide ice layer is formed on the water where the water meets land.

In Spring, all points within a 15-pixel radius of a waterbody and with less than 1-meter elevation from the neighboring waterbody is covered in mud due to all the ice/snow melting from the winter season.

| Spring | Winter | 
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86868857-81e9b200-c0a3-11ea-9d3c-c5d02ce2995b.jpg" height="300" width="237"> | <img src = "https://user-images.githubusercontent.com/35390062/86868856-81511b80-c0a3-11ea-93f9-c63c5a1a4bf0.jpg" height="300" width="237"> |

In Fall, the movement speed along the paths near the forested areas is decreased as the leaves have covered all the visible paths.
The base map is the summer season.

When using multiple checkpoints between start and end, the total distance covered, and path is displayed. The coordinates from the text-file (check\_points.txt) are:


| Points to be traversed | Map |
| --- | --- |
| <img src = "https://user-images.githubusercontent.com/35390062/86871304-ff172600-c0a7-11ea-8fc4-916c5795746f.png"> | <img src = "https://user-images.githubusercontent.com/35390062/86868867-84e4a280-c0a3-11ea-9240-ac49e7d04330.jpg" height="500" width="395"> |


Here, the path between the individual check points is highlighted in light-pink and points are black dots.

To see how the algorithm works, let&#39;s assume only a start and end point coordinate.

Our goal is to reach the end point in least amount of time.

![](RackMultipart20200708-4-1kecsc2_html_e9af0db1b48a2e4a.jpg) ![](RackMultipart20200708-4-1kecsc2_html_d0e02c171e89040c.gif) ![](RackMultipart20200708-4-1kecsc2_html_46591073bf3d1443.gif)In this case, [230, 327] is the start point (big green point) &amp; [350, 139] is the end point (big red point).

To see how the algorithm chooses this path:

**1)** All the neighboring points to the start point are considered.

**2)** Now, we have 8 coordinates with their respective elevations.

**3)** As we already know the location of the end point, we can calculate a heuristic cost based on that.

Heuristic cost (h): The direct distance between the selected point and the destination point assuming a level and direct paved path between them.

We need this cost to basically guide the algorithm in the right direction.

![](RackMultipart20200708-4-1kecsc2_html_a40ff3e69c4fa3ea.png)

We need the distance in 2D space and the maximum speed that is achievable on this map, hence we use those parameters to calculate the time required to go from **A** to **B**.

Distance (d) =

Speed = 8 m/s

Time taken = d/8 s

Path cost (g): We use the 3D distance, this time we need the actual time required to go from **A** to **B** considering the difference in elevations and terrains, the final time taken changes drastically.

Distance (D) =

Speed = [(speed)A + (speed)B]/2

Hence, we get the path cost (g) and heuristic cost (h).

**5)** Now, we have a bunch of points in a queue with their respective function costs (f).

**6)** The point at the top of the queue will the point with the lowest function cost. We select that point and then considers its neighbors. This way we always consider the points with the best chance of being considered in the best path first.

**7)** This procedure is continued until we&#39;ve reached the final point.

The algorithm does a basic best-first search; always considers the coordinates with the lowest cost (f = g + h). By doing an informed heuristic search like A\* the answer might not be the best possible result, but it provides a good-enough result in the shortest time possible by traversing the least possible nodes/coordinates.

T ![](RackMultipart20200708-4-1kecsc2_html_e9946dd48a641a59.jpg) he red area indicates all the coordinates searched for going from point A to B.

As we can see, the heuristic function chosen does it&#39;s job by guiding the algorithm in the correct direction.

The distance travelled was 2200 m. It&#39;s the best path considering the distance travelled and the time taken to reach there.

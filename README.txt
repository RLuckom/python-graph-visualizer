This is the beginning of a library to enable simple graph visualizations in python.

2013.02.10 
It does none of the visualizing, but provides basic Graph, Vertex and Edge
classes to allow a user to represent graphs.

2013.02.25 
Finished hacking out a prototype visualization using vtk, and have included
a proof-of-concept in the __main__ test of ContributionList. There's a lot 
of redundancy and inelegance. Three priorities: add functionality to the 
visualization (mouse navigation, interactive labels); enact a better
separation of functionality between the classes; document everything.

2013.03.01
Documented everything.
Combined redundant graph classes into a single class.
removed graph internals from ContributionList.
TODO: add functionality to the visualization

2013.03.02
Added autocoloring of nodes by type--each type is randomly assigned a color;
colors are distributed evenly through the colorspace based on the total number 
of types.
Experimented with different GraphLayoutStrategies. I've been thinking about 
turning the Graph class into a subclass of vtk.MutableDirectedGraph so it's easier
to set properties without modifying the class.

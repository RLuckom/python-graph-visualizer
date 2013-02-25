This is the beginning of a library to enable simple graph visualizations in python.

2013.02.10 It does none of the visualizing, but provides basic Graph, Vertex and Edge
           classes to allow a user to represent graphs.

2013.02.25 Finished hacking out a prototype visualization using vtk, and have included
           a proof-of-concept in the __main__ test of ContributionList. There's a lot 
           of redundancy and inelegance. Three priorities: add functionality to the 
           visualization (mouse navigation, interactive labels); enact a better
           separation of functionality between the classes; document everything.

# MakerBreakerGame
The Maker Break Game written in Python Arcade with AI enhancements

## Visuals
The generated hypergraph's nodes are randmoly distributed along the plane and then a 
[Force-directed](https://en.wikipedia.org/wiki/Force-directed_graph_drawing) algorithm
is applied to the graph for it to visually self-adjust.
<br/>
<br/>
The Force-directed algorithm works by using the Hooke's law for attracting the nodes at the endpoints of each edge, 
and using Coulomb's law for repelling nodes on the screen.
<br/>
<br/>
Additionally, the edges are drawn using [Bézier curves](https://en.wikipedia.org/wiki/B%C3%A9zier_curve).
# Can you color it?

## Team

The team is composed of Aditi Rupade, Rodrigo Chaves, Harshit Gupta, and Divyanshu Singh.

## Project Description

This game was developed for QCHack 2022 as part of the IBM challenge. It is based on a graph coloring game with a quantum
mechanical twist. In Graph Theory, you can mark nodes with colors and divide them in sets labeled by the color. If one has
numerous colors to paint, it is always easy to find a coloring for the graph. However, a proper coloring of the graph is
the minimum number of colors required to paint the graph such that there are no two neighbours with the same color. Different
graphs will have a different number of colors that they can be painted and this number is called the chromatic number of the graph.

Our game starts by creating a random graph for a player, and calculating its chromatic number with QAOA. Then, the user gets the
chance to use one color to paint a node. But a Quantum Computing will try to tricky the user into losing by entagling nodes 
and trying to force him to paint two neighbours. An example run of the game can be seen in the image below where the two nodes
with red borders are entangled.

![image](./Images/Example.png)

So, can you color it? Give it a try!

Every calculation is done by simulators due to time constraints.

## Steps to play the game

1. The user is presented with an empty graph along with a panel containing vertex number and color.
2. In order to color the graph, one has to select a color and a vertex. The particular vertex is selected with the color.
3. The user can continue coloring the graph keeping in mind that adjacent vertices should not be of the same color.
4. If the user tries to color adjacent vertices with the same color, the user loses the game.

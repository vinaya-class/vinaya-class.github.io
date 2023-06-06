# Libraries
library(svglite)
library(ggraph)
library(igraph)
library(tidyverse)
library(RColorBrewer)

set.seed(1234)

d1 <- read.csv("rule_classes.csv")
d2 <- read.csv("rule_list.csv")
edges=rbind(d1, d2)

d3 <- read.csv("rule_conn.csv")
connect = rbind(d3)
connect$value = 1

vertices = data.frame(name = unique(c(as.character(edges$from), as.character(edges$to))))

# Add a column with the group of each name, used for colouring points.
vertices$group = edges$from[ match( vertices$name, edges$to ) ]

# Add label information: angle, horizontal adjustement and potential flip.
# Calculate the angle of the labels.
vertices$id=NA
myleaves=which(is.na( match(vertices$name, edges$from) ))
nleaves=length(myleaves)
vertices$id[ myleaves ] = seq(1:nleaves)
vertices$angle= 90 - 360 * vertices$id / nleaves

# Calculate the alignment of labels: right or left.
# If I am on the left part of the plot, my labels have currently an angle < -90.
vertices$hjust<-ifelse( vertices$angle < -90, 1, 0)

# flip angle to make them readable
vertices$angle<-ifelse(vertices$angle < -90, vertices$angle+180, vertices$angle)

mygraph <- graph_from_data_frame( edges, vertices=vertices )

# The connection object must refer to the ids of the leaves:
from = match( connect$from, vertices$name)
to = match( connect$to, vertices$name)

svglite(file = "graph.svg", height=8, width=8)

ggraph(mygraph, layout = 'dendrogram', circular = TRUE) +

  geom_conn_bundle(data = get_con(from = from, to = to, value=connect$value), alpha=0.5, width=0.3, tension=0.95, colour="#50B6F4") +

  geom_node_text(aes(x = x*1.1, y=y*1.1, filter = leaf, label=name, angle = angle, hjust=hjust), size=2, alpha=0.9) +

  geom_node_circle(aes(filter = leaf, r=1.0, x = x*0.05, y=y*0.05, colour=group, alpha=0.4), size=2) +
  coord_fixed() +

  theme_void() +
  theme(legend.position="none",
        plot.margin=unit(c(0,0,0,0),"cm")) +

  expand_limits(x = c(-1.2, 1.2), y = c(-1.2, 1.2))


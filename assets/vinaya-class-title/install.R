# "~/R/x86_64-pc-linux-gnu-library/3.6"
path <- Sys.getenv('R_LIBS_USER')

# sudo apt-get install gfortran libxml2 libxml2-dev liblapack3 liblapack-dev libblas3 libblas-dev

install.packages("devtools", lib = path)
devtools::install_github("r-lib/svglite", lib = path)

install.packages("igraph", lib = path)
install.packages("ggraph", lib = path)
install.packages("tidyverse", lib = path)

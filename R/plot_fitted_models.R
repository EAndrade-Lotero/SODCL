source("Model_Plots.R")
source('MODELpred.R') # Load after Model_Plots

####################################################
# Loading parameters from estimations...
####################################################
archivo <- "../Data/humans_only_absent.csv"
print(paste("Loading and preparing data", archivo, "..."))
df1 = read.csv(archivo)
df1$Region <- df1$Category
df1$Exp <- "Humans"

archivo <- "../Data/MBiases_fitted.csv"
print(paste("Loading and preparing data", archivo, "..."))
df2 = read.csv(archivo)
df2$Region <- df2$Category
df2$Exp <- "MBiases"

archivo <- "../Data/WSLS_fitted.csv"
print(paste("Loading and preparing data", archivo, "..."))
df3 = read.csv(archivo)
df3$Region <- df3$Category
df3$Exp <- "WSLS"

archivo <- "../Data/FRA_fitted.csv"
print(paste("Loading and preparing data", archivo, "..."))
df4 = read.csv(archivo)
df4$Region <- df4$Category
df4$Exp <- "FRA"

p <- plot_behavioral_data_fit1(df1, df2, df3, df4)
ggsave("ModelComparisonFull.png", width=7, height=4, dpi=600, p)


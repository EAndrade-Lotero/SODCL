source("Model_Plots.R")
library(stats4)
library(bbmle)
library(dplyr)
library(ggplot2)
library(gridExtra)
library(beepr)
library(rgl)

#####################################################
# Global variables
#####################################################

thetaWSLS <- c(0.1, 0.05, 0.018, 0.002, 38, 30, 4.6, 0, 0, 0)
thetaFRA <- c(0.06, 0.05, 0.003, 0, 40, 30, 15, 0.52, 30, 0.95)

cbPalette <- c("#000000", "#E69F00", "#56B4E9", "#009E73", 
               "#F0E442", "#0072B2", "#D55E00", "#CC79A7",
               "#924900","#24ff24","#ffff6d","#b6dbff")

WSLS_color = cbPalette[5]
FRA_color = cbPalette[7]

legend2 <- get_legend_from_dummy1(WSLS_color, FRA_color)

###############################################################################
# Loading database with full information
###############################################################################

df = read.csv("../Data/humans_only_absent.csv")
head(df)

###############################################################################
# Obtaining frequencies...
###############################################################################

df1 <- getRelFreq_WSLS(df)
head(df1)

df2 <- getRelFreq_FRA(df)
head(df2)

###############################################################################
# Plot WSLS...
###############################################################################

p1 <- plot_FocalTransitions(df1)
p1 <- plot_ModelTransitions_Focal(thetaWSLS, p1, WSLS_color)
# p1 <- plot_ModelTransitions_Focal_FRA(thetaFRA, p1, FRA_color)
# p1 <- grid.arrange(p1, nrow = 1, right=legend2)
ggsave("WSLSprobs.pdf", width=2, height=2, dpi=1200, p1)

#######################################
# Plot FRA probabilities
#######################################
# x <- seq(-128,32,length.out=41)
# y <- seq(0,1.5,length.out=16)
# z <- outer(x, y, FRAprob, theta=thetaFRA)
# persp(x, y, z,
#       scale = TRUE,
#       main="Probability function\n for FRA model",
#       axes = TRUE,
#       xlab = "Score",
#       ylab = "FRAsim",
#       zlab = "Probability of focal",
#       theta = -35, phi = 30, r = 1,
#       col = "springgreen", shade = 0.5)

# Draw from RS to Focal
pasos_x <- 100
pasos_y <- 100
x <- seq(-128,32,length.out=pasos_x)
y <- seq(0,1.5,length.out=pasos_y)
z <- outer(x, y, FRAprob_RS, theta=thetaFRA)
persp3d(x, y, z, 
        xlab="",
        ylab="",
        zlab="",
        col="skyblue")
title3d(xlab = "Score", ylab = "Max. FRAsim", zlab="")
df3 <- df2[df2['RegionGo']=='Focal',]
df3 <- df3[df3['Region']!='Focal',]
head(df3)
x <- sort(df3$Score)
y <- sort(df3$MaxFRASim)
z <- sort(df3$Freqs)
z <- matrix(z, nrow = length(x), byrow = TRUE)
#rgl.open()# Open a new RGL device
#rgl.bg(color = "white") # Setup the background color
rgl.points(x, y, z, color = "blue", size = 5) # Scatter plot
#rgl.postscript("~/Repositorios/FRAprobability1.pdf",fmt="pdf")

# Draw reselect Focal
pasos_x <- 100
pasos_y <- 100
x <- seq(-128,32,length.out=pasos_x)
y <- seq(0,1.5,length.out=pasos_y)
z <- outer(x, y, FRAprob_Focal, theta=thetaFRA)
#z <- matrix(z, nrow = pasos_x, byrow = TRUE)
persp3d(x, y, z, 
        xlab="",
        ylab="",
        zlab="",
        col="skyblue")
title3d(xlab = "Score", ylab = "Max. FRAsim", zlab="")
df3 <- df2[df2['RegionGo']=='Focal',]
df3 <- df3[df3['Region']=='Focal',]
x <- sort(df3$Score)
y <- sort(df3$MaxFRASim)
z <- sort(df3$Freqs)
z <- matrix(z, nrow = length(x), byrow = TRUE)
#rgl.open()# Open a new RGL device
#rgl.bg(color = "white") # Setup the background color
rgl.points(x, y, z, color = "blue", size = 5) # Scatter plot


p2 <- plot_FRA_Transitions(df2)
p2 <- plot_ModelTransitions_FRA(thetaFRA, p2, FRA_color)
p2

grid.arrange(p1, p1, nrow = 1, 
             top=legend2,
             bottom=para_visualizar(thetaFRA))


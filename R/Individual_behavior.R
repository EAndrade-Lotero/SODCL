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
# thetaFRA <- c(0.06, 0.05, 0.003, 0, 40, 30, 15, 0.52, 30, 0.95)
thetaFRA <- c(0.1, 0.1, 0.1, 0.1, 100, 30, 30, 2, 30, 0.8)

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

p0 <- plot_FocalTransitions(df1)
p0 <- plot_ModelTransitions_Focal(thetaWSLS, p0, WSLS_color)
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


#################################################
# Heatmaps
#################################################

# Draw from RS to Focal
# Model predictions
pasos_x <- 32 + 128 + 1
pasos_y <- 15 + 1
x <- seq(-128,32,length.out=pasos_x)
y <- seq(0,1.5,length.out=pasos_y)
data <- expand.grid(X=x, Y=y)
data$Prob <- mapply(function(x,y) FRAprob_RS(x,y,theta=thetaFRA), data$X, data$Y)
p1 <- ggplot(data, aes(X, Y, fill=Prob)) + 
        geom_tile() +
        ylab("Max. FRAsim") +
        xlab("Score") +
        xlim(c(0,32)) +
        ggtitle("Probability of moving\n from RS to focal") +
        theme_bw()

# Behavioral data
df3 <- df2[df2['RegionGo']=='Focal',]
df3 <- df3[df3['Region']!='Focal',]
head(df3)
x <- df3$Score
y <- df3$MaxFRASim
data <- data.frame(x, y)
data$Prob <- df3$Freqs
p2 <- ggplot(data, aes(x, y, fill=Prob)) + 
        geom_tile() +
        ylab("Max. FRAsim") +
        xlab("Score") +
        xlim(c(0,32)) +
        ggtitle("Observed frequencies of\n moving from RS to focal") +
        theme_bw()

# Draw re-select Focal
# Model predictions
pasos_x <- 32 + 128 + 1
pasos_y <- 15 + 1
x <- seq(-128,32,length.out=pasos_x)
y <- seq(0,1.5,length.out=pasos_y)
data <- expand.grid(X=x, Y=y)
data$Prob <- mapply(function(x,y) FRAprob_Focal(x,y,theta=thetaFRA), data$X, data$Y)
p3 <- ggplot(data, aes(X, Y, fill=Prob)) + 
        geom_tile() +
        ylab("Max. FRAsim") +
        xlab("Score") +
        xlim(c(0,32)) +
        ggtitle("Probability of focal\n re-selection") +
        theme_bw()

# Behavioral data
df3 <- df2[df2['RegionGo']=='Focal',]
df3 <- df3[df3['Region']=='Focal',]
head(df3)
x <- df3$Score
y <- df3$MaxFRASim
data <- data.frame(x, y)
data$Prob <- df3$Freqs
p4 <- ggplot(data, aes(x, y, fill=Prob)) + 
        geom_tile() +
        ylab("Max. FRAsim") +
        xlab("Score") +
        xlim(c(0,32)) +
        ggtitle("Observed frequencies\n of focal re-selection") +
        theme_bw()

g <- grid.arrange(p1, p3, nrow=2)
# g <- grid.arrange(p1, p2, p3, p4, nrow=2)
ggsave("FRAprobs.pdf", width=3, height=4.5, dpi=1200, g)

#################################################
# 3D surfaces
#################################################

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
data <- data.frame(x, y)
data$Prob <- df3$Freqs
data <- data[order(data$x, data$y), ]
z <- data$Prob
z <- matrix(z, nrow = length(x), byrow = TRUE)
#rgl.open()# Open a new RGL device
#rgl.bg(color = "white") # Setup the background color
rgl.points(x, y, z, color = "red", size = 5) # Scatter plot
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
data <- data.frame(x, y)
data$Prob <- df3$Freqs
data <- data[order(data$x, data$y), ]
z <- data$Prob
z <- matrix(z, nrow = length(x), byrow = TRUE)
#rgl.open()# Open a new RGL device
#rgl.bg(color = "white") # Setup the background color
rgl.points(x, y, z, color = "red", size = 5) # Scatter plot



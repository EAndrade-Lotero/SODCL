source("Model_Plots.R")

archivo <- "../Data/MBiases_simulated.csv"
df1 = read.csv(archivo)
df1$Exp <- as.character("MBiases")
df1$Region <- df1$Category

archivo <- "../Data/WSLS_simulated.csv"
df2 = read.csv(archivo)
df2$Exp <- as.character("WSLS")
df2$Region <- df2$Category

archivo <- "../Data/FRA_simulated.csv"
df3 = read.csv(archivo)
df3$Exp <- as.character("FRA")
df3$Region <- df3$Category

p <- plot_3set_comparison_WSLS(df1, df2, df3)
ggsave("3models.png", width=5, height=4, dpi=600, p)

# Regressing DLIndex w.r.t. Consistency with interaction between Joint(n-1) and Dif_Consist
# MBiases

df1 <- df1[complete.cases(df1), ]
df2 <- df2[complete.cases(df2), ]
df3 <- df3[complete.cases(df3), ]

cor(df1$Consistency, df1$Score_LAG1)
cor(df2$Consistency, df2$Score_LAG1)
cor(df3$Consistency, df3$Score_LAG1)

modelMBiases <- lm(DLIndex ~ Consistency + Dif_consist*Joint_LAG1, data = df1)
summary(modelMBiases) # => Positive interaction is significant

# WSLS
modelWSLS <- lm(DLIndex ~ Consistency + Dif_consist*Joint_LAG1, data = df2)
summary(modelWSLS) # => Positive interaction is significant

# FRA
modelFRA <- lm(DLIndex ~ Consistency + Dif_consist*Joint_LAG1, data = df3)
summary(modelFRA) # => Positive interaction is significant

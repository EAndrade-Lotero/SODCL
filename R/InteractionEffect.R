library(ggplot2)
library(sjPlot)
library(sjmisc)

df1 = read.csv("../Data/humans_only_absent.csv")
# head(df1)

df1 <- df1[complete.cases(df1), ]

# Regressing DLIndex w.r.t. Consistency
model2h <- lm(DLIndex ~ Consistency, data = df1)
summary(model2h) # => Positive correlation is significant

# Regressing DLIndex w.r.t. Consistency with interaction between Joint(n-1) and Dif_Consist
model3h <- lm(DLIndex ~ Consistency + Dif_consist*Joint_LAG1, data = df1)
summary(model3h) # => Positive interaction is significant

anova(model2h, model3h) # => interaction effect significantly adds over main effect

g2 <- plot_model(model3h, 
                 type = "pred", 
                 terms = c("Dif_consist", "Joint_LAG1"), 
                 colors = c("black", "red", "blue"),
                 title = "",
                 legend.title = "Overlap",
                 axis.title = c("Absolute difference\nin consistency", "DLindex"))

g2

# ggsave("DegreesReactivity.eps", width=4, height=3.5, device=cairo_ps, g2)

# Check whether interaction coefficient changes sign when the effect of consistency is not included
model3h <- lm(DLIndex ~ Dif_consist*Joint_LAG1, data = df1)
summary(model3h) # => Positive interaction again (and higher)

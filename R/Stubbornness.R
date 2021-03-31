library(sjmisc)
library(ggplot2)

df1 = read.csv("../Data/humans_only_absent.csv")
# head(df1)

df1 <- df1[complete.cases(df1), ]

# Regressing Consistency w.r.t. max similarity to focal region
model4h <- lm(Consistency ~ Similarity_LAG1, data = df1)
summary(model4h) # => Positive correlation is significant

g3 <- ggplot(df1, aes(Similarity_LAG1, Consistency)) +
  geom_point(alpha = 1/8) +
  theme_bw() +
  xlab("Max similarity w.r.t.\nfocal regions on Round n-1") +
  ylab("Consistency on Round n") +
  geom_smooth(method = lm)


g3 

ggsave("ConsistencyWRTDist2FR.png", width=2, height=2, dpi=600, g3)

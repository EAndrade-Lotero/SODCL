library(sjmisc)
library(ggplot2)

df1 = read.csv("../Data/humans_only_absent.csv")
# head(df1)

df1 <- df1[complete.cases(df1), ]

# Pearson correlation
cor(df1$Consistency, df1$Score_LAG1) # => 0.23

# Regressing Consistency(n) w.r.t. Score(n-1)
model1h <- lm(Consistency ~ Score_LAG1, data = df1)
summary(model1h) # => Positive correlation is significant

g1 <- ggplot(df1, aes(Score_LAG1, Consistency)) +
  geom_point(alpha = 1/8) +
  theme_bw() +
  xlab("Score(n-1)") +
  ylab("Consistency(n)") +
  stat_smooth(method='lm', formula = y~poly(x,1))
  # geom_smooth(method = lm)

g1

ggsave("ConsistencyWRTScore.png", width=2, height=2, dpi=600, g1)

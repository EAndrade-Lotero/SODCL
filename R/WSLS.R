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


# Running an Ordinal Logistic Regression

## Cutting the Consistency variable into three levels
summary(df1$Consistency)
df1$Consistency_ordinal <- cut(df1$Consistency, 
                               breaks = c(0, 0.31, 0.86, 1),
                               labels = c("inconsistent", "moderately consistent", "consistent")
                               )

## Drawing boxplot
boxplot(df1$Score_LAG1~df1$Consistency_ordinal,
        xlab="Consistency",
        ylab="Score on previous round"
        )

## Running OLR model
m <- polr(Consistency_ordinal ~ Score_LAG1, data = df1)
summary(m)

## store table
(ctable <- coef(summary(m)))
## calculate and store p values
p <- pnorm(abs(ctable[, "t value"]), lower.tail = FALSE) * 2
## combined table
(ctable <- cbind(ctable, "p value" = p))

## Finding odds
(ci <- confint(m))
exp(cbind(coef(m),t(ci)))

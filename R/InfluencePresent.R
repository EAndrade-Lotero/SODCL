# library(sjmisc)
# library(ggplot2)

source("MODELpred.R")

df1 = read.csv("../Data/performances.csv")
head(df1)

df1 <- find_regionVector(df1)
df1$Size_visited <- sapply(df1$vR, function(x) {
  lista <- unlist(x)
  return(sum(lista))
})
df1$Is_there_LAG <- lag(df1$Is_there)
df <- data.frame(df1$Is_there_LAG, df1$Is_there, df1$Size_visited)
df <- df[complete.cases(df), ]
head(df)

df_present <- df[which(df$df1.Is_there_LAG == 'Unicorn_Present'), ]
df_present <- df_present[which(df_present$df1.Is_there == 'Unicorn_Absent'), ]
df_present$Exp <- "present"

df_absent <- df[which(df$df1.Is_there_LAG == 'Unicorn_Absent'), ]
df_absent <- df_absent[which(df_absent$df1.Is_there == 'Unicorn_Absent'), ]
df_absent$Exp <- "absent"

av_present <- mean(df_present$df1.Size_visited)
av_present_sd <- sd(df_present$df1.Size_visited)
av_present
av_present_sd

av_absent <- mean(df_absent$df1.Size_visited)
av_absent_sd <- sd(df_absent$df1.Size_visited)
av_absent
av_absent_sd

wilcox.test(df_present$df1.Size_visited, df_absent$df1.Size_visited) # => Difference size visited after present vs after absent is significant

df2 <- rbind(df_present, df_absent)
head(df2)

# Density plot
g2 <- ggplot(df2, aes(df1.Size_visited, colour=Exp, group=Exp)) +
  geom_density(size=1) +
#  scale_colour_manual(values = c("Last" = "#E69F00", "First" = "#56B4E9")) +
  #  scale_y_continuous(limits = c(0, 5)) +
  scale_y_continuous(position = "right") +
  labs(color = "Round") +
  theme_bw() +
  theme(legend.position="bottom")

g2

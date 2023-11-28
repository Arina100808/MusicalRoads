library(lme4) # This is the package that we need for using LMMs


# First, specify the path to the datafile:
setwd('/Users/arina/Desktop/Cognitive Psychology/Musical Roads')

data <- read.csv('collected_data_21.csv')

data$init_speed <- as.factor(data$init_speed)
data$init_speed <- relevel(data$init_speed, ref="1")
    
model_change <- lmer(
    change ~ -1 + init_speed + (1+init_speed|subject) + (1+init_speed|road_nr),
    data=data, )
	
model_answer <- lmer(
	answer ~ init_speed + (1+init_speed|subject) + (1+init_speed|road_nr),
	data=data, )


summary(model_change)
summary(model_answer)

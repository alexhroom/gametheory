library(tidyverse)
library(magrittr)
library(ggpubr)

winners <- read.csv("/home/alexhroom/Documents/University/Spring3/game/gametheory/code/winners.csv")
tppt <- read.csv("/home/alexhroom/Documents/University/Spring3/game/gametheory/code/trader_pop_per_turn.csv")
rppt <- read.csv("/home/alexhroom/Documents/University/Spring3/game/gametheory/code/regulator_pop_per_turn.csv")

tppt %<>% rename(winning_trader=player_name, trader_ppt=pop_per_turn)
rppt %<>% rename(winning_regulator=player_name, regulator_ppt=pop_per_turn)

# join average ppt data and make tidy
winning_trader_bar_data <- right_join(by="winning_trader", count(winners, winning_trader), tppt)
winning_trader_bar_data['n'] <- log2(winning_trader_bar_data['n'])
wtbd.long <- gather(winning_trader_bar_data, variable,value, -winning_trader)

winning_regulator_bar_data <- right_join(by="winning_regulator", count(winners, winning_regulator), rppt)
winning_regulator_bar_data['n'] <- log2(winning_regulator_bar_data['n'])
wrbd.long <- gather(winning_regulator_bar_data, variable,value, -winning_regulator)

labs <- c("log(number of wins)", "average survival time (turns)")

# create bar charts
winning_traders <- (ggplot(wtbd.long, mapping=aes(x = fct_reorder(winning_trader, desc(value)), y = value, fill = variable))
                    + geom_col(position="dodge")
                    + scale_fill_viridis_d(end = 0.7, labels=labs)
                    + labs(x="winning trader", y="value"))

winning_regulators <- (ggplot(wrbd.long, mapping=aes(x = fct_reorder(winning_regulator, desc(value)), y = value, fill = variable))
                    + geom_col(position="dodge")
                    + scale_fill_viridis_d(end = 0.7, labels=labs)
                    + labs(x="winning regulator", y="value")
                    + guides(fill="none"))

barplots <- ggarrange(winning_traders, winning_regulators, common.legend=TRUE, legend="right", ncol=1, nrow=2)
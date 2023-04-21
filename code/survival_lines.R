library(tidyverse)
library(magrittr)
library(ggpubr)

tppt <- readr::read_csv("/home/alexhroom/Documents/University/Spring3/game/gametheory/code/trader_ppt.csv")[-1]
rppt <- readr::read_csv("/home/alexhroom/Documents/University/Spring3/game/gametheory/code/regulator_ppt.csv")[-1]

tppt %<>% rename("trader_name"="key_0")
rppt %<>% rename("regulator_name"="key_0")

tppt %<>% pivot_longer(!trader_name, names_to="turn", values_to="avg_pop") %>% mutate(turn=as.numeric(turn))
rppt %<>% pivot_longer(!regulator_name, names_to="turn", values_to="avg_pop") %>% mutate(turn=as.numeric(turn))

trader_survival_lines <- (ggplot(tppt, mapping=aes(x=turn, y=avg_pop, group=trader_name, color=trader_name)) 
                         + geom_line()
                         + labs(x="turn", y="average population", color="trader name"))
regulator_survival_lines <- (ggplot(rppt, mapping=aes(x=turn, y=avg_pop, group=regulator_name, color=regulator_name)) 
                            + geom_line()
                            + labs(x="turn", y="average population", color="regulator name"))

survival_lines <- ggarrange(trader_survival_lines, regulator_survival_lines, ncol=1, nrow=2)

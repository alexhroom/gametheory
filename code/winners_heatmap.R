library(tidyverse)

winners <- read.csv("/home/alexhroom/Documents/University/Spring3/game/gametheory/code/winners.csv")

# count how many times each winner regulator pair occurs
winner_pairs <- unite(winners, "winning_pair", c("winning_trader", "winning_regulator"))
winner_pairs_with_count <- right_join(by="winning_pair", winner_pairs, count(winner_pairs, winning_pair))

# merge back into original dataset
winners <- right_join(by="time", winners, winner_pairs_with_count[c("time", "n")])

# create heatmap
winners_heatmap <- (ggplot(winners, aes(winning_regulator, winning_trader, fill=n)) 
                    + geom_tile() 
                    + scale_fill_viridis_c() 
                    + labs(x="winning regulator", y="winning trader", fill="shared wins")
                    + theme(panel.background = element_rect(fill="#31013D"),
                            panel.grid.major=element_blank()))
ggsave("/home/alexhroom/Documents/University/Spring3/game/gametheory/heatmap.png", winners_heatmap, width=800, height=500, units="px")
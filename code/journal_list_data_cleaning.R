########## 
##########
# This code contains some data cleaning/summary statistics tasks presented in
# in Brookson & Davis (in Prep) 
# A review on the accessibility of conservation-based research
##########
##########
# AUTHOR: Cole B. Brookson
# DATE OF CREATION: 2020-07-29
##########
##########

library(tidyverse)
library(here)

journals_scored = read_csv(here('./data/journals_scored.csv'))
all_papers = read_csv(here('./data/all_papers.csv'),
                      guess_max = 50000)

#get the type of the publication into the journals_scored dataframe
all_papers$Journal = as.factor(all_papers$Journal)
journals_scored$Journal = as.factor(journals_scored$Journal)

journal_type = all_papers %>% 
  select(PubType, Journal) %>% 
  unique()

journals_scored = merge(journals_scored, 
                        journal_type, 
                        by = 'Journal') %>% 
  filter(Management %in% c(0,1)) %>% 
  distinct(Journal, Management, .keep_all = TRUE)

table(journals_scored$PubType)



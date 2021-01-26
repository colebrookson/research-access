########## 
##########
# This code contains some data cleaning/summary statistics tasks presented in
# in Brookson & Davis (in Prep) 
##########
##########
# Data management script to access journal ISSNs for 
# review on the accessibility of conservation-based research
##########
##########
# AUTHOR: Cole B. Brookson
# DATE OF CREATION: 2020-07-29
##########
##########

library(tidyverse)
library(here)
`%notin%` = negate(`%in%`)


journals_scored = read_csv(here('./data/journals_scored.csv'))
all_papers = read_csv(here('./data/all_papers.csv'),
                      guess_max = 50000)
full_records = read_csv(here('./data/combined_review_papers.csv'),
                        guess_max = 50000)
open_access = read_csv(here('./data/combined_open_access_review_papers.csv'))
doaj_access = read_csv(here('./data/journalcsv__doaj_20210126_1836_utf8.csv'))

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
#write_csv(journals_scored, './data/grouped_journals_scored.csv')

# NOTE -- did a manual assessment of the 'relevance' of the different items
#         in the `grouped_journals_scored.csv` by hand. This allowed us to keep
#         items that were relevant but were coded as not being 'J'-type items

grouped_journals = read_csv(here('./data/grouped_journals_scored.csv'))

grouped_journals_manag = grouped_journals %>% 
  filter(Relevance == 1) %>% 
  filter(Management == 1)

full_records_issns = full_records %>% 
  select(SO, SN, BN, EI)

grouped_journals_manag_issns = 
  merge(grouped_journals_manag, full_records_issns, 
        by.x = 'Journal', by.y = 'SO') %>% 
  distinct(Journal, SN, .keep_all = TRUE)

doaj_access = doaj_access %>% 
  filter(`DOAJ Seal` == 'Yes')
  
grouped_journals_manag_issns = grouped_journals_manag_issns %>% 
  rowwise() %>% 
  mutate(open_access = 
           ifelse(SN %in% doaj_access$`Journal ISSN (print version)` |
                    SN %in% doaj_access$`Journal EISSN (online version)`, 
                          1, 0))


missing_journals = grouped_journals_manag %>% 
  filter(Journal %notin% grouped_journals_manag_issns$Journal)
# NOTE -- found the ISSNs manually for the missing journals and input them
#         into the dataframe. They are now present for every journal except
#         one. They were manually searched for on Web of Science Journals and
#         then secondarily on the broader internet

missing_journals = missing_journals %>% 
  rowwise() %>% 
  mutate(open_access = 
           ifelse(SN %in% doaj_access$`Journal ISSN (print version)` |
                    SN %in% doaj_access$`Journal EISSN (online version)`, 
                  1, 0))

n_distinct(grouped_journals_manag$Journal)
# get rid of duplicated elements
grouped_journals_manag = 
  grouped_journals_manag[!duplicated(grouped_journals_manag),]

n_distinct(journals_scored$Journal)

journals_scored$Journal = as.factor(journals_scored$Journal)

x = journals_scored %>% 
  filter(Management == 1)
n_distinct(x$Journal)





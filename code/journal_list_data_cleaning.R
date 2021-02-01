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
#open_access = read_csv(here('./data/combined_open_access_review_papers.csv'))
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
                          1, 0)) %>% 
  select(-c(BN, EI))
  


# missing_journals = grouped_journals_manag %>% 
#   filter(Journal %notin% grouped_journals_manag_issns$Journal)
# # NOTE -- found the ISSNs manually for the missing journals and input them
# #         into the dataframe. They are now present for every journal except
# #         one. They were manually searched for on Web of Science Journals and
# #         then secondarily on the broader internet
# write_csv(missing_journals, here('./data/missing_issn_journals.csv'))
missing_journals = read_csv(here('./data/missing_issn_journals.csv'))

missing_journals = missing_journals %>% 
  rowwise() %>% 
  mutate(open_access = 
           ifelse(ISSN %in% doaj_access$`Journal ISSN (print version)` |
                    ISSN %in% doaj_access$`Journal EISSN (online version)`, 
                  1, 0)) %>% 
  rename(SN = ISSN)

# join the journals that were previously missing their ISSNs to the other
# larger list

if(names(missing_journals) == names(grouped_journals_manag_issns)) {
  
  grouped_journals_manag_issns = rbind(grouped_journals_manag_issns,
                                       missing_journals)
  
}

grouped_journals_manag_issns$open_access = 
  as.factor(grouped_journals_manag_issns$open_access)

non_open_access_manag = grouped_journals_manag_issns %>% 
  select(Journal, open_access, SN) %>% 
  rename(ISSN = SN) %>% 
  filter(open_access == 0) %>% 
  distinct()

# so there are a few duplicated journals, so we'll manually go in and
# check the ISSNs and correct if necessary. If there is a correct ISSN,
# we'll go with that one, but if the duplicate is just an eISSN, the 
# print ISSN will be kept 
n_distinct(non_open_access_manag$Journal)

non_open_access_manag[duplicated(non_open_access_manag$Journal),]

non_open_access_manag$ISSN = as.character(non_open_access_manag$ISSN)

non_open_access_manag[which(
  non_open_access_manag$ISSN == '0257-7615'), 'ISSN'] = '1814-232X'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '0015-5551'), 'ISSN'] = '1211-9520'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '1931-7603'), 'ISSN'] = '2151-0733'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '1099-1085'), 'ISSN'] = '0885-6087'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '0303-2434'), 'ISSN'] = '1569-8432'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '0021-8375'), 'ISSN'] = '2193-7192'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '0743-8141'), 'ISSN'] = '1040-2381'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '2212-9790'), 'ISSN'] = '1872-7859'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '2210-6715'), 'ISSN'] = '2210-6707'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '0951-7359'), 'ISSN'] = '1747-6585'
non_open_access_manag[which(
  non_open_access_manag$ISSN == '1938-5463'), 'ISSN'] = '0091-7648'

# now ensure there are no more duplicates
non_open_access_manag = non_open_access_manag %>% 
  distinct(Journal, .keep_all = TRUE)
n_distinct(non_open_access_manag$ISSN)

# now there are some repeated ISSNs, manually check these out
repeated_issns_issns = 
  non_open_access_manag[duplicated(non_open_access_manag$ISSN),]
repeated_issns = non_open_access_manag %>% 
  filter(ISSN %in% repeated_issns_issns$ISSN)

### so I've double checked that all these ISSN duplicates are okay - they're
# simply some journals that are the same journal but listed multiple times
# under slightly different names. We will proceed with just the unique ISSNs

non_open_access_manag = non_open_access_manag %>% 
  distinct(ISSN, .keep_all = TRUE) %>% 
  select(-open_access)

# now write this as a csv
write_csv(non_open_access_manag, here('./data/list_of_issns_for_query.csv'))






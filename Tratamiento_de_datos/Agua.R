setwd("/Users/cgva/PycharmProjects/agua/files")
library(tidyverse)
library(readr)
concesiones <- read_csv("CONCESIONES.csv")
subterraneo <- read_csv("ANEXOS_SUBTERRANEOS.csv") %>%
  filter(ESTADO == 19)

union <- left_join(concesiones,subterraneo, by = "TÍTULO") %>%
  filter(ESTADO == 19) %>%
  mutate(Latitud = `GRADOS LATITUD` +(`MINUTOS LATITUD`/60)+(`SEGUNDOS LATITUD`/3600),
         Longitud = (`GRADOS LONGITUD`+(`MINUTOS LONGITUD`/60)+(`SEGUNDOS LONGITUD`/3600))*-1)

pub_priv <- read.csv("REPDA.csv", fileEncoding = "UTF-8") %>% select(c(Titulo,PubPriv))

union2 <- merge(union,pub_priv, by.x = "TÍTULO", by.y = "Titulo")
unique(union2$PubPriv)

union2$PubPriv -> str_replace_all(union2$PubPriv,c("\n"=""))

write.csv(union2,"unionregios.csv")

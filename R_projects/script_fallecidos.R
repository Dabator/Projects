
Dataset <- readXL("C:/Users/34647/Desktop/cosas dani uni/TFG/tfg/modelos/basem.xlsx", rownames=TRUE, 
  header=TRUE, na="", sheet="Hoja1", stringsAsFactors=TRUE)
library(rpart)
modelo2f <- rpart(FALLE ~., data = basefalle2)
modelo2f
library(rpart.plot)
rpart.plot(modelo)
editDataset(basefalle)
editDataset(basefalle)
editDataset(basefalle)
editDataset(basefalle)



basefalle2 <- readXL("C:/Users/Antenas_ITB/Desktop/TFG/tfg/modelos/basem_4.xlsx", rownames=TRUE, header=TRUE,
   na="", sheet="Hoja1", stringsAsFactors=TRUE)


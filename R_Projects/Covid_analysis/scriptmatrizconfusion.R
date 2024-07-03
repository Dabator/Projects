
Dataset <- readXL("C:/Users/34647/Desktop/cosas dani uni/TFG/tfg/modelos/basem.xlsx", rownames=TRUE, 
  header=TRUE, na="", sheet="Hoja1", stringsAsFactors=TRUE)
library(rpart)
modelo3f <- rpart(FALLE ~., data = basefalle3)
modelo3f
library(rpart.plot)
library(caret)
rpart.plot(modelo)
editDataset(basefalle)
editDataset(basefalle)
editDataset(basefalle)
editDataset(basefalle)
rpart.plot(modelo3f, main="¿Qué afecta al número de muertes por Covid-19?", extra=1, branch=1, varlen=0, digits=3, round=0, shadow.col="gray", xsep=" / ", split.suffix=" ?", split.box.col="lightgray",  split.border.col="darkgray", split.round=.5, yesno.yshift=0.6, eq=" ",lt=" < ", ge=" >= ")

prediccion_1 <- predict(modelo3f, newdata = basefalle3, type = "vector")
type = "vector"
confusionMatrix(prediccion_1, basefalle3[["tipo"]])


basefalle3 <- readXL("C:/Users/Antenas_ITB/Desktop/TFG/tfg/modelos/basem_4.xlsx", 
  rownames=TRUE, header=TRUE, na="", sheet="Hoja1", stringsAsFactors=TRUE)
basefalle3 <- readXL("C:/Users/Antenas_ITB/Desktop/TFG/tfg/modelos/basem_4.xlsx", rownames=TRUE, header=TRUE,
   na="", sheet="Hoja1", stringsAsFactors=TRUE)


myDataframe = read.csv("/Users/martinwurzer/developing/HCI/02_Übung/3/pulse_parsed.csv", sep=" ")
i <- 0
while(i<1000) {
  Sys.sleep(0.02)# in seconds
  con1 <- socketConnection(port = 3001, server = FALSE)
  mydata <- toString(myDataframe[i,]$pulse) 
  writeLines(toString(mydata))
  writeLines(mydata, con1) 
  close.connection(con1)
  i <- i+1;
}



city_map = "\
\chennai -> coimbatore madurai \n\
\coimbatore -> salem trichy \n\
\madurai -> tanjore dindigul" 

main = do print $ map words ( lines city_map )
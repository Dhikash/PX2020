while true
  do
  ./requestflights.py
  ./requestsatellite.py
  ./Convert_CSV_to_CZML.py; 
  sleep 6
done

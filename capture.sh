while true
  do
  ./requestflights.py
  ./Convert_CSV_to_CZML.py; 
  sleep 6
done

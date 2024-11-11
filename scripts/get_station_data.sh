#MYFILE="mta_test.csv"
MYFILE="MTA_Oct08.csv"
BASENAME=$(basename -s ".csv" "$MYFILE")

#bus https://catalog.data.gov/dataset/mta-bus-hourly-ridership-beginning-february-2022
if [ ! -f $BASENAME\_raw.csv  ]; then
    echo "Download"
    wget "https://data.ny.gov/api/views/wujg-7c2s/rows.csv?accessType=DOWNLOAD"
    mv "rows.csv?accessType=DOWNLOAD" $BASENAME\_raw.csv
fi

if [ -f $BASENAME\_raw.csv ] && [ ! -f $BASENAME\_sorted.csv ]; then
    echo "converting 12h to 24h format"
    #12h to 24h for sorting convenience, plus remove erronious March 13 2022 daylight savings hour
    sed -e 's/12:00:00 AM/00:00:00/g' -e 's/ AM//g' -e 's/01:00:00 PM/13:00:00/g' -e 's/02:00:00 PM/14:00:00/g' -e 's/03:00:00 PM/15:00:00/g' -e 's/04:00:00 PM/16:00:00/g' -e 's/05:00:00 PM/17:00:00/g' -e 's/06:00:00 PM/18:00:00/g' -e 's/07:00:00 PM/19:00:00/g' -e 's/08:00:00 PM/20:00:00/g' -e 's/09:00:00 PM/21:00:00/g' -e 's/10:00:00 PM/22:00:00/g' -e 's/11:00:00 PM/23:00:00/g' -e 's/12:00:00 PM/12:00:00/g' -e '/03\/13\/2022 02:00:00/d' $BASENAME\_raw.csv > $BASENAME\_unsorted.csv
    echo "sorting" 
    sort --sort=numeric --parallel=4 -o $BASENAME\_unsorted.csv -t "/" -k3n  --buffer-size=2G $BASENAME\_unsorted.csv
    mv $BASENAME\_unsorted.csv $BASENAME\_sorted.csv
    #delete last 4 lines that look incomplete
fi

if [ -f $BASENAME\_sorted.csv ] && [ ! -f $BASENAME\_sorted_skimmed_station.csv ]; then
    echo "skim and accumulate"
    #python skim.py $BASENAME\_sorted.csv
    python skim_station.py $BASENAME\_sorted.csv
    head -n -4 $BASENAME\_sorted_skimmed_station.csv > tmp.txt && mv tmp.txt $BASENAME\_sorted_skimmed_station.csv #remove last 4 lines that go beyond date cutoff and look incomplete
fi

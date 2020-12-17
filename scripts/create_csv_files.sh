# This isn't a standalone bash script. Just to capture
# the commands used to create/split the csv files (using 
# csvkit python package)

# Split into separate csv files
for file in `ls /uod/idr/filesets/idr0088-cox-phenomicprofiling/20201123-ftp/`
do
	echo ${file}
	ids=`csvcut -c 1 ${file} | uniq | tail -n +2`
	for id in ${ids}
		do csvgrep -c 1 -m ${id} ${file} >> /tmp/split/${id}.csv
	done
done

# Remove the 'A' from the plate names
files=`find * -iname "*A.csv"`
for file in ${files}
do
	outfile=${file/A\.csv/\.csv}
	sed 's/A,/,/' ${file} >> ${outfile}
done

